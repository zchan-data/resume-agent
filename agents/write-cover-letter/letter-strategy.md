# Letter Strategy

Choosing the format, and the paragraph architecture that follows from it.

## The two formats

| Format | Use when | Advantage | Risk |
| --- | --- | --- | --- |
| **Standard Narrative** | Default. Portal applications, structured ATS, large companies, entry level through mid. | Universally accepted. Room for a real story and for fit. | Degenerates into boilerplate the moment it stops being specific. |
| **Pain Letter** | Startups and scale-ups, cold outreach, a role that clearly exists because something is on fire, and you have real research to hypothesize from. | Demonstrates business judgment. Reads as a peer rather than an applicant. | Presumptuous or plain wrong if the pain hypothesis misses. Requires research you actually did. |

Choose one and record the choice and the reason in the draft's frontmatter. If it is a
close call, default to Standard Narrative. It never actively hurts, and the Pain Letter
can.

**A checklist posting is still a Standard Narrative.** The instinct to answer a rigid
requirements list point by point is the situation a T-Chart used to serve, and this system
no longer offers one. Map the requirements in `match-analysis.md` instead, then write
prose that hits the ones the records genuinely support. The resume already answers the
checklist; a letter that answers it a second time spends its only real advantage, which is
showing how the candidate thinks.

## Standard Narrative

Three or four paragraphs. Roughly 250 to 350 words total.

### Paragraph 1 (the hook), 2 to 4 sentences

Three jobs, in whatever order reads best:

1. Name the specific role.
2. Land one concrete, sourced company detail from `company-research.md`.
3. State one highly relevant thing the candidate has actually done.

Banned openers, all of which announce a form letter before the reader reaches the verb:

- "I am writing to express my interest in..."
- "I am excited to apply for the position of..."
- "As a passionate and results-driven..."
- "When I saw your posting for..."
- Anything that opens with the candidate's degree.

The strongest opening sentence usually starts with the company or with the work, not with
"I". Get to something the reader did not already know within two sentences.

### Paragraph 2 (the proof), 4 to 6 sentences

One accomplishment, in depth. Not a list.

The shape: what the problem was, what was tried or decided and why, the number that came
out the other end. The "why" is what a resume bullet cannot hold and what this paragraph
exists for. A reader learns more from one honest sentence about why an approach was
chosen over the obvious alternative than from four more accomplishments.

Every technical claim carries a number if the record has one. If the record has no
number, the paragraph stays unquantified rather than acquiring an invented one, and you
lean harder on the specificity of the method. See `story-selection.md`.

### Paragraph 3 (fit), 3 to 5 sentences

Two things, woven rather than sequential:

- A second, shorter piece of evidence, or how the candidate works: collaboration,
  reviewing, handing work off, learning an unfamiliar system fast.
- Why this company specifically. Not why the industry. Not why the mission is inspiring.
  This is where the user's own stated reason from `company-research.md` goes, in
  something close to their own words.

This is also the natural home for the imperfect moment described in `voice-rules.md`.

For a new grad or career changer, this paragraph does real work: it is where the letter
addresses the obvious objection without ever naming it defensively.

### Paragraph 4 (close), 2 to 3 sentences

Short. Point at one artifact worth clicking (a repo, a published dashboard, a live
project), and answer availability if the posting raised it. Answer it, do not negotiate
it: "I'm available from January" is an answer, "I can start whenever you need" is a
concession nobody asked for.

Banned: "Thank you for your time and consideration." "I look forward to hearing from
you." "I would welcome the opportunity to discuss how my skills can contribute to your
team's continued success."

The close should sound like someone who would be glad to hear back, not someone who is
owed a reply. Confidence belongs in the paragraph about the work; by the sign-off the
argument is already made, and a closing line that pushes reads as pressure.

Do not fix this by reaching back for the banned phrases above. They are banned for being
empty, not for being warm. See `voice-rules.md` §Confidence vs presumption for the
distinction and for what warmth with content looks like.

## Pain Letter

Four moves, tight. This format is short, usually under 250 words.

1. **The hook.** A specific, recent, sourced accomplishment of theirs. Proves you are
   watching the business, not just the job board.
2. **The pain hypothesis.** One sentence naming a plausible consequence of that growth or
   change. Frame it as a hypothesis, because it is one: "which probably means X is now
   harder than it was" rather than "your X is broken."
3. **The dragon-slaying story.** Two or three sentences on a time the candidate solved
   that exact class of problem, with the number.
4. **The offer.** Propose a short conversation about the specific problem. Not a job
   request.

Do not use this format without real research. A wrong hypothesis stated confidently reads
as arrogance from someone who did not do the reading, which is the exact opposite of the
impression the format is designed to create.

Hedge the hypothesis honestly. "I might be wrong about where the bottleneck actually is"
costs one clause and converts presumption into curiosity.

## Weighting by career stage

Read `profile/identity.md` for the current stage.

**Entry level and new grad.** Lean on projects, internships, and coursework-adjacent work
as real evidence. The thing being demonstrated is not seniority, it is judgment: explain
why an approach was chosen over the alternative, what the tradeoff was, what the
measurement showed. Junior candidates who reason about their decisions read as far more
senior than junior candidates who list technologies. Mention learning speed by showing it
happening, never by claiming to be a fast learner.

**Mid level.** Balance shipped production impact against ownership. Show a problem taken
from ambiguous to measured.

**Senior and above.** Drop coursework and tool lists entirely. System design, scale,
reliability, cross-functional work, mentorship. The reader assumes the candidate can code;
the letter must prove they can decide.

## Weighting by role type

**Data science.** Tools are table stakes. The letter must show the analysis connecting to a
decision somebody made. "Built a churn model with XGBoost" is weak. "Built a churn model
that flagged at-risk accounts early enough for the retention team to act, and here is what
it caught" is the whole game. Statistical rigor belongs in the letter too: how the result
was validated, what could have made it wrong.

**ML engineering.** Shift back toward software engineering. Deployment, latency, monitoring,
what happens when the model is wrong in production, automated checks. Model choice matters
less than the machinery around it.

**Backend, infra, platform.** Systems, failure modes, scale figures, what broke and what
was done about it. Debugging stories are strong here, especially with a real diagnosis.

**Career changer.** Never apologize and never write "while I lack traditional experience."
Frame the prior career as a genuine asset and then translate it into the target field's
vocabulary: not "managed a classroom" but "ran performance tracking and delivered training
against measured outcomes." Then prove current technical competence fast, in the first half
of the letter, with concrete recent work. The letter's job is to remove the reader's doubt
before they finish paragraph two.
