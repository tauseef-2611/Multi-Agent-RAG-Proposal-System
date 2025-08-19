# agents/writing_agent.py - Generates Proposal Text Using LLM

from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from utils.mcp import create_mcp
from typing import Dict

class WritingAgent:
    """
    Agent responsible for generating proposal text sections using LLM.
    
    Key concepts to implement:
    1. Local LLM integration (FLAN-T5)
    2. LangChain pipeline setup
    3. Prompt template design
    4. Multi-section text generation
    5. Structured output creation
    """
    
    def __init__(self):
        """
        Initialize writing agent with LLM and prompt templates.
        
        TODO: Set up the following:
        1. Transformers pipeline with FLAN-T5
        2. LangChain HuggingFacePipeline wrapper
        3. PromptTemplate objects for different sections
        """
        
        # Detect available device (GPU or CPU)
        import torch
        if torch.cuda.is_available():
            device = 0  # Use GPU
            device_name = f"GPU ({torch.cuda.get_device_name(0)})"
        else:
            device = -1  # Use CPU
            device_name = "CPU"
        
        print(f"🔧 Initializing Writing Agent on {device_name}")
        
        # Initialize LLM components with automatic device detection
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=300,  # Reduced to prevent repetition
            min_length=50,   # Ensure minimum content
            do_sample=True,  # Enable sampling for diversity
            temperature=0.7, # Add some creativity
            top_p=0.9,       # Nucleus sampling
            repetition_penalty=1.2,  # Penalize repetition
            device=device
        )
        
        print(f"✅ Model loaded on {device_name}")
        
        self.llm = HuggingFacePipeline(
            pipeline=self.generator,
            model_kwargs={
                "max_length": 300,
                "min_length": 50,
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.2,
                "pad_token_id": self.generator.tokenizer.eos_token_id
            }
        )
        
        self.section_prompts = {
            "executive_summary": PromptTemplate(
                input_variables=["client_name", "project_title", "project_description", "timeline_months", "key_benefits"],
                template="""Write an executive summary for {client_name}'s {project_title}.

Project: {project_description}
Timeline: {timeline_months} months
Benefits: {key_benefits}

Create a professional summary that highlights the project value, scope, and our expertise. Focus on business benefits and outcomes.

Executive Summary:"""
            ),
            "project_overview": PromptTemplate(
                input_variables=["client_name", "project_title", "project_description", "requirements", "timeline_months", "technologies"],
                template="""Write a project overview for {project_title}.

Description: {project_description}
Requirements: {requirements}
Technologies: {technologies}
Timeline: {timeline_months} months

Explain the project goals, technical approach, key features, and expected deliverables. Be specific and professional.

Project Overview:"""
            ),
            "methodology": PromptTemplate(
                input_variables=["project_title", "project_description", "technologies", "client_type"],
                template="""Write a methodology section for {project_title}.

Project: {project_description}
Technologies: {technologies}
Client: {client_type}

Describe our development process, project phases, quality assurance, and collaboration approach. Emphasize expertise and proven methods.

Methodology:"""
            )
        }
    
    def generate_proposal_sections(self, project_mcp: Dict) -> Dict:
        """
        Generate all proposal text sections.
        
        Key concepts:
        1. Extract project details from MCP
        2. Use prompt templates to format inputs
        3. Call LLM for each section (executive_summary, project_overview, methodology)
        4. Collect all generated sections
        5. Return structured MCP response
        
        Args:
            project_mcp: MCP message with project details
            
        Returns:
            MCP message with generated text sections
        """
        
        # Extract project data from MCP payload
        project_data = project_mcp["payload"]
        
        # Prepare enhanced variables for better content generation
        client_name = project_data.get("client_name", "Our Valued Client")
        project_title = project_data.get("project_title", "Digital Transformation Project")
        project_description = project_data.get("project_description", "A comprehensive digital solution")
        timeline_months = project_data.get("timeline_months", 6)
        requirements = ", ".join(project_data.get("requirements", ["Modern design", "User-friendly interface", "Scalable architecture"]))
        technologies = ", ".join(project_data.get("target_technologies", ["React", "Node.js", "MongoDB"]))
        client_type = project_data.get("client_type", "business")
        
        # Generate key benefits based on project type and description
        key_benefits = f"enhanced digital presence, improved user experience, scalable technology solutions, competitive advantage"
        
        # Initialize sections dictionary
        sections = {}
        
        try:
            # Generate executive summary
            print("🔤 Generating executive summary...")
            exec_prompt = self.section_prompts["executive_summary"].format(
                client_name=client_name,
                project_title=project_title,
                project_description=project_description,
                timeline_months=timeline_months,
                key_benefits=key_benefits
            )
            exec_result = self.llm(exec_prompt).strip()
            sections["executive_summary"] = self._clean_generated_text(exec_result)
            
            # Generate project overview
            print("🔤 Generating project overview...")
            overview_prompt = self.section_prompts["project_overview"].format(
                client_name=client_name,
                project_title=project_title,
                project_description=project_description,
                requirements=requirements,
                timeline_months=timeline_months,
                technologies=technologies
            )
            overview_result = self.llm(overview_prompt).strip()
            sections["project_overview"] = self._clean_generated_text(overview_result)
            
            # Generate methodology
            print("🔤 Generating methodology...")
            methodology_prompt = self.section_prompts["methodology"].format(
                project_title=project_title,
                project_description=project_description,
                technologies=technologies,
                client_type=client_type.replace("_", " ").title()
            )
            methodology_result = self.llm(methodology_prompt).strip()
            sections["methodology"] = self._clean_generated_text(methodology_result)
            
            print(f"✅ Generated {len(sections)} sections successfully")
            
        except Exception as e:
            print(f"❌ Error generating sections: {e}")
            # Provide fallback content
            sections = {
                "executive_summary": f"This proposal outlines a comprehensive {project_title} for {client_name}, designed to deliver significant business value through modern technology solutions and proven methodologies over a {timeline_months}-month timeline.",
                "project_overview": f"The {project_title} represents a strategic initiative to enhance {client_name}'s digital capabilities. This project encompasses {requirements} and will be implemented using cutting-edge technologies including {technologies}.",
                "methodology": f"Our proven methodology for {project_title} combines agile development practices with continuous client collaboration, ensuring high-quality deliverables and successful project outcomes."
            }
        
        # Return MCP message with generated sections
        return create_mcp(
            sender="WritingAgent",
            receiver="Orchestrator",
            msg_type="PROPOSAL_SECTIONS_GENERATED",
            payload={"sections": sections}
        )
    
    def _clean_generated_text(self, text: str) -> str:
        """
        Clean and improve generated text by removing repetition and improving formatting.
        
        Args:
            text: Raw generated text
            
        Returns:
            Cleaned and formatted text
        """
        # Remove excessive repetition
        sentences = text.split('. ')
        unique_sentences = []
        seen_sentences = set()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence.lower() not in seen_sentences:
                unique_sentences.append(sentence)
                seen_sentences.add(sentence.lower())
        
        # Rejoin sentences
        cleaned_text = '. '.join(unique_sentences)
        
        # Ensure proper ending
        if cleaned_text and not cleaned_text.endswith('.'):
            cleaned_text += '.'
        
        # Limit length if too long
        if len(cleaned_text) > 800:
            # Find a good breaking point
            words = cleaned_text.split()
            if len(words) > 120:
                cleaned_text = ' '.join(words[:120]) + '.'
        
        return cleaned_text
