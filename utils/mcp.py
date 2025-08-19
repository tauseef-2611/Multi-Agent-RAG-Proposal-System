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

def test_mcp():
    """
    Test function to debug and verify MCP implementation.
    """
    print("🧪 Testing MCP Implementation")
    print("="*50)
    
    # Test 1: Create a basic MCP message
    print("\n📝 Test 1: Creating Basic MCP Message")
    print("-" * 30)
    
    sample_payload = {
        "total_price": 15000,
        "project_type": "website",
        "complexity": "medium"
    }
    
    message = create_mcp(
        sender="PricingAgent",
        receiver="Orchestrator",
        msg_type="PRICING_CALCULATED",
        payload=sample_payload
    )
    
    print(f"✅ Message created successfully!")
    print(f"📄 Message structure:")
    for key, value in message.items():
        if key == "payload":
            print(f"   {key}: {value}")
        else:
            print(f"   {key}: {value}")
    
    # Test 2: Validate the created message
    print("\n🔍 Test 2: Validating Created Message")
    print("-" * 30)
    
    is_valid = validate_mcp(message)
    print(f"✅ Basic validation result: {is_valid}")
    
    # Test 3: Validate with expected type
    print("\n🎯 Test 3: Validating with Expected Type")
    print("-" * 30)
    
    is_valid_with_type = validate_mcp(message, "PRICING_CALCULATED")
    print(f"✅ Type-specific validation result: {is_valid_with_type}")
    
    # Test 4: Test with wrong expected type
    print("\n❌ Test 4: Testing Wrong Expected Type")
    print("-" * 30)
    
    is_valid_wrong_type = validate_mcp(message, "RETRIEVAL_RESULT")
    print(f"❌ Wrong type validation result: {is_valid_wrong_type} (should be False)")
    
    # Test 5: Test with invalid message (missing keys)
    print("\n🚫 Test 5: Testing Invalid Message (Missing Keys)")
    print("-" * 30)
    
    invalid_message = {
        "type": "TEST",
        "sender": "TestAgent"
        # Missing required keys: receiver, trace_id, timestamp, payload
    }
    
    is_invalid = validate_mcp(invalid_message)
    print(f"🚫 Invalid message validation result: {is_invalid} (should be False)")
    
    # Test 6: Test message uniqueness
    print("\n🔄 Test 6: Testing Message Uniqueness")
    print("-" * 30)
    
    message2 = create_mcp(
        sender="WritingAgent",
        receiver="Orchestrator",
        msg_type="SECTIONS_GENERATED",
        payload={"sections": {"intro": "Sample intro text"}}
    )
    
    print(f"📋 Message 1 trace_id: {message['trace_id']}")
    print(f"📋 Message 2 trace_id: {message2['trace_id']}")
    print(f"🔄 Trace IDs are unique: {message['trace_id'] != message2['trace_id']}")
    
    # Test 7: Test timestamp format
    print("\n⏰ Test 7: Testing Timestamp Format")
    print("-" * 30)
    
    print(f"⏰ Message 1 timestamp: {message['timestamp']}")
    print(f"⏰ Message 2 timestamp: {message2['timestamp']}")
    print(f"📅 Timestamp format is ISO: {'T' in message['timestamp'] and 'T' in message2['timestamp']}")
    
    # Test 8: Complex payload test
    print("\n📦 Test 8: Testing Complex Payload")
    print("-" * 30)
    
    complex_payload = {
        "pricing": {
            "base_price": 12000,
            "additional_services": 3000,
            "tax": 1200,
            "total": 16200
        },
        "project_details": {
            "type": "ecommerce",
            "timeline": 8,
            "features": ["shopping_cart", "payment_gateway", "inventory"]
        },
        "metadata": {
            "estimated_hours": 160,
            "team_size": 3
        }
    }
    
    complex_message = create_mcp(
        sender="PricingAgent",
        receiver="TemplateAgent",
        msg_type="COMPLEX_PRICING",
        payload=complex_payload
    )
    
    is_complex_valid = validate_mcp(complex_message, "COMPLEX_PRICING")
    print(f"✅ Complex message validation: {is_complex_valid}")
    print(f"📦 Complex payload keys: {list(complex_payload.keys())}")
    
    # Summary
    print("\n🎉 Test Summary")
    print("="*50)
    print(f"✅ Basic message creation: PASSED")
    print(f"✅ Basic validation: {'PASSED' if is_valid else 'FAILED'}")
    print(f"✅ Type validation: {'PASSED' if is_valid_with_type else 'FAILED'}")
    print(f"✅ Wrong type rejection: {'PASSED' if not is_valid_wrong_type else 'FAILED'}")
    print(f"✅ Invalid message rejection: {'PASSED' if not is_invalid else 'FAILED'}")
    print(f"✅ Unique trace IDs: {'PASSED' if message['trace_id'] != message2['trace_id'] else 'FAILED'}")
    print(f"✅ Complex payload handling: {'PASSED' if is_complex_valid else 'FAILED'}")
    
    print(f"\n🚀 MCP Implementation Status: READY FOR USE!")

# Run tests if this file is executed directly
if __name__ == "__main__":
    test_mcp()
