# orchestrator.py - Main Coordinator for All Agents

from agents.pricing_agent import PricingAgent
from agents.writing_agent import WritingAgent
from agents.case_study_agent import CaseStudyAgent
from agents.template_agent import TemplateAgent
from utils.mcp import create_mcp, validate_mcp
from typing import Dict
import streamlit as st

class ProposalOrchestrator:
    """
    Main orchestrator that coordinates all agents to generate complete proposals.
    
    Key concepts to implement:
    1. Agent initialization and management
    2. Sequential agent execution with error handling
    3. Data flow between agents using MCP protocol
    4. Progress tracking with Streamlit spinners
    5. Result aggregation and validation
    """
    
    def __init__(self):
        """
        Initialize all agents for proposal generation.
        """
        print("🚀 Initializing Proposal Orchestrator...")
        
        # Initialize all agents
        try:
            print("💰 Loading Pricing Agent...")
            self.pricing_agent = PricingAgent()
            
            print("✍️ Loading Writing Agent...")
            self.writing_agent = WritingAgent()
            
            print("🔍 Loading Case Study Agent...")
            self.case_study_agent = CaseStudyAgent()
            
            print("📄 Loading Template Agent...")
            self.template_agent = TemplateAgent()
            
            print("✅ All agents initialized successfully!")
            
        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            raise e
    
    def generate_complete_proposal(self, project_data: Dict) -> Dict:
        """
        Orchestrate all agents to generate complete proposal.
        
        Flow:
        1. Create initial MCP message from project data
        2. Call pricing agent -> get pricing breakdown
        3. Call writing agent -> get proposal sections
        4. Call case study agent -> get relevant examples
        5. Combine all data and call template agent -> get final PDF
        
        Returns: MCP message with final PDF and all data
        """
        
        try:
            # Step 1: Create initial MCP message from project data
            project_mcp = create_mcp(
                sender="UserInterface",
                receiver="Orchestrator",
                msg_type="PROPOSAL_REQUEST",
                payload=project_data
            )
            
            print(f"📋 Starting proposal generation for {project_data.get('client_name', 'Client')}")
            
            # Step 2: Calculate pricing
            with st.spinner("💰 Calculating pricing..."):
                pricing_mcp = self.pricing_agent.calculate_pricing(project_mcp)
                
                if not validate_mcp(pricing_mcp, "PRICING_CALCULATED"):
                    raise Exception("Pricing calculation failed - invalid MCP response")
                
                print(f"✅ Pricing calculated: ${pricing_mcp['payload']['pricing']['total']:,.2f}")
            
            # Step 3: Generate proposal sections
            with st.spinner("✍️ Writing proposal sections..."):
                sections_mcp = self.writing_agent.generate_proposal_sections(project_mcp)
                
                if not validate_mcp(sections_mcp, "PROPOSAL_SECTIONS_GENERATED"):
                    raise Exception("Proposal writing failed - invalid MCP response")
                
                sections = sections_mcp['payload']['sections']
                print(f"✅ Generated {len(sections)} proposal sections")
            
            # Step 4: Retrieve relevant case studies
            with st.spinner("🔍 Finding relevant case studies..."):
                cases_mcp = self.case_study_agent.retrieve_relevant_cases(project_mcp, k=3)
                
                if not validate_mcp(cases_mcp, "CASE_STUDIES_RETRIEVED"):
                    raise Exception("Case study retrieval failed - invalid MCP response")
                
                relevant_cases = cases_mcp['payload']['relevant_cases']
                print(f"✅ Found {len(relevant_cases)} relevant case studies")
            
            # Step 5: Combine all data for template generation
            combined_data = {
                **project_data,  # Original project data
                "pricing": pricing_mcp["payload"]["pricing"],
                "sections": sections_mcp["payload"]["sections"],
                "relevant_cases": cases_mcp["payload"]["relevant_cases"]
            }
            
            combined_mcp = create_mcp(
                sender="Orchestrator",
                receiver="TemplateAgent",
                msg_type="GENERATE_PDF",
                payload=combined_data
            )
            
            # Step 6: Generate final PDF
            with st.spinner("📄 Generating PDF proposal..."):
                pdf_mcp = self.template_agent.generate_pdf_proposal(combined_mcp)
                
                # Accept both PDF_GENERATED and HTML_GENERATED (fallback)
                if not validate_mcp(pdf_mcp, "PDF_GENERATED") and not validate_mcp(pdf_mcp, "HTML_GENERATED"):
                    raise Exception("PDF generation failed - invalid MCP response")
                
                print(f"✅ Final document generated: {pdf_mcp['type']}")
            
            # Step 7: Combine all data into final response
            final_payload = {
                **combined_data,  # All the combined data from previous steps
                **pdf_mcp["payload"]  # Add PDF/HTML content from template agent
            }
            
            # Return complete result with all agent outputs
            return create_mcp(
                sender="Orchestrator",
                receiver="UserInterface", 
                msg_type=pdf_mcp["type"],  # Keep the PDF_GENERATED or HTML_GENERATED type
                payload=final_payload
            )
            
        except Exception as e:
            st.error(f"❌ Proposal generation failed: {str(e)}")
            print(f"❌ Orchestration error: {e}")
            
            # Return error MCP
            return create_mcp(
                sender="Orchestrator",
                receiver="UserInterface",
                msg_type="GENERATION_ERROR",
                payload={
                    "error": str(e),
                    "partial_data": locals().get('combined_data', {})
                }
            )
