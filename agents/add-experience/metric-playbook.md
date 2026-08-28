# Metric Playbook

What number to chase, by domain — and what to do when no business metric exists.

## The hard rule

You may only record a number the user supplied. Never estimate, never infer, never
offer a plausible figure for the user to confirm. Anchoring is real: a user shown "so
roughly 40%?" will often agree to a number they have never measured, and it ends up on
a resume they have to defend.

The correct move when a number is missing is to help the user **find** it, not to
supply it.

## Where numbers hide

Before concluding a metric is unknowable, ask the user to check:

| Source | Yields |
| --- | --- |
| Pull request title/description | Before/after benchmarks, scope of change |
| CI run history | Build and test runtimes |
| Grafana / Datadog / CloudWatch | Latency, throughput, error rate, uptime |
| Analytics dashboard | Users, sessions, conversion, retention |
| `git log --stat`, repo insights | Files changed, commits, contributors |
| Cloud billing console | Cost before/after |
| Performance review or self-review | The impact framing the user already wrote |
| Slack or email threads | "This cut our runtime in half" said at the time |
| README or project docs | Dataset size, supported scale |
| Course rubric or project spec | Required scope, dataset size |
| App store / package registry | Downloads, installs, stars |

Most metrics people call unknowable are one lookup away. Ask before accepting a gap.

## Domain-specific targets

Chase the metrics that the target audience for that domain actually cares about.

### Backend and distributed systems
Latency (average, p95, p99 — prefer p95/p99, they signal production maturity),
throughput in requests/second, error rate reduction, database query execution time,
queue depth or lag, cache hit rate, compute cost reduction, records processed,
concurrent users supported, uptime.

### Frontend and UI
Core Web Vitals (Largest Contentful Paint, Interaction to Next Paint, Cumulative Layout
Shift), initial bundle size, Time to Interactive, render time, conversion rate, bounce
rate, accessibility compliance level reached (WCAG A/AA/AAA), number of components or
screens shipped, browser/device coverage.

### DevOps, infrastructure, SRE
Mean Time to Detection, Mean Time to Recovery, deployment frequency, deployment
rollback rate, CI/CD pipeline duration, infrastructure provisioning time, uptime
against SLA, incident count reduction, cloud spend reduction, number of services or
environments managed.

### Data and machine learning
Dataset size (rows, GB, records), model accuracy/precision/recall/F1 and the baseline
it beat, training time, inference latency, pipeline runtime, data freshness or lag,
number of features or sources integrated, cost per training run.

### Security
Vulnerabilities found or remediated and their severity, time-to-patch, coverage of
scanned surface, reduction in attack surface, compliance standard achieved, incidents
prevented.

### Product and program
Revenue or cost impact, adoption rate, user growth, feature usage, cycle time
reduction, number of stakeholders or teams coordinated, roadmap items shipped.

## Scope-and-scale proxies

When the user has no access to business metrics — which is normal for students,
interns, and personal projects — quantify the *inputs and scope* instead of the
outcome. This is a legitimate technique, not a consolation prize: it demonstrates the
size of the problem the user handled.

Reach for:

- **Volume handled** — rows, records, files, GB, images, documents, transactions
- **Surface built** — endpoints, components, screens, models, services, tables, tests
- **Reach** — users, teammates, classmates, downloads, stars, club members
- **Time** — hours saved per week, manual steps eliminated, runtime reduced
- **Scope** — courses, datasets, integrations, data sources, supported platforms
- **Adoption** — who else used it, and whether it is still in use
- **Comparison** — beat a baseline by how much, ranked where in a cohort or competition

Example of the difference:

> Weak: Built a web application for my senior project.
>
> Strong: Built a course scheduling optimizer (React, Flask, PostgreSQL) generating
> conflict-free schedules across 200+ courses — adopted by the CS department advising
> office for Fall 2025 registration.

No business metric appears. The bullet works because it names the stack, quantifies the
problem space, and proves real adoption.

## When there is genuinely no number

Some real accomplishments resist quantification — a refactor that unblocked a team, a
design document that changed a decision, a debugging session that found a root cause.
These are legitimate.

Record them with `verified: false` and no `Y` field. Write the default bullet with the
strongest available substitute for measurement:

- **Named difficulty** — "diagnosed a race condition surfacing only under concurrent
  writes"
- **Named consequence** — "unblocking the team's migration to the new schema"
- **Named validation** — "adopted as the team's standard approach"
- **Named specificity** — precise technology and method, which itself signals depth

Do not pad these with vague intensifiers. "Significantly improved" and "greatly
enhanced" are weaker than a plain factual statement, because a reader discounts
adjectives and trusts specifics.

## Recording

Every metric gets a `source` field naming where it came from: `PR #204`,
`CI log 2025-07`, `Datadog dashboard`, `manager's review`, `user's direct recollection`.

`user's direct recollection` is acceptable and honest — it flags to future-you that
this one was never verified against a system of record, which matters if the user is
about to walk into an interview and be asked about it.
