# 🧠 Open Deep Researcher  
**AI-Powered Research Automation Agent**

Open Deep Researcher is an **agentic AI research assistant** that can understand **any research topic or academic paper URL** and generate either a **detailed research report** or a **concise paper summary** automatically.

This project was built as part of the **Infosys Springboard Virtual Internship (Artificial Intelligence)** and focuses on applying real-world **AI, LLMs, and multi-agent workflows**.

---

## 🚀 Features

- 🔍 Accepts **any research topic** or **academic paper URL**
- 🧠 Automatically detects input type (topic vs. paper)
- 📄 Generates:
  - Detailed research reports  
  - Concise academic paper summaries
- 🤖 **Multi-Agent AI Architecture**
  - **Planner Agent** – designs research structure
  - **Searcher Agent** – gathers relevant information
  - **Writer Agent** – produces clean, formatted output
- 🕘 Research history stored for continuity
- 🎨 Clean, modern **Streamlit UI**
- ⚡ Modular, scalable project structure

---

## 🧠 Agent Workflow

User Input
↓
Planner Agent → Research plan & structure
↓
Searcher Agent → Relevant data & context
↓
Writer Agent → Final research report / summary

yaml
Copy code

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **LLM / Agentic AI**
- **JSON-based memory handling**
- **Modular architecture**
  - Agents
  - State management
  - Memory handling

---

## 📂 Project Structure

<img width="448" height="361" alt="image" src="https://github.com/user-attachments/assets/2b6c1435-e5d7-42e0-876a-8d7a77dffa8f" />

## ⚙️ Setup & Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ankitkumar72767/open-deep-researcher.git
cd open-deep-researcher
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure API Keys
Create config.py and add:

python
Copy code
OPENROUTER_API_KEY = "your_openrouter_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
5️⃣ Run the App
bash
Copy code
streamlit run app.py
🌐 Live Demo
🔗 Streamlit App:
https://ankitkumar72767-open-deep-researcher-app-zyg9xh.streamlit.app/

🎯 Skills Demonstrated
Agentic AI system design

Prompt engineering

Research automation

Python application development

Modular & scalable architecture

State and memory management

📌 Internship Context
This project was developed during the Infosys Springboard Virtual Internship (AI), focusing on practical implementation of Artificial Intelligence and Machine Learning concepts through hands-on projects.

📬 Contact
Ankit Kumar
AI & ML Developer
🔗 GitHub: https://github.com/ankitkumar72767
🔗 LinkedIn: https://www.linkedin.com/in/ankit-kumar-/

