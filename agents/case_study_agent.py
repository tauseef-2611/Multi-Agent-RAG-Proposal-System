# agents/case_study_agent.py - Retrieves Relevant Case Studies Using RAG

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, List
from utils.mcp import create_mcp

class CaseStudyAgent:
    """
    Agent responsible for retrieving relevant case studies using RAG approach.
    
    Key concepts to implement:
    1. Loading case studies from JSON
    2. Embedding generation with sentence-transformers
    3. FAISS vector index creation
    4. Similarity search implementation
    5. Relevant case study retrieval
    """
    
    def __init__(self, case_studies_path: str = "data/case_studies.json"):
        """
        Initialize case study agent with RAG components.
        
        TODO: Set up the following:
        1. Load case studies from JSON
        2. Initialize sentence transformer model
        3. Build FAISS index for similarity search
        """
        
        # Load case studies from JSON file
        try:
            with open(case_studies_path, 'r') as f:
                self.case_studies = json.load(f)
            print(f"✅ Loaded {len(self.case_studies)} case studies")
        except FileNotFoundError:
            print(f"❌ Case studies file not found at {case_studies_path}")
            self.case_studies = []
            return
        
        # Initialize sentence transformer model for embeddings
        print("🔄 Loading sentence transformer model...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")
        
        # Build FAISS index for similarity search
        if self.case_studies:
            print("🔄 Building FAISS index...")
            self._build_index()
            print("✅ FAISS index built successfully")
        else:
            self.index = None
    
    def _build_index(self):
        """
        Build FAISS index for case study similarity search.
        
        Key concepts:
        1. Text preprocessing for embeddings
        2. Batch embedding generation
        3. FAISS index creation and population
        4. Vector normalization for cosine similarity
        """
        
        # Create embeddings for each case study
        case_study_texts = []
        for case in self.case_studies:
            # Combine relevant fields for embedding
            text = f"{case['title']} {case['industry']} {case['project_type']} {case['description']}"
            case_study_texts.append(text)
        
        print(f"🔄 Generating embeddings for {len(case_study_texts)} case studies...")
        
        # Generate embeddings using sentence transformer
        embeddings = self.embedding_model.encode(case_study_texts)
        
        # Build FAISS index
        dimension = embeddings.shape[1]  # Embedding dimension (384 for MiniLM)
        self.index = faiss.IndexFlatIP(dimension)  # Inner product similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"✅ FAISS index created: {self.index.ntotal} vectors, {dimension} dimensions")
    
    def retrieve_relevant_cases(self, project_mcp: Dict, k: int = 3) -> Dict:
        """
        Retrieve most relevant case studies for the project.
        
        Key concepts:
        1. Query text construction from project details
        2. Query embedding generation
        3. FAISS similarity search
        4. Result ranking and filtering
        5. Structured response creation
        
        Args:
            project_mcp: MCP message with project details
            k: Number of case studies to retrieve
            
        Returns:
            MCP message with relevant case studies
        """
        
        # Check if index is available
        if self.index is None or len(self.case_studies) == 0:
            print("⚠️ No case studies available for retrieval")
            return create_mcp(
                sender="CaseStudyAgent",
                receiver="Orchestrator",
                msg_type="CASE_STUDIES_RETRIEVED",
                payload={"relevant_cases": []}
            )
        
        # Extract project data from MCP payload
        project_data = project_mcp["payload"]
        
        # Create query text from project details
        query_components = [
            project_data.get("project_type", ""),
            project_data.get("industry", ""),
            project_data.get("description", ""),
            project_data.get("complexity", ""),
            " ".join(project_data.get("additional_services", []))
        ]
        query_text = " ".join(filter(None, query_components))  # Remove empty strings
        
        print(f"🔍 Searching for cases similar to: '{query_text[:100]}...'")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query_text])
        faiss.normalize_L2(query_embedding)
        
        # Search for similar case studies
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Retrieve relevant case studies with similarity scores
        relevant_cases = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid index
                case = self.case_studies[idx].copy()
                case['similarity_score'] = float(scores[0][i])
                relevant_cases.append(case)
        
        print(f"✅ Found {len(relevant_cases)} relevant case studies")
        for i, case in enumerate(relevant_cases):
            print(f"   {i+1}. {case['title']} (similarity: {case['similarity_score']:.3f})")
        
        # Return MCP message with relevant case studies
        return create_mcp(
            sender="CaseStudyAgent",
            receiver="Orchestrator",
            msg_type="CASE_STUDIES_RETRIEVED",
            payload={"relevant_cases": relevant_cases}
        )
