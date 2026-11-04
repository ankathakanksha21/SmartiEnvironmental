# Smarti Environmental CRM

A simple web-based CRM for managing customers, appointments, fitters and maintenance engineers.

## Getting started

You need Python 3.11 or newer and Node.js 20.19 or newer. There is no database to install, because SQLite comes with Python. The app creates its database file, `backend/crm.db`, the first time it starts.

### 1. Start the backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the packages and start the server. Leave this terminal running.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API now runs at http://localhost:8000. You can try every API call from your browser at http://localhost:8000/docs.

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The page should say "Backend status: ok".

### 3. Run the tests

With the virtual environment active, in the `backend` folder:

```bash
pytest
```
