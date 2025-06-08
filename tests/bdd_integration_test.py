# tests/bdd_integration_test.py
import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.bdd import registry # Import the whole registry module

class TestBddIntegration(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        registry.clear_bdd_results() # Ensure clean slate for each test

    def test_full_bdd_flow_populates_registry(self):
        lispy_code = """
        (describe "User Authentication"
          (it "should allow login with correct credentials"
            (given "a registered user 'testuser' with password 'pass123'" 
              nil ; (print "Setting up user...")
            )
            (action "the user attempts to login with 'testuser' and 'pass123'"
              nil ; (print "Simulating login...")
            )
            (then "the login should be successful"
              nil ; (print "Verifying success...")
            )
            (then "a session token should be generated"
              nil ; (print "Verifying token...")
            )
          )
          
          (it "should deny login with incorrect credentials"
            (given "a registered user 'testuser' with password 'pass123'" nil)
            (action "the user attempts to login with 'testuser' and 'wrongpass'" nil)
            (then "the login should fail" nil)
          )
        )
        """
        run_lispy_string(lispy_code, self.env)

        self.assertEqual(len(registry.BDD_RESULTS), 1)
        feature = registry.BDD_RESULTS[0]
        self.assertEqual(feature["description"], "User Authentication")
        self.assertEqual(len(feature["scenarios"]), 2)

        scenario1 = feature["scenarios"][0]
        self.assertEqual(scenario1["description"], "should allow login with correct credentials")
        self.assertEqual(len(scenario1["steps"]), 4)
        self.assertEqual(scenario1["steps"][0]["keyword"], "Given")
        self.assertEqual(scenario1["steps"][0]["description"], "a registered user 'testuser' with password 'pass123'")
        self.assertEqual(scenario1["steps"][1]["keyword"], "Action")
        self.assertEqual(scenario1["steps"][2]["keyword"], "Then")
        self.assertEqual(scenario1["steps"][3]["keyword"], "Then")

        scenario2 = feature["scenarios"][1]
        self.assertEqual(scenario2["description"], "should deny login with incorrect credentials")
        self.assertEqual(len(scenario2["steps"]), 3)
        self.assertEqual(scenario2["steps"][0]["keyword"], "Given")
        self.assertEqual(scenario2["steps"][1]["keyword"], "Action")
        self.assertEqual(scenario2["steps"][2]["keyword"], "Then")

    def test_nested_describes_not_supported_yet(self):
        # Or decide if they should be. For now, let's assume they form separate top-level features.
        lispy_code = """
        (describe "Outer Feature"
            (describe "Inner Feature - treated as new top-level"
                (it "inner it" (given "g" ) (action "w") (then "t"))))
        """
        run_lispy_string(lispy_code, self.env)
        self.assertEqual(len(registry.BDD_RESULTS), 2)
        self.assertEqual(registry.BDD_RESULTS[0]["description"], "Outer Feature")
        self.assertEqual(len(registry.BDD_RESULTS[0]["scenarios"]), 0) # Inner describe is not a scenario of outer
        self.assertEqual(registry.BDD_RESULTS[1]["description"], "Inner Feature - treated as new top-level")
        self.assertEqual(len(registry.BDD_RESULTS[1]["scenarios"]), 1)

if __name__ == '__main__':
    unittest.main() 