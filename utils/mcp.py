# utils/mcp.py - Message Communication Protocol

import uuid
from datetime import datetime
from typing import Dict, Any

def create_mcp(sender: str, receiver: str, msg_type: str, payload: Dict[Any, Any]) -> Dict:
    """
    Create standardized message between agents.
    
    Key concepts:
    1. Structured communication between agents
    2. Unique trace IDs for debugging
    3. Timestamp tracking
    4. Consistent message format
    
    Args:
        sender: Agent sending the message
        receiver: Agent receiving the message
        msg_type: Type of message (e.g., "PRICING_CALCULATED")
        payload: Actual data being sent
    
    Returns:
        Standardized MCP message dictionary
    """
    
    # TODO: Implement MCP creation
    # Should return a dictionary with:
    # - type: msg_type
    # - sender: sender agent name
    # - receiver: receiver agent name  
    # - trace_id: unique UUID for tracking
    # - timestamp: current ISO timestamp
    # - payload: the actual data

    return{
        "type":msg_type,
        "sender":sender,
        "receiver":receiver,
        "trace_id":str(uuid.uuid4()),
        "timestamp":datetime.now().isoformat(),
        "payload":payload
    }
    

def validate_mcp(mcp: Dict, expected_type: str = None) -> bool:
    """
    Validate MCP message structure.
    
    Key concepts:
    1. Input validation and error prevention
    2. Message format consistency
    3. Optional type checking
    
    Args:
        mcp: Message to validate
        expected_type: Optional expected message type
    
    Returns:
        True if valid, False otherwise
    """
    
    # TODO: Implement validation logic
    # Check for required keys: type, sender, receiver, trace_id, payload
    # Optionally check if type matches expected_type
    # Return True/False based on validation
    
    required_keys=["type","sender","receiver","trace_id","timestamp","payload"]
    if not all(key in mcp for key in required_keys):
        return False
    
    if expected_type and mcp["type"]!=expected_type:
        return False
    return True