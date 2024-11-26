# AI Banking Assistant

A sophisticated AI-powered banking assistant that leverages Llama 3.1 and vector search to provide accurate, secure banking information and assistance.

## 🌟 Features

### Core Capabilities
- 🤖 AI-powered banking assistance using Llama 2
- 🔍 Semantic search for banking information
- 🛡️ Built-in security guardrails
- 💬 Interactive chat interface
- 🏦 Comprehensive banking knowledge base

### Domain Coverage
- Account Types & Services
- Credit Products
- Digital Banking
- Security Features
- Financial Planning
- Fees & Charges
- Credit Building
- Business Banking
- Insurance Products
- Financial Education

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.9+ required
python --version
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-assistant.git
cd banking-assistant
```

2. Install required packages:
```bash
pip install streamlit sentence-transformers faiss-cpu requests
```

3. Install Ollama and Llama 3.1:
```bash
# Install Ollama from: https://ollama.ai/
ollama pull llama3.1
```

### Running the Application

```bash
streamlit run bank_assistant.py
```

The application will be available at `http://localhost:8501`

## 🏗️ Project Structure

```
banking-assistant/
├── bank_assistant.py    # Main application file
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## 🔧 Components

### VectorStore
- Manages banking knowledge base
- Implements semantic search functionality
- Uses FAISS for efficient similarity search
- Powered by Sentence Transformers

### BankingGuardrails
- Ensures secure and appropriate responses
- Prevents sharing of sensitive information
- Maintains banking compliance
- Implements content filtering

### LlamaInterface
- Handles communication with Llama 2 model
- Manages prompt engineering
- Processes model responses
- Handles error cases

### ConversationHistory
- Maintains chat history
- Manages conversation state
- Handles message formatting

## 🛡️ Security Features

- Sensitive information detection
- Built-in content filtering
- No storage of personal data
- Secure conversation handling

## 💡 Usage Examples

```python
# Initialize the banking assistant
assistant = BankingAssistant()

# Ask about banking products
response = assistant.query("What types of savings accounts are available?")

# Get information about credit cards
response = assistant.query("How do credit card rewards work?")

# Learn about mortgage options
response = assistant.query("What are the different types of mortgages?")
```

## 🚫 Limitations

- Cannot access real account information
- Cannot perform actual transactions
- Limited to educational/informational responses
- Requires local Llama 2 installation

## 🔄 Future Improvements

- [ ] Add multi-language support
- [ ] Implement document upload for analysis
- [ ] Add financial calculators
- [ ] Enhance vector search capabilities
- [ ] Add more banking knowledge
- [ ] Implement A/B testing framework

## 📚 References

- [Llama 3](https://github.com/facebookresearch/llama)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)

## 📧 Contact

Devin Mony Thomas - devin24thomas@gmail.com
Project Link: https://github.com/yourusername/banking-assistant
