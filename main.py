"""
Automated Proposal & Pricing Agent - Main Application

This is the main Streamlit interface for the multi-agent RAG system.
Demonstrates:
- User interface design
- Form validation and data collection
- Progress tracking during agent execution
- Results display and download options
- Error handling and user feedback

Architecture:
User Input -> Orchestrator -> [Pricing, Writing, Case Study, Template] Agents -> Final PDF

Learning Concepts:
1. Streamlit application development
2. Form-based data collection
3. Multi-a    # Render sidebar and handle demo/example loading
    demo_or_example_data = render_sidebar()
    
    # Handle demo/example data loading
    if demo_or_example_data:
        if demo_or_example_data == {}:  # Clear action
            st.session_state.demo_data = {}
            st.success("🧹 Form cleared! You can now enter your own project details.")
        else:  # Load demo/example
            st.session_state.demo_data = demo_or_example_data
            project_title = demo_or_example_data.get('project_title', 'Example Project')
            st.success(f"✅ Loaded: **{project_title}**")
            
            # Show brief info about loaded data
            st.info("📋 Form fields have been pre-filled with the selected example. You can modify any fields before generating the proposal.")
        
        st.rerun()  # Refresh to update form with new data
4. Progress visualization
5. File download functionality
"""

import streamlit as st
import json
import tempfile
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# Import our orchestrator
from orchestrator import ProposalOrchestrator

# Page configuration
st.set_page_config(
    page_title="Automated Proposal & Pricing Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #1f77b4;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}
.section-header {
    color: #2e86c1;
    font-size: 1.5rem;
    margin: 1rem 0;
    border-bottom: 2px solid #2e86c1;
    padding-bottom: 0.5rem;
}
.success-box {
    padding: 1rem;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
.error-box {
    padding: 1rem;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    
    if 'proposal_generated' not in st.session_state:
        st.session_state.proposal_generated = False
    
    if 'proposal_data' not in st.session_state:
        st.session_state.proposal_data = None
    
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    
    if 'demo_data' not in st.session_state:
        st.session_state.demo_data = {}

def load_orchestrator():
    """Load and cache the orchestrator with all agents."""
    if st.session_state.orchestrator is None:
        with st.spinner("🤖 Initializing AI agents..."):
            try:
                st.session_state.orchestrator = ProposalOrchestrator()
                st.success("✅ All agents initialized successfully!")
            except Exception as e:
                st.error(f"❌ Failed to initialize agents: {e}")
                return False
    return True

def render_sidebar():
    """Render the sidebar with optional demo loading and clear instructions."""
    st.sidebar.markdown("## 🎛️ **Project Setup**")
    
    # Quick actions section
    st.sidebar.markdown("### 🚀 **Quick Start**")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📊 Demo", help="Load comprehensive enterprise project example", use_container_width=True):
            return load_demo_project()
    
    with col2:
        if st.button("🧹 Clear", help="Clear all form fields", use_container_width=True):
            return {}  # This will clear the demo_data
    
    st.sidebar.markdown("---")
    
    # Example projects section
    st.sidebar.markdown("### 📋 **Example Templates**")
    
    if st.sidebar.button("💻 E-commerce Platform", help="Online store with payment integration"):
        return load_example_project("ecommerce")
    
    if st.sidebar.button("🏥 Healthcare Portal", help="Patient management system"):
        return load_example_project("healthcare")
    
    if st.sidebar.button("📱 Mobile App", help="Cross-platform mobile application"):
        return load_example_project("mobile")
    
    if st.sidebar.button("📊 Analytics Dashboard", help="Business intelligence platform"):
        return load_example_project("analytics")
    
    st.sidebar.markdown("---")
    
    # How it works section
    st.sidebar.markdown("### � **Agent Workflow**")
    
    st.sidebar.markdown("""
    **1. � Pricing Agent**
    - Rule-based cost calculation
    - Complexity assessment
    
    **2. ✍️ Writing Agent** 
    - AI-powered content generation
    - Professional proposal sections
    
    **3. 🔍 Case Study Agent**
    - RAG similarity search
    - Relevant project examples
    
    **4. 🎨 Template Agent**
    - PDF generation
    - Professional formatting
    """)
    
    st.sidebar.markdown("---")
    
    # Tips section
    st.sidebar.markdown("### � **Tips**")
    st.sidebar.markdown("""
    - Use **specific requirements** for better results
    - Include **technical details** for accurate matching
    - Choose **realistic timelines** and budgets
    - Load examples to understand the format
    """)
    
    return None

def load_demo_project() -> Dict:
    """Load a comprehensive demo project for testing."""
    return {
        "client_name": "TechCorp Solutions",
        "project_title": "Enterprise Digital Transformation Platform",
        "project_description": "Design and develop a comprehensive digital transformation platform that integrates customer relationship management, inventory tracking, employee management, and advanced analytics. The platform will feature a modern responsive web interface, mobile applications for iOS and Android, real-time data visualization dashboards, automated reporting systems, and secure API integrations with existing enterprise systems. This solution aims to streamline business operations, improve decision-making through data insights, and enhance overall organizational efficiency.",
        "client_type": "enterprise",
        "timeline_months": 8,
        "budget_range": "$100,000 - $250,000",
        "recurring_client": True,
        "priority_client": False,
        "requirements": [
            "Responsive web application with modern UI/UX",
            "Mobile applications for iOS and Android",
            "Real-time analytics and reporting dashboard",
            "Customer relationship management (CRM) module",
            "Inventory management system",
            "Employee management and HR integration",
            "Secure API development and integrations",
            "Data visualization and business intelligence",
            "Multi-role user authentication and authorization",
            "Automated email notifications and alerts",
            "Cloud deployment with scalable infrastructure",
            "Comprehensive testing and quality assurance"
        ],
        "target_technologies": [
            "React.js", "TypeScript", "Node.js", "Express.js", 
            "PostgreSQL", "Redis", "Docker", "AWS", 
            "React Native", "GraphQL", "JWT Authentication",
            "Chart.js", "Material-UI", "Jest", "Cypress"
        ]
    }

def load_example_project(project_type: str) -> Dict:
    """Load predefined example projects."""
    examples = {
        "ecommerce": {
            "client_name": "TechStart Solutions",
            "project_title": "E-commerce Platform Development",
            "project_description": "Build a modern e-commerce platform with product catalog, shopping cart, payment integration, and admin dashboard. Requires mobile-responsive design and SEO optimization.",
            "client_type": "startup",
            "timeline_months": 4,
            "budget_range": "$25,000 - $50,000",
            "requirements": [
                "Product catalog management",
                "Shopping cart and checkout",
                "Payment gateway integration",
                "User authentication and profiles",
                "Admin dashboard",
                "Mobile responsive design",
                "SEO optimization"
            ],
            "target_technologies": ["React", "Node.js", "MongoDB", "Stripe API"]
        },
        "enterprise": {
            "client_name": "Global Manufacturing Corp",
            "project_title": "Enterprise Resource Planning System",
            "project_description": "Comprehensive ERP system for manufacturing operations including inventory management, supply chain tracking, financial reporting, and workforce management.",
            "client_type": "enterprise",
            "timeline_months": 12,
            "budget_range": "$100,000 - $250,000",
            "requirements": [
                "Inventory management system",
                "Supply chain tracking",
                "Financial reporting module",
                "Workforce management",
                "Real-time analytics dashboard",
                "Multi-location support",
                "Integration with existing systems"
            ],
            "target_technologies": ["Java", "Spring Boot", "PostgreSQL", "Angular", "Microservices"]
        },
        "mobile": {
            "client_name": "FitLife Wellness",
            "project_title": "Fitness Tracking Mobile Application",
            "project_description": "Cross-platform mobile app for fitness tracking with workout plans, nutrition logging, progress analytics, and social features for community engagement.",
            "client_type": "small_business",
            "timeline_months": 6,
            "budget_range": "$40,000 - $80,000",
            "requirements": [
                "Cross-platform mobile app",
                "Workout tracking and plans",
                "Nutrition logging",
                "Progress analytics",
                "Social features",
                "Wearable device integration",
                "Offline functionality"
            ],
            "target_technologies": ["React Native", "Firebase", "TensorFlow Lite", "GraphQL"]
        }
    }
    
    return examples.get(project_type, {})

def render_project_form() -> Optional[Dict]:
    """Render the main project input form."""
    st.markdown('<h2 class="section-header">📝 Project Information</h2>', unsafe_allow_html=True)
    
    # Check if demo data should be loaded
    demo_data = st.session_state.get('demo_data', {})
    
    with st.form("project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input(
                "Client Name *",
                value=demo_data.get("client_name", ""),
                placeholder="e.g., TechStart Solutions",
                help="Name of the client or company"
            )
            
            project_title = st.text_input(
                "Project Title *",
                value=demo_data.get("project_title", ""),
                placeholder="e.g., E-commerce Platform Development",
                help="Concise title describing the project"
            )
            
            client_type = st.selectbox(
                "Client Type *",
                ["startup", "small_business", "enterprise"],
                index=["startup", "small_business", "enterprise"].index(demo_data.get("client_type", "startup")),
                help="Affects pricing multipliers and approach"
            )
            
            timeline_months = st.slider(
                "Timeline (Months) *",
                min_value=1,
                max_value=24,
                value=demo_data.get("timeline_months", 6),
                help="Expected project duration"
            )
        
        with col2:
            budget_options = [
                "Under $10,000",
                "$10,000 - $25,000", 
                "$25,000 - $50,000",
                "$50,000 - $100,000",
                "$100,000 - $250,000",
                "Over $250,000"
            ]
            default_budget = demo_data.get("budget_range", "$25,000 - $50,000")
            budget_index = budget_options.index(default_budget) if default_budget in budget_options else 2
            
            budget_range = st.selectbox(
                "Budget Range *",
                budget_options,
                index=budget_index,
                help="Expected budget range for the project"
            )
            
            recurring_client = st.checkbox(
                "Recurring Client",
                value=demo_data.get("recurring_client", False),
                help="Client has worked with us before (discount applies)"
            )
            
            priority_client = st.checkbox(
                "Priority Client",
                value=demo_data.get("priority_client", False),
                help="High-priority client requiring expedited service"
            )
        
        project_description = st.text_area(
            "Project Description *",
            value=demo_data.get("project_description", ""),
            placeholder="Describe the project goals, features, and requirements in detail...",
            height=120,
            help="Detailed description used for case study matching and content generation"
        )
        
        # Requirements as tags
        st.markdown("**Key Requirements:**")
        default_requirements = "\n".join(demo_data.get("requirements", []))
        requirements_text = st.text_area(
            "Requirements (one per line)",
            value=default_requirements,
            placeholder="User authentication\nPayment integration\nMobile responsive design\nAPI development",
            height=100,
            help="List major requirements, one per line"
        )
        
        # Technologies
        default_technologies = ", ".join(demo_data.get("target_technologies", []))
        technologies_text = st.text_input(
            "Target Technologies (comma-separated)",
            value=default_technologies,
            placeholder="React, Node.js, MongoDB, AWS",
            help="Preferred technologies or tech stack"
        )
        
        submitted = st.form_submit_button("🚀 Generate Proposal", type="primary")
        
        if submitted:
            # Validation
            if not all([client_name, project_title, project_description]):
                st.error("❌ Please fill in all required fields marked with *")
                return None
            
            # Process requirements and technologies
            requirements = [req.strip() for req in requirements_text.split('\n') if req.strip()]
            technologies = [tech.strip() for tech in technologies_text.split(',') if tech.strip()]
            
            # Build project data
            project_data = {
                "client_name": client_name,
                "project_title": project_title,
                "project_description": project_description,
                "client_type": client_type,
                "timeline_months": timeline_months,
                "budget_range": budget_range,
                "recurring_client": recurring_client,
                "priority_client": priority_client,
                "requirements": requirements,
                "target_technologies": technologies,
                "submission_date": datetime.now().isoformat()
            }
            
            return project_data
    
    return None

def render_proposal_results(proposal_result: Dict):
    """Render the generated proposal results."""
    st.markdown('<h2 class="section-header">🎉 Proposal Generated Successfully!</h2>', unsafe_allow_html=True)
    
    if proposal_result.get('type') == 'GENERATION_ERROR':
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f"❌ Generation failed: {proposal_result['payload']['error']}")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    payload = proposal_result.get('payload', {})
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pricing_data = payload.get('pricing', {})
        total_cost = pricing_data.get('total', 0)
        # Calculate discount percentage from discount amount and base price
        base_price = pricing_data.get('base_price', 0)
        discount_amount = pricing_data.get('discount_amount', 0)
        discount_percent = (discount_amount / base_price * 100) if base_price > 0 else 0
        
        st.metric(
            "Total Cost",
            f"${total_cost:,.2f}",
            delta=f"{discount_percent:.1f}% discount" if discount_amount > 0 else "No discount applied"
        )
    
    with col2:
        timeline_months = payload.get('timeline_months', 0)
        st.metric(
            "Timeline",
            f"{timeline_months} months",
            delta="As requested"
        )
    
    with col3:
        sections = payload.get('sections', {})
        st.metric(
            "Proposal Sections",
            len(sections),
            delta="AI generated"
        )
    
    with col4:
        cases = payload.get('relevant_cases', [])
        st.metric(
            "Relevant Cases",
            len(cases),
            delta="RAG retrieved"
        )
    
    # Tabs for detailed view
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Pricing", "📝 Content", "🔍 Case Studies", "📄 Download", "🔧 Debug"])
    
    with tab1:
        st.markdown("### Pricing Breakdown")
        pricing = payload.get('pricing', {})
        
        if pricing:
            st.json(pricing)
        else:
            st.warning("No pricing data available")
    
    with tab2:
        st.markdown("### Generated Content")
        sections = payload.get('sections', {})
        
        for section_name, content in sections.items():
            st.markdown(f"#### {section_name.replace('_', ' ').title()}")
            st.markdown(content)
            st.markdown("---")
    
    with tab3:
        st.markdown("### Relevant Case Studies")
        cases = payload.get('relevant_cases', [])
        
        for i, case in enumerate(cases, 1):
            with st.expander(f"📋 Case Study {i}: {case.get('title', 'Untitled')}"):
                st.markdown(f"**Similarity Score:** {case.get('similarity_score', 0):.3f}")
                st.markdown(f"**Description:** {case.get('description', 'No description')}")
                st.markdown(f"**Technologies:** {', '.join(case.get('technologies', []))}")
    
    with tab4:
        st.markdown("### Download Options")
        
        # Check if we have PDF or HTML
        if 'pdf_bytes' in payload:
            st.download_button(
                label="📄 Download PDF Proposal",
                data=payload['pdf_bytes'],
                file_name=f"proposal_{payload.get('client_name', 'client').replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF generated successfully!")
        
        elif 'html_content' in payload:
            st.download_button(
                label="🌐 Download HTML Proposal",
                data=payload['html_content'],
                file_name=f"proposal_{payload.get('client_name', 'client').replace(' ', '_')}.html",
                mime="text/html"
            )
            st.warning("⚠️ PDF generation failed, HTML version available")
        
        else:
            st.error("❌ No downloadable content generated")
        
        # Raw data download
        proposal_json = json.dumps(payload, indent=2, default=str)
        st.download_button(
            label="📊 Download Raw Data (JSON)",
            data=proposal_json,
            file_name=f"proposal_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with tab5:
        st.markdown("### Debug Information")
        st.markdown("**Full MCP Response:**")
        st.json(proposal_result)

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Main title
    st.markdown('<h1 class="main-title">🤖 Automated Proposal & Pricing Agent</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to the **Multi-Agent RAG System** for automated proposal generation! 
    This demonstrates advanced AI concepts including:
    - 🧠 **LangChain** for LLM integration
    - 🔍 **FAISS** for similarity search
    - 🤖 **Multi-agent architecture** 
    - 📊 **Business rule engines**
    - 📄 **Document generation**
    """)
    
    # Load orchestrator
    if not load_orchestrator():
        st.stop()
    
    # Render sidebar and handle demo/example loading
    demo_or_example_data = render_sidebar()
    
    # If demo or example was loaded, store in session state and show notification
    if demo_or_example_data:
        st.session_state.demo_data = demo_or_example_data
        st.success(f"✅ Loaded: {demo_or_example_data.get('project_title', 'Project Data')}")
        
        # Show loaded data in an expander
        with st.expander("📋 Loaded Project Data", expanded=False):
            st.json(demo_or_example_data)
        
        st.info("👆 The form above has been pre-filled with the loaded data. You can modify any fields as needed before generating the proposal.")
        
        # Add a clear button
        if st.button("�️ Clear Pre-filled Data"):
            st.session_state.demo_data = {}
            st.rerun()
    
    # Main content area
    if not st.session_state.proposal_generated:
        # Show the form
        project_data = render_project_form()
        
        if project_data:
            # Generate proposal
            with st.spinner("🔄 Generating proposal... This may take a few minutes."):
                try:
                    proposal_result = st.session_state.orchestrator.generate_complete_proposal(project_data)
                    
                    # Store results
                    st.session_state.proposal_data = proposal_result
                    st.session_state.proposal_generated = True
                    
                    # Add to history
                    st.session_state.generation_history.append({
                        "timestamp": datetime.now(),
                        "client_name": project_data.get("client_name"),
                        "project_title": project_data.get("project_title"),
                        "success": proposal_result.get('type') != 'GENERATION_ERROR'
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
    
    else:
        # Show results
        render_proposal_results(st.session_state.proposal_data)
        
        # Option to generate another proposal
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Generate New Proposal", type="primary"):
                st.session_state.proposal_generated = False
                st.session_state.proposal_data = None
                st.session_state.demo_data = {}  # Clear demo data for fresh start
                st.rerun()
        
        with col2:
            if st.button("📈 View Generation History"):
                st.markdown("### 📊 Generation History")
                for entry in reversed(st.session_state.generation_history):
                    status = "✅" if entry['success'] else "❌"
                    st.markdown(f"{status} **{entry['client_name']}** - {entry['project_title']} ({entry['timestamp'].strftime('%Y-%m-%d %H:%M')})")

if __name__ == "__main__":
    main()
