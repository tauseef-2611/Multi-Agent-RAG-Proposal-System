# agents/pricing_agent.py - Calculates Project Pricing

import json
from typing import Dict, Any
from utils.mcp import create_mcp

class PricingAgent:
    """
    Agent responsible for calculating project pricing based on business rules.
    
    Key concepts to implement:
    1. Loading pricing rules from JSON configuration
    2. Rule-based calculation logic (not ML, pure business logic)
    3. Structured pricing breakdown
    4. MCP message creation for output
    """
    
    def __init__(self, pricing_rules_path: str = "data/pricing_rules.json"):
        """
        Initialize pricing agent with rules.
        
        TODO: Load pricing rules from JSON file
        Store rules in self.pricing_rules
        """
        
        # TODO: Load pricing rules from JSON file
        # self.pricing_rules = {...}
        try:
            with open(pricing_rules_path,'r') as f:
                self.pricing_rules=json.load(f)
        except FileNotFoundError:
            print(f"Warning: Pricing rules file not found at {pricing_rules_path}")
            self.pricing_rules = {}
    
    def calculate_pricing(self, project_mcp: Dict) -> Dict:
        """
        Calculate project pricing based on rules.
        
        Key concepts:
        1. Extract project details from MCP payload
        2. Apply base pricing rules by project type + complexity
        3. Apply timeline multipliers (rush jobs cost more)
        4. Add costs for additional services
        5. Calculate tax and total
        6. Return structured MCP response
        
        Args:
            project_mcp: MCP message with project details
            
        Returns:
            MCP message with pricing breakdown
        """
        
        # TODO: Implement pricing calculation
        # Steps:
        # 1. Extract project_data = project_mcp["payload"]
        # 2. Get base_price from rules based on project_type + complexity
        # 3. Apply timeline_multiplier based on timeline_weeks
        # 4. Calculate additional_services_cost
        # 5. Calculate subtotal, tax, total
        # 6. Create pricing_breakdown dictionary
        # 7. Return create_mcp with "PRICING_CALCULATED" message
        
        # Extract project data from MCP payload
        project_data = project_mcp["payload"]
        project_type = project_data.get("project_type", "website")
        complexity = project_data.get("complexity", "medium")
        timeline_weeks = project_data.get("timeline_weeks", 4)
        additional_services = project_data.get("additional_services", [])
        
        # NEW: Extract client information for advanced pricing
        is_recurring_client = project_data.get("is_recurring_client", False)
        client_type = project_data.get("client_type", "enterprise")  # enterprise, startup, nonprofit
        projects_completed_before = project_data.get("projects_completed_before", 0)
        
        # Get base price from pricing rules
        base_price = self.pricing_rules["base_pricing"][project_type][complexity]
        
        # Apply timeline multiplier
        timeline_multiplier = self.pricing_rules["timeline_multipliers"].get(str(timeline_weeks), 1.0)
        
        # Calculate additional services cost
        additional_cost = 0                
        for service in additional_services:
            additional_cost += self.pricing_rules["additional_services"].get(service, 0)
        
        # Calculate base subtotal (before client-specific adjustments)
        base_subtotal = (base_price * timeline_multiplier) + additional_cost
        
        # NEW: Apply client type pricing adjustments
        client_type_multiplier = self.pricing_rules.get("client_type_multipliers", {}).get(client_type, 1.0)
        
        # NEW: Apply recurring client discounts
        recurring_discount = 0
        if is_recurring_client:
            # Base recurring discount
            recurring_discount = self.pricing_rules.get("recurring_client_discount", 0.1)  # 10% default
            
            # Additional loyalty discount based on project history
            if projects_completed_before >= 5:
                recurring_discount += 0.05  # Extra 5% for 5+ projects
            elif projects_completed_before >= 3:
                recurring_discount += 0.03  # Extra 3% for 3+ projects
            elif projects_completed_before >= 1:
                recurring_discount += 0.02  # Extra 2% for 1+ projects
        
        # Apply all multipliers and discounts
        adjusted_price = base_subtotal * client_type_multiplier
        discount_amount = adjusted_price * recurring_discount
        subtotal = adjusted_price - discount_amount
        
        # Calculate tax and final total
        tax = subtotal * self.pricing_rules["tax_rate"]
        total = subtotal + tax
        
        # Create detailed pricing breakdown
        pricing_breakdown = {
            "base_price": base_price,
            "timeline_multiplier": timeline_multiplier,
            "additional_services_cost": additional_cost,
            "base_subtotal": base_subtotal,
            "client_type_multiplier": client_type_multiplier,
            "recurring_discount_rate": recurring_discount,
            "discount_amount": discount_amount,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "project_details": {
                "type": project_type,
                "complexity": complexity,
                "timeline_weeks": timeline_weeks,
                "services": additional_services,
                "client_type": client_type,
                "is_recurring_client": is_recurring_client,
                "projects_completed_before": projects_completed_before
            }
        }
        
        return create_mcp(
            sender="PricingAgent",
            receiver="Orchestrator",
            msg_type="PRICING_CALCULATED",
            payload={"pricing": pricing_breakdown}
        )
