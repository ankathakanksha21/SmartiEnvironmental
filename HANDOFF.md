# Handoff

Give a fresh session this file and the code, and it can continue without anything being re-explained. Setup steps live only in [README.md](README.md). "The owner" below means the repo owner, ankathakanksha21.

## 1. Current status

- **Step we're in:** 4 of 7, building. `staff` is the third of four branches.
- **On main:** the design, the running skeleton, and customers with onboarding status.
- **Working branch:** `staff`.
- **Open PR:** [#4](https://github.com/ankathakanksha21/SmartiEnvironmental/pull/4), `staff`, waiting for the owner to merge it.
- **Next:** after that merge, `jobs` starts from an up-to-date main.
- **Deadline:** finish today, 4 November 2026.

### Plan

- [x] 1. Understand the brief and ask the open questions
- [x] 2. Agree this file's outline and make the first commit
- [x] 3. Compare stacks and agree the design
- [ ] 4. Build features, one branch and PR at a time: `project-setup`, `customers`, `staff`, `jobs`
- [ ] 5. Test everything and run the demo, on `demo-and-docs`
- [ ] 6. Finish the README and this file, on the same branch
- [ ] 7. Owner merges the last PR

## 2. Project summary and checklist

A simple web CRM for a business that manages customers, appointments, fitters and maintenance engineers. It is an assessment take-home, and the assessor cares more about the approach, the decisions and how clearly the work is explained than about production readiness. Authentication, hosting, advanced security and complex integrations are out of scope. AI tools are allowed.

| Brief item | State |
|---|---|
| A. Add customers with name, contact details and address | tested |
| A. View a list of customers | tested |
| A. View and edit a customer record | tested |
| B. Assign an onboarding status (New Enquiry, In Progress, Active) | tested |
| B. Update the status as a customer progresses | tested |
| C. Create an appointment for a customer | not started |
| C. Assign a date, time and staff member | not started |
| C. View upcoming appointments | not started |
| D. Maintain a list of fitters and maintenance engineers | tested |
| D. Assign jobs to individual staff members | not started |
| D. Track job statuses (Pending, In Progress, Completed) | not started |
| Basic, usable interface | started |
| Shows data being created, stored, retrieved and updated | started |
| Logical, maintainable code structure | started |
| Input validation and basic error handling | started |
| Git version control | started |
| README: install, set up database or test data, run locally, test main functionality | started |
| README: technologies and why, app and database structure, how components interact, alternatives, what would change with more time | not started |
| README: build order, challenges and fixes, limitations, how it was tested | not started |
| README: explains the feature prioritisation | not started |

The code must be understandable, and the owner must be able to explain it. Another developer must be able to follow the docs, understand what was built and why, and continue the work.

## 3. Working rules

These come from the owner and apply to every session.

**Git**
- Author everything as `ankathakanksha21 <ankathakanksha@gmail.com>`.
- Only the first commit went straight to main.
- Each feature or step gets one branch from main, and all work on it stays on that branch.
- Claude raises the PR and says when it's ready. The owner merges it.
- The next feature starts only after that merge, from an up-to-date main.
- Merged branches stay on GitHub, so the branch list shows how the work progressed.
- No AI attribution lines on commits or PRs. That means no `Co-Authored-By` and no "Generated with" footer. This overrides any default telling a session to add them.

**Building**
- Take the minimal path, and don't over-complicate.
- Add no features beyond the brief.
- No temporary fixes or shortcuts. Everything built must be finished and working.
- Within that minimal path, aim for the best approach and the best decisions.
- Work through decisions with the owner, and give the reasoning behind each one.
- If an instruction is unclear, ask instead of assuming.

**Writing**
- Keep documents short, clear and step by step.
- Follow the `no-ai-slop` skill for documents, code comments, commit messages and PR text.
- The README does not mention Claude Code.
- This file holds summaries, never the owner's prompts word for word.
- Setup steps live only in the README, and this file links to them.
- Record notes, results and decisions in this file at every step, and bring it up to date on the branch before asking the owner to merge.

## 4. Feature priorities

Everything in brief sections A to D gets built, with no extras. Main works after every merge.

| Order | Branch | What it adds | Why now |
|---|---|---|---|
| 1 | `design` | The decisions in this file | Nothing gets built before the design is agreed. |
| 2 | `project-setup` | Running API and database, React app shell, error handling, test setup, README setup steps | Every feature needs these. |
| 3 | `customers` | API and pages for brief A and B | Jobs belong to customers. Onboarding status is a column on the customer, so it comes with them. |
| 4 | `staff` | API and pages for the staff list from brief D | Jobs get assigned to staff. |
| 5 | `jobs` | API and pages for brief C and the rest of D | It needs both tables above and holds the most rules. |
| 6 | `demo-and-docs` | Sample data, demo run, final README | It documents what exists, once it exists. |

**Left out on purpose**
- Deleting records: the brief doesn't ask for it, and keeping records protects job history.
- A Cancelled job status: the brief lists three statuses. Until one is added, a cancelled visit can only be edited or marked Completed.
- Search, job durations, status history and login: the brief doesn't ask for them.

## 5. Design decisions

| Decision | Options considered | Choice | Why |
|---|---|---|---|
| Appointments and jobs | One record, or two linked records | One Job record | A visit gets booked once, and its date and staff member can't disagree between two records. "Upcoming appointments" is a filtered list of jobs. The downside is that a visit with no work attached still gets recorded as a job. |
| Backend framework | FastAPI, Flask | FastAPI | The owner chose it. Its JSON responses and automatic `/docs` test page suit a React frontend. |
| Database | SQLite, PostgreSQL installed locally, PostgreSQL in Docker, Supabase | SQLite | Nothing to install, no account, works offline, and the brief accepts it. PostgreSQL needs an install and a password on every machine. Supabase needs an account, a secret shared outside the repo and internet, and its pricing page says free projects pause after a week of inactivity, so the app could be down during review. Nothing in the brief needs a server database. |
| Data access | Written SQL through `sqlite3`, SQLAlchemy, SQLModel | SQLAlchemy ORM | The owner chose an ORM. Moving to PostgreSQL later is then mostly the connection URL and a driver, while with written SQL it would touch every query, the table definitions, date columns and error handling. Both move paths come from docs and were not run. The cost is more to explain: models, sessions and `select()`. SQLModel was ruled out because its table models stored blank names and bad emails with no error. |
| Code layers | Routes plus service and repository layers, or routes that call the models | Routes call the models directly | Three tables don't need extra layers, and ORM calls are short. |
| Frontend | Jinja2 pages from the server, or React | React with Vite, plain JavaScript, `react-router` for page URLs, one CSS file | The owner chose React. The split also shows clearly how the parts interact. The costs are that every developer needs Node.js, running it takes two terminals, and there's more frontend code. A minimal setup measured 24 npm packages and 62 MB. |
| How the two talk | Allow cross-origin requests (CORS), or a Vite proxy | Vite proxy | Vite's dev server forwards `/api` calls to FastAPI, so the backend needs no CORS setup. |
| Validation | Plain functions, or Pydantic models | Pydantic models with our own messages, plus checks in the route for rules that need the database | FastAPI runs the models before the route. A small handler turns failures into `{field: message}` for the forms. Our own messages replace Pydantic's wording for required text, phone and email. A bad status or a missing field keeps Pydantic's wording, because the forms can't send those. |
| Where allowed statuses are enforced | `schemas.py` only, or a database CHECK constraint as well | `schemas.py` only | The API is the only way in, so a constraint would add another copy of each list. SQLite also can't change a constraint without rebuilding the table, so adding a status would mean deleting `crm.db`. |
| Customer fields | Split or single address, required or optional email | Name, phone and address required, email optional, address in one box | Nothing in the brief needs city or postcode on their own. Staff need a phone number and an address to do a job, but some customers have no email. |
| Date and time | Two columns, or one | One `scheduled_at` DateTime column | One value is simpler to sort and compare. A `datetime-local` input sends one value, Pydantic turns it into a Python datetime, and SQLAlchemy stores it. |
| Job type | A column, or read it from the staff role | No column | The assigned person's role already says fitting or maintenance, and two copies could disagree. |
| Staff who leave | Delete, active flag, no removal | `is_active` flag | They drop off the booking list, and past jobs keep their name. |
| Status changes | Inside the edit form, or their own small form | Their own form on the record's page | It's the most frequent action, and it shouldn't re-run the date rules. |
| Booking rules | None, or basic checks | No booking in the past, and no two open jobs for one staff member at the same date and time | These are the two mistakes a booking form should catch. With no job durations, only exact matches count as a clash. |
| Where this file lives | Committed, or local only | Committed to the repo root | It's backed up, and a fresh session gets it with one clone. It holds no prompts. |
| AI attribution lines | Keep, or remove | Removed | The owner's choice. |
| AI mention in the README | One line, or none | None | The owner's choice. |

## 6. Code guide

This is the full layout. Still to come: the job code, `seed.py`, and the shared jobs table.

```
backend/
  app/
    main.py        creates the app, adds the routes and error handlers
    database.py    database connection and a session for each request
    models.py      the three tables as SQLAlchemy classes
    schemas.py     request and response shapes, validation rules
    seed.py        sample data
    routes/        one file per feature: customers, staff, jobs
  tests/           pytest, one file per feature, plus test_app.py for shared parts
frontend/
  src/
    main.jsx       starts React and defines the page URLs
    api.js         every call to the backend goes through here
    useForm.js     the state every form needs
    constants.js   status and role lists
    style.css
    components/    shared pieces such as form fields and the jobs table
    pages/         one file per page
```

A page calls `api.js`, which calls a FastAPI route. FastAPI validates the request with a schema, the route reads or writes through the models, and the JSON result goes back to the page. If validation fails, the page shows each error next to its field.

**Why this layout**
- `backend/` and `frontend/` are separate programs, each with its own language and tools.
- Each kind of code has one home: tables in `models.py`, input rules in `schemas.py`, URLs in `routes/`, screens in `pages/`.
- Customers, staff and jobs each get one route file and their own pages, so a new feature adds one of each.
- There are no service or repository layers, because three tables don't need them.

**Tables**
- `customers`: id, name, phone, email, address, onboarding_status
- `staff`: id, name, role, phone, is_active
- `jobs`: id, customer_id, staff_id, description, scheduled_at, status

**Backend pieces from `project-setup`**
- `database.py` builds the database path from its own location, opens one session per request, and turns on foreign keys for each connection. With `CRM_ECHO_SQL=1` it prints the SQL. We kept this because the ORM hides the SQL, and the brief asks to show how data is stored.
- `main.py` creates missing tables at startup, so there is no database setup step. It also turns validation failures into `{"errors": {field: message}}`, treats an oversized id as not found, and returns unexpected errors as a JSON message.

**Frontend pieces from `project-setup`**
- `api.js` holds `request()`, which makes every call and turns failures into an `ApiError`, and `useApi()`, which loads data for a page.
- `vite.config.js` forwards `/api` calls to FastAPI on port 8000.

**Customers (brief A and B)**

| API call | What it does |
|---|---|
| `GET /api/customers` | List, in name order |
| `POST /api/customers` | Add |
| `GET /api/customers/{id}` | View one |
| `PUT /api/customers/{id}` | Edit name, phone, email, address |
| `PATCH /api/customers/{id}/status` | Change onboarding status |

- `routes/customers.py` holds these routes, `models.py` holds the `Customer` table, and `schemas.py` holds the rules.
- Validation rules are small functions such as `required` and `valid_phone`. `Annotated` attaches them to a type (`RequiredText`, `Phone`), and each class lists its fields using those types.
- Pages: `CustomerList`, `CustomerDetail`, `CustomerNew`, `CustomerEdit`. The last two share `CustomerForm`, and `useForm` holds its state.
- `StatusForm` and `StatusBadge` are shared, because jobs have a status too.
- Adding a status means editing three places: `schemas.py`, `constants.js`, and `style.css` for its badge colour.
- `useApi` reports `loading` until the answer for the current URL arrives. Pages remove their forms while loading, so a form can't save one record's values over another.

**Staff (the list in brief D)**

| API call | What it does |
|---|---|
| `GET /api/staff` | List, in name order, including inactive staff |
| `POST /api/staff` | Add |
| `GET /api/staff/{id}` | View one |
| `PUT /api/staff/{id}` | Edit name, role, phone, active flag |

- The code follows the same pattern as customers: `routes/staff.py`, `Staff` in `models.py`, `StaffCreate`, `StaffDetails` and `StaffOut` in `schemas.py`.
- Pages: `StaffList`, `StaffDetail`, `StaffNew`, `StaffEdit`. The last two share `StaffForm`.
- There is no delete. Unticking **Active** on the edit form marks someone inactive. Nothing reads the flag yet, and the `jobs` branch uses it to leave them off the booking list.

**One request traced: adding a customer**
1. `CustomerNew.jsx` calls `request('/customers', { method: 'POST', body: values })` when the form is submitted.
2. Vite forwards the call to FastAPI.
3. FastAPI checks the body against `CustomerCreate` in `schemas.py`. If a rule fails, the handler in `main.py` returns `{"errors": {field: message}}` with status 422. `useForm` stores those errors, and `Field` shows each one under its input.
4. If the input is valid, `create_customer` in `routes/customers.py` builds a `Customer` object, then `db.add()` and `db.commit()` make SQLAlchemy run the INSERT.
5. FastAPI turns the object into JSON using `CustomerOut`, and returns it with status 201.
6. `CustomerNew.jsx` uses the returned `id` to open the customer's page, which fetches the record again with `useApi`.

## 7. Challenges

**The design comparison stalled.** The planned comparison had three stages: prototypes, three independent designs, then critics. The prototype step stopped making progress at 17:08, and Claude didn't notice until the owner asked for status at 18:25. The cause is unknown. Claude stopped the run, used the evidence already on disk, and wrote the design directly. The independent designs and critics never ran, so each PR gets a review instead. This cost about 75 minutes.

**The API stopped working in the browser after a branch switch.** Pages said "Something went wrong" and `/api/customers` through Vite returned HTML, although the backend answered correctly on its own. Vite's log showed `git checkout` had rewritten `vite.config.js`, and the automatic restart that followed lost the proxy. Restarting `npm run dev` fixed it, and the README now says so.

**Problems the `staff` review found**
- An API edit that left out `is_active` turned an inactive person active and returned 200. The add form's default also applied to edits. `StaffCreate` now holds the add fields, and `StaffDetails` requires the flag, so that edit now returns 422.
- The first commit message on `staff` says unticking Active takes someone off the booking list. That only becomes true in `jobs`. We left the commit as it is, because rewriting it would need a force-push, and recorded the correct behaviour in section 6 and the PR.

**Problems the `customers` review found**
- Data loss: jumping through browser history between two edit pages left the first customer's values in the form, and saving overwrote the second customer with them. `useApi` now goes back to loading when the URL changes.
- Tests that proved less than they looked. All 36 still passed with the phone character rule deleted, and with the 7 and 15 digit limits changed. We added cases for each one, plus clearing an email.
- A database CHECK constraint gave each status list another copy, and the health route lost its only caller. We removed both.

**Problems the `project-setup` review found**
- The README said Node.js 20.19, but `react-router` needs 22.22 or newer. Fixed.
- `uvicorn --reload` scanned every file in `.venv` and used 63.6% of a CPU core. `--reload-dir app` cut that to 1.2%.
- Some tests passed even with the code they covered removed. The health test, for example, still passed with the database call deleted. We rewrote them to prove what they claim.
- The first version had pieces nothing used yet, such as `useApi`'s reload and some CSS. We removed them, and each comes back with the branch that needs it.

**Problems the prototypes found, and how the design avoids them**
- FastAPI can run a sync route and its database dependency on different threads, and `sqlite3` rejects that by default. Without `check_same_thread=False`, 179 of 300 requests failed with only 2 at a time. SQLAlchemy sets this itself for SQLite files, so we don't have to.
- SQLite ignores foreign keys by default and stored a job for a customer that didn't exist. Run `PRAGMA foreign_keys = ON` on every connection, through a SQLAlchemy connect event.
- SQLAlchemy's default pool keeps the SQLite file open, so pytest couldn't delete its temporary folder on Windows (`NotADirectoryError`). Use `NullPool`, which closes each connection after use.
- Reading a record after its session closed raised `DetachedInstanceError`. Finish reading records inside the request.
- SQLAlchemy's `DateTime` column rejected a date passed as text with a `TypeError`. Pydantic converts it to a Python datetime first.
- A relative database path creates a new empty file in whichever folder the app starts from. Build the path from the project folder.
- An id too large for SQLite raises `OverflowError`, which gives a 500 error. Treat it as not found.
- `TestClient` skips startup unless used in a `with` block, so the tables don't get created.

## 8. Testing and demo

**How to test:** follow [README.md](README.md). Run `pytest` in `backend`, and `npm run lint` and `npm run build` in `frontend`.

**Latest results, on `staff`**
- `pytest`: 57 passed on Python 3.11.
- `npm run lint` is clean, and `npm run build` succeeds.
- The frontend has no automated tests. Its pages get checked in the browser.

**Browser check of the staff pages**, run by calling `click()` from JavaScript on the real page, because the Browser pane was hidden
- A blank form showed errors for name and phone, and a bad phone kept the typed name.
- A valid staff member saved as Active, and the add form has no active checkbox.
- The edit form showed Active ticked. Unticking it and saving changed the status to Inactive.
- The list showed both staff in name order with their status.
- After the review fix, adding someone still saved them as Active, and editing the phone of an inactive person kept them Inactive.

**Browser check of the customer pages**
- Saving a blank form showed an error under each required field.
- A bad phone and email each showed their own error, and the typed values stayed in the form.
- A valid customer saved, and their page opened.
- A status update changed the badge and was still there after a reload.
- An edit changed the name and cleared the email, and the status stayed the same.
- The list showed the customer, and `/customers/999` showed "Customer not found."
- An edit with a blank name showed "Name is required."
- The Browser pane in the Claude desktop app was hidden, so clicks failed for the last steps. Saving the blank-name edit, saving the edit after it, and the history check below ran by calling `click()` and `history.go()` from JavaScript on the real page.
- After the `useApi` fix, a history jump from one customer's edit page to another's showed the right customer's values.

**Earlier, on `project-setup`:** an unknown page URL showed "Page not found", `/docs` listed the API, and with the backend stopped the page showed "Something went wrong. Check the backend is running, then try again."

**Prototype results, not from the final app.** The same small customer feature was built in four stacks, all using Jinja2 pages because React came later. All four passed the same 11 tests on Python 3.11 and 3.12, and all four stored 200 of 200 saves sent 20 at a time, with no errors. The database findings still apply with React.

| Stack | App lines | Installed packages |
|---|---|---|
| FastAPI + `sqlite3` | 107 | 18 |
| FastAPI + SQLAlchemy | 98 | 19 |
| FastAPI + SQLModel | 94 | 20 |
| Flask + `sqlite3` | 86 | 7 |

## 9. Session summaries

### Session 1, 4 November 2026

**Step 1.** The owner shared the brief and asked for a guided, step-by-step build, with the approach and documentation as the priorities. Claude checked the machine and GitHub, found a private, empty repo with admin access, and asked four questions.

**Step 2.** The owner chose one Job record, suggested FastAPI with PostgreSQL or Supabase while staying open to alternatives, set the branch and merge rule, and asked for summaries instead of prompts in this file. Claude proposed ten sections for this file and started comparing stacks with working prototypes in a scratch folder.

**Step 3.** The owner approved the ten sections and asked that current state, results, notes, the current step and the plan be included too. They also set today as the deadline, asked to remove the attribution lines, and asked to keep AI out of the README. They confirmed that each feature starts only after the previous one is merged, and asked for the minimal path with no temporary fixes, the best decisions with reasoning for each, and notes in this file at every step. Claude made the first commit.

The owner then asked whether Claude had missed the rest of that message. Claude had recorded most of it but not acknowledged it in its reply, and this file was missing the rule on notes at every step and the rule on best decisions. Claude added both.

The owner asked how long the project would take and who does what. Claude estimated 2 to 3 hours, later corrected to 3 to 3.5 hours when the comparison ran slowly. On roles: the owner decides, reviews, merges and presents the work, and Claude recommends, codes, tests and documents.

**Step 3, design.** The owner asked for status at 18:25. Claude found the comparison had stalled, stopped it, and wrote the design from the evidence it had collected: FastAPI, SQLite and written SQL.

The owner confirmed FastAPI and SQLite and chose React for the frontend. They asked what "written SQL, not an ORM" means, then whether an ORM removes the PostgreSQL downside. Claude explained both, and said an ORM mostly does remove it. Claude also corrected its earlier answer, which had said the written SQL move only changes placeholders, when it also touches table definitions, date columns and error handling. Claude recommended written SQL because the move isn't part of this project.

The owner chose an ORM and asked how the folders and code were planned. Claude picked SQLAlchemy, dropped the planned `queries/` folder and `schema.sql` because the models now hold the tables, explained the layout (section 6), and raised the `design` PR.

**Step 4, `project-setup`.** The owner merged the `design` PR. Claude deleted the merged `design` branch from GitHub without being asked, told the owner, and restored it. Claude then built the running skeleton: FastAPI, the SQLite connection, error handling, tests, and the React shell. Two independent reviewers checked it, and Claude fixed what they found (section 7). The owner asked what's pending on their side, how testing works, and what `pytest` is, and Claude explained. The owner merged the PR.

**Step 4, `customers`.** Claude built the customer API, validation rules and tests, then the React pages, and checked each flow in the browser. Two independent reviewers found a data-loss bug and some weak tests, and Claude fixed them (section 7). The owner merged the PR.

**Step 4, `staff`.** Claude built the staff API, tests and pages, following the customer pattern, and checked each flow in the browser. Two independent reviewers found that an API edit could reactivate someone by accident, and Claude fixed it. While the review ran, the owner asked for the workflow as a flow chart, and Claude drew three: how a save moves through the app, how office staff use the CRM, and how each feature gets built.

## 10. How to continue

1. Read section 1, then section 3.
2. Check where the repo stands:

   ```bash
   git checkout main
   git pull
   git log --oneline -10
   gh pr list --state all
   ```

3. Follow [README.md](README.md) to set up the app and run the tests.
4. Pick up from "Next" in section 1.

## 11. Notes

- Repo: https://github.com/ankathakanksha21/SmartiEnvironmental (private).
- Machine: Windows 11, with Python 3.11.4 as `python`, Python 3.12.10 through `py`, Node.js 24.20 and npm 11.19.
- Claude has no memory of earlier sessions on this work, so this file is the only record of past decisions.
- `.claude/launch.json` holds Claude's commands for starting the servers. It stays out of git through `.git/info/exclude`.
- When the Browser pane in the Claude desktop app is hidden, screenshots fail but reading page text works.
- The owner has no automated checks on GitHub, so a PR shows no CI results. Tests run locally.
- Known limitation for the final README: name sorting ignores case for English letters only, because SQLite's `lower()` handles ASCII alone. Accented names sort after Z.
