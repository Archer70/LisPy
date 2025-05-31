import glob
import os
from typing import List, Dict, Any, Tuple

from lispy.bdd import registry, clear_bdd_results
# LispyInterpreter will be passed in, so no direct import needed to avoid circularity
# from .lispy_interpreter import LispyInterpreter # Avoid this if possible

EMOJI_PASS = "✅"
EMOJI_FAIL = "❌"
EMOJI_ERROR = "🔥"

def _print_bdd_summary(results: List[Dict[str, Any]]) -> Tuple[int, int, int, int, int]:
    """
    Prints a formatted summary of BDD results and returns counts.
    Returns: (total_features, total_scenarios, total_steps, passed_steps, failed_steps)
    """
    total_features = len(results)
    total_scenarios = 0
    total_steps = 0
    passed_steps = 0
    failed_steps = 0

    print("\n--- LisPy BDD Test Report ---")

    if not results:
        print("No BDD tests were found or executed.")
        return 0, 0, 0, 0, 0

    for feature_idx, feature in enumerate(results):
        feature_description = feature.get('description', 'Unnamed Feature')
        scenarios_in_feature = feature.get("scenarios", [])
        total_scenarios += len(scenarios_in_feature)
        
        feature_has_failures = False
        current_feature_passed_steps = 0
        current_feature_failed_steps = 0
        current_feature_total_steps = 0

        for scenario in scenarios_in_feature:
            steps_in_scenario = scenario.get("steps", [])
            current_feature_total_steps += len(steps_in_scenario)
            for step in steps_in_scenario:
                if step.get('status', 'unknown').upper() == "PASSED":
                    current_feature_passed_steps += 1
                else:
                    current_feature_failed_steps += 1
                    feature_has_failures = True
        
        passed_steps += current_feature_passed_steps
        failed_steps += current_feature_failed_steps
        total_steps += current_feature_total_steps

        if not feature_has_failures:
            print(f"{EMOJI_PASS} Feature {feature_idx + 1}: {feature_description} ... PASSED ({len(scenarios_in_feature)} scenarios, {current_feature_total_steps} steps)")
        else:
            print(f"{EMOJI_FAIL} Feature {feature_idx + 1}: {feature_description} ... FAILED")
            if feature.get("raw_output"):
                for line in feature["raw_output"]:
                    print(f"  [RAW_OUTPUT]: {line}")

            for scenario_idx, scenario in enumerate(scenarios_in_feature):
                scenario_description = scenario.get('description', 'Unnamed Scenario')
                steps_in_scenario = scenario.get("steps", [])
                scenario_has_failures = any(s.get('status', 'unknown').upper() != "PASSED" for s in steps_in_scenario)
                num_steps_in_scenario = len(steps_in_scenario)

                if not scenario_has_failures:
                    print(f"  {EMOJI_PASS} Scenario {scenario_idx + 1}: {scenario_description} ... PASSED ({num_steps_in_scenario} steps)")
                else:
                    print(f"  {EMOJI_FAIL} Scenario {scenario_idx + 1}: {scenario_description} ... FAILED")
                    if scenario.get("raw_output"):
                        for line in scenario["raw_output"]:
                            print(f"    [RAW_OUTPUT]: {line}")
                    
                    for step_idx, step in enumerate(steps_in_scenario):
                        status = step.get('status', 'unknown').upper()
                        # Only print failed steps in a failed scenario
                        if status != "PASSED":
                            keyword = step.get('keyword', '').title()
                            description = step.get('description', '')
                            details = step.get('details')
                            print(f"    {EMOJI_FAIL} {step_idx + 1}. {keyword} {description} ... {status}")
                            if details:
                                print(f"      Details: {details}")
    
    print("\n--- Summary ---")
    print(f"Features:  {total_features}")
    print(f"Scenarios: {total_scenarios}")
    # total_steps, passed_steps, failed_steps are now correctly aggregated before this point
    print(f"Steps:     {total_steps} (Passed: {passed_steps}, Failed: {failed_steps})")
    
    if failed_steps > 0:
        print(f"\n{EMOJI_FAIL} RESULT: FAILED")
    else:
        print(f"\n{EMOJI_PASS} RESULT: PASSED")
        
    return total_features, total_scenarios, total_steps, passed_steps, failed_steps

def run_bdd_tests(
    test_file_patterns: List[str], 
    interpreter: Any, # Actually LispyInterpreter, but type hint as Any to avoid import
    base_dir: str
) -> bool:
    """
    Runs BDD tests from the specified files or patterns.

    Args:
        test_file_patterns: A list of file paths or glob patterns for test files.
        interpreter: An instance of the LispyInterpreter.
        base_dir: The base directory to resolve glob patterns against.

    Returns:
        True if all tests passed, False otherwise.
    """
    clear_bdd_results()
    
    all_test_files: List[str] = []
    for pattern in test_file_patterns:
        # If it's an absolute path, glob will handle it.
        # If relative, it's relative to base_dir.
        if os.path.isabs(pattern):
            matched_files = glob.glob(pattern, recursive=True)
        else:
            matched_files = glob.glob(os.path.join(base_dir, pattern), recursive=True)
        
        for f in matched_files:
            if f.endswith(".lpy") and f not in all_test_files: # Ensure .lpy and unique
                all_test_files.append(f)

    if not all_test_files:
        # print(f"No BDD test files found matching patterns: {test_file_patterns}") # Removed verbosity
        _print_bdd_summary(registry.BDD_RESULTS) # Print empty summary (will say no tests found)
        return True # No tests found is not a failure of the runner itself

    # Removed: Printing found files and "Running tests in..."
    # print(f"Found {len(all_test_files)} BDD test file(s):")
    # for f_path in all_test_files:
    #     print(f"  - {f_path}")

    files_with_errors = 0
    for file_path in all_test_files:
        # print(f"\nRunning tests in: {file_path}...") # Removed verbosity
        return_code = interpreter.run_file(file_path, is_bdd_run=True)
        if return_code != 0:
            files_with_errors += 1
            # Still print file execution errors, as these are critical
            print(f"  {EMOJI_ERROR} CRITICAL ERROR executing BDD file {file_path}. Execution might be incomplete.")

    _, _, _, _, failed_steps_from_summary = _print_bdd_summary(registry.BDD_RESULTS)

    if failed_steps_from_summary > 0 or files_with_errors > 0:
        # The RESULT: FAILED is already printed by _print_bdd_summary if there are failed steps
        if files_with_errors > 0 and failed_steps_from_summary == 0:
            # If only file errors but no step failures, print FAILED here.
            print(f"\n{EMOJI_FAIL} RESULT: FAILED (due to critical file errors)") 
        print(f"Overall BDD Test Run Status: {files_with_errors} file(s) with critical errors, {failed_steps_from_summary} failed steps.")
        return False
    else:
        # The RESULT: PASSED is already printed by _print_bdd_summary
        # print("\nOverall BDD Test Run: PASSED") # Redundant
        return True

if __name__ == '__main__':
    # This part is for potential direct execution for testing the runner itself,
    # but it's primarily designed to be called from lispy_interpreter.py
    print("LisPy BDD Runner (intended to be invoked via lispy_interpreter.py --bdd)")
    pass 