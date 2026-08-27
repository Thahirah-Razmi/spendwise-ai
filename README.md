# SpendWise AI 💰

SpendWise AI is a simple AI-powered expense management SaaS application built around an open-source language model.

The application allows users to manage expenses using natural language. Instead of manually selecting operations, users can simply ask questions such as:

> "Add 20 dollars for lunch"

The local AI model interprets the request and generates a structured JSON tool call. The backend then validates the request, executes the appropriate tool, and stores or retrieves data from an SQLite database.

---

## ✨ Features

* 🤖 Local AI inference using **Qwen3-0.6B**
* 🔓 Open model from **Hugging Face**
* 🚫 No AI API key required
* 🧠 Natural-language expense management
* 🛠️ JSON-based tool calling
* ⚡ FastAPI REST API
* 🗄️ SQLite database
* 💵 Add expenses
* 📋 List expenses
* 📊 Calculate total spending
* 🏷️ Calculate spending by category
* 🔐 Backend-controlled tool execution

---

## 🏗️ Architecture

```text
                    User
                      │
                      ▼
              ┌───────────────┐
              │    FastAPI    │
              │   REST API    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   AI Wrapper  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Qwen3-0.6B   │
              │ Local Model   │
              └───────┬───────┘
                      │
                      ▼
                JSON Tool Call
                      │
                      ▼
              ┌───────────────┐
              │  Tool Router  │
              └───────┬───────┘
                      │
          ┌───────────┼────────────┐
          │           │            │
          ▼           ▼            ▼
    add_expense  list_expenses  get_total
          │           │            │
          └───────────┼────────────┘
                      │
                      ▼
                ┌───────────┐
                │  SQLite   │
                │ Database  │
                └───────────┘
```

---

## 🧠 How It Works

A user sends a natural-language request to the FastAPI API.

For example:

```text
Add 20 dollars for lunch
```

The request is passed to the local **Qwen3-0.6B** model.

The model produces a structured JSON tool call:

```json
{
  "tool": "add_expense",
  "arguments": {
    "amount": 20,
    "category": "lunch",
    "description": "Lunch purchase"
  }
}
```

The application then:

1. Parses the JSON output.
2. Identifies the requested tool.
3. Validates the tool.
4. Extracts the arguments.
5. Executes the corresponding Python function.
6. Stores the expense in SQLite.
7. Returns the result to the client.

The model is responsible for **understanding intent and selecting a tool**, while the backend is responsible for **executing the operation**.

---

## 🛠️ Available Tools

### `add_expense`

Adds a new expense.

**Example:**

```text
Add 50 dollars for groceries
```

**Tool call:**

```json
{
  "tool": "add_expense",
  "arguments": {
    "amount": 50,
    "category": "groceries",
    "description": "Grocery purchase"
  }
}
```

---

### `list_expenses`

Returns the user's recorded expenses.

**Example:**

```text
Show my expenses
```

---

### `get_total_expenses`

Calculates total spending.

**Example:**

```text
How much have I spent?
```

**Example response:**

```text
Total expenses: 95.00
```

---

### `get_expenses_by_category`

Calculates spending for a particular category.

**Example:**

```text
How much did I spend on lunch?
```

**Example response:**

```text
Total spent on lunch: 45.00
```

The application also supports broader categories such as:

```text
food
```

which can include categories such as:

* groceries
* lunch
* dinner
* breakfast
* snacks
* restaurant
* takeaway
* coffee

---

## 🔑 No API Key Required

This project does **not** use OpenAI, Anthropic, Gemini, or another hosted AI API.

The model is downloaded from Hugging Face and executed locally using:

* Hugging Face Transformers
* PyTorch

A Hugging Face API token is therefore **not required for normal local inference**.

Hugging Face is used as the **model repository**, not as a hosted inference API.

---

## 💻 Technology Stack

| Technology                | Purpose                     |
| ------------------------- | --------------------------- |
| Python                    | Application language        |
| Qwen3-0.6B                | Local language model        |
| Hugging Face Transformers | Model loading and inference |
| PyTorch                   | Model execution             |
| FastAPI                   | REST API                    |
| SQLite                    | Persistent storage          |
| Pydantic                  | Request validation          |
| Uvicorn                   | ASGI server                 |

---

## 📁 Project Structure

```text
spendwise-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── ai.py            # Local AI model wrapper
│   ├── tools.py         # Expense tools
│   └── database.py      # SQLite database operations
│
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/spendwise-ai.git
cd spendwise-ai
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --port 8080
```

The API will be available at:

```text
http://127.0.0.1:8080
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8080/docs
```

---

## 🧪 Testing the API

You can test the API using PowerShell, `curl`, Postman, or another HTTP client.

### Add an Expense

**PowerShell:**

```powershell
$body = @{ message = "Add 20 dollars for lunch" } | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

**Expected result:**

```text
Expense added successfully: 20.00 for lunch
```

---

### List Expenses

```powershell
$body = @{ message = "Show my expenses" } | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

---

### Calculate Total Spending

```powershell
$body = @{ message = "How much have I spent?" } | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8080/api/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

---

## 🔄 Example Request Flow

### User

```text
Add 20 dollars for lunch
```

### AI

```json
{
  "tool": "add_expense",
  "arguments": {
    "amount": 20,
    "category": "lunch",
    "description": "Lunch purchase"
  }
}
```

### Backend

```text
JSON parsing
      ↓
Tool validation
      ↓
add_expense()
      ↓
SQLite
```

### Response

```text
Expense #3 added successfully: 20.00 for lunch
```

---

## 🔐 Tool Execution and Security

The model does **not** have direct access to the database.

Instead, the backend maintains a controlled set of available tools.

Conceptually:

```python
TOOLS = {
    "add_expense": add_expense,
    "list_expenses": list_expenses,
    "get_total_expenses": get_total_expenses,
    "get_expenses_by_category": get_expenses_by_category
}
```

Only registered tools can be executed.

This creates a separation between:

```text
AI reasoning
     │
     ▼
Structured tool request
     │
     ▼
Backend validation
     │
     ▼
Tool execution
```

This is safer than allowing the language model to directly execute arbitrary database queries or code.

---

## ⚠️ Current Limitations

This project is a **proof-of-concept SaaS application**.

Current limitations include:

* Single local SQLite database
* No user authentication
* No multi-user account isolation
* Local model inference can be slower on CPU
* Small language model may occasionally produce incorrect tool calls
* No production deployment configuration
* No frontend dashboard yet

---

## 🔮 Future Improvements

Potential future improvements include:

* User authentication and authorization
* Per-user expense databases
* PostgreSQL for production storage
* Web-based dashboard
* Expense charts and analytics
* Budget tracking
* Monthly spending reports
* Better tool-call schema validation
* Retry handling for invalid model output
* Larger tool-capable open models
* Docker deployment
* Cloud deployment
* Automated tests
* Rate limiting and monitoring

---

## 🎯 Project Objective

The main objective of this project is to demonstrate how an **open language model can be wrapped into a practical application without relying on a proprietary AI API**.

The project demonstrates:

```text
Open Model
    +
Local Inference
    +
AI Wrapper
    +
Structured JSON Tool Calling
    +
FastAPI
    +
Business Logic
    +
Database
    =
AI-Powered SaaS Application
```

---

## 📜 License

This project is intended for **educational and demonstration purposes**.

The Qwen model is subject to its own model license and terms. Users should review the applicable model license before redistributing or deploying the model commercially.
