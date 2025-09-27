<!-- filepath: /README.md -->
# Chat SQL Assistant

A full-stack application that allows users to interact with databases through natural language queries, similar to ChatGPT but for SQL databases.

## 🚀 Features

- **Natural Language to SQL**: Convert plain English questions into SQL queries
- **Interactive Chat Interface**: ChatGPT-like conversation experience
- **Data Visualization**: Automatic chart generation from query results
- **Real-time Results**: Execute queries and display results instantly
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture
The application is built using the following technologies:

- **Frontend**: Angular +18 with Bootstrap 5 for styling
- **Backend**: Python FastAPI for API handling and dealing with LLMs
- **Database**: PostgreSQL for storing and querying data
- **Natural Language Processing**: Ellbendls/Qwen-3-4b-Text_to_SQL-GGUF | alirezamsh/small100
- **Data Visualization**: Datatables and Chart.js for generating charts

## 📂 Directory Structure
The project is organized into the following directories:

1- Frontend (Angular 19):
src/
├── app/
│   ├── components/
│   │   ├── chat/              # Main chat interface
│   │   ├── data-table/        # Query results display
│   │   └── chart/             # Data visualization
│   ├── services/
│   │   └── chat.service.ts    # API communication
│   ├── models/
│   │   └── chat-message.ts    # TypeScript interfaces
│   └── app.component.ts       # Root component
├── assets/                    # Static files
└── styles.css                # Global styles

2- Backend (Python FastAPI):
app/
├── main.py                    # Entry point
├── api/
│   ├── chat.py                # Chat API endpoints
│   └── utils.py               # Utility functions
├── models/
│   └── chat_message.py        # Pydantic models
└── config.py                  # Configuration settings



