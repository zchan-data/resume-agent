# Resume Agent System

A folder-and-markdown agentic system for capturing career experience and generating
tailored, ATS-safe resumes. This file is the router: it tells you which agent handles
a request and where the data lives.

## Routing

When a request matches a row below, **read that file and follow it before doing
anything else.** Do not improvise from this table alone — it names the agent, but the
agent's own file holds the procedure, and skipping it produces work that ignores the
research these agents are built on.

| The user wants to... | Read and follow |
| --- | --- |
| Log a job, internship, project, research, club, or anything they did | `agents/add-experience/SKILL.md` |
| Add detail or metrics to something already captured | `agents/add-experience/SKILL.md` |
| Turn a job description into a tailored resume | `agents/tailor-resume/SKILL.md` |
| Edit or re-render a resume already generated | `agents/tailor-resume/SKILL.md` |
| Write a cover letter or letter of interest for a role | `agents/write-cover-letter/SKILL.md` |
| Write a cold email to a hiring manager or recruiter | `agents/write-cover-letter/SKILL.md` |
| Edit or re-render a cover letter already generated | `agents/write-cover-letter/SKILL.md` |

Natural-language triggers that should route to **add-experience**: "I want to add my
internship", "let me tell you about a project", "I did X this summer", "I have more
details about Y", "log this".

Natural-language triggers that should route to **tailor-resume**: pasting a job
description, "make me a resume for this", "tailor my resume", "apply to X".

Natural-language triggers that should route to **write-cover-letter**: "write a cover
letter", "they want a cover letter too", "email the hiring manager", "reach out to this
recruiter", "why do I want to work here".

If the request is ambiguous, ask which one rather than guessing. The agents write to
different places and a wrong guess corrupts data.

**tailor-resume and write-cover-letter share an application folder.** Both write into
`resumes/<YYYY-MM-DD>-<company-slug>-<role-slug>/`, and the cover letter agent reuses the
`match-analysis.md` the resume agent produced. If the user asks for both, run
tailor-resume first: the job-description analysis is the expensive part and the letter
agent should not redo it.

## Where things live

```
agents/           The agents themselves. Each folder is one agent.
profile/          Who the user is. Contact, education, skills inventory.
experiences/      The evidence base. One file per experience + INDEX.md.
resumes/          One folder per application. JD, analysis, drafts, outputs.
                  Cover letters live here too, alongside the resume they accompany.
templates/        Typst styling modules, one per document type.
research/         Source research the rules are derived from. Read-only reference.
scripts/          Section reader and consistency checks. Not part of any agent.
```

**Experience records are split in two.** `## Claims` holds the structured facts and every
prohibition, and is what retrieval reads. `## Narrative` holds prose and is read only for
an accomplishment already selected. See `agents/add-experience/record-schema.md`
§The two halves of a record.

`experiences/INDEX.md` is the retrieval entry point. Always read it before opening
individual experience files.

### How agents are structured

Every agent is a folder under `agents/` containing a `SKILL.md` entry point plus the
rule files it loads on demand. There is no framework and nothing hidden — an agent is a
folder of markdown, and routing to one means reading its `SKILL.md` and following it.

Load rule files at the step that needs them rather than all at once. `SKILL.md` says
when to read each one. This keeps a small task from pulling every rule file into context.

Each `SKILL.md` opens with a **contract table**: one row per step, naming what that step
reads and writes. Reads are scoped to sections, written as `` `<file>.md` §<Heading> ``.
Read the sections named, not the whole file — most of a rule file does not apply to the
step citing it. Where a step deliberately skips a section, the contract says so and why.

**Section scoping is only real if you use the tool for it.** `Read` loads a whole file,
so a contract row naming two sections of an eight-section rule file costs the same as
ignoring the contract. Use:

```bash
python3 scripts/read-section.py -s "The bullet formula" -s Mechanics \
    agents/tailor-resume/writing-rules.md
```

It accepts several files at once, which is how experience records should be read:
`-s Claims experiences/jobs/*.md` returns the claim blocks for every shortlisted record
and none of their prose. `--list <file>` shows the available headings. It exits nonzero
on a heading that does not exist, so a rename fails loudly instead of silently widening
the read.

Two notations, deliberately: `§<Heading>` cites a **rule file**, and
`scripts/check-section-refs.py` validates every one of those citations against the file
named. Experience records are cited with a plain `` `## Claims` `` instead, because they
are data enumerated at runtime rather than a fixed set of rule files, and the checker has
nothing stable to validate them against.

`agents/write-cover-letter/voice-rules.md` is the one file exempt from section routing.
It is read whole, every time. Its failure mode is cumulative: a letter can satisfy every
individual rule you happened to load and still read as machine-written.

**When you edit an experience record, run `python3 scripts/check-claims.py`.** It verifies
that every accomplishment declares a `claim`, that `restricted` and `blocked` ones say
what is off limits, and that no `default_bullet` repeats a figure its own `do_not_claim`
names. That last case is not hypothetical: it shipped in this repo before the fields
existed, in a record whose prose warned against the exact number sitting in its bullet.
It exits nonzero, so it works as a pre-commit hook.

**When you rename a heading in a rule file, run `python3 scripts/check-section-refs.py`.**
Every `§<Heading>` citation is a cross-file dependency that nothing else enforces, and a
stale one fails open — the agent quietly reads the whole file instead of the section it
was scoped to, which is invisible in the output. The script also catches a real heading
cited against the wrong file. It exits nonzero, so it works as a pre-commit hook.

**To add an agent later:** create `agents/<name>/SKILL.md` with a contract table, add a
row to the routing table above, and add its natural-language triggers to the list below.
Nothing else needs to change.

`experiences/INDEX.md` is the retrieval entry point. Always read it before opening
individual experience files.

## Versioning the career data

`experiences/`, `profile/`, and `resumes/` are gitignored here on purpose: this repo
tracks the workflow, and anyone cloning it supplies their own data. They are versioned
separately, by a second repo that shares this working tree:

```bash
git --git-dir=.git-private --work-tree=. status
git --git-dir=.git-private --work-tree=. log --oneline
```

Worth setting `alias gitp='git --git-dir=.git-private --work-tree=.'` in your shell.

**Commit to it after any change to those three directories** — a captured experience, an
updated skills inventory, a rendered application. Nothing does this automatically, and a
change left uncommitted there is invisible to the history that exists to protect it.

Two things about it that will bite otherwise:

- **New files need `add -f`.** The working tree carries this repo's `.gitignore`, which
  lists all three directories, and a shared working tree cannot opt out of it. Only
  untracked files are affected, so once a file is committed its later edits stage
  normally. Check what you are forcing: `-f` overrides `.git-private/info/exclude` too,
  which is how a `.DS_Store` got in once.
- **It tracks PDFs.** `*.pdf` is ignored in this repo but not there, deliberately: the
  rendered resume and letter are the deliverables and are worth keeping.

If `.git-private/` does not exist, this machine has no data history and nothing depends
on it. Say so rather than creating one uninvited.

## System-wide invariants

These hold for every agent, now and as the system grows.

1. **Never invent a fact about the user.** No metric, date, title, technology, or
   outcome may appear anywhere unless the user supplied it. If a number would strengthen
   a bullet and you do not have one, ask for it or write the bullet without it. This is
   not a stylistic preference — a fabricated number becomes a lie the user has to defend
   in an interview.
2. **Never invent a fact about the company either.** Funding rounds, product names, blog
   posts, hiring manager names. This applies wherever a document references an employer,
   and it is the failure mode specific to cover letters and outreach. Unlike a soft
   resume claim, the reader will catch it instantly, because it is their own company.
   Every company claim traces to a source recorded in the application folder.
3. **Never write to `experiences/` from a document-generating agent.** Experience records
   are the source of truth. Resume and cover letter generation read them and write only
   into `resumes/`. If a missing fact surfaces, tell the user and offer to run
   add-experience.
4. **Generated output is single-column, text-only.** No tables, text boxes, images,
   icons, or multi-column layouts in anything that becomes a PDF. See
   `agents/tailor-resume/format-rules.md` and
   `agents/write-cover-letter/format-rules.md` for why.
5. **Stop at the draft.** `resume.md` and `cover-letter.md` are approval gates. Never
   render a PDF without the user seeing and approving the markdown first.
6. **Preserve user edits.** If the user has hand-edited a draft, never regenerate it from
   scratch without asking. Re-render from their version.
7. **Cite the source of every metric.** Records carry a `source` field. "PR #204",
   "CI log", "manager's review doc", so a claim can be re-verified later.
8. **A `do_not_claim` field is binding on every agent.** Experience records carry
   prohibitions as fields, at the accomplishment level and experience-wide. They are read
   on every retrieval and they override anything a headline, a `default_bullet`, or a job
   description makes attractive. A prohibition exists because the claim is *true but not
   defensible* — a leaked metric, an unauthored implementation, an unmeasured effect —
   which is exactly the kind of claim that survives a plausibility check and fails an
   interview. If one blocks evidence a role needs, report the gap; never route around it.
9. **Anything the user sends must sound like a person wrote it.** Prose documents are
   read by someone who can recognize machine-generated writing and will discount the
   application for it. See `agents/write-cover-letter/voice-rules.md`, which is binding
   for every prose deliverable this system produces, current and future.

## Conventions

- Dates are `MM/YYYY` everywhere, including inside experience records. Ongoing work uses
  `Present` as the end date. One deliberate exception: the dateline on a cover letter is
  written out in full (`August 20, 2026`), because a numeric dateline on a letter reads
  as a generated document.
- Experience IDs are `exp-<org-slug>-<year>`. Accomplishment IDs are `ACC-NNN`, unique
  within their experience file.
- New files use kebab-case names.
- When a skill needs a rule file, read it at that step rather than loading everything up
  front.

## Not yet built

GitHub and job finder agents are planned but do not exist. If the user asks for one, say
so rather than improvising. Improvised output would not follow the research these agents
are built on.
