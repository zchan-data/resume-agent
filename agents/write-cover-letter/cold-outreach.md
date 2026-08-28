# Cold Outreach

Writing the email that goes directly to a hiring manager, engineering lead, or founder
instead of through the portal.

## When this is the right move

Direct outreach bypasses the ATS entirely, which is why it works. It is most effective at
startups and small teams where the person reading the email has hiring authority, and least
effective at large enterprises where everything routes back to a recruiting queue.

Use it when:

- The company is small enough that the decision-maker is reachable
- The user has a real connection, a referral, or a genuine technical reason to write
- The portal application is already in and has gone quiet
- The role is a strong fit and the applicant pool is likely enormous

This is a different document from a cover letter, not a shortened one. The reader is not in
review mode. They are in inbox mode, on a phone, deciding in two seconds whether to keep
reading. Everything below follows from that.

## Length

**120 to 175 words in the body.** Shorter than a cover letter by half.

The single most common failure is pasting a cover letter into an email. It arrives as a
wall of text and gets archived unread.

## Structure

Attention, interest, desire, action. Four short moves.

### Subject line

The highest-leverage sixty characters in the whole system. Vague or formal subjects get
ignored or filtered.

Working patterns:

- A referral, if one exists: `Referred by <name> re: <role>`
- A specific question about their work: `Question about how <company> handles <specific thing>`
- Concrete self-description tied to the team: `<Specific skill> engineer interested in your <specific team>`

Avoid: `Job Application`, `Seeking Opportunities`, `Experienced Data Analyst Available`,
anything with an exclamation mark, anything in title case that reads like a press release.

Never write a subject line implying a prior relationship that does not exist. It gets the
email opened once and destroys the sender's credibility on the same click.

### 1. The opener, one or two sentences

Must prove within the first line that this is not a mass send. Reference a specific thing:
something they shipped, a talk they gave, a post they wrote, a nuanced observation about
their product. Straight from `company-research.md`.

If the research turned up nothing specific about this person or team, do not send the email.
Send the portal application instead. A cold email with a generic opener is worse than no
email, because it consumes the one chance to reach that person directly.

### 2. Problem and solution alignment, two or three sentences

Connect the user's background to something the team is actually working on. One
accomplishment, one number, no list.

> You mentioned scaling the ingestion pipeline in the post. I spent this summer on
> something adjacent: a nightly warehouse sync that reported success every run while
> quietly dropping about one order in fifty. Tracking that down and rebuilding the
> incremental cursor took row loss to zero.

### 3. The ask, one sentence

Low friction. The goal is a reply, not an offer. Asking for a job puts the recipient in a
position where the easiest answer is silence.

Good:

- "Would you be open to a fifteen-minute call in the next couple of weeks?"
- "Is there someone on the team it would make more sense to talk to?"
- "Happy to send the repo if it's useful. Is it worth applying through the posting, or is
  there a better path?"

Bad:

- "I would love the opportunity to interview for this position."
- "Please review my attached resume and let me know about next steps."
- Anything that asks the recipient to do work before they have decided to engage.

### 4. Signature

Name, one line, one link. The most clickable artifact the user has. Not four links.

## Attachments

Do not attach a resume to a first cold email. Attachments from unknown senders trip spam
filters and read as a mass application. Link to the portfolio or repo instead, and send the
resume when they reply.

## Voice

`voice-rules.md` applies in full and matters more here, because an email is where formal
register looks most obviously wrong. Nobody writes "I am reaching out to express my
interest" to a colleague.

Email-specific:

- Lowercase, conversational subject lines usually outperform formal ones
- Contractions throughout
- No salutation more elaborate than `Hi <first name>,`
- No signature block with a title the user does not have
- One idea per paragraph, and paragraphs of one to three sentences. Long paragraphs are
  unreadable on a phone

## Follow-up cadence

Silence is almost never rejection. It is workload. A multi-stage sequence roughly doubles
response rates over a single message.

- **First follow-up: 3 to 5 business days.** Short, in the same thread, no guilt. Restate
  the value in one sentence and add something new: a project that shipped since, a relevant
  article, an update.
- **Second follow-up: 7 to 10 business days after that.** Shorter still. Two sentences.
- **Then stop.** Two follow-ups is persistence. Three is a problem, and the tech world is
  small.

Never mention how long it has been or that a previous email went unanswered. "Following up
on my email from last week" reads as an accusation. Lead with the new thing instead.

## Output

Write `outreach-email.md` in the application folder:

```markdown
---
to: <name>, <title>
found_via: <source>
subject: <subject line>
word_count:
followup_1_due: <date, 3-5 business days out>
---

Subject: <subject line>

Hi <first name>,

<body>

<name>
<one link>
```

Record the follow-up date. The user will not remember, and the follow-up is where half the
value of this whole approach lives.

Do not send anything. Give the user the text and let them send it from their own account.
