
import logging
import time
from typing import Dict
from src.core.base.core.AuthCore import AuthCore

class AuthManager:
    """Shell for agent authentication and access control.
    Wraps AuthCore with stateful session management.
    """
    
    def __init__(self) -> None:
        self.core = AuthCore()
        self.pending_challenges: Dict[str, str] = {} # agent_id -> challenge
        self.sessions: Dict[str, float] = {} # agent_id -> expiry

    def initiate_auth(self, agent_id: str) -> str:
        """Starts auth flow by issuing a challenge."""
        challenge = self.core.generate_challenge(agent_id)
        self.pending_challenges[agent_id] = challenge
        logging.info(f"Auth: Issued challenge for {agent_id}")
        return challenge

    def authenticate(self, agent_id: str, proof: str) -> bool:
        """Completes auth flow using the provided proof."""
        challenge = self.pending_challenges.pop(agent_id, None)
        if not challenge:
            return False
            
        # Mock: we assume we have a way to look up the agent's public artifact/hash
        mock_secret_hash = "secret_hash_123"
        
        if self.core.verify_proof(challenge, proof, mock_secret_hash):
            self.sessions[agent_id] = time.time() + 3600
            logging.info(f"Auth: Agent {agent_id} verified successfully.")
            return True
            
        return False