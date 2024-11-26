import streamlit as st
import json
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import requests
from sentence_transformers import SentenceTransformer
import faiss
import logging

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorStore:
    """Vector database for semantic search of banking information"""
    
    def __init__(self):
        try:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            self.dimension = 384
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []
            
            self._load_banking_knowledge()
        except Exception as e:
            logger.error(f"Error initializing VectorStore: {str(e)}")
            st.error("Error initializing search functionality. Some features may be limited.")
    
    def _load_banking_knowledge(self):
        """Load comprehensive banking documentation"""
        banking_docs = [
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
            "Auto loans help finance vehicle purchases with the car serving as collateral",
            "Student loans help finance education expenses with federal and private options available",
            
            # Banking Services
            "Online banking provides 24/7 access to accounts through web browsers",
            "Mobile banking apps allow account management and mobile check deposits",
            "Bill pay services automate regular payments to service providers",
            "Direct deposit enables automatic deposit of paychecks into your account",
            "Wire transfers send money electronically between banks domestically or internationally",
            "ATM services provide cash withdrawals, deposits, and account information access",
            
            # Security Features
            "Two-factor authentication adds an extra layer of security to account access",
            "Fraud monitoring systems detect and alert unusual account activity",
            "Zero liability protection covers unauthorized transactions on credit cards",
            "Secure messaging allows safe communication with bank representatives",
            "Account alerts notify you about balance changes and suspicious activity",
            
            # Financial Planning
            "Budgeting tools help track income and expenses for better financial management",
            "Goal-based savings accounts help you save for specific purposes",
            "Investment accounts allow you to invest in stocks, bonds, and mutual funds",
            "Retirement planning services help prepare for long-term financial security",
            "Financial advisors provide personalized guidance on money management",
            
            # Fees and Charges
            "Monthly maintenance fees may apply to certain checking accounts",
            "Overdraft fees are charged when accounts are overdrawn",
            "ATM fees may apply when using out-of-network machines",
            "Wire transfer fees vary for domestic and international transfers",
            "Late payment fees apply to missed credit card or loan payments",
            
            # Digital Features
            "Mobile check deposit allows depositing checks through smartphone cameras",
            "Peer-to-peer payments enable sending money to friends and family",
            "Digital wallets support contactless payments using smartphones",
            "Online bill negotiation services help reduce monthly bills",
            "Automated savings tools round up purchases to save spare change",
            
            # Credit Building
            "Credit monitoring services track your credit score and report changes",
            "Secured credit products help establish credit history",
            "Credit building loans help improve credit scores over time",
            "Payment history reporting helps build positive credit records",
            "Credit limit increases are available with good payment history",
            
            # Business Banking
            "Business checking accounts support company transactions and payments",
            "Merchant services enable businesses to accept card payments",
            "Business loans provide capital for company growth and expenses",
            "Payroll services help manage employee compensation",
            "Business credit cards separate personal and company expenses",
            
            # Insurance Products
            "Life insurance policies protect family financial security",
            "Property insurance covers damage to homes and belongings",
            "Auto insurance provides vehicle accident coverage",
            "Identity theft insurance protects against fraud losses",
            "Travel insurance covers trip cancellations and emergencies",
            
            # Additional Services
            "Notary services authenticate important documents",
            "Safe deposit boxes store valuable items securely",
            "Foreign currency exchange for international travel",
            "Cashier's checks provide guaranteed payment for large transactions",
            "Money orders offer secure payment alternatives to cash",
            
            # Financial Education
            "Financial literacy resources teach money management basics",
            "Investment education explains market and portfolio concepts",
            "Credit score education helps understand credit reporting",
            "Debt management guidance helps reduce and eliminate debt",
            "Retirement planning workshops prepare for future needs",
            
            # Digital Security
            "Encryption protects online and mobile banking data",
            "Biometric authentication uses fingerprints or face recognition",
            "Regular security updates protect against new threats",
            "Secure password requirements protect account access",
            "Multi-device authentication verifies login attempts"
        ]
        
        # Encode and index documents
        embeddings = self.encoder.encode(banking_docs)
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(banking_docs)

        
        # Encode and index documents
        embeddings = self.encoder.encode(banking_docs)
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(banking_docs)
    
    def search(self, query: str, k: int = 3) -> List[str]:
        """Search for relevant banking information"""
        try:
            query_vector = self.encoder.encode([query])
            scores, indices = self.index.search(query_vector.astype('float32'), k)
            return [self.documents[i] for i in indices[0]]
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

class BankingGuardrails:
    """Enhanced guardrails with banking-specific rules"""
    
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
    """Simple conversation history"""
    
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
            # Get relevant context from vector store
            relevant_docs = st.session_state.vector_store.search(user_input)
            
            # Generate response with context
            safe_prompt = st.session_state.guardrails.create_prompt(user_input, relevant_docs)
            response = st.session_state.llm.generate_response(safe_prompt)
            
            st.write(response)
            st.session_state.conversation.add_message("assistant", response)

if __name__ == "__main__":
    main()