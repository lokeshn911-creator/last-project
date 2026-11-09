# mock_llm.py
import json
import random

class TransientLLMError(Exception):
    """Raised when the LLM service experiences a temporary 503 error."""
    pass

def chat(messages, temperature=0.0):
    """Mock LLM chat function for testing triage and agent logic."""
    # Simulate occasional transient 503 errors (approx 10% chance)
    if random.random() < 0.1:
        raise TransientLLMError("Temporary service unavailable (503)")
        
    # Extract user message content
    user_msg = ""
    for msg in messages:
        if msg.get("role") == "user":
            user_msg = msg.get("content", "")
            
    # Simple rule-based mock responses for triage/agent testing
    text_lower = user_msg.lower()
    
    if "refund" in text_lower or "money" in text_lower or "charged" in text_lower:
        response_data = {
            "category": "billing",
            "reason": "Customer inquiry regarding financial charges or refunds."
        }
    elif "fraud" in text_lower or "unauthorized" in text_lower:
        response_data = {
            "category": "fraud",
            "reason": "Customer reported suspicious or unauthorized account activity."
        }
    else:
        response_data = {
            "category": "technical",
            "reason": "General support or technical query."
        }
        
    class MockMessage:
        def __init__(self, content):
            self.content = content

    class MockChoice:
        def __init__(self, message):
            self.message = message

    class MockResponse:
        def __init__(self, choices):
            self.choices = choices

    return MockResponse([MockChoice(MockMessage(json.dumps(response_data)))])