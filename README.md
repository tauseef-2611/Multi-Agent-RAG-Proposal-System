# 🤖 Automated Proposal & Pricing Agent

> **A Multi-Agent RAG System for Intelligent Business Proposal Generation**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Lang## 📊 Data Structure

### Project Input Schema
```python
{
  "client_name": str,
  "project_title": str,
  "project_description": str,
  "project_type": str,
  "industry": str,
  "timeline_months": int,
  "budget_range": str,
  "complexity": str,
  "requirements": List[str],
  "target_technologies": List[str],
  "additional_services": List[str]
}
```

### MCP Message Format
```python
{
  "id": "unique_message_id",
  "timestamp": "2025-08-19T10:30:00Z",
  "sender": "AgentName",
  "receiver": "TargetAgent",
  "msg_type": "ACTION_TYPE",
  "payload": {...}
}
```

## 🔧 Configuration

### Environment Variables
Create `.env` file (optional):
```bash
# Model Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=google/flan-t5-base
MAX_LENGTH=512

# FAISS Configuration  
VECTOR_DIMENSION=384
SIMILARITY_THRESHOLD=0.7

# Application Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### Model Configuration
```python
# GPU/CPU Detection
device = "cuda" if torch.cuda.is_available() else "cpu"

# Model Parameters
max_length = 512
temperature = 0.7
top_p = 0.9
```

## 🧪 Testing

### Run Individual Agent Tests
```bash
# Test pricing agent
python test_pricing_agent.py

# Test writing agent  
python test_writing_agent.py

# Test case study agent
python test_case_study_agent.py

# Test template agent
python test_template_agent.py
```

### Run Orchestrator Test
```bash
# Full workflow test
python debug_orchestrator.py
```

### Validate Installation
```bash
# Check all dependencies
python -c "
import streamlit
import torch
import faiss
import transformers
import sentence_transformers
print('✅ All packages imported successfully')
"
```

## 🎓 Learning Concepts

This project demonstrates key AI/ML concepts commonly asked about in interviews:

### 🔍 **RAG (Retrieval-Augmented Generation)**
- Vector embeddings with Sentence-BERT
- FAISS similarity search
- Document retrieval and ranking
- Context-aware generation

### 🤖 **Multi-Agent Systems**
- Agent communication protocols (MCP)
- Task specialization and coordination
- Parallel processing and orchestration
- Modular architecture design

### 🧠 **Large Language Models**
- FLAN-T5 for text generation
- Prompt engineering techniques
- Model parameter optimization
- GPU/CPU acceleration

### 📊 **Vector Databases**
- FAISS index creation and management
- Cosine similarity calculations
- Approximate nearest neighbor search
- Vector normalization techniques

### 🔧 **Production Considerations**
- Error handling and validation
- Scalability and performance
- Memory management
- Model deployment strategies

## 📁 Project Structure

```
proposal_pricing_agent/
├── 📄 main.py                    # Streamlit application entry point
├── 🎭 orchestrator.py            # Main coordinator for all agents
├── 📋 requirements.txt           # Python dependencies
├── 🤖 agents/                    # Individual agent implementations
│   ├── __init__.py
│   ├── 💰 pricing_agent.py       # Calculates pricing using business rules
│   ├── ✍️  writing_agent.py       # Generates proposal text using LLM
│   ├── 🔍 case_study_agent.py    # Retrieves relevant examples using RAG
│   └── 🎨 template_agent.py      # Creates final PDF from template
├── 📊 data/                      # Configuration and sample data
│   ├── pricing_rules.json        # Business rules for pricing calculation
│   ├── case_studies.json         # Sample case studies for RAG retrieval
│   └── templates/
│       └── proposal_template.html  # HTML template for PDF generation
├── 🛠️  utils/                     # Utility functions
│   ├── __init__.py
│   └── mcp.py                     # Message Communication Protocol
└── 🧪 test_*.py                  # Individual agent test files
```

## 🚀 Getting Started (Detailed)

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-username/proposal_pricing_agent.git
cd proposal_pricing_agent

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
# Test core dependencies
python -c "
import streamlit as st
import torch
import faiss
import transformers
from sentence_transformers import SentenceTransformer
print('✅ All core dependencies working')
"

# Test FAISS specifically
python -c "
import faiss
import numpy as np
d = 64
nb = 100
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
index = faiss.IndexFlatL2(d)
index.add(xb)
print(f'✅ FAISS working: {index.ntotal} vectors indexed')
"
```

### 3. Run Individual Tests
```bash
# Test each agent individually
python test_pricing_agent.py      # Tests pricing calculations
python test_case_study_agent.py   # Tests RAG retrieval
python test_writing_agent.py      # Tests LLM generation
python test_template_agent.py     # Tests HTML/PDF generation

# Test full orchestrator
python debug_orchestrator.py      # Tests complete workflow
```

### 4. Launch Application
```bash
streamlit run main.py
```

Visit `http://localhost:8501` to access the web interface.

## 🎯 Interview Concepts Covered

### **Technical Skills Demonstrated**

1. **Python Ecosystem**:
   - Advanced Python patterns and OOP
   - Virtual environment management
   - Package dependency management

2. **Machine Learning**:
   - Transformer models (FLAN-T5)
   - Embedding generation (Sentence-BERT)
   - Vector similarity search
   - Model optimization and deployment

3. **Data Engineering**:
   - JSON data handling and validation
   - Vector database operations (FAISS)
   - Data pipeline design
   - ETL process implementation

4. **Software Architecture**:
   - Multi-agent system design
   - Message passing protocols
   - Modular component architecture
   - Separation of concerns

5. **Web Development**:
   - Streamlit application development
   - Session state management
   - File upload/download handling
   - User interface design

6. **DevOps & Production**:
   - Git version control
   - Environment configuration
   - Error handling and logging
   - Performance optimization

### **AI/ML Concepts Explained**

1. **RAG Architecture**:
   ```python
   # Query Processing
   query → embedding → similarity_search → document_retrieval → context_injection → generation
   ```

2. **Vector Operations**:
   ```python
   # Cosine Similarity
   similarity = np.dot(query_vec, doc_vec) / (norm(query_vec) * norm(doc_vec))
   
   # FAISS Search
   scores, indices = index.search(query_embedding, k=top_k)
   ```

3. **Agent Communication**:
   ```python
   # MCP Message Flow
   orchestrator → pricing_agent → MCP_message → pricing_result → orchestrator
   ```

## 🤝 Contributing

### Development Workflow
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and test**: `python -m pytest tests/`
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

### Code Style Guidelines
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Add comprehensive docstrings for all classes and methods
- Include unit tests for new functionality
- Maintain backward compatibility when possible

### Adding New Agents
To add a new agent to the system:

1. **Create agent file**: `agents/new_agent.py`
2. **Implement MCP interface**:
   ```python
   def process_request(self, mcp_message: Dict) -> Dict:
       # Agent logic here
       return create_mcp(sender="NewAgent", ...)
   ```
3. **Add to orchestrator**: Import and integrate in `orchestrator.py`
4. **Create tests**: `test_new_agent.py`
5. **Update documentation**: Add agent details to README

## 📞 Support & Resources

- **Documentation**: Comprehensive code comments and this README
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Learning**: Each agent includes educational comments explaining concepts
- **Testing**: Extensive test suite for validation and learning

## 🏆 Project Goals

This project serves multiple purposes:

1. **📚 Educational**: Learn modern AI/ML concepts through hands-on implementation
2. **💼 Professional**: Demonstrate practical software development skills
3. **🔬 Research**: Explore multi-agent architectures and RAG systems
4. **🚀 Production**: Build a scalable, maintainable business application

---

**Built with ❤️ using Python, Streamlit, LangChain, FAISS, and the Transformers ecosystem**

*This project demonstrates the integration of multiple AI/ML technologies to solve real-world business problems while serving as an educational resource for learning modern AI development practices.*ttps://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange.svg)](https://faiss.ai)

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🏗️ Architecture](#️-architecture)
- [🔄 Workflow](#-workflow)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Installation](#️-installation)
- [📖 Usage Guide](#-usage-guide)
- [🤖 Agent Details](#-agent-details)
- [📊 Data Structure](#-data-structure)
- [🔧 Configuration](#-configuration)
- [🧪 Testing](#-testing)
- [🎓 Learning Concepts](#-learning-concepts)
- [🤝 Contributing](#-contributing)

## 🎯 Overview

The **Automated Proposal & Pricing Agent** is a sophisticated multi-agent system that demonstrates key AI/ML concepts through a practical business application. It automatically generates comprehensive business proposals by orchestrating specialized agents that handle different aspects of proposal creation.

### 🌟 Key Features

- **🔍 RAG Implementation**: Retrieval-Augmented Generation for case study matching
- **🤖 Multi-Agent Architecture**: Specialized agents for different proposal components
- **💰 Intelligent Pricing**: Rule-based pricing with complexity calculations
- **📝 Professional Writing**: LLM-powered content generation with quality controls
- **🎨 Template Management**: Dynamic proposal formatting and styling
- **🌐 Web Interface**: Interactive Streamlit application with demo functionality
- **📊 Vector Search**: FAISS-powered similarity search for relevant case studies

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Orchestrator Agent                        │
│            (Coordinates all agents via MCP)                │
└─┬─────────────┬─────────────┬─────────────┬─────────────────┘
  │             │             │             │
┌─▼───────┐ ┌─▼───────┐ ┌─▼───────┐ ┌─▼───────────┐
│ Pricing │ │ Writing │ │  Case   │ │  Template   │
│ Agent   │ │ Agent   │ │ Study   │ │   Agent     │
│         │ │         │ │ Agent   │ │             │
└─┬───────┘ └─┬───────┘ └─┬───────┘ └─┬───────────┘
  │           │           │           │
┌─▼───────┐ ┌─▼───────┐ ┌─▼───────┐ ┌─▼───────────┐
│Pricing  │ │FLAN-T5  │ │ FAISS   │ │   Jinja2    │
│Rules    │ │  LLM    │ │Vector   │ │ Templates   │
│JSON     │ │         │ │Database │ │             │
└─────────┘ └─────────┘ └─────────┘ └─────────────┘
```

## 🔄 Workflow

### 1. **Project Input Phase** 📝
```
User Input → Form Validation → Project Data Structure
```
- Client information and project requirements
- Technology preferences and timeline
- Budget range and complexity assessment

### 2. **Agent Orchestration Phase** 🎭
```
Orchestrator → Parallel Agent Execution → Result Aggregation
```

#### **Pricing Agent** 💰
```python
# Rule-based pricing calculation
base_price = complexity_multiplier × base_rate
total_price = base_price + additional_services + timeline_adjustments
```

#### **Case Study Agent** 🔍
```python
# RAG-powered similarity search
project_embedding = sentence_transformer.encode(project_description)
similar_cases = faiss_index.search(project_embedding, k=3)
```

#### **Writing Agent** ✍️
```python
# LLM-powered content generation
sections = {
    "executive_summary": generate_summary(project_data),
    "project_overview": generate_overview(project_data),
    "methodology": generate_methodology(project_data)
}
```

#### **Template Agent** 🎨
```python
# Dynamic HTML generation
html_content = jinja2_template.render(
    client_data=client_info,
    pricing=pricing_data,
    sections=content_sections,
    case_studies=relevant_cases
)
```

### 3. **Generation Phase** 🏭
```
Combined Data → HTML Template → PDF Generation → Final Proposal
```

## 🚀 Quick Start

### Demo Mode (Fastest Way to Test)

1. **Start the application**:
   ```bash
   streamlit run main.py
   ```

2. **Load demo data**:
   - Click "Load Demo Project" button
   - Review pre-filled form data
   - Click "Generate Proposal"

3. **View results**:
   - Check generated sections and pricing
   - Download PDF proposal

### Custom Project

1. **Fill the form** with your project details
2. **Generate proposal** and review results
3. **Download PDF** for client presentation

## 🛠️ Installation

### Prerequisites

- **Python 3.11+**
- **Git** (for cloning)
- **4GB+ RAM** (for ML models)

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd proposal_pricing_agent
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python -c "import streamlit, torch, faiss; print('✅ All dependencies installed')"
   ```

5. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## 📖 Usage Guide

### Basic Usage

1. **Access the web interface** at `http://localhost:8501`
2. **Fill out the project form**:
   - Client Name and Project Title
   - Project Description and Requirements
   - Technology Stack and Timeline
   - Budget Range and Complexity

3. **Generate the proposal**:
   - Click "Generate Proposal"
   - Wait for agent processing (~30-60 seconds)
   - Review generated content

4. **Download results**:
   - View HTML preview
   - Download PDF proposal
   - Save for client presentation

### Advanced Features

#### **Custom Case Studies**
Add your own case studies to `data/case_studies.json`:
```json
{
  "title": "Custom Project",
  "industry": "Healthcare",
  "project_type": "web_application",
  "description": "Custom project description",
  "technologies": ["React", "Node.js"],
  "outcome": "Successful implementation"
}
```

#### **Pricing Rules Customization**
Modify `data/pricing_rules.json`:
```json
{
  "base_rates": {
    "web_application": 5000,
    "mobile_app": 7000,
    "enterprise_software": 15000
  },
  "complexity_multipliers": {
    "simple": 1.0,
    "medium": 1.5,
    "complex": 2.0
  }
}
```

#### **Template Customization**
Edit templates in `data/templates/`:
- `proposal_template.html` - Main proposal structure
- Customize styling, branding, and layout

## 🤖 Agent Details

### 🏦 **Orchestrator Agent**
**Purpose**: Coordinates all agents and combines results

**Key Methods**:
- `generate_complete_proposal()` - Main orchestration logic
- `validate_mcp_response()` - Message validation
- `combine_agent_results()` - Result aggregation

**MCP Flow**:
```python
project_mcp → pricing_agent → writing_agent → case_study_agent → template_agent → final_result
```

### 💰 **Pricing Agent**
**Purpose**: Calculates project pricing using business rules

**Features**:
- Rule-based pricing calculation
- Complexity assessment
- Timeline adjustments
- Additional services pricing

**Example Output**:
```json
{
  "base_price": 25000,
  "complexity_multiplier": 1.5,
  "timeline_adjustment": 1.2,
  "additional_services": 5000,
  "total_price": 50000
}
```

### ✍️ **Writing Agent**
**Purpose**: Generates proposal content using LLM

**Features**:
- FLAN-T5 model integration
- Professional tone optimization
- Section-specific prompts
- Content quality controls

**Generated Sections**:
- Executive Summary
- Project Overview  
- Methodology
- Technical Approach

### 🔍 **Case Study Agent**
**Purpose**: Retrieves relevant case studies using RAG

**RAG Components**:
- **Embeddings**: Sentence-BERT (384 dimensions)
- **Vector Store**: FAISS with cosine similarity
- **Retrieval**: Top-K similar projects
- **Ranking**: Similarity score filtering

**Process Flow**:
```python
query_text → embedding → vector_search → top_k_results → filtered_cases
```

### 🎨 **Template Agent**
**Purpose**: Generates formatted HTML/PDF proposals

**Features**:
- Jinja2 template engine
- Responsive HTML generation
- PDF conversion with WeasyPrint
- Custom styling and branding

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

## Implementation Notes

All files contain detailed TODO comments and concept explanations to guide implementation. The structure is designed to teach:

- Agent coordination and orchestration
- RAG patterns with real business data
- LLM integration for text generation  
- PDF generation from structured data
- Error handling and validation
- Streamlit UI development

## Dependencies

- Python 3.11.8+ ✅
- Streamlit for UI
- LangChain for LLM orchestration
- FAISS for vector search
- Transformers for local LLM
- WeasyPrint for PDF generation
- Sentence-transformers for embeddings

Start by implementing the MCP protocol in `utils/mcp.py`, then work through each agent one by one!
