# Human-Assisted Ticket Closer: Customer Support AI Agent

## 📌 Overview
A full-stack, agentic customer support ticket resolution system designed to automate and streamline the customer service pipeline. Built with LangGraph, LlamaIndex, FastAPI, and React, this system classifies incoming tickets, retrieves relevant context (RAG), and drafts intelligent responses. To ensure maximum accuracy and safety, it features a conditional **Human-in-the-Loop** workflow that automatically auto-resolves high-confidence tickets while intelligently escalating ambiguous or low-confidence queries to human supervisors. 

## ✨ Key Features
*   **Agentic Workflow Orchestration:** Uses LangGraph to manage stateful, conditional routing of support tickets between AI nodes and human review.
*   **Conditional Human-in-the-Loop (HITL):** Computes confidence scores for generated responses. High-confidence tickets are auto-executed, while low-confidence tickets are paused for a human agent to approve, edit, or reject via the dashboard.
*   **RAG-Powered Knowledge Base:** Integrates LlamaIndex to query semantic matches from past resolutions and FAQ documents to ground the LLM's draft responses.
*   **"Lifelong Learning" Loop:** Dynamically updates the vector database in real-time. Once a ticket is resolved (either by the AI or a human override), the final resolution is embedded back into the knowledge base to improve future accuracy.
*   **Full-Stack Glassmorphism Dashboard:** A premium, responsive React/Vite frontend serving both a "Customer Portal" for ticket submission and an "Agent Workspace" for real-time ticket monitoring and HITL intervention.

## 🛠️ Tech Stack
*   **AI & Orchestration:** LangGraph, LangChain, LlamaIndex
*   **Backend & API:** Python, FastAPI, Pydantic, Uvicorn
*   **Frontend Library:** React, Vite, TypeScript
*   **Styling:** Modern Vanilla CSS (Dark Mode, Glassmorphism)

## 🧠 System Architecture

1.  **Ingest:** Customer submits a ticket via the React frontend. FastAPI processes the payload and initiates the LangGraph background task.
2.  **Retrieve:** LlamaIndex performs a similarity search against the vector database to find related past tickets and FAQs.
3.  **Draft & Decide (LLM):** The generative model drafts a response and assigns a confidence score.
4.  **Route:**
    *   *Confidence > 80%: -> Auto-Execute*
    *   *Confidence < 80%: -> Human Review (Dashboard)*
5.  **Learn:** The final, executed response is appended back into the LlamaIndex storage, completing the lifelong learning feedback loop.

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js & npm
*   An OpenAI API Key (or equivalent LLM provider)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/human-assisted-ticket-closer.git
   cd human-assisted-ticket-closer
   ```

2. **Backend Setup:**
   ```bash
   # Install Python dependencies
   pip install fastapi uvicorn llama-index langgraph python-dotenv pydantic

   # Set your environment variables
   echo "OPENAI_API_KEY=your_api_key_here" > .env

   # Start the FastAPI server
   python server.py
   ```

3. **Frontend Setup:**
   ```bash
   # Open a new terminal and navigate to the frontend folder
   cd frontend

   # Install Node dependencies
   npm install

   # Start the Vite development server
   npm run dev
   ```

4. **Access the Application:**
   *   **Web App (Customer & Agent Portals):** `http://localhost:5173`
   *   **FastAPI Interactive Docs:** `http://localhost:8000/docs`

## 💡 Use Cases
*   **E-commerce:** Automating routine refund status checks while escalating complex shipping disputes.
*   **SaaS/Tech Support:** Resolving common login/billing issues automatically and forwarding technical bug reports to engineers.
