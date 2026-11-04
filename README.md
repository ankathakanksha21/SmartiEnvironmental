# Smarti Environmental CRM

A simple web-based CRM for managing customers, appointments, fitters and maintenance engineers.

## Getting started

You need Python 3.11 or newer and Node.js 22.22 or newer. There is no database to install, because SQLite comes with Python. The app creates its database file, `backend/crm.db`, the first time it starts.

### 1. Start the backend

```bash
cd backend
python -m venv .venv
```

On macOS or Linux, use `python3` if `python` isn't found.

Activate the virtual environment:

| Terminal | Command |
|---|---|
| Windows Command Prompt or PowerShell | `.venv\Scripts\activate` |
| Git Bash | `source .venv/Scripts/activate` |
| macOS or Linux | `source .venv/bin/activate` |

If PowerShell refuses to run the script, use Command Prompt instead.

Install the packages and start the server. Leave this terminal running.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --reload-dir app
```

The server restarts when the code changes. `--reload-dir app` stops it scanning the thousands of files in `.venv`.

The API now runs at http://localhost:8000. You can try every API call from your browser at http://localhost:8000/docs.

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. You should see the Customers page.

If you switch git branches while `npm run dev` is running, stop it and start it again. A branch switch can make Vite restart itself and lose its link to the backend.

### 3. Run the tests

With the virtual environment active, in the `backend` folder:

```bash
pytest
```

### 4. Try the main features

**Customers**
1. Click **Add customer**, then click the button on the form without filling anything in. Each required field shows an error.
2. Fill in the form and save. The customer's page opens.
3. Under **Onboarding status**, choose another status and click **Update status**.
4. Click **Edit details**, change something and save.
5. Click **Customers** in the header. The list shows your customer with its status.

**Staff**
1. Click **Staff**, then **Add staff member**. Add a fitter and a maintenance engineer.
2. Open one, click **Edit details**, untick **Active** and save. Their status changes to Inactive, and they stay in the list.

**Jobs and appointments**

A job is a booked visit, so one record covers both the appointment and the work.

1. Click **Jobs**, then **Book a job**. Click **Book job** without filling anything in to see the errors.
2. Choose a customer and a staff member, pick a date and time in the future, add a description and save. The job's page opens with the status Pending. Inactive staff aren't offered.
3. Try booking the same staff member at the same date and time again. The form refuses it.
4. On the job's page, choose **In Progress** and click **Update status**, then do the same with **Completed**.
5. Click **Jobs**. **Upcoming** shows future jobs that aren't completed, soonest first. **All jobs** shows everything.
6. Open the customer and the staff member. Each page lists their jobs.
