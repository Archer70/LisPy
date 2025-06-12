# LisPy Async Programming Guide

## Table of Contents

1. [Introduction to Async Programming](#introduction-to-async-programming)
2. [Basic Concepts](#basic-concepts)
3. [Core Promise Functions](#core-promise-functions)
4. [Promise Chaining](#promise-chaining)
5. [Async/Await Pattern](#asyncawait-pattern)
6. [Promise Combinators](#promise-combinators)
7. [Utility Functions](#utility-functions)
8. [Real-World Use Cases](#real-world-use-cases)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)
11. [Troubleshooting](#troubleshooting)

---

## Introduction to Async Programming

Asynchronous programming allows your code to handle operations that take time (like network requests, file I/O, or complex calculations) without blocking the entire program. Instead of waiting for one operation to complete before starting the next, async programming lets multiple operations run concurrently.

### Why Use Async Programming?

**Benefits:**
- **Non-blocking**: Other code can run while waiting for slow operations
- **Concurrency**: Multiple operations can run simultaneously  
- **Responsiveness**: Applications remain responsive during long operations
- **Efficiency**: Better resource utilization and throughput

**When to Use:**
- Network requests (APIs, databases)
- File I/O operations
- Long-running calculations
- Operations that can be parallelized
- User interfaces that need to stay responsive

---

## Basic Concepts

### Promises

A **Promise** represents the eventual result of an asynchronous operation. It can be in one of three states:

- **Pending**: The operation hasn't completed yet
- **Fulfilled**: The operation completed successfully
- **Rejected**: The operation failed with an error

```lisp
;; Creating a simple promise
(define my-promise (promise (fn [] 
  (+ 42 (* 6 7)))))

;; Promises are "lazy" - they represent future values
(println my-promise) ; => #<Promise:pending>
```

### Async Context

The `async` special form creates an asynchronous context where you can use `await`:

```lisp
;; Basic async usage
(async 
  (let [result (await my-promise)]
    (println "Result:" result)))
```

---

## Core Promise Functions

### `promise`

Creates a new promise that executes a function asynchronously.

```lisp
;; Syntax: (promise function)
(define calculation (promise (fn [] 
  (+ 1 2 3 4 5))))

;; The function runs in the background
(async 
  (let [result (await calculation)]
    (println "Sum:" result))) ; => Sum: 15
```

### `resolve`

Creates a promise that immediately resolves with a value.

```lisp
;; Syntax: (resolve value)
(define immediate-value (resolve "Hello, World!"))

(async 
  (let [greeting (await immediate-value)]
    (println greeting))) ; => Hello, World!
```

### `reject`

Creates a promise that immediately rejects with an error.

```lisp
;; Syntax: (reject reason)
(define error-promise (reject "Something went wrong"))

;; Note: Awaiting a rejected promise will cause an error
;; Handle with appropriate error handling in real applications
```

---

## Promise Chaining

Promise chaining allows you to transform and handle promises in a functional, composable way without nested callbacks or complex async/await blocks.

### `promise-then`

Transforms the resolved value of a promise using a callback function.

```lisp
;; Syntax: (promise-then promise callback)

;; Basic transformation
(-> (resolve 10)
    (promise-then (fn [x] (* x 2)))
    (promise-then (fn [x] (+ x 5))))
;; => Promise that resolves to 25

;; Chaining with thread-first operator
(-> (promise (fn [] (fetch-user-id)))
    (promise-then (fn [id] (fetch-user-data id)))
    (promise-then (fn [user] (extract-user-name user)))
    (promise-then (fn [name] (append "Hello, " name))))
```

### `on-reject`

Handles promise rejections and provides error recovery.

```lisp
;; Syntax: (on-reject promise error-handler)

;; Basic error handling
(-> (reject "network-error")
    (on-reject (fn [err] (append "Handled: " (str err)))))
;; => Promise that resolves to "Handled: network-error"

;; Error recovery with fallback data
(-> (fetch-from-api)
    (on-reject (fn [_] (fetch-from-cache)))
    (on-reject (fn [_] "default-data")))
```

### `on-complete`

Executes cleanup code regardless of whether the promise resolves or rejects.

```lisp
;; Syntax: (on-complete promise cleanup-callback)

;; Resource cleanup
(-> (open-database-connection)
    (promise-then (fn [conn] (query-database conn)))
    (on-complete (fn [_] (close-database-connection))))

;; Logging and monitoring
(-> (critical-operation)
    (promise-then (fn [result] (log-success result)))
    (on-reject (fn [error] (log-error error)))
    (on-complete (fn [_] (log-completion))))
```

### Combining Chaining Functions

```lisp
;; Complete error handling and cleanup pipeline
(-> (fetch-user-data user-id)
    (promise-then (fn [user] (validate-user user)))
    (promise-then (fn [user] (enrich-user-data user)))
    (on-reject (fn [err] 
      (do 
        (log-error "User processing failed:" err)
        (get-default-user))))
    (on-complete (fn [_] (cleanup-temp-resources)))
    (promise-then (fn [user] (render-user-profile user))))
```

---

## Async/Await Pattern

The async/await pattern provides an imperative style for handling promises, while promise chaining offers a functional style. Choose based on your preference and use case.

### Basic Async/Await

```lisp
;; Define an async function
(defn-async fetch-user-data [user-id]
  (let [_ (println "Fetching user:" user-id)]
    ; Simulate network delay and return mock data
    (append "User-" (str user-id) "-Data")))

;; Use the async function
(async 
  (let [user (await (fetch-user-data "123"))]
    (println "Retrieved:" user)))
```

### Async/Await vs Promise Chaining

```lisp
;; Async/await style (imperative)
(async 
  (let [user-id "123"
        user-data (await (fetch-user-data user-id))
        processed-data (await (process-user-data user-data))
        final-result (await (save-processed-data processed-data))]
    (println "Pipeline complete:" final-result)))

;; Promise chaining style (functional)
(-> (resolve "123")
    (promise-then fetch-user-data)
    (promise-then process-user-data)
    (promise-then save-processed-data)
    (promise-then (fn [result] (println "Pipeline complete:" result))))
```

### When to Use Each Style

**Use async/await when:**
- You need complex control flow (loops, conditionals)
- You prefer imperative programming style
- You need to handle multiple unrelated async operations

**Use promise chaining when:**
- You have linear data transformation pipelines
- You prefer functional programming style
- You want to leverage thread-first (`->`) operator
- You need composable, reusable promise transformations

---

## Promise Combinators

Promise combinators allow you to coordinate multiple asynchronous operations.

### `promise-all`

**When to use**: When you need ALL operations to succeed before proceeding.

**Behavior**: 
- Waits for all promises to resolve
- Fails fast (rejects immediately if any promise rejects)
- Returns results in the same order as input

```lisp
;; Use for coordinating multiple parallel operations
(async 
  (let [user-tasks (vector
                     (fetch-user-data "user1")
                     (fetch-user-data "user2")
                     (fetch-user-data "user3"))
        results (await (promise-all user-tasks))]
    (println "All users loaded:" results)))

;; Perfect for dependent operations that can run in parallel
(async 
  (let [page-data (await (promise-all (vector
                                        (fetch-header-data)
                                        (fetch-content-data)
                                        (fetch-sidebar-data))))]
    (render-page page-data)))
```

### `promise-race`

**When to use**: When you want the first operation to complete (success or failure).

**Behavior**:
- Returns as soon as ANY promise settles
- Useful for timeouts and competing data sources

```lisp
;; Timeout pattern - very common use case
(async 
  (let [result (await (promise-race (vector
                                      (fetch-data-from-api)
                                      (delay 5000 (reject "timeout")))))]
    (println "Got result within timeout:" result)))

;; Racing multiple data sources
(async 
  (let [data (await (promise-race (vector
                                    (fetch-from-cache)
                                    (fetch-from-database)
                                    (fetch-from-api))))]
    (println "Fastest data source won:" data)))
```

### `promise-any`

**When to use**: When you want the first SUCCESS, ignoring failures.

**Behavior**:
- Resolves with first successful promise
- Ignores rejections until all promises are checked
- Only rejects if ALL promises reject

```lisp
;; API fallback pattern - try multiple endpoints
(async 
  (let [data (await (promise-any (vector
                                   (fetch-from-primary-api)
                                   (fetch-from-backup-api)
                                   (fetch-from-fallback-api))))]
    (println "Got data from first working API:" data)))

;; Resilient data fetching
(async 
  (let [content (await (promise-any (vector
                                      (load-from-cache)     ; might fail
                                      (load-from-database)  ; might fail
                                      (load-from-network)   ; fallback
                                      (load-default-content)))) ; last resort
    (render-content content)))
```

### `promise-all-settled`

**When to use**: When you want comprehensive results regardless of individual failures.

**Behavior**:
- NEVER rejects - always resolves
- Waits for ALL promises to settle
- Returns detailed status objects for each promise

```lisp
;; Graceful degradation - continue despite some failures
(async 
  (let [results (await (promise-all-settled (vector
                                              (load-user-profile)
                                              (load-user-preferences)  ; might fail
                                              (load-user-history)      ; might fail
                                              (load-user-friends))))
        successful-data (filter results 
                                (fn [r] (equal? (get r ':status) "fulfilled")))
        failed-operations (filter results 
                                  (fn [r] (equal? (get r ':status) "rejected")))]
    (println "Loaded" (count successful-data) "out of" (count results) "data sources")
    (when (> (count failed-operations) 0)
      (println "Failed operations:" (count failed-operations)))))

;; Comprehensive monitoring and reporting
(async 
  (let [health-checks (await (promise-all-settled (vector
                                                    (check-database-health)
                                                    (check-api-health)
                                                    (check-cache-health)
                                                    (check-storage-health))))
        healthy-services (filter health-checks 
                                 (fn [h] (equal? (get h ':status) "fulfilled")))
        unhealthy-services (filter health-checks 
                                   (fn [h] (equal? (get h ':status) "rejected")))]
    (println "System health:" (count healthy-services) "/" (count health-checks) "services healthy")))
```

---

## Utility Functions

### `delay`

Creates a promise that resolves after a specified time delay.

```lisp
;; Syntax: (delay milliseconds value)
(delay 1000 "Hello") ; Resolves to "Hello" after 1 second

;; Use for timeouts
(async 
  (let [result (await (promise-race (vector
                                      (some-operation)
                                      (delay 3000 "timeout"))))]
    (if (equal? result "timeout")
      (println "Operation timed out")
      (println "Operation completed:" result))))

;; Use for rate limiting
(async 
  (let [_ (await (delay 100 nil))]  ; Wait 100ms between requests
    (fetch-next-batch)))
```

---

## Real-World Use Cases

### 1. API Data Aggregation

```lisp
;; Using promise chaining for clean, functional data aggregation
(defn load-dashboard-data [user-id]
  "Load all data needed for a user dashboard"
  (-> (promise-all (vector
                     (fetch-user-profile user-id)
                     (fetch-user-settings user-id)))
      (promise-then (fn [core-data]
        (let [profile (first core-data)
              settings (nth core-data 1)]
          ; Load optional data in parallel
          (-> (promise-all-settled (vector
                                     (fetch-user-activity user-id)
                                     (fetch-user-notifications user-id)
                                     (fetch-user-recommendations user-id)))
              (promise-then (fn [optional-data]
                ; Extract successful optional data safely
                (let [activity (extract-fulfilled-value (first optional-data))
                      notifications (extract-fulfilled-value (nth optional-data 1) [])
                      recommendations (extract-fulfilled-value (nth optional-data 2) [])]
                  {:profile profile
                   :settings settings  
                   :activity activity
                   :notifications notifications
                   :recommendations recommendations})))))))

;; Helper function for extracting fulfilled values
(defn extract-fulfilled-value [result default-value]
  (if (equal? (get result ':status) "fulfilled")
    (get result ':value)
    default-value))

;; Alternative async/await version for comparison
(defn-async load-dashboard-data-async [user-id]
  "Load all data needed for a user dashboard (async/await style)"
  (let [; Core data must succeed - use promise-all
        core-data (await (promise-all (vector
                                        (fetch-user-profile user-id)
                                        (fetch-user-settings user-id))))
        profile (first core-data)
        settings (nth core-data 1)
        
        ; Optional data - continue even if some fail
        optional-data (await (promise-all-settled (vector
                                                    (fetch-user-activity user-id)
                                                    (fetch-user-notifications user-id)
                                                    (fetch-user-recommendations user-id))))
        
        ; Extract successful optional data safely
        activity (extract-fulfilled-value (first optional-data))
        notifications (extract-fulfilled-value (nth optional-data 1) [])
        recommendations (extract-fulfilled-value (nth optional-data 2) [])]
    
    {:profile profile
     :settings settings  
     :activity activity
     :notifications notifications
     :recommendations recommendations}))
```

### 2. Resilient Service Communication

```lisp
;; Promise chaining approach with graceful fallbacks
(defn resilient-api-call [endpoint]
  "Try multiple strategies to get data with promise chaining"
  (-> (fetch-from-cache endpoint)
      (on-reject (fn [_] 
        (-> (fetch-from-api endpoint)
            (on-reject (fn [_] (fetch-from-backup-api endpoint)))
            (on-reject (fn [_] (get-default-data endpoint))))))
      (on-complete (fn [_] (log-api-call-completion endpoint)))))

;; Alternative using promise-any for concurrent attempts
(defn resilient-api-call-concurrent [endpoint]
  "Try multiple strategies concurrently"
  (-> (promise-any (vector
                     ; Try cache first (fastest)
                     (fetch-from-cache endpoint)
                     
                     ; Try primary API with timeout
                     (promise-race (vector
                                     (fetch-from-api endpoint)
                                     (delay 2000 (reject "primary-timeout"))))
                     
                     ; Try backup API with longer timeout
                     (promise-race (vector
                                     (fetch-from-backup-api endpoint)
                                     (delay 5000 (reject "backup-timeout"))))
                     
                     ; Last resort: return default data
                     (delay 100 (get-default-data endpoint))))
      (promise-then (fn [data] 
        (do 
          (log-successful-source endpoint)
          data)))
      (on-reject (fn [err] 
        (do 
          (log-all-sources-failed endpoint err)
          (get-emergency-fallback-data endpoint))))))
```

### 3. Batch Processing with Error Handling

```lisp
;; Promise chaining approach for batch processing
(defn process-batch [items]
  "Process a batch of items, handling individual failures gracefully"
  (-> (map items (fn [item] (promise (fn [] (process-item item)))))
      (promise-all-settled)
      (promise-then (fn [results]
        ; Separate successful and failed results
        (let [successful (filter results (fn [r] (equal? (get r ':status) "fulfilled")))
              failed (filter results (fn [r] (equal? (get r ':status) "rejected")))
              
              ; Extract values and reasons
              successful-values (map successful (fn [r] (get r ':value)))
              error-reasons (map failed (fn [r] (get r ':reason)))]
          
          {:processed successful-values
           :errors error-reasons
           :total-items (count items)
           :success-count (count successful)
           :failure-count (count failed)
           :success-rate (/ (count successful) (count results))})))
      (promise-then (fn [summary]
        (do 
          (log-batch-summary summary)
          summary)))
      (on-reject (fn [err] 
        (do 
          (log-batch-error err)
          {:processed []
           :errors [err]
           :total-items (count items)
           :success-count 0
           :failure-count 1
           :success-rate 0}))))

;; Enhanced version with progress tracking
(defn process-batch-with-progress [items progress-callback]
  "Process batch with progress updates using promise chaining"
  (-> (map items (fn [item] 
        (-> (promise (fn [] (process-item item)))
            (promise-then (fn [result] 
              (do 
                (progress-callback item result)
                result)))
            (on-reject (fn [err] 
              (do 
                (progress-callback item err)
                (reject err)))))))
      (promise-all-settled)
      (promise-then (fn [results]
        (let [summary (create-batch-summary results items)]
          (do 
            (progress-callback :complete summary)
            summary))))))
```

---

## Best Practices

### 1. Choose the Right Programming Style

**Use Promise Chaining when:**
- You have linear data transformation pipelines
- You prefer functional programming style
- You want to leverage thread-first (`->`) operator
- You need composable, reusable transformations
- Error handling can be localized to specific steps

```lisp
;; Good: Clean functional pipeline
(-> (fetch-user-data user-id)
    (promise-then validate-user)
    (promise-then enrich-user-data)
    (on-reject get-default-user)
    (promise-then render-user-profile))
```

**Use Async/Await when:**
- You need complex control flow (loops, conditionals)
- You prefer imperative programming style
- You need to handle multiple unrelated async operations
- You have complex error handling requirements

```lisp
;; Good: Complex control flow
(async 
  (let [users (await (fetch-all-users))]
    (for [user users]
      (when (user-needs-update? user)
        (let [updated-user (await (update-user user))]
          (await (notify-user-updated updated-user)))))))
```

### 2. Choose the Right Combinator

**Use `promise-all` when:**
- All operations must succeed
- You need all results before proceeding
- Failing fast is desired behavior

**Use `promise-race` when:**
- You want the fastest response
- Implementing timeouts
- Racing multiple equivalent data sources

**Use `promise-any` when:**
- You need at least one success
- Implementing fallback patterns
- Building resilient systems

**Use `promise-all-settled` when:**
- You need comprehensive results
- Some failures are acceptable
- Building monitoring/reporting systems

### 3. Error Handling Patterns

**Promise Chaining Error Handling:**
```lisp
;; Good: Localized error handling with recovery
(-> (fetch-user-data user-id)
    (promise-then validate-user)
    (on-reject (fn [err] 
      (do 
        (log-validation-error err)
        (get-default-user))))
    (promise-then enrich-user-data)
    (on-reject (fn [err] 
      (do 
        (log-enrichment-error err)
        (resolve user)))) ; Continue with basic user data
    (promise-then render-user-profile))

;; Good: Comprehensive error handling with cleanup
(-> (acquire-resource)
    (promise-then use-resource)
    (on-reject handle-resource-error)
    (on-complete (fn [_] (release-resource))))
```

**Async/Await Error Handling:**
```lisp
;; Good: Use promise-any for graceful fallbacks
(async 
  (let [data (await (promise-any (vector
                                   (primary-source)
                                   (backup-source)
                                   (resolve "default-data"))))]
    (process-data data)))

;; Good: Use timeouts to prevent hanging
(async 
  (let [result (await (promise-race (vector
                                      (long-running-operation)
                                      (delay 5000 (reject "timeout")))))]
    (handle-result result)))
```

### 4. Performance Optimization

**Sequential vs Concurrent Operations:**

```lisp
;; Sequential (slow) - operations run one after another
(async 
  (let [user1 (await (fetch-user "1"))
        user2 (await (fetch-user "2"))
        user3 (await (fetch-user "3"))]
    [user1 user2 user3]))

;; Concurrent (fast) - operations run simultaneously
(async 
  (let [users (await (promise-all (vector
                                    (fetch-user "1")
                                    (fetch-user "2")
                                    (fetch-user "3"))))]
    users))

;; Promise chaining with concurrent operations
(-> (promise-all (vector
                   (fetch-user "1")
                   (fetch-user "2") 
                   (fetch-user "3")))
    (promise-then (fn [users] (process-users users)))
    (promise-then (fn [processed] (save-processed-users processed))))
```

**Optimizing Promise Chains:**

```lisp
;; Good: Parallel independent operations
(-> (promise-all (vector
                   (fetch-user-profile user-id)
                   (fetch-user-preferences user-id)
                   (fetch-user-history user-id)))
    (promise-then (fn [data] (merge-user-data data))))

;; Good: Sequential dependent operations
(-> (authenticate-user credentials)
    (promise-then (fn [user] (fetch-user-permissions user)))
    (promise-then (fn [permissions] (authorize-action permissions action))))
```

### 5. Avoid Common Anti-Patterns

**Promise Creation Anti-Patterns:**
```lisp
;; Bad: Unnecessary promise wrapping
(defn bad-async-function []
  (promise (fn [] (resolve "already a promise"))))

;; Good: Return promises directly
(defn good-async-function []
  (some-async-operation))

;; Bad: Mixing async styles unnecessarily
(defn mixed-style-bad []
  (async 
    (let [result (await (-> (fetch-data)
                            (promise-then process-data)))]
      result)))

;; Good: Choose one style and stick with it
(defn promise-chain-good []
  (-> (fetch-data)
      (promise-then process-data)))

(defn async-await-good []
  (async 
    (let [data (await (fetch-data))
          result (await (process-data data))]
      result)))
```

**Error Handling Anti-Patterns:**
```lisp
;; Bad: Not handling rejections appropriately
(async 
  (let [result (await (risky-operation))]  ; May throw unhandled error
    (process result)))

;; Bad: Ignoring errors in promise chains
(-> (risky-operation)
    (promise-then process-result))  ; No error handling

;; Good: Use appropriate error handling
(async 
  (let [result (await (promise-any (vector
                                     (risky-operation)
                                     (resolve "fallback-value"))))]
    (process result)))

;; Good: Handle errors in promise chains
(-> (risky-operation)
    (promise-then process-result)
    (on-reject handle-error))
```

---

## Common Patterns

### 1. Retry Pattern

```lisp
(defn-async retry-operation [operation max-attempts delay-ms]
  "Retry an operation with exponential backoff"
  (let [attempt (fn [remaining current-delay]
                  (if (> remaining 0)
                    (promise-any (vector
                                   (operation)
                                   (delay current-delay
                                          (attempt (- remaining 1) 
                                                   (* current-delay 2)))))
                    (reject "max-retries-exceeded")))]
    (attempt max-attempts delay-ms)))

;; Usage
(async 
  (let [result (await (retry-operation 
                        (fn [] (unreliable-api-call))
                        3      ; max attempts
                        1000))] ; initial delay
    (process-result result)))
```

### 2. Rate Limiting Pattern

```lisp
(defn-async rate-limited-batch [items rate-limit-ms process-fn]
  "Process items with rate limiting between operations"
  (let [process-with-delay (fn [acc item]
                             (let [result (await (process-fn item))
                                   _ (await (delay rate-limit-ms nil))]
                               (conj acc result)))]
    (reduce items process-with-delay [])))

;; Usage
(async 
  (let [results (await (rate-limited-batch 
                         ["item1" "item2" "item3"]
                         500  ; 500ms between each operation
                         api-call-fn))]
    (println "All processed with rate limiting:" results)))
```

### 3. Cache-Aside Pattern

```lisp
(defn-async get-with-cache [key fetch-fn cache-ttl-ms]
  "Get data with cache-aside pattern and TTL"
  (promise-any (vector
                 ; Try cache first
                 (get-from-cache key)
                 
                 ; Fetch and cache if not available
                 (let [data (await (fetch-fn key))
                       _ (await (put-in-cache key data cache-ttl-ms))]
                   data)
                 
                 ; Fallback timeout
                 (delay 10000 (reject "cache-and-fetch-timeout")))))
```

### 4. Circuit Breaker Pattern

```lisp
(define circuit-state (atom {:failures 0 :last-failure nil :state "closed"}))

(defn-async call-with-circuit-breaker [operation]
  "Call operation with circuit breaker protection"
  (let [state @circuit-state
        current-time (current-time-ms)]
    
    ; Check if circuit should be open
    (if (and (equal? (get state ':state) "open")
             (< (- current-time (get state ':last-failure)) 30000)) ; 30 second timeout
      (reject "circuit-breaker-open")
      
      ; Try the operation
      (promise-any (vector
                     (let [result (await (operation))]
                       ; Reset on success
                       (swap! circuit-state assoc ':failures 0 ':state "closed")
                       result)
                     
                     (delay 0 ; Immediate failure handling
                            (let [failures (+ (get state ':failures) 1)]
                              (if (> failures 5)
                                (swap! circuit-state assoc 
                                       ':failures failures 
                                       ':last-failure current-time
                                       ':state "open")
                                (swap! circuit-state assoc ':failures failures))
                              (reject "operation-failed"))))))))
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Promise Never Resolves

**Problem**: Promise remains pending indefinitely

```lisp
;; Problematic code
(define broken-promise (promise (fn [] 
  (let [x 1]
    ; Function never returns
    (loop [])))))

;; Solution: Always add timeouts
(async 
  (let [result (await (promise-race (vector
                                      broken-promise
                                      (delay 5000 "timeout"))))]
    (if (equal? result "timeout")
      (handle-timeout)
      (handle-result result))))
```

#### 2. Unhandled Promise Rejections

**Problem**: Rejected promises cause unexpected errors

```lisp
;; Problematic code
(async 
  (let [result (await (risky-operation))]  ; May reject
    (process result)))

;; Solution: Use defensive patterns
(async 
  (let [result (await (promise-any (vector
                                     (risky-operation)
                                     (resolve "safe-default"))))]
    (process result)))
```

#### 3. Race Conditions with Shared State

**Problem**: Multiple async operations modifying shared state

```lisp
;; Problematic code
(define shared-counter (atom 0))

(async 
  (let [_ (await (promise-all (vector
                                (increment-counter)  ; Both modify shared-counter
                                (increment-counter))))] ; Race condition!
    @shared-counter))

;; Solution: Sequence dependent operations or use proper coordination
(async 
  (let [_ (await (increment-counter))
        _ (await (increment-counter))]
    @shared-counter))
```

### Debugging Techniques

#### 1. Add Strategic Logging

```lisp
(defn-async debug-operation [name operation]
  "Wrapper that adds logging to async operations"
  (let [_ (println "Starting:" name)
        start-time (current-time-ms)
        result (await (promise-race (vector
                                      (operation)
                                      (delay 30000 (reject "debug-timeout")))))
        end-time (current-time-ms)
        duration (- end-time start-time)]
    (println "Completed:" name "in" duration "ms")
    result))

;; Usage
(async 
  (let [user (await (debug-operation "fetch-user" 
                                     (fn [] (fetch-user-data "123"))))]
    (process-user user)))
```

#### 2. Use promise-all-settled for Comprehensive Debugging

```lisp
(async 
  (let [results (await (promise-all-settled debug-operations))
        successful (filter results (fn [r] (equal? (get r ':status) "fulfilled")))
        failed (filter results (fn [r] (equal? (get r ':status) "rejected")))]
    
    (println "Debug Summary:")
    (println "  Successful operations:" (count successful))
    (println "  Failed operations:" (count failed))
    
    (when (> (count failed) 0)
      (println "  Failure details:")
      (map failed (fn [failure] 
                    (println "    -" (get failure ':reason)))))))
```

#### 3. Timeout-Based Debugging

```lisp
(defn-async debug-with-timeout [operation timeout-ms]
  "Add debug timeout to catch hanging operations"
  (promise-race (vector
                  (operation)
                  (delay timeout-ms 
                         (do 
                           (println "DEBUG: Operation timed out after" timeout-ms "ms")
                           (reject "debug-timeout"))))))
```

---

## Quick Reference

### Function Summary

| Function | Purpose | When to Use |
|----------|---------|-------------|
| **Core Functions** | | |
| `promise` | Create async operation | Wrapping sync functions |
| `resolve` | Create resolved promise | Immediate values |
| `reject` | Create rejected promise | Immediate errors |
| **Promise Chaining** | | |
| `promise-then` | Transform resolved values | Data transformation pipelines |
| `on-reject` | Handle rejections | Error recovery, fallbacks |
| `on-complete` | Cleanup operations | Resource management, logging |
| **Promise Combinators** | | |
| `promise-all` | Wait for all, fail-fast | All operations must succeed |
| `promise-race` | First to settle wins | Timeouts, competing sources |
| `promise-any` | First success wins | Fallbacks, resilience |
| `promise-all-settled` | Comprehensive results | Monitoring, graceful degradation |
| **Utilities** | | |
| `delay` | Timed operations | Timeouts, rate limiting |

### Programming Style Decision Tree

```
What type of async operation are you building?

Linear data transformation pipeline?
├─ Yes → Use Promise Chaining
│  ├─ (-> promise (promise-then transform) (on-reject handle-error))
│  └─ Benefits: Functional, composable, thread-first compatible
└─ No → Complex control flow needed?
   ├─ Yes → Use Async/Await
   │  ├─ (async (let [x (await op1)] (if condition (await op2) (await op3))))
   │  └─ Benefits: Imperative, familiar, complex logic support
   └─ Mixed → Use appropriate style for each part
```

### Combinator Decision Tree

```
Do you need ALL operations to succeed?
├─ Yes → Use `promise-all` (fails fast on any error)
└─ No
   ├─ Do you want the fastest response?
   │  └─ Yes → Use `promise-race` (first to settle)
   └─ No
      ├─ Do you need at least one success?
      │  └─ Yes → Use `promise-any` (ignores failures)
      └─ No → Use `promise-all-settled` (comprehensive results)
```

### Error Handling Guide

**Promise Chaining Error Handling:**
- **For step-by-step recovery**: Use `on-reject` after each `promise-then`
- **For comprehensive cleanup**: Use `on-complete` at the end of chains
- **For fallback chains**: Chain multiple `on-reject` calls
- **For resource management**: Always use `on-complete` for cleanup

**Combinator Error Handling:**
- **For critical operations**: Use `promise-all` with proper fallbacks
- **For optional operations**: Use `promise-all-settled` 
- **For fallback chains**: Use `promise-any`
- **For timeouts**: Use `promise-race` with `delay`

**Quick Error Handling Patterns:**
```lisp
;; Immediate fallback
(-> (risky-operation)
    (on-reject (fn [_] "safe-default")))

;; Retry pattern
(-> (operation)
    (on-reject (fn [_] (operation)))  ; Simple retry
    (on-reject (fn [_] "final-fallback")))

;; Resource cleanup
(-> (acquire-resource)
    (promise-then use-resource)
    (on-complete (fn [_] (release-resource))))
```

---

## Conclusion

LisPy's async programming capabilities provide powerful tools for building responsive, efficient applications. With both promise chaining and async/await patterns, you can choose the style that best fits your use case and programming preferences.

### Key Success Factors:

1. **Choose the right programming style**: Promise chaining for functional pipelines, async/await for complex control flow
2. **Understand each combinator's behavior**: Know when to use `promise-all`, `promise-race`, `promise-any`, and `promise-all-settled`
3. **Implement comprehensive error handling**: Use `on-reject` for recovery, `on-complete` for cleanup
4. **Add appropriate timeouts**: Prevent hanging operations with `promise-race` and `delay`
5. **Test async flows thoroughly**: Both success and failure scenarios

### Promise Chaining Benefits:

- **Functional composition**: Clean, readable transformation pipelines
- **Thread-first compatibility**: Works seamlessly with `->` operator
- **Localized error handling**: Handle errors at each step as needed
- **Resource management**: Built-in cleanup with `on-complete`
- **Composability**: Easy to build reusable async components

### Next Steps

1. **Practice with examples**: Start with simple promise chains using `promise-then`
2. **Build gradually**: Add error handling with `on-reject` and cleanup with `on-complete`
3. **Experiment with styles**: Try both promise chaining and async/await for different scenarios
4. **Focus on error handling**: Build resilient systems with comprehensive error recovery
5. **Monitor and debug**: Use logging and comprehensive error reporting
6. **Consider performance**: Choose concurrent over sequential when possible

### Quick Start Template

```lisp
;; Basic promise chain template
(-> (initial-operation)
    (promise-then transform-data)
    (promise-then validate-data)
    (on-reject (fn [err] 
      (do 
        (log-error err)
        (get-fallback-data))))
    (on-complete (fn [_] (cleanup-resources)))
    (promise-then final-processing))
```

Happy async programming in LisPy! 🚀
