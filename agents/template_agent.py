# agents/template_agent.py - Generates Final PDF from Template

from jinja2 import Template
import weasyprint
from io import BytesIO
from typing import Dict
from utils.mcp import create_mcp

class TemplateAgent:
    """
    Agent responsible for generating final PDF proposal from template.
    
    Key concepts to implement:
    1. HTML template loading and management
    2. Jinja2 template rendering with dynamic data
    3. PDF generation from HTML using WeasyPrint
    4. Binary data handling for PDF output
    """
    
    def __init__(self, template_path: str = "data/templates/proposal_template.html"):
        """
        Initialize template agent with HTML template.
        
        TODO: Load HTML template file and create Jinja2 Template object
        """
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            self.template = Template(template_content)
        except FileNotFoundError:
            print(f"Warning: Template file not found at {template_path}")
            self.template = Template("<html><body><h1>Error: Template not found</h1></body></html>")
    
    def generate_pdf_proposal(self, combined_data_mcp: Dict) -> Dict:
        """
        Generate final PDF proposal from all agent outputs.
        
        Key concepts:
        1. Data extraction from combined MCP message
        2. HTML rendering using Jinja2 template
        3. PDF generation using WeasyPrint
        4. Binary data handling and return
        
        Args:
            combined_data_mcp: MCP message with all aggregated data
            
        Returns:
            MCP message with PDF bytes and HTML content
        """
        
        # Extract data from MCP payload
        data = combined_data_mcp["payload"]
        
        # Render HTML from template
        html_content = self.template.render(
            client_name=data.get("client_name", "Valued Client"),
            project_type=data.get("project_type", "Website"),
            sections=data.get("sections", {}),
            pricing=data.get("pricing", {}),
            case_studies=data.get("relevant_cases", []),
            company_name="Creative Agency Pro",
            date=data.get("date", ""),
            timeline_weeks=data.get("timeline_weeks", 4)
        )
        
        # Create PDF buffer
        pdf_buffer = BytesIO()
        pdf_bytes = None
        
        # Try to generate PDF from HTML
        try:
            # Import WeasyPrint specifically to avoid conflicts
            from weasyprint import HTML as WeasyHTML, CSS
            
            # Create WeasyPrint HTML document
            html_doc = WeasyHTML(string=html_content)
            
            # Write PDF to buffer
            html_doc.write_pdf(pdf_buffer)
            
            # Extract PDF bytes
            pdf_bytes = pdf_buffer.getvalue()
            
            print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
            
        except ImportError as e:
            print(f"Warning: WeasyPrint not installed properly: {e}")
            print("Install with: pip install weasyprint")
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            print(f"Error type: {type(e)}")
            print("Continuing with HTML-only output...")
        
        # Return appropriate MCP message
        if pdf_bytes:
            # PDF generation successful
            return create_mcp(
                sender="TemplateAgent",
                receiver="Orchestrator",
                msg_type="PDF_GENERATED",
                payload={
                    "pdf_bytes": pdf_bytes,
                    "html_content": html_content
                }
            )
        else:
            # PDF generation failed, return HTML only
            return create_mcp(
                sender="TemplateAgent",
                receiver="Orchestrator",
                msg_type="HTML_GENERATED",
                payload={
                    "html_content": html_content,
                    "note": "PDF generation unavailable - HTML output provided"
                }
            )
