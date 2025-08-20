# 🤖 Automated Proposal & Pricing Agent

> **A Multi-Agent RAG System for Intelligent Business Proposal Generation**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange.svg)](https://faiss.ai)

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🏗️ Architecture](#️-architecture)
- [ Quick Start](#-quick-start)
- [🛠️ Installation](#️-installation)
- [📖 Usage Guide](#-usage-guide)
- [🤖 Agent Details](#-agent-details)
- [� Project Structure](#-project-structure)

## 🎯 Overview

The **Automated Proposal & Pricing Agent** is a multi-agent system that automatically generates business proposals using RAG (Retrieval-Augmented Generation) and specialized AI agents.

### Key Features

- **Multi-Agent Architecture**: Specialized agents for pricing, writing, case studies, and templates
- **RAG Implementation**: FAISS-powered similarity search for relevant case studies
- **Intelligent Pricing**: Rule-based pricing with complexity calculations
- **Professional Output**: LLM-generated content with PDF export
- **Web Interface**: Interactive Streamlit application

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Orchestrator Agent                        │
└─┬─────────────┬─────────────┬─────────────┬─────────────────┘
  │             │             │             │
┌─▼───────┐ ┌─▼───────┐ ┌─▼───────┐ ┌─▼───────────┐
│ Pricing │ │ Writing │ │  Case   │ │  Template   │
│ Agent   │ │ Agent   │ │ Study   │ │   Agent     │
└─────────┘ └─────────┘ └─────────┘ └─────────────┘
```

**Components:**
- **Orchestrator**: Coordinates all agents and combines results
- **Pricing Agent**: Calculates project costs using business rules
- **Writing Agent**: Generates proposal content using FLAN-T5
- **Case Study Agent**: Retrieves relevant examples using RAG
- **Template Agent**: Creates formatted HTML/PDF output

## � Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/tauseef-2611/Multi-Agent-RAG-Proposal-System.git
cd proposal_pricing_agent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Run Application
```bash
streamlit run main.py
```

### 3. Generate Proposal
- Click "📊 Demo" button for sample data, or
- Fill out the project form manually
- Click "Generate Proposal"
- Download the PDF result

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Git
- 4GB+ RAM

### Setup Steps
1. **Clone repository**: 
   ```bash
   git clone https://github.com/tauseef-2611/Multi-Agent-RAG-Proposal-System.git
   cd proposal_pricing_agent
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run application**:
   ```bash
   streamlit run main.py
   ```

## 📖 Usage Guide

1. **Access the web interface** at `http://localhost:8501`
2. **Fill the project form**:
   - Client information and project details
   - Technology stack and timeline
   - Budget range and complexity level
3. **Generate proposal**: Click "Generate Proposal" and wait ~30-60 seconds
4. **Download results**: View HTML preview and download PDF

### Custom Configuration
- **Case Studies**: Edit `data/case_studies.json` to add your own examples
- **Pricing Rules**: Modify `data/pricing_rules.json` for custom pricing logic
- **Templates**: Update `data/templates/proposal_template.html` for custom styling

## 🤖 Agent Details

### Orchestrator Agent
Coordinates all agents and combines their results using Message Communication Protocol (MCP).

### Pricing Agent
Calculates project costs using configurable business rules and complexity multipliers.

### Writing Agent
Generates professional proposal content using FLAN-T5 language model with optimized prompts.

### Case Study Agent
Retrieves relevant project examples using RAG with FAISS vector similarity search.

### Template Agent
Creates formatted HTML proposals and converts them to PDF using Jinja2 templates.

## 📁 Project Structure

```
proposal_pricing_agent/
├── main.py                    # Streamlit application
├── orchestrator.py            # Main coordinator
├── requirements.txt           # Dependencies
├── agents/                    # Agent implementations
│   ├── pricing_agent.py       # Cost calculation
│   ├── writing_agent.py       # Content generation
│   ├── case_study_agent.py    # RAG retrieval
│   └── template_agent.py      # PDF generation
├── data/                      # Configuration files
│   ├── pricing_rules.json     # Business rules
│   ├── case_studies.json      # Sample cases
│   └── templates/
│       └── proposal_template.html
└── utils/                     # Utility functions
    └── mcp.py                 # Message protocol
```

---

**Built with Python, Streamlit, LangChain, FAISS, and Transformers**
