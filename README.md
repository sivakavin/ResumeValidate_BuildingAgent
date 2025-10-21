# Resume Multi-Agent System

An intelligent resume tailoring system that uses LLM agents to analyze job descriptions, improve resumes, and generate professionally formatted documents.

## Features

- 🤖 **Multi-Agent Architecture**
  - JD Analyzer: Extracts key skills, tone, and keywords from job descriptions
  - Resume Builder: Tailors resumes to match job requirements
  - Supervisor: Evaluates and ensures quality of modifications
  - Template Manager: Handles professional document formatting

- 📝 **Resume Templates**
  - Multiple professional templates available
  - Clean, modern layouts with consistent formatting
  - Supports dynamic content injection
  - Easy to add new templates

- 🎯 **Smart Analysis**
  - Identifies key job requirements
  - Suggests targeted improvements
  - Maintains professional tone
  - Multiple refinement iterations if needed

- 🌐 **User-Friendly Interface**
  - Streamlit-based chat interface
  - Upload resume (PDF, DOCX, TXT)
  - Paste job description
  - Download formatted results

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd resume_multiagent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run ui/app.py
```

2. Upload your resume (PDF, DOCX, or TXT format)
3. Paste the job description
4. Click "Analyze and Refine Resume"
5. Review the AI feedback
6. Download your tailored resume in your chosen template

## Project Structure

```
resume_multiagent/
├── agents/
│   ├── jd_analyzer.py      # Analyzes job descriptions
│   ├── resume_builder.py   # Tailors resumes
│   ├── supervisor.py       # Quality control
│   └── template_manager.py # Handles document templates
├── templates/
│   ├── docx/              # DOCX template files
│   ├── json/              # Template metadata
│   ├── assets/            # Images and previews
│   └── index.json         # Template catalog
├── ui/
│   └── app.py            # Streamlit interface
├── graph/
│   └── resume_flow.py    # LangGraph workflow
└── requirements.txt      # Project dependencies
```

## Adding New Templates

1. Create a new DOCX template in `templates/docx/`
2. Add template metadata to `templates/json/[template_name].json`
3. Add template preview to `templates/assets/`
4. Update `templates/index.json` with new template info

Template fields supported:
- name, title, email, phone, linkedin
- summary
- skills (list)
- experience (list of jobs)
- education (list of schools)

## Technology Stack

- **LangChain & Groq**: LLM integration and chat
- **python-docx-template**: Document generation
- **Streamlit**: User interface
- **PyPDF2 & docx2txt**: Document parsing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license]

## Acknowledgments

- Built with Groq LLM
- Powered by LangChain
- UI built with Streamlit