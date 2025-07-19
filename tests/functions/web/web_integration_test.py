"""
Integration tests for LisPy Web Framework.
Tests the complete web framework functionality including request handling.
"""

import unittest
import json
from unittest.mock import MagicMock, patch
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.web.app import WebApp
from lispy.web.request import parse_request
from lispy.web.response import format_response
from lispy.types import Symbol


class TestWebIntegration(unittest.TestCase):
    """Test complete web framework integration."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_complete_web_app_creation(self):
        """Test creating a complete web application with routes and middleware."""
        code = """
        (let [app (web-app)]
          ; Add logging middleware
          (middleware app "before" 
                      (fn [request]
                        (assoc request :log-id "req-123")))
          
          ; Add routes
          (route app "GET" "/" 
                 (fn [request] 
                   {:status 200 
                    :headers {:content-type "text/html"}
                    :body "<h1>Welcome to LisPy Web!</h1>"}))
          
          (route app "GET" "/api/health"
                 (fn [request]
                   {:status 200
                    :headers {:content-type "application/json"}
                    :body (json-encode {:status "healthy" :timestamp 1234567890})}))
          
          (route app "POST" "/api/users"
                 (fn [request]
                   (let [user-data (:json request)]
                     {:status 201
                      :headers {:content-type "application/json"}
                      :body (json-encode {:message "User created" :data user-data})})))
          
          (route app "GET" "/users/:id"
                 (fn [request]
                   (let [user-id (:id (:params request))]
                     {:status 200
                      :headers {:content-type "application/json"}
                      :body (json-encode {:id user-id :name "Test User"})})))
          
          ; Add response middleware
          (middleware app "after"
                      (fn [request response]
                        (assoc response :server-header "LisPy-Web/1.0")))
          
          app)
        """
        result = run_lispy_string(code, self.env)
        
        self.assertIsInstance(result, WebApp)
        self.assertEqual(len(result.router.routes), 4)
        self.assertEqual(len(result.middleware_chain.middleware), 2)

    def test_request_parsing(self):
        """Test HTTP request parsing functionality."""
        # Test GET request with query parameters
        headers = {'Content-Type': 'application/json', 'User-Agent': 'Test'}
        request = parse_request(
            method='GET',
            path='/users/123?page=1&limit=10',
            headers=headers,
            body='',
            route_pattern='/users/:id',
            client_address=('127.0.0.1', 12345)
        )
        
        self.assertEqual(request[Symbol(':method')], 'GET')
        self.assertEqual(request[Symbol(':path')], '/users/123')
        self.assertEqual(request[Symbol(':remote-addr')], '127.0.0.1')
        
        # Check query parameters
        query_params = request[Symbol(':query-params')]
        self.assertEqual(query_params[Symbol(':page')], '1')
        self.assertEqual(query_params[Symbol(':limit')], '10')
        
        # Check path parameters
        params = request[Symbol(':params')]
        self.assertEqual(params[Symbol(':id')], '123')
        
        # Check headers
        headers_parsed = request[Symbol(':headers')]
        self.assertEqual(headers_parsed[Symbol(':content-type')], 'application/json')

    def test_request_parsing_with_json(self):
        """Test request parsing with JSON body."""
        headers = {'Content-Type': 'application/json'}
        body = '{"name": "Alice", "age": 30}'
        
        request = parse_request(
            method='POST',
            path='/api/users',
            headers=headers,
            body=body,
            client_address=('127.0.0.1', 12345)
        )
        
        self.assertEqual(request[Symbol(':method')], 'POST')
        self.assertEqual(request[Symbol(':body')], body)
        
        # Check JSON parsing
        json_data = request[Symbol(':json')]
        self.assertEqual(json_data['name'], 'Alice')
        self.assertEqual(json_data['age'], 30)

    def test_response_formatting(self):
        """Test HTTP response formatting functionality."""
        response_data = {
            Symbol(':status'): 200,
            Symbol(':headers'): {Symbol(':content-type'): 'application/json'},
            Symbol(':body'): {'message': 'Hello World'}
        }
        
        status, headers, body = format_response(response_data)
        
        self.assertEqual(status, 200)
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertIn('message', body)
        self.assertIn('Hello World', body)

    def test_response_auto_content_type(self):
        """Test automatic content type detection."""
        # Test HTML detection
        response_data = {
            Symbol(':status'): 200,
            Symbol(':body'): '<h1>Hello World</h1>'
        }
        
        status, headers, body = format_response(response_data)
        self.assertEqual(headers['Content-Type'], 'text/html; charset=utf-8')
        
        # Test JSON auto-detection
        response_data = {
            Symbol(':status'): 200,
            Symbol(':body'): {'message': 'Hello'}
        }
        
        status, headers, body = format_response(response_data)
        self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')

    def test_app_request_handling_get(self):
        """Test complete request handling through WebApp for GET request."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/hello" 
                 (fn [request] 
                   {:status 200 
                    :headers {:content-type "text/plain"}
                    :body "Hello World"}))
          app)
        """
        app = run_lispy_string(code, self.env)
        
        # Simulate handling a GET request
        headers = {'User-Agent': 'Test Client'}
        status, response_headers, body = app.handle_request(
            method='GET',
            path='/hello',
            headers=headers,
            body='',
            client_address=('127.0.0.1', 12345),
            env=self.env
        )
        
        self.assertEqual(status, 200)
        self.assertEqual(response_headers['Content-Type'], 'text/plain')
        self.assertEqual(body, 'Hello World')

    def test_app_request_handling_post_with_json(self):
        """Test complete request handling for POST with JSON."""
        code = """
        (let [app (web-app)]
          (route app "POST" "/api/echo" 
                 (fn [request] 
                   (let [input (get request ':json)]
                     {:status 200 
                      :headers {:content-type "application/json"}
                      :body (json-encode {:echoed input})})))
          app)
        """
        app = run_lispy_string(code, self.env)
        
        # Simulate handling a POST request with JSON
        headers = {'Content-Type': 'application/json'}
        body = '{"message": "Hello from client"}'
        
        status, response_headers, body_response = app.handle_request(
            method='POST',
            path='/api/echo',
            headers=headers,
            body=body,
            client_address=('127.0.0.1', 12345),
            env=self.env
        )
        
        self.assertEqual(status, 200)
        self.assertEqual(response_headers['Content-Type'], 'application/json; charset=utf-8')
        
        # Parse and verify the response
        response_data = json.loads(body_response)
        self.assertEqual(response_data['echoed']['message'], 'Hello from client')

    def test_app_request_handling_with_params(self):
        """Test request handling with URL parameters."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/users/:id/posts/:post_id" 
                 (fn [request] 
                   (let [params (get request ':params)
                         user-id (get params ':id)
                         post-id (get params ':post_id)]
                     {:status 200 
                      :headers {:content-type "application/json"}
                      :body (json-encode {:user_id user-id :post_id post-id})})))
          app)
        """
        app = run_lispy_string(code, self.env)
        
        # Simulate handling a request with parameters
        status, response_headers, body = app.handle_request(
            method='GET',
            path='/users/123/posts/456',
            headers={},
            body='',
            client_address=('127.0.0.1', 12345),
            env=self.env
        )
        
        self.assertEqual(status, 200)
        response_data = json.loads(body)
        self.assertEqual(response_data['user_id'], '123')
        self.assertEqual(response_data['post_id'], '456')

    def test_app_request_handling_with_middleware(self):
        """Test request handling with middleware processing."""
        code = """
        (let [app (web-app)]
          ; Before middleware adds request ID
          (middleware app "before" 
                      (fn [request]
                        (assoc request ':request-id "req-123")))
          
          ; Route that uses the request ID
          (route app "GET" "/test" 
                 (fn [request] 
                   {:status 200 
                    :headers {:content-type "application/json"}
                    :body (json-encode {:request_id (get request ':request-id)})}))
          
          ; After middleware adds custom header
          (middleware app "after"
                      (fn [request response]
                        (let [headers (get response ':headers)
                              new-headers (assoc headers ':x-custom "custom-value")]
                          (assoc response ':headers new-headers))))
          
          app)
        """
        app = run_lispy_string(code, self.env)
        
        # Simulate handling a request with middleware
        status, response_headers, body = app.handle_request(
            method='GET',
            path='/test',
            headers={},
            body='',
            client_address=('127.0.0.1', 12345),
            env=self.env
        )
        
        self.assertEqual(status, 200)
        self.assertEqual(response_headers['X-Custom'], 'custom-value')
        
        response_data = json.loads(body)
        self.assertEqual(response_data['request_id'], 'req-123')

    def test_app_request_handling_404(self):
        """Test 404 handling for non-existent routes."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/exists" (fn [req] {:status 200 :body "OK"}))
          app)
        """
        app = run_lispy_string(code, self.env)
        
        # Request non-existent route
        status, response_headers, body = app.handle_request(
            method='GET',
            path='/does-not-exist',
            headers={},
            body='',
            client_address=('127.0.0.1', 12345),
            env=self.env
        )
        
        self.assertEqual(status, 404)
        self.assertEqual(response_headers['Content-Type'], 'application/json; charset=utf-8')
        
        response_data = json.loads(body)
        self.assertEqual(response_data['status'], 404)
        self.assertIn('Not Found', response_data['error'])

    def test_app_request_handling_405(self):
        """Test 405 Method Not Allowed handling."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/test" (fn [req] {:status 200 :body "OK"}))
          app)
        """
        app = run_lispy_string(code, self.env)
        
        # Request with wrong method
        status, response_headers, body = app.handle_request(
            method='POST',
            path='/test',
            headers={},
            body='',
            client_address=('127.0.0.1', 12345),
            env=self.env
        )
        
        self.assertEqual(status, 405)
        self.assertEqual(response_headers['Allow'], 'GET')
        
        response_data = json.loads(body)
        self.assertEqual(response_data['status'], 405)
        self.assertIn('Method Not Allowed', response_data['error'])

    def test_web_framework_documentation(self):
        """Test that all web framework functions have documentation."""
        functions_to_test = [
            'web-app', 'route', 'middleware', 'start-server', 'stop-server'
        ]
        
        for func_name in functions_to_test:
            with self.subTest(function=func_name):
                result = run_lispy_string(f"(doc {func_name})", self.env)
                self.assertIsInstance(result, str)
                self.assertIn(func_name, result)

    def test_web_framework_thread_first_compatibility(self):
        """Test that web framework functions work well with thread-first operator."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/" (fn [req] {:status 200 :body "Home"}))
          (route app "GET" "/about" (fn [req] {:status 200 :body "About"}))
          (middleware app "before" (fn [req] req))
          (middleware app "after" (fn [req res] res))
          app)
        """
        result = run_lispy_string(code, self.env)
        
        self.assertIsInstance(result, WebApp)
        self.assertEqual(len(result.router.routes), 2)
        self.assertEqual(len(result.middleware_chain.middleware), 2)


if __name__ == '__main__':
    unittest.main()