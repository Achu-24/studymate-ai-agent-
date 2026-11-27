# 📚 StudyMate AI – Personal Study Planning Agent

## Overview
StudyMate AI is an AI-powered study planning assistant built using Streamlit, LangGraph, and Google Gemini. It helps students explore study topics, calculate preparation time, and create personalized study schedules.

## Features
- **Find Topics:** Retrieve available topics for a selected subject.
- **Calculate Study Time:** Calculate total study hours and estimated completion days.
- **Draft Study Plan:** Generate a study schedule based on available days and daily study hours.
- **Conversational AI:** Ask study-related questions through an interactive chat interface.
- **Agent Execution Trace:** View tool calls and their results.
- **Session-based Chat:** Chat history is maintained during the current session.

## Tech Stack
- Python
- Streamlit
- LangGraph
- LangChain
- Google Gemini API
- Pandas
- CSV Dataset

## Project Structure

```text
studymate-ai-agent/
│
├── app.py
├── agent_core.py
├── tools.py
├── requirements.txt
├── README.md
│
└── data/
    └── study_topics.csv
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd studymate-ai-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Enter your Gemini API key

Enter your Google Gemini API key in the sidebar to start chatting with StudyMate AI.

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Example Questions

- Show me all the DAA topics available in the study database.
- How many days will I need to complete DAA if I study 2 hours daily?
- Create a 10-day study plan for COA.
- Help me plan my preparation with 3 hours of study every day.

## Privacy
- The Gemini API key is entered by the user.
- Chat history is maintained in the current Streamlit session.
- API keys and conversations should not be committed to the repository.

