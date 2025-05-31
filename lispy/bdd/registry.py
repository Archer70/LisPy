from typing import List, Optional, Dict, Any

# These lists will act as stacks for current feature/scenario context
_active_features_stack: List[Dict[str, Any]] = []
_active_scenarios_stack: List[Dict[str, Any]] = []

# This will eventually hold all collected BDD results
BDD_RESULTS: List[Dict[str, Any]] = [] 

def clear_bdd_results():
    """Clears all stored BDD results and context."""
    global BDD_RESULTS, _active_features_stack, _active_scenarios_stack
    BDD_RESULTS = []
    _active_features_stack = []
    _active_scenarios_stack = []

def start_feature(description: str) -> None:
    """Starts a new feature block."""
    global BDD_RESULTS
    feature_details = {
        "description": description,
        "scenarios": [],
        "raw_output": [] # For any print statements etc. during feature setup
    }
    _active_features_stack.append(feature_details)
    BDD_RESULTS.append(feature_details) # Add to overall results immediately
    # print(f"[REGISTRY] Started Feature: {description}")

def end_feature() -> None:
    """Ends the current feature block."""
    if _active_features_stack:
        feature = _active_features_stack.pop()
        # print(f"[REGISTRY] Ended Feature: {feature['description']}")
    else:
        # This case should ideally not happen if start/end are paired
        print("[REGISTRY_WARNING] end_feature called without an active feature.")

def get_current_feature() -> Optional[Dict[str, Any]]:
    """Gets the currently active feature details, if any."""
    if _active_features_stack:
        return _active_features_stack[-1]
    return None

def start_scenario(description: str) -> None:
    """Starts a new scenario block within the current feature."""
    current_feature = get_current_feature()
    if not current_feature:
        # This indicates an 'it' block outside a 'describe' block.
        # The special form handler should catch this before calling start_scenario.
        raise Exception("INTERNAL ERROR: start_scenario called without an active feature.")

    scenario_details = {
        "description": description,
        "steps": [],
        "raw_output": [] # For any print statements etc. during scenario setup/execution
    }
    _active_scenarios_stack.append(scenario_details)
    current_feature["scenarios"].append(scenario_details)
    # print(f"[REGISTRY]   Started Scenario: {description}")

def end_scenario() -> None:
    """Ends the current scenario block."""
    if _active_scenarios_stack:
        scenario = _active_scenarios_stack.pop()
        # print(f"[REGISTRY]   Ended Scenario: {scenario['description']}")
    else:
        # This case should ideally not happen
        print("[REGISTRY_WARNING] end_scenario called without an active scenario.")

def get_current_scenario() -> Optional[Dict[str, Any]]:
    """Gets the currently active scenario details, if any."""
    if _active_scenarios_stack:
        return _active_scenarios_stack[-1]
    return None

def add_step(keyword: str, description: str, status: str = "passed", details: Optional[str] = None) -> None:
    """Adds a step (given, when, then) to the current scenario."""
    current_scenario = get_current_scenario()
    if not current_scenario:
        # This indicates a given/when/then block outside an 'it' block.
        # The special form handler should catch this.
        raise Exception("INTERNAL ERROR: add_step called without an active scenario.")

    step_details = {
        "keyword": keyword,
        "description": description,
        "status": status # 'passed', 'failed', 'skipped'
    }
    if details:
        step_details["details"] = details
        
    current_scenario["steps"].append(step_details)
    # print(f"[REGISTRY]     Added Step: {keyword.title()} {description} ({status})")

def mark_last_step_status(new_status: str, details: Optional[str] = None) -> None:
    """Marks the status of the last added step in the current scenario."""
    current_scenario = get_current_scenario()
    if not current_scenario:
        print("[REGISTRY_WARNING] mark_last_step_status called without an active scenario.")
        return
    
    if not current_scenario["steps"]:
        print("[REGISTRY_WARNING] mark_last_step_status called but no steps in current scenario.")
        return
        
    last_step = current_scenario["steps"][-1]
    last_step["status"] = new_status
    if details:
        last_step["details"] = details
    else:
        last_step.pop("details", None) # Remove details if new status doesn't have them
    # print(f"[REGISTRY]     Updated Step: {last_step['keyword']} {last_step['description']} to {new_status}")

# --- Functions for checking context (to be used by special form handlers) ---

def is_feature_context_active() -> bool:
    """Checks if a feature context is currently active."""
    return bool(_active_features_stack)

def is_scenario_context_active() -> bool:
    """Checks if a scenario context is currently active."""
    return bool(_active_scenarios_stack)

# Example of how results might look:
# BDD_RESULTS = [
#     {
#         "description": "Feature A", 
#         "scenarios": [
#             {"description": "Scenario A.1", "steps": [{"keyword": "Given", ...}, ...]},
#             {"description": "Scenario A.2", "steps": [...]},
#         ],
#         "raw_output": [] 
#     },
#     # ... more features
# ] 