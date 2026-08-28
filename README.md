# Resume Agent

A folder-and-markdown agentic system for capturing career experience and generating
tailored, ATS-safe resumes and cover letters from it.

There is no framework here and nothing hidden. An agent is a folder of markdown that a
coding agent reads and follows. The interesting part is not that it writes resumes; it is
the constraints that keep it from writing things that are not true.

## The problem it solves

A language model asked to write a resume will produce plausible numbers. That is the
failure mode, and it is worse than a bad resume, because a fabricated metric becomes
something you have to defend in an interview.

So the system separates two things that are usually conflated:

- **What is true.** Captured once, in structured experience records, from an interview
  that pushes for sources.
- **What is defensible.** A subset. A metric can be real and still unusable, because the
  methodology was flawed, or the work was not yours, or nobody actually measured the
  effect you want to claim.

Every record carries prohibitions as **fields**, not prose. They are read on every
retrieval and they override anything a job description makes attractive.

## Three design decisions worth stealing

**1. Records are split into a retrieval head and a prose tail.**

`## Claims` holds structured facts and every prohibition. `## Narrative` holds prose.
Retrieval reads several records and uses a fraction of each, so storing them interleaved
means paying for prose you will not read. Splitting them cut characters on the retrieval
path by 47.8% on the author's own data.

**2. Every step declares what it may read.**

Each agent opens with a contract table naming the exact sections each step loads, written
as `` `<file>.md` §<Heading> ``. Rules load at the step that needs them rather than all at
once.

Section scoping is only real if you use a tool for it, so there is one:

```bash
python3 scripts/read-section.py -s "The bullet formula" -s Mechanics \
    agents/tailor-resume/writing-rules.md
```

It takes many files at once, and it **exits nonzero on a heading that does not exist**.
Without that, a renamed heading fails open: the agent silently reads the whole file
instead of the section it was scoped to, and nothing in the output reveals it.

**3. The guardrails are checked, not documented.**

```bash
python3 scripts/check-claims.py        # prohibitions are declared and self-consistent
python3 scripts/check-section-refs.py  # every §Heading citation resolves
```

Both exit nonzero, so both work as pre-commit hooks.

`check-claims.py` verifies that every accomplishment declares a claim status, that
restricted and blocked ones say what is off limits, and that **no ready-made bullet
repeats a figure its own prohibition names**. That last rule is not hypothetical. It
exists because a record shipped in this repo whose prose warned against the exact number
sitting in its own bullet. The caveat was written down. It was in a section retrieval does
not read, so it did nothing.

That is the general lesson, and it is the reason for the head/tail split: **a guardrail in
the wrong location is not a guardrail.**

## Layout

```
agents/           One folder per agent. SKILL.md is the entry point.
  add-experience/       Interview the user, capture structured records
  tailor-resume/        Job description in, tailored resume out
  write-cover-letter/   Cover letters and cold outreach
profile/          Contact, education, skills inventory          (not included)
experiences/      The evidence base, one file per experience    (not included)
resumes/          One folder per application                    (not included)
templates/        Typst styling, one module per document type
research/         Source research the rules derive from
scripts/          Section reader and the two checkers
```

`CLAUDE.md` is the router: it maps a request to the agent that handles it.

**The three data directories are gitignored on purpose.** This repo tracks the workflow;
anyone using it supplies their own career data. `experiences/_template.md` shows the
record format.

## Using it

Clone it, open the directory with an agentic coding tool that reads `CLAUDE.md`, and say
what you want:

- "I want to log my internship" routes to add-experience
- Pasting a job description routes to tailor-resume
- "Write a cover letter for this" routes to write-cover-letter

Rendering to PDF needs [Typst](https://github.com/typst/typst). The agents stop at the
markdown draft and wait for approval before rendering anything.

## Non-negotiables

These hold for every agent:

1. Never invent a fact about the user. No metric, date, title, or outcome that the user
   did not supply.
2. Never invent a fact about the company either. This is the failure mode specific to
   cover letters, and the reader will catch it instantly, because it is their own company.
3. Document-generating agents never write to `experiences/`. Records are the source of
   truth.
4. Output is single-column and text-only. No tables, text boxes, images, or icons in
   anything that becomes a PDF.
5. Stop at the draft. Never render a PDF without the user approving the markdown first.
6. A `do_not_claim` field binds every agent. If it blocks evidence a role needs, report
   the gap; never route around it.

## License

MIT
