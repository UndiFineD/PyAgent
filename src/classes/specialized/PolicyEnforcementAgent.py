import time

class PolicyEnforcementAgent:
    """
    Monitors agent activity against a set of governance-defined policies
    and enforces restrictions (quarantining) if violations occur.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = workspace_path
        self.active_policies = {
            "no_external_data_leak": True,
            "max_token_spend_per_hour": 100000,
            "required_security_scan": True
        }
        self.violation_log = []
        self.quarantine_list = set()
        
    def evaluate_action(self, agent_id, action_type, metadata):
        """
        Evaluates if an agent action complies with active policies.
        """
        violations = []
        
        if action_type == "external_push" and self.active_policies["no_external_data_leak"]:
            if "credentials" in str(metadata).lower():
                violations.append("DATA_LEAK_PREVENTION")
                
        if len(violations) > 0:
            self.violation_log.append({
                "agent_id": agent_id,
                "violations": violations,
                "timestamp": time.time()
            })
            return {"status": "violation", "details": violations}
            
        return {"status": "authorized"}

    def quarantine_agent(self, agent_id, reason):
        """
        Isolates an agent from the fleet.
        """
        self.quarantine_list.add(agent_id)
        return {"agent_id": agent_id, "status": "quarantined", "reason": reason}

    def is_agent_quarantined(self, agent_id):
        return agent_id in self.quarantine_list
