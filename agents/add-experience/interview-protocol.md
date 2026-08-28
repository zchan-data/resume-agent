# Interview Protocol

How to extract complete, specific, defensible facts from someone who will naturally
under-report what they did.

## Why this is hard

People describe their work in the vocabulary of their job, not the vocabulary of impact.
They say "I worked on the payments service" because that is how they described it in
standup for six months. They omit the hard parts because those felt normal at the time.
They round their contributions down out of modesty, or up out of anxiety, and both are
problems.

Your job is to convert lived experience into evidence.

## Rules of engagement

**Ask one question at a time.** A batch of six questions gets six shallow answers. A
single pointed question gets a real one, and the answer usually tells you what to ask
next. This is a conversation, not a form.

**Follow the energy.** When the user gives a longer or more animated answer, you have
found something that mattered to them. Dig there. That is usually where the strongest
accomplishment lives.

**Never accept the first answer to "what did you do".** The first answer is always the
job description. The second is usually the real work.

**Do not fill silence with your own guesses.** If you find yourself about to say "so
that probably improved performance by a lot, right?" — stop. Ask what happened instead.
Suggesting a number invites the user to agree with it, and now it is in the record and
neither of you knows if it is true.

**Say when you have enough.** Do not interview indefinitely. Three to five strong,
quantified accomplishments beats ten thin ones, because a one-page resume will never
have room for ten.

## The arc

### Phase 1 — Frame

Establish the container before its contents.

- What was the organization, and what does it actually do?
- What was the team responsible for?
- What was your title, and what were you actually hired to do? (These differ more often
  than people expect.)
- Start and end dates, in `MM/YYYY`.
- How big was the team? Who did you report to?
- Was this remote, hybrid, or onsite, and where?

### Phase 2 — Inventory

Get the full surface area before going deep on any one thing.

- What did you ship or produce? List everything, even small things.
- What did you work on that never shipped? (Often still resume-worthy — the technical
  work was real even if the product decision changed.)
- What broke, and what did you fix?
- What did you build that other people used or still use?
- What did you do that nobody asked you to do?
- What is the thing you are proudest of?
- What did you learn to do that you could not do before?

Let the user dump. Do not evaluate yet.

### Phase 3 — Deepen

Now pick the strongest three to five items and interrogate each one properly. For each:

**The problem.** What was actually wrong or missing before you started? Why did it
matter to anyone? Who was feeling the pain? This is what makes a result meaningful —
"reduced latency" means nothing without knowing latency was a problem.

**Your specific contribution.** What did *you* write, decide, or design, as distinct
from what the team did? If it was collaborative, what was your piece? Push politely
here: "when you say the team migrated the service, which parts did you personally
own?" This protects the user in interviews.

**The method.** What technology, algorithm, pattern, or approach? Why that one over the
alternative? What did you try first that did not work? Specificity here is what
separates a credible bullet from a generic one — `pg_stat_statements` and "partial
indexes" carry signal that "database optimization" does not.

**The scale.** How much data, how many users, how many requests, how many files, how
many services? Users chronically omit this and it is often the most impressive part.

**The outcome.** What was true afterward that was not true before? Then: how do you
know? What did you measure? Where would the number be recorded?

**The validation.** Did anyone use it, adopt it, merge it, cite it, or extend it? Did
it get you feedback, a mention, an award, a return offer? External validation converts
a homework assignment into a product.

### Phase 4 — Metric chase

For every accomplishment still missing a number, work `metric-playbook.md`. Do this as
a distinct pass so it does not get skipped in conversational drift.

If the user does not know a number, ask where it might be recorded before giving up:
a pull request description, a CI run, a Grafana or Datadog dashboard, an analytics
page, a commit history, a Slack message, a performance review, a demo recording, a
README, a course grading rubric. Most "unknowable" metrics are one lookup away.

It is completely fine to leave a record unquantified and come back. Say so explicitly:
"Leaving ACC-003 unquantified — if you can find the runtime in the CI logs later, tell
me and I'll update it."

### Phase 5 — Confirm

Play back what you understood in compressed form and ask the user to correct it. People
catch errors in a summary that they will not catch in a transcript. Specifically
re-confirm anything about scope of ownership and any number.

## Question bank

Use these when the conversation stalls. Prefer the specific over the general.

**When the answer was a job duty:**
- "That's what you were responsible for — what did you actually change while you were
  there?"
- "If you had not been on that team, what would be different today?"

**When the answer is vague about method:**
- "What did you reach for to do that, and why that instead of the obvious alternative?"
- "What was the hard part? What took longest?"
- "What did you try first that did not work?"

**When scale is missing:**
- "How much data was moving through that?"
- "How many people or systems depended on it?"
- "What would have happened if it went down?"

**When impact is missing:**
- "Who noticed when it was done?"
- "What could the team do afterward that they could not do before?"
- "Did anyone give you feedback on it?"

**For projects with no users:**
- "Did you deploy it anywhere? Did anyone besides you run it?"
- "How large was the dataset or problem space it handled?"
- "What was technically hardest about it, and what did you do about that?"

**For research:**
- "Was it published, presented, or cited? Where?"
- "What was the dataset size or experimental scale?"
- "What did you build to make the research possible?"

**For leadership or clubs:**
- "How many people, and what changed under you?"
- "What did you inherit versus what did you start?"
- "What was the before and after in numbers — attendance, budget, membership?"

## What to do about weak experiences

Some experiences genuinely are thin. Do not manufacture depth. Capture what is real,
mark it honestly, and tell the user plainly: "This one is thin as captured — it will
probably only earn a line on a resume unless we find a metric. That's fine; not
everything needs to be a headline."

An honest thin record is useful. A padded one poisons every resume that draws on it.
