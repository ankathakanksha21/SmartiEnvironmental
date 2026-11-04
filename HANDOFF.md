# Handoff

Give a fresh session this file and the code, and it can continue without anything being re-explained. Setup steps live only in [README.md](README.md). "The owner" below means the repo owner, ankathakanksha21.

## 1. Current status

- **Step we're in:** 3 of 7, comparing stacks and agreeing the design.
- **On main:** this file, a README title and `.gitignore`.
- **Working branch:** `design`, for this step's notes and decisions.
- **Open PR:** none.
- **Next:** the owner approves the stack and design in sections 4 and 5. Claude then raises the `design` PR, the owner merges it, and `project-setup` starts.
- **Deadline:** finish today, 4 November 2026.

### Plan

- [x] 1. Understand the brief and ask the open questions
- [x] 2. Agree this file's outline and make the first commit
- [ ] 3. Compare stacks and agree the design (waiting for the owner's approval)
- [ ] 4. Build features, one branch and PR at a time: `project-setup`, `customers`, `staff`, `jobs`
- [ ] 5. Test everything and run the demo, on `demo-and-docs`
- [ ] 6. Finish the README and this file, on the same branch
- [ ] 7. Owner merges the last PR

## 2. Project summary and checklist

A simple web CRM for a business that manages customers, appointments, fitters and maintenance engineers. It is an assessment take-home, and the assessor cares more about the approach, the decisions and how clearly the work is explained than about production readiness. Authentication, hosting, advanced security and complex integrations are out of scope. AI tools are allowed.

| Brief item | State |
|---|---|
| A. Add customers with name, contact details and address | not started |
| A. View a list of customers | not started |
| A. View and edit a customer record | not started |
| B. Assign an onboarding status (New Enquiry, In Progress, Active) | not started |
| B. Update the status as a customer progresses | not started |
| C. Create an appointment for a customer | not started |
| C. Assign a date, time and staff member | not started |
| C. View upcoming appointments | not started |
| D. Maintain a list of fitters and maintenance engineers | not started |
| D. Assign jobs to individual staff members | not started |
| D. Track job statuses (Pending, In Progress, Completed) | not started |
| Basic, usable interface | not started |
| Shows data being created, stored, retrieved and updated | not started |
| Logical, maintainable code structure | not started |
| Input validation and basic error handling | not started |
| Git version control | started |
| README: install, set up database or test data, run locally, test main functionality | not started |
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
| 2 | `project-setup` | Running app, database, base page, error pages, test setup, README setup steps | Every feature needs these. |
| 3 | `customers` | Brief A and B | Jobs belong to customers. Onboarding status is a column on the customer, so it comes with them. |
| 4 | `staff` | The staff list from brief D | Jobs get assigned to staff. |
| 5 | `jobs` | Brief C and the rest of D | It needs both tables above and holds the most rules. |
| 6 | `demo-and-docs` | Sample data, demo run, final README | It documents what exists, once it exists. |

**Left out on purpose**
- Deleting records: the brief doesn't ask for it, and keeping records protects job history.
- A Cancelled job status: the brief lists three statuses. Until one is added, a cancelled visit can only be edited or marked Completed.
- Search, job durations, status history and login: the brief doesn't ask for them.

## 5. Design decisions

| Decision | Options considered | Choice | Why |
|---|---|---|---|
| Appointments and jobs | One record, or two linked records | One Job record | A visit gets booked once, and its date and staff member can't disagree between two records. "Upcoming appointments" is a filtered list of jobs. The downside is that a visit with no work attached still gets recorded as a job. |
| Web framework | FastAPI, Flask | FastAPI | The owner named it. In the prototypes it cost 21 more lines and 11 more installed packages than Flask. |
| Database | SQLite, PostgreSQL installed locally, PostgreSQL in Docker, Supabase | SQLite | Nothing to install, no account, works offline, and the brief accepts it. PostgreSQL needs an install and a password on every machine. Supabase needs an account, a secret shared outside the repo and internet, and its pricing page says free projects pause after a week of inactivity, so the app could be down during review. Nothing in the brief needs a server database. |
| Data access | Written SQL through `sqlite3`, SQLAlchemy, SQLModel | Written SQL through `sqlite3` | The INSERT, SELECT and UPDATE statements are visible, which is what the brief asks to demonstrate. The ORMs saved 9 to 13 lines and added concepts to explain. SQLModel table models stored blank names and bad emails with no error. The downside is that moving to PostgreSQL means changing every placeholder, but all the SQL sits in `app/queries/`. |
| Interface | Jinja2 pages from the server, or a JSON API with a separate frontend | Jinja2 pages, one CSS file, no JavaScript | One language and no build step. |
| Validation | Plain functions, Pydantic form models | Plain functions that return `{field: message}` | We control the wording. Pydantic's default message reads "String should have at least 1 character". |
| Customer fields | Split or single address, required or optional email | Name, phone and address required, email optional, address in one box | Nothing in the brief needs city or postcode on their own. Staff need a phone number and an address to do a job, but some customers have no email. |
| Date and time | Two columns, or one | One `scheduled_at` text column as `YYYY-MM-DDTHH:MM` | This text sorts in date order, and a `datetime-local` input sends exactly this format. |
| Job type | A column, or read it from the staff role | No column | The assigned person's role already says fitting or maintenance, and two copies could disagree. |
| Staff who leave | Delete, active flag, no removal | `is_active` flag | They drop off the booking list, and past jobs keep their name. |
| Status changes | Inside the edit form, or their own small form | Their own form on the record's page | It's the most frequent action, and it shouldn't re-run the date rules. |
| Booking rules | None, or basic checks | No booking in the past, and no two open jobs for one staff member at the same date and time | These are the two mistakes a booking form should catch. With no job durations, only exact matches count as a clash. |
| Where this file lives | Committed, or local only | Committed to the repo root | It's backed up, and a fresh session gets it with one clone. It holds no prompts. |
| AI attribution lines | Keep, or remove | Removed | The owner's choice. |
| AI mention in the README | One line, or none | None | The owner's choice. |

## 6. Code guide

No application code yet. This is the planned layout.

```
app/
  main.py          creates the app, adds the routes and error pages
  database.py      opens a connection per request, creates tables at startup
  schema.sql       the three tables
  seed.py          sample data
  validation.py    input rules as plain functions
  templating.py    shared templates and one-time messages
  routes/          one file per feature, handles HTTP only
  queries/         one file per feature, holds all the SQL
  templates/       Jinja2 pages
  static/style.css
tests/             pytest, one file per feature plus validation
```

A request goes from the route to validation, then to the queries, and the route either redirects or shows the form again with errors.

**Tables**
- `customers`: id, name, phone, email, address, onboarding_status
- `staff`: id, name, role, phone, is_active
- `jobs`: id, customer_id, staff_id, description, scheduled_at, status

## 7. Challenges

**The design comparison stalled.** The planned comparison had three stages: prototypes, three independent designs, then critics. The prototype step stopped making progress at 17:08, and Claude didn't notice until the owner asked for status at 18:25. The cause is unknown. Claude stopped the run, used the evidence already on disk, and wrote the design directly. The independent designs and critics never ran, so each PR gets a review instead. This cost about 75 minutes.

**Problems the prototypes found, and how the design avoids them**
- FastAPI can run a sync route and its database dependency on different threads, and `sqlite3` rejects that by default. Without `check_same_thread=False`, 179 of 300 requests failed with only 2 at a time. Each request owns its connection, so the setting is safe.
- `RedirectResponse` defaults to 307, which repeats the POST. The test client ran one form submission 21 times. Use 303 after every form.
- FastAPI answers 404 and bad ids with JSON. Use `{id:int}` in paths and HTML error handlers.
- SQLite ignores foreign keys by default and stored a job for a customer that didn't exist. Run `PRAGMA foreign_keys = ON` on every connection.
- A relative database path creates a new empty file in whichever folder the app starts from. Build the path from the project folder.
- An id too large for SQLite raises `OverflowError`, which gives a 500 page. Treat it as not found.
- `TestClient` skips startup unless used in a `with` block, so the tables don't get created.

## 8. Testing and demo

The app has no tests or demo yet.

**Prototype results, not from the final app.** The same small customer feature was built in four stacks. All four passed the same 11 tests on Python 3.11 and 3.12, and all four stored 200 of 200 saves sent 20 at a time, with no errors.

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

**Step 3, design.** The owner asked for status at 18:25. Claude found the comparison had stalled, stopped it, and wrote the design from the evidence it had collected: FastAPI, SQLite and written SQL. The design is waiting for the owner's approval.

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
- Machine: Windows 11, with Python 3.11.4 as `python` and Python 3.12.10 through `py`.
- The owner started this work with no memory of earlier sessions, so this file is the only record of past decisions.
