# Handoff

Give a fresh session this file and the code, and it can continue without anything being re-explained. Setup steps, the code layout and the database diagram live only in [README.md](README.md). "The owner" below means the repo owner, ankathakanksha21.

## 1. Current status

- **Step we're in:** Step 9, `connected-workflow`, waiting for the owner to merge.
- **On main:** All of brief sections A to D, the sample data, the final README and the Smarti-branded design.
- **On this branch:** Six small additions that connect the steps into one journey (section 4).
- **Open PR:** #10, on `connected-workflow`.
- **Next:** The owner merges the PR. Claude then checks main and corrects this status in a small follow-up PR, as with PR #7 and PR #9. After that, the owner tries the app, gives the assessor access to the private repo, and presents the work. New work starts only if the owner asks.

### Plan

- [x] 1. Understand the brief and ask the open questions
- [x] 2. Agree this file's outline and make the first commit
- [x] 3. Compare stacks and agree the design
- [x] 4. Build features, one branch and PR at a time: `project-setup`, `customers`, `staff`, `jobs`
- [x] 5. Test everything and run the demo, on `demo-and-docs`
- [x] 6. Finish the README and this file, on the same branch
- [x] 7. Owner merges the last PR
- [x] 8. Design refresh the owner asked for, on `ui-design`
- [ ] 9. Connect the steps into one workflow, on `connected-workflow`, after the owner's cross-check

## 2. Project summary and checklist

A simple web CRM for a business that manages customers, appointments, fitters and maintenance engineers. It is an assessment take-home, and the assessor cares more about the approach, the decisions and how clearly the work is explained than about production readiness. Authentication, hosting, advanced security and complex integrations are not required. AI tools are allowed.

Office staff are the end users. The brief doesn't name them, so this is Claude's reading, which the owner asked about and didn't object to. Fitters and engineers are records that jobs get assigned to, and customers don't use the app. The brief lists features rather than what each kind of user wants, so an office admin is fully covered, and a manager, fitter or engineer only partly.

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

The six additions on `connected-workflow` go beyond this table, and the owner approved them (section 4).

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
- Add no features beyond the brief unless the owner approves them.
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

Everything in brief sections A to D got built, and main worked after every merge. There are two sets of small extras:

- The Overdue label (section 5), from the design.
- Six additions on `connected-workflow`. The owner's cross-check showed that the records were linked but the steps weren't, and the owner approved these to connect them. They are an Overview home page, success messages, clickable names in job lists, onboarding that follows the jobs, a Next step line on the customer's page, and a follow-up maintenance visit after a completed job.

| Order | Branch | What it added | Why then |
|---|---|---|---|
| 1 | `design` | The decisions in this file | Nothing got built before the design was agreed. |
| 2 | `project-setup` | Running API and database, React app shell, error handling, test setup, README setup steps | Every feature needs these. |
| 3 | `customers` | API and pages for brief A and B | Jobs belong to customers. Onboarding status is a column on the customer, so it came with them. |
| 4 | `staff` | API and pages for the staff list from brief D | Jobs get assigned to staff. |
| 5 | `jobs` | API and pages for brief C and the rest of D | It needs both tables above and holds the most rules. |
| 6 | `demo-and-docs` | Sample data, demo run, final README | The docs describe the finished app. |
| 7 | `ui-design` | Smarti's colours, font and cards | The owner asked for it after trying the app. It changes no behaviour. |
| 8 | `connected-workflow` | The six additions above | The owner approved them after a cross-check. They build on every finished feature. |

**Left out on purpose**
- Deleting records. The brief doesn't ask for it, and keeping records protects job history.
- A Cancelled job status. The brief lists three statuses. Until one is added, a cancelled visit can only be edited or marked Completed.
- Search, job durations, status history and login. The brief doesn't ask for them.
- A duplicate-customer check. Claude offered it as a seventh addition, and the owner chose the six.
- Recording the work done on a job. It would need a new column, and the six additions need no database change.

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
| Look and feel | Keep the first version, or follow Smarti's brand | Smarti's brand, read from smartilimited.com: navy `#253551`, sky blue `#509EC7`, green `#5BB906`, square navy buttons, and a hand-drawn green stroke under page titles and the active menu item. Cards stay, as the owner asked. | The owner asked for a design refresh with no change in behaviour, and gave the website as the reference. Only `style.css`, the favicon, the font imports in `main.jsx` and the font package in `package.json` and its lock file changed. The stroke is our own SVG, not copied from the site. |
| Where the green goes | Every link, or only key places | The green stroke marks page titles, the active menu item and the active tab. Other links have a thin sky-blue underline that turns green on hover. | Smarti's site uses green as a rare accent on headings. On every link it lost its effect and blurred what was clickable. |
| Small blue text | Smarti's sky blue, or a darker shade | `#2b73a0` for table headers, labels and the focus outline | Smarti's `#509EC7` is about 3:1 on white, too low for small text. It stays for the top strip, link underlines and focus on the navy header. |
| Corners | Rounded, or square like Smarti's site | Buttons and fields square, cards and badges only 3 to 4px | The owner asked for cards, and a small radius keeps them looking like cards while staying close to the brand. |
| Font | System fonts, a Google Fonts link, or a package | Poppins, Smarti's font, through `@fontsource/poppins` | The package works offline and needs no extra setup step beyond `npm install`. A Google Fonts link would need internet to look right. |
| Where validation runs | Repeat the rules in the browser, or keep them in the backend | Backend only. Forms use `noValidate` and show the API's errors | Each rule has one copy. The owner confirmed this in the cross-check. |
| Sample data wording | Generic, or Smarti's product wording | Stays as it is | The owner's choice in the cross-check. |
| Home page | A redirect to Customers, or an Overview | Overview | It shows what needs attention first, and each count links to the page behind it. It reads the existing API, so it adds no backend code. |
| Onboarding status | Only by hand, or following the jobs | Follows the jobs, and can still be set by hand | Booking takes New Enquiry to In Progress, and completing a job makes the customer Active. A separate manual step would let the status disagree with the jobs. |
| When a job reopens | Move onboarding back, or leave it | Leave it | The office may have set the status by hand, and a reopened job may be a correction. The README lists this as a limitation. |
| Next step | Store it, or work it out from the jobs | Worked out by one shared component from the customer's jobs, on the customer's page and on a completed job's page | A stored value could go stale, one component means the two pages can't disagree, and this needs no database change. |
| Next step wording | "Visit" or "job" | "Book the first job" and "Complete the job on...", and "Book a follow-up maintenance visit" | "Job" matches the **Book a job** button and the job pages, so the two don't look like different things. The follow-up stays a maintenance visit, the term the owner uses. |
| Success messages | A toast library, React Router's location state, or React state in `Layout` | React state in `Layout`, shown for 5 seconds at the bottom of the screen | It needs no new package. Location state came first, and the review showed why it's wrong (section 7). A message may stay on screen for its 5 seconds after you move to another page, which does no harm. |
| Follow-up visit | A job type, a link between jobs, or a filled-in form | A filled-in form, `/jobs/new?customer_id=1&description=...` | It needs no database change, and the office can change anything before saving. |
| Customer's status on a job page | A badge beside the name, or a labelled line | A labelled line, "Onboarding status: In Progress" | The onboarding and job statuses share words such as In Progress, so an unlabelled badge read as the job's own status. |
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
- `Layout.jsx` draws the header and the success message. It keeps the message in React state, clears it after 5 seconds, and hands `showMessage` to the current page through `<Outlet context>`. A page gets it with `useOutletContext()`.
- `CustomerNextStep` draws the highlighted Next step line from a customer's jobs. The customer's page and a completed job's page use it.
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
- `JobsTable` loads its own data from a `path` prop, so the Overview, the jobs page, customer pages and staff pages all reuse it. A `limit` prop shows only the first few, and customer and staff names link to their pages.
- `JobForm` loads the customer and staff lists for its dropdowns. It keeps an inactive staff member as an option only if the job already has them.
- A customer's **Book a job** button opens `/jobs/new?customer_id=1`, and `JobNew` starts with that customer selected. It also reads `description` from the URL, for follow-up visits.

**Onboarding that follows the jobs, in `routes/jobs.py`**
- `start_onboarding` moves a New Enquiry customer to In Progress. `create_job` calls it, and `update_job` calls it only when the job moves to another customer. Any other edit leaves a status set by hand alone. Both call it after their checks pass, so a refused request changes nothing.
- `update_job_status` makes the customer Active when a job becomes Completed. Reopening a job leaves the customer as they are.
- Each change saves in the same `db.commit()` as the job.

**The connected pages**
- `Overview.jsx` loads customers, all jobs, upcoming jobs and staff through the existing API calls and works out the counts in the browser. Staff workload lists active staff, plus anyone inactive who still has open jobs.
- `CustomerNextStep` reads the customer's jobs. With none, it offers the first job. With an open job, it links to the earliest one and says if it's overdue. With every job completed, it offers a follow-up maintenance visit.
- `JobDetail.jsx` shows that line once the job is Completed, and shows the customer's onboarding status as a labelled line under their name.

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
- **`useOutletContext`.** How a page gets something from the layout around it. Here it's `showMessage`.

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

**The first redesign missed the brand.** The owner's design request said "green underlining". No images reached Claude with that message, and Claude read it as something to remove, then built a look of its own with PR #8. The owner then shared screenshots of smartilimited.com, where the green hand-drawn underline is the brand's signature. Claude read the real fonts and colours from the live site and redid the design on the same branch. Lesson for later sessions: ask for the reference before designing, and check what a word refers to before acting on it.

**The design review on `ui-design`.** A visual reviewer found that the phone header had lost its padding, and that phone numbers wrapped in phone-sized tables. An accessibility reviewer found that removing the focus outline left the checkbox and error fields with almost no visible focus, and that fields under 16px make iPhones zoom in when tapped. Claude fixed all of these before redoing the design, and kept the fixes.

**The brand review on `ui-design`.** A reviewer measured the green stroke against the owner's images: it sat three times too far below the text and was too thin, where Smarti's crosses the descenders like a brush mark. It also found green on every link, where the site uses it sparingly. An accessibility reviewer found the sky-blue focus outline under 3:1 on light backgrounds, field borders at 1.72:1, and long job descriptions pushing Status far off-screen on phones. Claude fixed all of these. All normal text passes 4.5:1, and the disabled button (exempt) is 3.36:1. The green stroke itself is about 2.5:1 on white, which is fine as decoration because it carries no meaning of its own.

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
| `connected-workflow` | Saving any job edit re-ran the onboarding rule and overwrote a status set by hand. Two reviewers found this separately, and no test covered it | The rule only runs when a job moves to another customer. Added tests |
| `connected-workflow` | The success message lived in browser history, so a reload or Back showed it again. A slow save could pull you back to the page you'd left, and the timer that cleared it could cancel a link click | Moved it into React state in `Layout` |
| `connected-workflow` | On a phone, the message from a status save appeared off-screen. On desktop, the page jumped about 72px when it cleared | Fixed it to the bottom of the screen |
| `connected-workflow` | A completed job's page offered a follow-up even when one was already booked, which contradicted the customer's page | Both pages now share `CustomerNextStep` |
| `connected-workflow` | The onboarding badge on the job page read as the job's own status | A labelled line under the customer's name |
| `connected-workflow` | The four counts wrapped 3 and 1 at tablet widths, and stacked on phones so no appointment showed on the first screen | Four across, or two rows at 975px and under |
| `connected-workflow` | The Next step bar broke the rule on where green goes, and its text sat 3px off the card below | Sky blue, and lined up |
| `connected-workflow` | The count cards didn't look clickable, and on a touch screen had no hover to show it | Underlined labels, like other links |
| `connected-workflow` | "Visit" and "job" named the same thing on one page, and the follow-up link was written in two files | One word and one component |
| `connected-workflow` | The new CSS repeated the card and label rules, and some tests couldn't fail when their rule broke | Grouped the rules. Five more test cases, and two tests corrected |

**Findings left alone on purpose, on `connected-workflow`.** Count labels stay plural beside a 1, because they name the metric. A customer's name in the jobs table on their own page still links there, which does no harm. The Next step line appears 40 to 70ms after the customer's details. Within 5 seconds of a successful save, a refused status change shows the green and red messages together, and both are true. A customer id typed into the booking URL by hand can show a raw error, such as "Input should be a valid integer", as it did before this branch. The header wraps below 355px wide. Moving a job between customers is listed as a limitation in the README.

**The journey script read too early.** The first run stopped with "element is not enabled", and the next failed four checks. The URL changes a moment before React redraws, and the customer and job pages share a status dropdown and badge, so the script was reading the old page. It now waits for the next page's heading, and every check passed with no change to the app. Each failure could have been a real bug, so each was rerun on a fresh database before being dismissed.

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

**Results on `ui-design`:** `pytest` 114 passed, `npm run lint` clean, `npm run build` succeeds. A throwaway Playwright script in a scratch folder walked the whole app with real clicks and key presses on a scratch copy of the app, and all its checks passed. Screenshots of 11 pages or states at 1280px and 390px wide showed no sideways scrolling and no console errors.

**Results on `connected-workflow`:** `pytest` 133 passed, `npm run lint` clean, `npm run build` succeeds. On a scratch copy, three throwaway Playwright scripts ran with real clicks. The journey below passed 50 checks, the whole app passed 49, and an empty database passed 6. Screenshots of 12 pages or states at 1280px and 390px wide showed no sideways scrolling and no console errors.

**Demo script**

Start both servers, add the sample data, and open http://localhost:5173. Every step passed using scripted clicks on the real pages, on a fresh clone for `demo-and-docs` and on a scratch copy for `connected-workflow`.

**The connected journey**

| Step | What to do | What you should see |
|---|---|---|
| Overview | Open the app | Four counts, the next appointments, and each person's open jobs |
| Enquiry | Click **New enquiries**, then **Chloe Evans** | Status New Enquiry, and Next step says to book the first job |
| Booking | Click **Book the first job**, then choose Sam Patel, a date and time in the future and a description, and save | The form starts with Chloe selected, then "Job booked." appears and the job's page says "Onboarding status: In Progress" |
| Customer's page | Click Chloe's name | Status In Progress, and Next step says to complete the job on that date |
| Completion | Click the Next step link, choose Completed and click **Update status** | "Job status updated." appears, the job's page says "Onboarding status: Active", and Next step offers a follow-up maintenance visit |
| Follow-up | Click **Book a follow-up maintenance visit**, then choose Priya Shah and a date and time in the future, and save | The form starts with Chloe and "Maintenance visit" filled in, and Chloe stays Active |
| Back to the start | Click **Overview** | New enquiries has dropped by one, and Priya Shah has one more open job |

**The brief, item by item**

| Brief item | What to do | What you should see |
|---|---|---|
| A. List customers | Click **Customers** | The customer list, in name order |
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

**Step 5, `demo-and-docs`.** Claude added the sample data and final README, took screenshots to check how the pages look, tested from a fresh clone on both Python versions, and ran the full demo against the brief. Three reviewers then acted as a new developer, a brief auditor and an editor. They found every brief line met and no code bug, plus documentation fixes, which Claude made before raising the last PR. Claude pointed out that this file names Claude and is visible to anyone with repo access. The owner merged the PR, and Claude confirmed that main passes every check.

**After the plan, `ui-design`.** The owner tried the app, asked how to test it by hand, and added their own test customer. They then asked for a design refresh with the same functionality: colours, font, sizes, spacing, cards instead of boxes, and green underlining, which Claude misread as something to remove. Claude restyled the app on the `ui-design` branch, using a scratch copy for any test that writes data, so the owner's data stayed untouched. Two independent reviewers checked the look, accessibility and behaviour, and Claude fixed what they found (section 7), then raised the PR.

The owner then shared two screenshots of smartilimited.com and asked whether Claude had considered them. Claude said it hadn't: no images had come through, and it had also misread "green underlining" as something to remove. The owner's business is now clear from that site: Smarti Environmental makes waterless urinal valves, and its customers get installation and maintenance. Claude read the brand's fonts and colours from the live site and redid the design to match. Reviewers measured it against the owner's images, Claude fixed what they found, and the owner merged the PR.

**After the plan, `connected-workflow`.** The owner cross-checked the app and asked four things: whether validation covers both backend and frontend, whether the sample data is realistic, whether the app feels like a business tool, and whether it works as one journey from enquiry to maintenance. Claude said the backend enforces the rules and the frontend displays the errors, that the sample data is partly realistic, that the app was closer to good CRUD pages than a tool, and that the records were linked while the steps weren't. The owner kept validation and the sample data as they were, and asked for minimal suggestions to make the app feel more like a tool and more like a story, while staying close to the brief.

The owner also asked whether the app should be designed around what each kind of user wants, whether it confirms every important action, and whether it avoids duplicates and stale job details. Claude said the brief lists features rather than users, so the design matches it, with an office admin fully covered and a manager, fitter or engineer partly covered. Errors were shown but successes weren't. Duplicate customers weren't prevented, and job details stay current because each visit is one record read live.

Claude suggested six additions and offered a duplicate check as a seventh. The owner chose the six. Claude built them on one branch and tested them with real clicks on a scratch copy, so the owner's data stayed untouched. Independent reviewers then checked the branch (section 7).

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
- A running Vite server can't find a package installed after it started, and the page goes blank with a 500 error. Restart `npm run dev` after `npm install`.
- `playwright-core` with the installed Chrome (`channel: 'chrome'`) gives real clicks and screenshots even when the Browser pane is hidden. Keep it in a scratch folder, because the project doesn't need it.
- In a browser script, the URL changes a moment before React redraws, and the customer and job pages share a status dropdown and badge. Wait for the next page's heading before reading anything.
- The repo has no automated checks on GitHub, so a PR shows no CI results. Tests run locally.
- Known limitations are in the README. In testing, simultaneous requests double-booked 4 of 10 slots in one run and 8 of 10 in another.
- The README is written in the owner's voice and leaves out AI by the owner's choice, while this file records how the work was done.
