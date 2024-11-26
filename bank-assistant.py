import streamlit as st
import json
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import requests
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorStore:
    """Vector database using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.documents = [
            # Account Types
            "Checking accounts are transactional accounts used for daily banking needs like paying bills and making purchases",
            "Savings accounts earn interest on deposited money and are best for building emergency funds",
            "Money market accounts typically offer higher interest rates than regular savings accounts with some check-writing privileges",
            "Certificates of deposit (CDs) lock your money for a fixed term in exchange for higher interest rates",
            "Individual Retirement Accounts (IRAs) provide tax advantages for long-term retirement savings",
            
            # Credit Products
            "Credit cards offer revolving credit lines with different rewards programs like cash back or travel points",
            "Secured credit cards require a security deposit and help build credit history",
            "Personal loans provide fixed-amount borrowing with regular monthly payments",
            "Home equity lines of credit (HELOCs) let you borrow against your home's equity",
            "Mortgages are long-term loans used to finance home purchases with various term options",
            
            # Banking Services
            "Online banking provides 24/7 access to accounts through web browsers",
            "Mobile banking apps allow account management and mobile check deposits",
            "Bill pay services automate regular payments to service providers",
            "Direct deposit enables automatic deposit of paychecks into your account",
            "Wire transfers send money electronically between banks domestically or internationally",
            
            # Security Features
            "Two-factor authentication adds an extra layer of security to account access",
            "Fraud monitoring systems detect and alert unusual account activity",
            "Zero liability protection covers unauthorized transactions on credit cards",
            "Secure messaging allows safe communication with bank representatives",
            "Account alerts notify you about balance changes and suspicious activity",
            
            # Additional common banking topics
            "Overdraft protection helps prevent declined transactions when your balance is low",
            "Mobile deposit limits vary based on account type and history",
            "ATM networks provide convenient access to cash worldwide",
            "Digital wallets enable contactless payments using your phone",
            "Auto-pay features help ensure bills are paid on time"
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
    
    def search(self, query: str, k: int = 3) -> List[str]:
        """Search for relevant banking information using TF-IDF similarity"""
        try:
            # Transform query to TF-IDF vector
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarity with all documents
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top k similar documents
            top_k_indices = similarities.argsort()[-k:][::-1]
            
            return [self.documents[i] for i in top_k_indices]
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

class BankingGuardrails:
    """Banking security guardrails"""
    
    FORBIDDEN_TOPICS = [
        "account numbers",
        "social security",
        "password",
        "pin number",
        "mother's maiden name",
        "credit card number",
        "routing number"
    ]
    
    BANKING_CONTEXT = """You are a helpful banking assistant. You can:
    - Explain banking products and services
    - Help with general account questions
    - Provide financial education
    - Assist with transaction explanations
    
    You cannot:
    - Access specific account details
    - Make transactions
    - Change account settings
    - Share sensitive information
    """
    
    @staticmethod
    def check_sensitive_info(text: str) -> bool:
        """Check if text contains sensitive information"""
        return any(topic.lower() in text.lower() for topic in BankingGuardrails.FORBIDDEN_TOPICS)
    
    def create_prompt(self, user_input: str, relevant_docs: List[str]) -> str:
        """Create a safe prompt with context and relevant information"""
        if self.check_sensitive_info(user_input):
            return "I apologize, but I cannot discuss sensitive account information. How else may I help you?"
            
        context = f"""Context: {self.BANKING_CONTEXT}
        
Relevant Information:
{chr(10).join(f'- {doc}' for doc in relevant_docs)}

User Question: {user_input}

Provide a helpful response while maintaining security and privacy standards."""
        return context

class LlamaInterface:
    """Interface with local Llama model through Ollama"""
    
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from Llama model"""
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            return response.json()['response']
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble generating a response at the moment. Please try again."

class ConversationHistory:
    """Conversation history manager"""
    
    def __init__(self):
        self.history: List[Dict] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to history"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

def main():
    st.set_page_config(page_title="Capital One AI Assistant", layout="wide")
    
    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = ConversationHistory()
    if 'llm' not in st.session_state:
        st.session_state.llm = LlamaInterface()
    if 'guardrails' not in st.session_state:
        st.session_state.guardrails = BankingGuardrails()
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStore()
    
    # UI Components
    st.title("🏦 Capital One AI Assistant")
    
    # Sidebar with capabilities
    with st.sidebar:
        st.header("Capabilities")
        st.markdown("""
        - General banking information
        - Product explanations
        - Financial education
        - Transaction support
        """)
        
        st.header("Security Notes")
        st.markdown("""
        - No sensitive information
        - No account access
        - No transactions
        - Educational only
        """)
    
    # Chat interface
    for message in st.session_state.conversation.history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("How can I help you with banking today?")
    
    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.conversation.add_message("user", user_input)
        
        # Generate and show response
        with st.chat_message("assistant"):
            # Get relevant context
            relevant_docs = st.session_state.vector_store.search(user_input)
            
            # Generate response with context
            safe_prompt = st.session_state.guardrails.create_prompt(user_input, relevant_docs)
            response = st.session_state.llm.generate_response(safe_prompt)
            
            st.write(response)
            st.session_state.conversation.add_message("assistant", response)

if __name__ == "__main__":
    main()