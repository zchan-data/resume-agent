# Voice Rules

How to write prose that reads as though a person wrote it, because a person is going to
decide whether it did.

## Why this file is the important one

About 74% of recruiters report being able to identify an AI-generated application, and
roughly 80% of hiring managers hold it against the candidate when they spot one. Over
two-thirds say they can specifically spot it in cover letters. The penalty is not neutral:
a letter judged machine-written reads as low effort, and low effort reads as low interest.

That is the whole risk. The letter is not competing against other letters on quality. It
is competing against the reader's assumption that nobody wrote it.

Note the corollary, because it is the operating principle here: research on this is
consistent that AI-drafted content which has been genuinely edited, with specific details
and a real voice, is not reliably detectable and is received well. The problem is never
that a model helped. The problem is default register, generic content, and machine rhythm.
All three are fixable, and this file is how.

**Read this before writing the first sentence.** A draft written in default register and
then "humanized" still reads as processed. The tells live in structure and rhythm, not in
individual words, and you cannot substitute your way out of them afterward.

## The register

Write the way you would explain a project to a senior person you respect and have not met
yet. Not a friend, not a review board, and not a peer either. They know their own world
better than you do, and you are the one who asked for the meeting.

That asymmetry is real, and the letter reads better for acknowledging it quietly, in how
things are said, than loudly, in a paragraph about how honored the candidate would be. The
target still sits between stiff formality and inappropriate casualness, which is where
experienced technical writers live. It just sits nearer the formal end than a conversation
between equals would.

Concretely, and in contrast to the resume:

| | Resume | Cover letter |
| --- | --- | --- |
| First person | Banned | Correct. Use "I". |
| Contractions | Never | Yes. "I'd", "didn't", "it wasn't". |
| Sentence fragments | No | Sparingly. A fragment is emphatic, and accumulated emphasis reads as insistence. |
| Full sentences | No, bullets | Yes, prose. |
| Tone | Compressed, telegraphic | Direct, warm, unhurried |

**Unhurried is the load-bearing word.** A letter that clips every sentence to its shortest
possible form reads as impatient, and impatience reads as pressure on the reader. Leaving
room for a qualifying clause, a "for me", or an "as far as I could tell" costs three words
and changes how a whole paragraph sounds. Confidence does not require compression, and the
shortest version of a sentence is usually its most assertive version.

This interacts with §Rhythm, which asks for a short sentence in most paragraphs. Both hold.
A short sentence does not have to be a flat assertion: "That took two years to notice"
is six words and carries no swagger at all, while "The bug was scope" is four words and
is nothing but swagger.

Contractions are the cheapest single improvement available. Their absence is one of the
most reliable machine tells, because formal drafts expand every one of them by default.

## Confidence vs presumption

The table above says confident, and confident is easy to overshoot in a document whose
entire purpose is asking someone for something. The overcorrection has its own failure
mode, and it is worse than the servility it replaced. Servile reads as forgettable.
Entitled reads as someone who will be difficult to manage, and that thought is very hard
for a reader to un-have.

The line to hold:

> **Confidence is a claim about the work. Presumption is a claim about the reader.**

The test for any sentence: does it describe something the candidate did, built, or wants,
or does it describe something the reader needs, should do, or has already decided?

| Presumptuous | Confident |
| --- | --- |
| "I'd like to talk about where Systems Validation needs that kind of pressure-testing most." | "The repo is public if that kind of pressure-testing is useful to you." |
| "Four days a week on site suits me fine, and I can start whenever you need." | "Four days a week on site works for me, and I'm available from January." |
| "The dashboard is public, so you can check the work instead of taking my word for it." | "The dashboard is public, so the work is there to check." |
| "This is a measurement problem before it is a basketball one." | "The measurement side of that is what I'd want to spend a season on." |

Three patterns to watch, in order of how often they appear:

1. **Diagnosing their problem.** Naming a need the posting did not name, or telling them
   which category their real problem falls into. An outside candidate does not have the
   standing for this, and the reader knows their own team.
2. **Availability as terms rather than an answer.** "I can start whenever you need" sounds
   accommodating and reads as granting permission. State the fact and stop.
3. **Instructing the reader.** Telling them what to do with a link, or how to weigh what
   they just read.

**This is not license to reach back for the banned phrases.** "Thank you for your time and
consideration" is on the blacklist for being empty, not for being polite. Warmth with
content in it has always been fine and costs nothing: "Happy to talk whenever it's useful"
is warm, specific, and presumes nothing about whether they will.

The hiring decision is theirs. The letter's job is to make that decision easy, not to
write it for them.

## The blacklist

### Phrases that announce a form letter

Delete on sight, no rewriting, no salvaging:

- "I am writing to express my interest in"
- "I am excited to apply for the position of"
- "results-oriented professional", "results-driven", "proven track record"
- "detail-oriented team player", "self-starter", "go-getter"
- "innovative and dynamic team", "fast-paced environment"
- "leverage my skills", "utilize my expertise", "align with your mission"
- "I am confident that my skills and experience make me an ideal candidate"
- "I would welcome the opportunity to discuss"
- "Thank you for your time and consideration"
- "passionate about technology"

Roughly nine in ten AI-drafted cover letters contain several of these in the first two
paragraphs. A reader who has seen forty applications this week has seen every one of them
already today.

### Words that read as machine vocabulary

`leverage` (as a verb), `utilize`, `delve`, `robust`, `seamless`, `seamlessly`,
`cutting-edge`, `spearheaded`, `synergy`, `pivotal`, `underscore`, `resonate`,
`meticulous`, `keen eye`, `landscape` (figurative), `realm`, `tapestry`, `navigate`
(figurative), `foster`, `myriad`, `plethora`, `holistic`, `bespoke`, `elevate`,
`transformative`, `unwavering`, `testament to`.

Use `used`, not `utilized`. Use `led`, not `spearheaded`. Use `built`, not `architected a
robust solution`.

### Structures that give it away

- **"Not only X, but also Y."** Almost never written by a person in a letter.
- **The rule of three.** "Scalable, reliable, and maintainable." Two is human, three is
  generated. Allow at most one triad in the whole letter, and only if it is doing real
  work.
- **Perfect parallelism across paragraph openings.** If every paragraph starts with a
  participial phrase, or every one starts with "I", vary them.
- **"It's not just X, it's Y."**
- **Every sentence being grammatically complete and identically shaped.**
- **Em-dashes.** They have become a strong tell, and they are banned in this project
  anyway. Use commas, colons, parentheses, or a full stop.
- **Bold text scattered through body paragraphs.** A letter is prose, with no exceptions.
  If a sentence needs bolding to land, it is the wrong sentence.

### Enthusiasm that means nothing

"I'm excited about your innovative approach to solving complex problems." That sentence
fits every company that has ever existed, which is exactly why it fails.

Replace hollow praise with the specific reason, from `company-research.md`. The test: if
you can swap in a different company name and the sentence still works, it is not a reason,
it is filler. Cut it or make it specific.

Real reasons are often small and slightly odd. That is what makes them credible. "I have
been reading your postmortems since the routing outage writeup, mostly because I have
never seen a company publish that much detail about a bad week" beats any sentence
containing the word "mission."

## Rhythm

Machine-generated prose produces sentences of remarkably uniform length, usually 15 to 25
words each. The result is a flat, even cadence that a reader registers as wrong before
they can say why. Human writing swings. Short punch. Then a longer sentence that develops
the thought, qualifies it, and lands somewhere the short one could not reach.

Targets, and these are checkable:

- **Every paragraph contains at least one sentence under 8 words.**
- **The letter contains at least one sentence over 25 words**, so the range is real.
- **No three consecutive sentences within 3 words of each other in length.**
- **Do not start three consecutive sentences with the same word**, especially "I".

### The check

Run this on the draft. It prints each sentence's word count so a flat stretch is obvious.

```bash
python3 - "resumes/<slug>/cover-letter.md" <<'PY'
import re, sys, statistics
text = open(sys.argv[1]).read()
text = re.sub(r'^---.*?^---', '', text, flags=re.S | re.M)   # frontmatter
text = re.sub(r'^#.*$', '', text, flags=re.M)                # headings
text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)                 # bold
# keep only prose paragraphs: drop letterhead, dateline, salutation, sign-off
paras = [' '.join(p.split()) for p in re.split(r'\n\s*\n', text) if p.strip()]
paras = [p for p in paras if p.endswith(('.', '!', '?')) and len(p.split()) > 8]
sents = [s for p in paras for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
counts = [len(s.split()) for s in sents]
for n, s in zip(counts, sents):
    print(f'{n:3d}  {s[:70]}' + ('  <-- long' if n > 32 else ''))
print(f'\nsentences {len(counts)}  words {sum(counts)}  '
      f'mean {statistics.mean(counts):.1f}  min {min(counts)}  '
      f'max {max(counts)}  stdev {statistics.pstdev(counts):.1f}')
PY
```

The `word_count` in the draft's frontmatter should match the reported total plus the
salutation and sign-off, give or take. If it does not, update the frontmatter.

Read the column, not just the summary. A standard deviation above about 7 with a visible
mix of short and long lines is healthy. Everything clustered between 15 and 25 is the
machine signature, and it needs rewriting rather than word substitution.

## Transitions

Formal transitional adverbs are one of the most reported tells. Cut them:

`Furthermore`, `Moreover`, `In addition`, `Additionally`, `Consequently`, `Therefore`,
`Thus`, `Nevertheless`, `In conclusion`, `Overall`.

Replace with conversational connectors, or with nothing at all:

- "Here's what I mean."
- "Because of this,"
- "So,"
- "But"  (starting a sentence with But is fine and always has been)
- "That's the part that"
- "The short version is"

Most of the time the sentence works better with the transition simply deleted. Human
paragraphs connect by content, not by signposting.

## Show, don't tell

"Excellent problem-solving skills" and "highly motivated fast learner" are assertions with
no evidence attached, and an engineering reader discounts both automatically.

Replace every trait claim with a micro-story: one or two sentences of a specific technical
process and its specific outcome.

| Telling | Showing |
| --- | --- |
| "I have strong debugging skills." | "There was no error and nothing to grep for, so I read the contracts by hand until the pattern showed up." |
| "I learn new technologies quickly." | "I had not written R before that quarter and had an ARIMA model fit and residual-validated by the end of it." |
| "I collaborate well with non-technical stakeholders." | "The staff needed a pitcher's count-by-count tendencies as one line they could act on during a game. Not as a distribution." |

The rule is mechanical: if a sentence describes a quality the candidate has, either attach
the evidence or delete the sentence.

**The evidence has to come from a record.** This is where invented detail gets in, because
a micro-story wants a texture that the structured fields do not carry, and inventing one is
easy and feels harmless. It is not harmless: it is a fabrication about the user, and it is
the kind they get asked to elaborate on. Every specific in a micro-story traces to `X`,
`Y`, `Z`, `scale`, `context`, or the raw notes. If the texture you want is not there, use
the texture that is.

## The imperfect moment

Perfect narratives read as constructed, because they are. One honest mention of a real
hurdle, a wrong first guess, a slow stretch, or an unplanned pivot does more for
credibility than another accomplishment. It is also the thing current models are worst at
producing, precisely because it requires a fact rather than a shape.

**The constraint that makes this safe: the imperfect moment must come from a record.** Read
the accomplishment's `### ACC-NNN notes` in `## Narrative`, its `role` and `origin`
fields, the raw notes, and the open metric opportunities. Real friction is already
captured there. Do not invent a struggle for
texture. An invented failure is still a fabrication, and it is the kind the user will be
asked to elaborate on in an interview.

Sources of genuine imperfection already in this system, as examples of what to look for:

- Diagnosis that took manual, unglamorous work before the pattern appeared
- A hypothesis the record explicitly marks as untested
- An approach that was handed down rather than chosen, where the interesting decisions
  were in the parts left open
- A measurement that had to be re-run, or a result the user knows is not yet solid

One such moment per letter. Two starts to sound like hedging, and the letter is still an
argument for hiring the candidate.

Keep it brief and keep it resolved. "The first version was wrong and here is how I found
out" is confidence. "I struggled with this project" is not.

## Do not overcorrect

Humanizing is not sloppiness. The letter still needs correct grammar, correct spelling,
correct company name, and a clean line of argument. Do not manufacture typos, do not
ramble, do not get cute, and do not open with a joke.

The goal is a letter that reads like a competent person wrote it in twenty minutes and
meant it. Not one that reads like a first draft.

## Audit checklist

Run every item against the finished draft before showing the user anything. Every letter
fails something on the first pass.

**Content**

- [ ] Every company fact traces to a line in `company-research.md`
- [ ] Every number appears in an experience record, verbatim
- [ ] No claim contradicts `resume.md`
- [ ] No sentence is a reworded resume bullet
- [ ] Verbs match the `origin` field of the record they describe
- [ ] The reason for wanting this company would not survive a company-name swap

**Voice**

- [ ] Zero phrases from the blacklist
- [ ] Zero words from the machine vocabulary list
- [ ] Zero formal transitional adverbs
- [ ] At least two contractions
- [ ] No em-dashes
- [ ] No "not only... but also", at most one triad
- [ ] Paragraph openings vary, no three consecutive sentences starting with "I"
- [ ] Every trait claim has evidence attached, or is gone
- [ ] Exactly one imperfect moment, sourced from a record
- [ ] No sentence diagnoses the reader's problem, sets a term of the arrangement, or tells
      them what to do with the letter. See §Confidence vs presumption

**Rhythm**

- [ ] Sentence-length check run
- [ ] At least one sentence under 8 words per paragraph
- [ ] At least one sentence over 25 words in the letter
- [ ] No three consecutive sentences within 3 words of each other

**Final**

- [ ] Read it aloud. Anywhere you stumble, run out of breath, or hear a sentence you would
      not say out loud, rewrite that sentence.
