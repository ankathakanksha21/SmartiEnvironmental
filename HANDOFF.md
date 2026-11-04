# Handoff

Give a fresh session this file and the code, and it can continue without anything being re-explained. Setup steps live only in [README.md](README.md). "The owner" below means the repo owner, ankathakanksha21.

## 1. Current status

- **Step we're in:** 3 of 7, comparing stacks and agreeing the design.
- **On main:** this file, a README title and `.gitignore`.
- **Working branch:** `design`, for this step's notes and decisions.
- **Open PR:** none.
- **Next:** the owner approves the stack and design, then the first feature branch starts.
- **Deadline:** finish today, 4 November 2026.

### Plan

- [x] 1. Understand the brief and ask the open questions
- [x] 2. Agree this file's outline and make the first commit
- [ ] 3. Compare stacks and agree the design (in progress)
- [ ] 4. Build features, one branch and PR at a time
- [ ] 5. Test everything and run the demo
- [ ] 6. Finish the README and this file
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

Everything in brief sections A to D gets built, with no extras. The build order goes here once the design is agreed.

## 5. Design decisions

| Decision | Options considered | Choice | Why |
|---|---|---|---|
| Appointments and jobs | One record, or two linked records | One Job record | A visit gets booked once, and its date and staff member can't disagree between two records. "Upcoming appointments" is a filtered list of jobs. The downside is that a visit with no work attached still gets recorded as a job. |
| Stack | FastAPI or Flask, with SQLite, PostgreSQL or Supabase | Not decided yet | The comparison is running. |
| Where this file lives | Committed, or local only | Committed to the repo root | It's backed up, and a fresh session gets it with one clone. It holds no prompts. |
| AI attribution lines | Keep, or remove | Removed | The owner's choice. |
| AI mention in the README | One line, or none | None | The owner's choice. |

## 6. Code guide

No application code yet.

## 7. Challenges

None yet.

## 8. Testing and demo

No tests or demo yet.

## 9. Session summaries

### Session 1, 4 November 2026

**Step 1.** The owner shared the brief and asked for a guided, step-by-step build, with the approach and documentation as the priorities. Claude checked the machine and GitHub, found a private, empty repo with admin access, and asked four questions.

**Step 2.** The owner chose one Job record, suggested FastAPI with PostgreSQL or Supabase while staying open to alternatives, set the branch and merge rule, and asked for summaries instead of prompts in this file. Claude proposed ten sections for this file and started comparing stacks with working prototypes in a scratch folder.

**Step 3.** The owner approved the ten sections and asked that current state, results, notes, the current step and the plan be included too. They also set today as the deadline, asked to remove the attribution lines, and asked to keep AI out of the README. They confirmed that each feature starts only after the previous one is merged, and asked for the minimal path with no temporary fixes, the best decisions with reasoning for each, and notes in this file at every step. Claude made the first commit.

The owner then asked whether Claude had missed the rest of that message. Claude had recorded most of it but not acknowledged it in its reply, and this file was missing the rule on notes at every step and the rule on best decisions. Claude added both.

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
