# Banking AI Assistant 🏦

A secure, AI-powered banking assistant built with Streamlit and LLM integration. This application provides general banking information, product explanations, and financial education while maintaining strict security standards.

## Features

- Interactive chat interface for banking queries
- Local LLM integration via Ollama
- TF-IDF based vector search for relevant banking information
- Built-in security guardrails for sensitive information
- Conversation history management
- Responsive Streamlit UI

## Prerequisites

- Docker
- Ollama (with llama3.1 model installed)
- Python 3.9+ (if running locally)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-ai-assistant.git
cd banking-ai-assistant
```

2. Build the Docker image:
```bash
docker build -t banking-assistant .
```

3. Run the container:
```bash
docker run -p 8501:8501 banking-assistant
```

4. Access the application at `http://localhost:8501`

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
banking-ai-assistant/
├── app.py                 # Main application file
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Security Features

- No handling of sensitive banking information
- Secure prompt engineering
- Input validation and sanitization
- Forbidden topics filtering
- No account access or transaction capabilities

## Configuration

The application can be configured through environment variables:
- `STREAMLIT_SERVER_PORT`: Port for the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)



## Disclaimer

This is a demonstration project and should not be used for actual banking operations. It is intended for educational purposes only.