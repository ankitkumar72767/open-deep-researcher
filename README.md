# Open Deep Researcher  
AI-Powered Research Automation System

---

## Project Overview

Open Deep Researcher is an AI-powered research assistant that automates
topic-based and academic paper research using a multi-agent architecture.

---

## What Problem It Solves

- Manual research is time-consuming
- Academic paper summarization requires expertise
- Switching between tools is inefficient

---

## Objective

- Automatically detect user input type (topic or URL)
- Generate structured research reports
- Summarize academic papers efficiently

---

## Software Dependencies

- Python 3.10+
- Streamlit
- OpenAI API
- Tavily Search API

---

## Hardware Requirements

- Minimum 8 GB RAM
- Internet connection
- GPU not required

---

## Architecture

User Interface → Planner Agent → Searcher Agent → Writer Agent → Memory

---

## Workflow

- User enters a topic or paper URL
- Planner agent decides research flow
- Searcher agent gathers information
- Writer agent generates final output
- Results are stored in history

---

## Agent Roles

### Planner Agent
- Defines research structure
- Identifies input type

### Searcher Agent
- Fetches web and academic data

### Writer Agent
- Generates clean and formatted output

---

## Outputs

- Detailed research reports
- Short topic summaries
- Academic paper summaries
- Stored research history

---

## Limitations

- API rate limits may apply
- Output quality depends on source data
- Long documents are summarized at a high level

---

## Future Enhancements

- Multi-chat threads
- DOCX / PDF export
- Dark / Light theme
- Improved citation accuracy

---

## Deployed Link

- https://ankitkumar72767-open-deep-researcher-app-zyg9xh.streamlit.app/

---

## GitHub Repository

- https://github.com/ankitkumar72767/open-deep-researcher
