📘 Open Deep Researcher

AI-Powered Research Automation System

1️⃣ Project Title

Open Deep Researcher – Agentic AI for Automated Research & Paper Summarization

2️⃣ Project Overview (Brief Description)

Open Deep Researcher is an AI-powered research assistant designed to automate academic and topic-based research using a multi-agent architecture.

🔍 Problem Statement

Manual research is time-consuming and unstructured

Summarizing academic papers requires expertise and effort

Switching between topic research and paper summaries is inefficient

🎯 Objective

Automatically understand user intent (topic or URL)

Generate structured research reports or concise paper summaries

Provide a ChatGPT-like research experience with memory support

3️⃣ Software and Hardware Dependencies
🧑‍💻 Software Dependencies

Programming Language: Python 3.10+

Framework: Streamlit

AI / LLM APIs:

OpenAI (GPT models)

Tavily Search API

Libraries & Tools:

openai

streamlit

requests

python-dotenv

json

uuid

💻 Hardware Dependencies

Minimum 8 GB RAM

Internet connection required

GPU not mandatory (optional for heavy workloads)

4️⃣ Architecture Diagram
User Interface (Streamlit)
        |
        v
Planner Agent
        |
        v
Searcher Agent (Web / Paper Search)
        |
        v
Writer Agent (Summarization / Report)
        |
        v
Memory Module (History + Context)

5️⃣ Workflow
Step-by-Step Flow

User enters a topic or academic paper URL

Planner Agent identifies input type

Searcher Agent gathers relevant information

Writer Agent generates:

Detailed research report OR

Concise paper summary

Output is displayed and stored in history

6️⃣ Agent Roles (Brief Explanation)
🧠 Planner Agent

Determines research structure

Identifies whether input is a topic or URL

🔎 Searcher Agent

Fetches academic or web-based information

Uses Tavily / web search APIs

✍️ Writer Agent

Generates clean, structured output

Supports APA / IEEE citation styles

🔗 Agent Pipeline

Planner → Searcher → Writer

Modular and extensible architecture

7️⃣ Sample Working Demo (Optional)
Example Inputs

Natural Language Processing

https://arxiv.org/abs/1810.04805

Example Outputs

Structured literature-style report

Bullet-based academic paper summary

(Screenshots can be added here)

8️⃣ Outputs / Results

The system produces:

📄 Detailed academic research reports

📌 Short topic summaries

📘 Paper-specific summaries (URL-based)

🧠 Stored research history for continuity

9️⃣ Limitations

Depends on external APIs (rate limits apply)

Accuracy depends on source availability

Very long documents may be summarized at a high level

🔮 10️⃣ Future Enhancements

Multi-chat thread support (ChatGPT-style)

DOCX / PDF export

Dark / Light theme toggle

Improved citation validation

Advanced memory-based follow-up queries

🌐 11️⃣ Deployed Project Link

🔗 Live App:
https://ankitkumar72767-open-deep-researcher-app-zyg9xh.streamlit.app/

🔗 GitHub Repository:
https://github.com/ankitkumar72767/open-deep-researcher

📌 Important Notes

README follows mentor-provided structure

Written in simple, academic-friendly language

Fully suitable for final evaluation
