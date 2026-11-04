# Handoff

Give a fresh session this file and the code, and it can continue without anything being re-explained. Setup steps, the code layout and the database diagram live only in [README.md](README.md). "The owner" below means the repo owner, ankathakanksha21.

## 1. Current status

- **Step we're in:** 7 of 7. All the work is done, and the last PR is waiting for the owner to merge it.
- **On main:** all of brief sections A to D.
- **Open PR:** [#6](https://github.com/ankathakanksha21/SmartiEnvironmental/pull/6), `demo-and-docs`, with the sample data and final README.
- **Next:** the owner merges the PR, tries the app and presents it. New work starts only if the owner asks.

### Plan

- [x] 1. Understand the brief and ask the open questions
- [x] 2. Agree this file's outline and make the first commit
- [x] 3. Compare stacks and agree the design
- [x] 4. Build features, one branch and PR at a time: `project-setup`, `customers`, `staff`, `jobs`
- [x] 5. Test everything and run the demo, on `demo-and-docs`
- [x] 6. Finish the README and this file, on the same branch
- [ ] 7. Owner merges the last PR

## 2. Project summary and checklist

A simple web CRM for a business that manages customers, appointments, fitters and maintenance engineers. It is an assessment take-home, and the assessor cares more about the approach, the decisions and how clearly the work is explained than about production readiness. Authentication, hosting, advanced security and complex integrations are not required. AI tools are allowed.

Office staff are the end users. The brief doesn't name them, so this is Claude's reading, which the owner asked about and didn't object to. Fitters and engineers are records that jobs get assigned to, and customers don't use the app.

This table is the brief, with the state of each item.

| Brief item | State |
|---|---|
| A. Add customers with name, contact details and address | tested |
| A. View a list of customers | tested |
| A. View and edit a customer record | tested |
| B. Assign an onboarding status (New Enquiry, In Progress, Active) | tested |
| B. Update the status as a customer progresses | tested |
| C. Create an appointment for a customer | tested |
| C. Assign a date, time and staff member | tested |
| C. View upcoming appointments | tested |
| D. Maintain a list of fitters and maintenance engineers | tested |
| D. Assign jobs to individual staff members | tested |
| D. Track job statuses (Pending, In Progress, Completed) | tested |
| C and D may share one workflow, if that is the better design | done, one Job record |
| Basic, usable interface | tested |
| Shows data being created, stored, retrieved and updated | tested |
| Logical, maintainable code structure | reviewed |
| Input validation and basic error handling | tested |
| Git version control | done |
| README: install, set up database or test data, run locally, test main functionality | tested |
| README: technologies and why, app and database structure, how components interact, alternatives, what would change with more time | reviewed |
| README: build order, challenges and fixes, limitations, how it was tested | reviewed |
| README: explains the feature prioritisation | reviewed |

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
- Work through new decisions with the owner, and give the reasoning behind each one. The decisions in section 5 are settled.
- If an instruction is unclear, ask instead of assuming.

**Writing**
- Keep documents short, clear and step by step.
- Follow the `no-ai-slop` skill for documents, code comments, commit messages and PR text.
- The README does not mention Claude or AI.
- This file holds summaries, never the owner's prompts word for word.
- Use they/them for people.
- Setup steps live only in the README, and this file links to them.
- Record notes, results and decisions in this file at every step, and bring it up to date on the branch before asking the owner to merge.

## 4. Feature priorities

Everything in brief sections A to D got built. The one small extra is the Overdue label (section 5). Main worked after every merge.

| Order | Branch | What it added | Why then |
|---|---|---|---|
| 1 | `design` | The decisions in this file | Nothing got built before the design was agreed. |
| 2 | `project-setup` | Running API and database, React app shell, error handling, test setup, README setup steps | Every feature needs these. |
| 3 | `customers` | API and pages for brief A and B | Jobs belong to customers. Onboarding status is a column on the customer, so it came with them. |
| 4 | `staff` | API and pages for the staff list from brief D | Jobs get assigned to staff. |
| 5 | `jobs` | API and pages for brief C and the rest of D | It needs both tables above and holds the most rules. |
| 6 | `demo-and-docs` | Sample data, demo run, final README | The docs describe the finished app. |

**Left out on purpose**
- Deleting records. The brief doesn't ask for it, and keeping records protects job history.
- A Cancelled job status. The brief lists three statuses. Until one is added, a cancelled visit can only be edited or marked Completed.
- Search, job durations, status history and login. The brief doesn't ask for them.

## 5. Design decisions

| Decision | Options considered | Choice | Why |
|---|---|---|---|
| Appointments and jobs | One record, or two linked records | One Job record | The brief allows it. A visit gets booked once, and its date and staff member can't disagree between two records. A visit with no work attached still gets recorded as a job. |
| Backend framework | FastAPI, Flask | FastAPI | The owner chose it. Its JSON responses and `/docs` page suit a React frontend. |
| Database | SQLite, PostgreSQL installed locally, PostgreSQL in Docker, Supabase | SQLite | Nothing to install, and nothing in the brief needs a server database. The README's alternatives table has the reasons against the others. |
| Data access | Written SQL through `sqlite3`, SQLAlchemy, SQLModel | SQLAlchemy ORM | The owner chose an ORM, for the easier move to PostgreSQL. That move comes from the SQLAlchemy and psycopg docs and was not run. The cost is more to explain: models, sessions and `select()`. SQLModel stored bad data with no error. |
| Code layers | Routes plus service and repository layers, or routes that call the models | Routes call the models directly | Three tables don't need extra layers, and ORM calls are short. |
| Frontend | Jinja2 pages from the server, or React | React with Vite, plain JavaScript, `react-router` for page URLs, one CSS file | The owner chose React. Every developer needs Node.js, running it takes two terminals, and there's more frontend code. A minimal setup measured 24 npm packages and 62 MB. |
| How the two talk | Allow cross-origin requests (CORS), or a Vite proxy | Vite proxy | Vite's dev server forwards `/api` calls to FastAPI, so the backend needs no CORS setup. |
| Validation | Plain functions, or Pydantic models | Pydantic models with our own messages, plus checks in the route for rules that need the database | FastAPI runs the models before the route, and a small handler turns failures into `{field: message}`. A bad status or a missing field keeps Pydantic's wording, because the forms can't send those. |
| Where allowed statuses are enforced | `schemas.py` only, or a database CHECK constraint as well | `schemas.py` only | The API is the only way in. A constraint would add another copy of each list, and SQLite can't change one without rebuilding the table. |
| Customer fields | Split or single address, required or optional email | Name, phone and address required, email optional, address in one box | Nothing in the brief needs city or postcode on their own. Staff need a phone number and an address to do a job, but some customers have no email. |
| Date and time | Two columns, or one | One `scheduled_at` DateTime column | One value is simpler to sort and compare, and a `datetime-local` input sends one value. |
| Job type | A column, or read it from the staff role | No column | The assigned person's role already says fitting or maintenance, and two copies could disagree. |
| Staff who leave | Delete, active flag, no removal | `is_active` flag | They drop off the booking list, and past jobs keep their name. |
| Status changes | Inside the edit form, or their own small form | Their own form on the record's page | It's the most frequent action, and it shouldn't re-run the date rules. |
| Booking rules | None, or basic checks | No booking in the past, and no two open jobs for one staff member at the same date and time | These are the two mistakes a booking form should catch. With no job durations, only exact matches count as a clash. |
| Missed visits | Let them vanish from Upcoming, or label them | An Overdue label under All jobs | Upcoming only shows future jobs, so a missed visit would otherwise look fine. The owner approved this in the design. |
| Where to book from | The jobs page only, or customer pages too | Both | The brief says to create an appointment for a customer, so a customer's page has **Book a job**. The owner approved this in the design. |
| Where this file lives | Committed, or local only | Committed to the repo root | It's backed up, and a fresh session gets it with one clone. It holds no prompts. |
| AI attribution lines | Keep, or remove | Removed | The owner's choice. |
| AI mention in the README | One line, or none | None | The owner's choice. |

## 6. Code guide

The README has the folder tree, the reasons for the layout, the database diagram and how to extend the app. This section adds what you need to explain the code.

A page calls `api.js`, which calls a FastAPI route. FastAPI validates the request with a schema, the route reads or writes through the models, and the JSON result goes back to the page. If validation fails, the page shows each error next to its field.

**Shared backend code**
- `database.py` builds the database path from its own location, opens one session per request, and turns on foreign keys for each connection. With `CRM_ECHO_SQL=1` it prints the SQL. It stays because the ORM hides the SQL, and the brief asks to show how data is stored.
- `main.py` creates missing tables at startup, so there is no database setup step. It also turns validation failures into `{"errors": {field: message}}`, treats an oversized id as not found, and returns unexpected errors as a JSON message.
- `schemas.py` holds small validation functions such as `required` and `valid_phone`. `Annotated` attaches them to a type (`RequiredText`, `Phone`), and each class lists its fields using those types.

**Shared frontend code**
- `api.js` holds `request()`, which makes every call and turns failures into an `ApiError`, and `useApi()`, which loads data for a page. `useApi` reports `loading` until the response for the current URL arrives. Pages remove their forms while loading, so a form can't save one record's values over another.
- `useForm.js` holds a form's values, errors and saving state.
- `StatusForm`, `StatusBadge`, `Field` and `ErrorMessage` are shared by all three features.
- `vite.config.js` forwards `/api` calls to FastAPI on port 8000.

**Customers (brief A and B)**

| API call | What it does |
|---|---|
| `GET /api/customers` | List, in name order |
| `POST /api/customers` | Add |
| `GET /api/customers/{id}` | View one |
| `PUT /api/customers/{id}` | Edit name, phone, email, address |
| `PATCH /api/customers/{id}/status` | Change onboarding status |

Pages: `CustomerList`, `CustomerDetail`, `CustomerNew`, `CustomerEdit`. The last two share `CustomerForm`.

**Staff (the list in brief D)**

| API call | What it does |
|---|---|
| `GET /api/staff` | List, in name order, including inactive staff |
| `POST /api/staff` | Add |
| `GET /api/staff/{id}` | View one |
| `PUT /api/staff/{id}` | Edit name, role, phone, active flag |

Pages: `StaffList`, `StaffDetail`, `StaffNew`, `StaffEdit`. The last two share `StaffForm`. There is no delete. Unticking **Active** on the edit form marks someone inactive, which leaves them off the booking list.

**Jobs (brief C and the rest of D)**

| API call | What it does |
|---|---|
| `GET /api/jobs` | List all, earliest first |
| `GET /api/jobs?upcoming=true` | Upcoming appointments: future jobs not completed |
| `GET /api/jobs?customer_id=1` or `?staff_id=1` | One customer's or one staff member's jobs |
| `POST /api/jobs` | Book. A new job is always Pending |
| `GET /api/jobs/{id}` | View one |
| `PUT /api/jobs/{id}` | Edit customer, staff member, date and time, description |
| `PATCH /api/jobs/{id}/status` | Change status |

**Booking rules, in `routes/jobs.py`.** These live in the routes because they need the database or the job being edited. `booking_errors` checks the first four, and `update_job_status` checks the last.
- The customer and staff member must exist.
- A staff member must be active, unless the job already has them.
- The time must be in the future, unless an edit leaves it unchanged.
- One staff member can't have two open jobs at the same date and time. Jobs have no duration, so only exact matches count, and `booking_time` in `schemas.py` drops seconds so that 09:30:00 and 09:30:59 match. An edit only runs this check if it changes the staff member or time, which also stops a job clashing with itself.
- Reopening a completed job returns 409 if its slot has since been taken.

**Other job details**
- `Job.is_overdue` in `models.py` is true when the time has passed and the status is still Pending.
- `Job.customer` and `Job.staff` are SQLAlchemy relationships, and `JobOut` includes both records. `joinedload` in `list_jobs` fetches them in one query.
- `JobsTable` loads its own data from a `path` prop, so the jobs page, customer pages and staff pages all reuse it.
- `JobForm` loads the customer and staff lists for its dropdowns. It keeps an inactive staff member as an option only if the job already has them.
- A customer's **Book a job** button opens `/jobs/new?customer_id=1`, and `JobNew` starts with that customer selected.

**Sample data.** `seed.py` adds 4 customers, 4 staff members and 7 jobs. Dates are relative to today, so Upcoming and the Overdue label always have something to show. It adds nothing if the database already has customers, so running it twice can't duplicate records.

**Terms to be able to explain**
- **ORM.** It lets the code use Python objects, and SQLAlchemy writes the SQL.
- **Session (`db`).** One conversation with the database. `get_db` gives each request its own, and `db.commit()` saves the changes.
- **`Depends(get_db)`.** FastAPI runs `get_db` and passes the result to the route.
- **`response_model`.** The shape of the JSON a route returns.
- **`Annotated[str, AfterValidator(required)]`.** A string that also has to pass that function.
- **`joinedload`.** It fetches related records in the same query, so a list doesn't run one extra query per row.
- **`useState`.** A value a component remembers between renders.
- **`useEffect`.** Code that runs after a render. Here it loads data when the URL changes.
- **Vite proxy.** The dev server passes `/api` calls to FastAPI, so the browser only ever talks to one address.

**One request traced: adding a customer**
1. `CustomerNew.jsx` calls `request('/customers', { method: 'POST', body: values })` when the form is submitted.
2. Vite forwards the call to FastAPI.
3. FastAPI checks the body against `CustomerCreate` in `schemas.py`. If a rule fails, the handler in `main.py` returns `{"errors": {field: message}}` with status 422. `useForm` stores those errors, and `Field` shows each one under its input.
4. If the input is valid, `create_customer` in `routes/customers.py` builds a `Customer` object, then `db.add()` and `db.commit()` make SQLAlchemy run the INSERT.
5. FastAPI turns the object into JSON using `CustomerOut`, and returns it with status 201.
6. `CustomerNew.jsx` uses the returned `id` to open the customer's page, which fetches the record again with `useApi`.

## 7. Challenges

**The design comparison stalled.** The planned comparison had three stages: prototypes, three independent designs, then critics. The prototype step stopped making progress at 17:08, and Claude didn't notice until the owner asked for status at 18:25. The cause is unknown. Claude stopped the run, used the evidence already on disk, and wrote the design directly. The independent designs and critics never ran, so each code branch got a review instead. This cost about 75 minutes.

**Nobody had seen the pages.** The Browser pane in the Claude desktop app stayed hidden, so screenshots failed and clicks sometimes failed too. Page checks read the text and called `click()` from JavaScript, which proves behaviour but not appearance. On `demo-and-docs`, headless Chrome took real screenshots, and the pages looked right on desktop. Dates wrapped onto five lines in a narrow window, so Claude stopped that column wrapping.

**The API stopped working in the browser after a branch switch.** Pages said "Something went wrong" and `/api/customers` through Vite returned HTML, although the backend answered correctly on its own. Vite's log showed `git checkout` had rewritten `vite.config.js`, and the automatic restart that followed lost the proxy. Restarting `npm run dev` fixed it, and the README says so.

**What each review found, and Claude fixed**

| Branch | Finding | Fix |
|---|---|---|
| `project-setup` | The README said Node.js 20.19, but `react-router` needs 22.22 | Corrected |
| `project-setup` | `uvicorn --reload` scanned `.venv` and used 63.6% of a CPU core | `--reload-dir app` cut it to 1.2% |
| `project-setup` | A health test still passed with its database call deleted | Rewritten |
| `customers` | Jumping through browser history between two edit pages saved the first customer's values over the second | `useApi` goes back to loading when the URL changes |
| `customers` | All 36 tests still passed with the phone character rule deleted | Added cases for that rule, the digit limits and clearing an email |
| `customers` | A CHECK constraint copied each status list, and the health route lost its only caller | Removed both |
| `staff` | An API edit leaving out `is_active` turned an inactive person active | `StaffDetails` requires the flag |
| `jobs` | `has_clash` excluded the job being edited, but no caller could reach that case | Removed the dead code |
| `jobs` | A date typed straight through in Chrome sent a six-digit year and showed Pydantic's wording | `booking_time` reads the date and gives a plain message |
| `jobs` | Nothing proved that an In Progress job blocks its slot | Added tests |
| `jobs` | Inactive staff looked normal in job lists, and customers with the same name looked identical | Added a badge, and the phone in the dropdown |
| `jobs` | With no customers or staff, the booking form gave no way forward | Links to the add pages |
| `demo-and-docs` | This file's status was out of date, and section 10 sent a session to the wrong branch | Corrected |
| `demo-and-docs` | The README never said to clone the repo or reload after seeding, and left out the Overdue label | Added |
| `demo-and-docs` | "By hand" overstated the page checks, which used scripted clicks | Reworded |

The first commit message on `staff` says unticking Active takes someone off the booking list, which only became true in `jobs`. Claude left it, because rewriting it would need a force-push.

**Problems the prototypes found, and how the design avoids them**
- FastAPI can run a sync route and its database dependency on different threads, and `sqlite3` rejects that by default. Without `check_same_thread=False`, 179 of 300 requests failed with only 2 at a time. SQLAlchemy sets this itself for SQLite files.
- SQLite ignores foreign keys by default and stored a job for a customer that didn't exist. `database.py` runs `PRAGMA foreign_keys = ON` on every connection.
- SQLAlchemy's default pool keeps the SQLite file open, so pytest couldn't delete its temporary folder on Windows (`NotADirectoryError`). `NullPool` closes each connection after use.
- Reading a record after its session closed raised `DetachedInstanceError`, so routes finish reading records inside the request.
- A relative database path creates a new empty file in whichever folder the app starts from, so the path comes from the project folder.
- An id too large for SQLite raises `OverflowError`, so `main.py` treats it as not found.
- `TestClient` skips startup unless used in a `with` block, so the tables don't get created.

## 8. Testing and demo

**How to test:** follow [README.md](README.md). Run `pytest` in `backend`, and `npm run lint` and `npm run build` in `frontend`.

**Latest results, on `demo-and-docs`, from a fresh clone of GitHub**
- `pytest`: 114 passed on Python 3.11.4 and on Python 3.12.10.
- `npm run lint` is clean, and `npm run build` succeeds on Node.js 24.20.
- Both servers started with the README's exact commands, in Git Bash and in PowerShell, and `python -m app.seed` added the sample data.
- `git status` stayed clean afterwards, so nothing the app or tests create gets committed.
- In the final review, an auditor walked every line of the brief and found all of it met, with no code bug. A second reviewer followed the README as a new developer, and every step worked.
- The frontend has no automated tests. Its pages get checked in the browser.

**Demo script**

Start both servers, add the sample data, and open http://localhost:5173. Every step passed on the fresh clone, using scripted clicks on the real pages.

| Brief item | What to do | What you should see |
|---|---|---|
| A. List customers | Open the app | The customer list, in name order |
| A. Validation | Click **Add customer**, then submit it blank | An error under name, phone and address |
| A and B. Add a customer | Enter a bad email and pick an onboarding status, then correct the email and save | The email error appears and the typed values stay, then the customer's page opens with that status |
| A. Edit a customer | Click **Edit details** and change the address | The new address on their page |
| B. Update a status | Change it to In Progress, then Active | The badge changes each time |
| C. Create an appointment | Click **Book a job** on the customer's page | The form opens with that customer selected, and Lena Fox isn't offered |
| C. Date, time, staff | Choose Sam Patel and a past date, then a future date, and add a description | The past date is refused, then the job's page opens as Pending |
| C. Upcoming appointments | Click **Jobs** | The job appears, soonest first |
| D. Double booking | Book Sam Patel at the same date and time again | "This staff member already has an open job at that time." |
| D. Job status | On the job's page, choose In Progress, then Completed | The badge changes, and the job leaves Upcoming but stays in All jobs |
| Overdue label | Click **All jobs** | The job "Survey the site" shows Overdue |
| D. Staff list | Click **Staff** | Fitters and engineers, with Lena Fox Inactive |
| D. Jobs per person | Open Sam Patel | Sam Patel's page lists their jobs |

**Checked outside the demo script**
- Unknown records: `/customers/999` and `/jobs/999` show a clear message, and an unknown page URL shows "Page not found".
- A stopped backend: pages show "Something went wrong. Check the backend is running, then try again."
- A history jump between two customers' edit pages shows the right values, and saving leaves both customers intact.
- A six-digit year shows "Enter a valid date and time."
- Reopening a completed job onto a taken slot shows the clash message.
- A past Pending job's description can be corrected without changing its time or inactive staff member, but it can't move to another past time.
- An empty database shows links to add a customer and a staff member on the booking form.

**Prototype results, not from the final app.** The same small customer feature was built in four stacks, all using Jinja2 pages because React came later. All four passed the same 11 tests on Python 3.11 and 3.12, and all four stored 200 of 200 saves sent 20 at a time, with no errors.

| Stack | App lines | Installed packages |
|---|---|---|
| FastAPI + `sqlite3` | 107 | 18 |
| FastAPI + SQLAlchemy | 98 | 19 |
| FastAPI + SQLModel | 94 | 20 |
| Flask + `sqlite3` | 86 | 7 |

## 9. Session summaries

### Session 1, 4 November 2026

**Step 1, understanding.** The owner shared the brief and asked for a guided, step-by-step build, with the approach and documentation as the priorities. Claude checked the machine and GitHub, found a private, empty repo with admin access, and asked four questions.

**Step 2, outline.** The owner chose one Job record, suggested FastAPI with PostgreSQL or Supabase while staying open to alternatives, set the branch and merge rule, and asked for summaries instead of prompts in this file. Claude proposed ten sections for this file and started comparing stacks with working prototypes in a scratch folder.

**Step 3, rules.** The owner approved the ten sections and asked that current state, results, notes, the current step and the plan be included too. They also set that day as the deadline, asked to remove the attribution lines, and asked to keep AI out of the README. They confirmed that each feature starts only after the previous one is merged, and asked for the minimal path with no temporary fixes, the best decisions with reasoning for each, and notes in this file at every step. Claude made the first commit.

The owner then asked whether Claude had missed the rest of that message. Claude had recorded most of it but not acknowledged it, and this file was missing two rules, so Claude added them. On roles, Claude told the owner that they decide, review, merge and present the work, and Claude recommends, codes, tests and documents.

**Step 3, design.** The owner asked for status at 18:25. Claude found the comparison had stalled, stopped it, and wrote the design from the evidence it had collected: FastAPI, SQLite and written SQL.

The owner confirmed FastAPI and SQLite and chose React for the frontend. They asked what written SQL and an ORM are, then whether an ORM removes the PostgreSQL downside. Claude explained both, and said an ORM mostly does remove it. Claude also corrected its earlier answer, which had said the written SQL move only changes placeholders, when it also touches table definitions, date columns and error handling. Claude recommended written SQL because the move isn't part of this project.

The owner chose an ORM and asked how the folders and code were planned. Claude picked SQLAlchemy, dropped the planned `queries/` folder and `schema.sql` because the models now hold the tables, explained the layout, and raised the `design` PR.

**Step 4, `project-setup`.** The owner merged the `design` PR. Claude deleted the merged `design` branch from GitHub without being asked, told the owner, and restored it. Claude then built the running skeleton. Two independent reviewers checked it, and Claude fixed what they found. The owner asked what's pending on their side, how testing works, and what `pytest` is, and Claude explained. The owner merged the PR.

**Step 4, `customers`.** Claude built the customer API, validation rules and tests, then the React pages, and checked each flow in the browser. Two independent reviewers found a data-loss bug and some weak tests, and Claude fixed them. The owner merged the PR.

**Step 4, `staff`.** Claude built the staff API, tests and pages, following the customer pattern. Two independent reviewers found that an API edit could reactivate someone by accident, and Claude fixed it. The owner asked for the workflow as a flow chart, and Claude drew three: how a save moves through the app, how office staff use the CRM, and how each feature gets built. The owner merged the PR.

**Step 4, `jobs`.** Claude built the job API, the booking rules and tests, then the job pages, and added job lists to the customer and staff pages. Three independent reviewers found dead code, a raw date error and some weak tests, and Claude fixed them. The owner asked who the end users are and how long was left. Claude said office staff are the users, that fitters and engineers would be the natural next users if login existed, and that about an hour remained. The owner merged the PR.

**Step 5, `demo-and-docs`.** Claude added the sample data and final README, took screenshots to check how the pages look, tested from a fresh clone on both Python versions, and ran the full demo against the brief. Three reviewers then acted as a new developer, a brief auditor and an editor. They found every brief line met and no code bug, plus documentation fixes, which Claude made before raising the last PR.

## 10. How to continue

1. Read section 1, then section 3.
2. Check where the repo stands:

   ```bash
   git checkout main
   git pull
   git branch -r
   git log --oneline -10
   gh pr list --state all
   ```

3. If a PR is still open, its branch is ahead of main. Check out that branch and read its copy of this file, because it's the newer one.
4. Follow [README.md](README.md) to set up the app and run the tests.
5. Pick up from "Next" in section 1. For new features, the README's "How to continue developing it" lists what to add.

## 11. Notes

- Repo: https://github.com/ankathakanksha21/SmartiEnvironmental (private). An assessor will need access.
- Machine: Windows 11, with Python 3.11.4 as `python`, Python 3.12.10 through `py`, Node.js 24.20 and npm 11.19.
- Claude has no memory of earlier sessions on this work, so this file is the only record of past decisions.
- `.claude/launch.json` holds Claude's commands for starting the servers. It stays out of git through `.git/info/exclude`.
- When the Browser pane in the Claude desktop app is hidden, screenshots fail but reading page text works. Headless Chrome can take screenshots instead.
- Stopping a server that was started through a Git Bash wrapper left its Vite process running. Check ports 8000 and 5173 before trusting what answers there.
- The repo has no automated checks on GitHub, so a PR shows no CI results. Tests run locally.
- Known limitations are in the README. In testing, simultaneous requests double-booked 4 of 10 slots in one run and 8 of 10 in another.
- The README is written in the owner's voice and leaves out AI by the owner's choice, while this file records how the work was done.
