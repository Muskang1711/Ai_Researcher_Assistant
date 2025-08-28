# AI Researcher 🔬🤖

**Generate ready-to-publish research papers in 2-3 minutes using AI Agents and LangGraph**


## 📋 Overview

AI Researcher is an intelligent research paper generation system that leverages LangGraph agents and advanced AI tools to automate the entire research paper creation process. From literature review to final paper generation, this tool streamlines academic research workflow using agentic AI architecture.

## 🎯 Problem Addressed

- **Time-consuming research**: Traditional research paper writing takes weeks or months
- **Literature review complexity**: Finding and synthesizing relevant papers is tedious
- **Manual paper analysis**: Reading and extracting key information from multiple PDFs
- **Writing consistency**: Maintaining academic writing standards throughout the paper

## 💡 Solution

An AI-powered research assistant that:
- Automatically searches and retrieves relevant papers from arXiv
- Scrapes and analyzes PDF content using advanced LLMs
- Generates comprehensive research papers with proper academic structure
- Provides an intuitive web interface for seamless user interaction

## ✨ Key Features

### 🤖 AI Agents & Workflow
- **LangGraph Integration**: Multi-agent system with nodes and edges
- **Agentic Architecture**: Intelligent workflow orchestration
- **Gemini 2.5-Pro LLM**: Powerful language model for content generation

### 🛠️ Advanced Tools
- **arXiv Integration**: Automated literature review and paper retrieval
- **PDF Processing**: Online paper reading and content extraction
- **Document Generation**: Ready-to-publish PDF creation
- **Web Scraping**: Intelligent content gathering

### 🖥️ User Interface
- **Streamlit Frontend**: Clean and intuitive web interface
- **Interactive Q&A**: Natural language query support
- **Real-time Processing**: Live agent response display
- **Downloadable Output**: Instant PDF paper download

## 🏗️ Technical Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   LangGraph     │    │   AI Tools      │
│   Frontend      │◄──►│   Agents        │◄──►│   & Services    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    User Input              Agent Workflow         arXiv, PDF Tools
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Muskang1711/ai-research_assistant.git
cd ai-researcher
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Add your API keys for Gemini and other services
```

4. **Run the application**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
ai-researcher/
│
├── frontend.py                  # Streamlit frontend
├── ai_researcher_langgraph.py
├── tools/
│   ├── __init__.py
│   ├── arxiv_tool.py       # arXiv paper retrieval
│   ├── read_pdf.py       # PDF processing tool
│   └── write_pdf.py     # Research paper generator
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables
```env
GOOGLE_API_KEY=your_gemini_api_key
ARXIV_API_URL=http://export.arxiv.org/api/query
MAX_PAPERS=10
OUTPUT_FORMAT=pdf
```

### Agent Configuration
- **LLM Model**: Gemini 2.5-Pro
- **Max Iterations**: 5
- **Timeout**: 300 seconds
- **Temperature**: 0.7

## 💻 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Enter your research query**
   - Type your research question or topic
   - Specify any particular focus areas

3. **Let AI agents work**
   - Watch real-time agent responses
   - Monitor literature review progress
   - See paper generation status

4. **Download your research paper**
   - Get a ready-to-publish PDF
   - Review and customize as needed

## 📊 Workflow Phases

### Phase 1: Agent & Tools Setup
- Configure arXiv retrieval tool
- Setup PDF reading capabilities
- Initialize paper writing tool
- Create LangGraph agent workflow

### Phase 2: Frontend Development
- Design Streamlit interface
- Implement user query handling
- Display agent responses
- Enable PDF download functionality

### Phase 3: Integration Testing
- End-to-end workflow testing
- Performance optimization
- Error handling implementation

## 🎯 Impact & Benefits

- **⚡ Speed**: Reduce research time from weeks to minutes
- **📚 Comprehensiveness**: Access vast arXiv database automatically
- **🎯 Accuracy**: AI-powered content analysis and synthesis
- **📝 Quality**: Maintain academic writing standards
- **🔄 Reproducibility**: Consistent research methodology
- **💰 Cost-effective**: 100% free and open-source

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LangChain team for LangGraph framework
- Google for Gemini API
- arXiv for providing open access to research papers
- Streamlit for the amazing web framework

⭐ **Star this repository if you find it helpful!** ⭐