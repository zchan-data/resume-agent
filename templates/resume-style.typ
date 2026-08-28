// Shared resume styling. Generated resumes import this and contain content only.
//
// Design constraints (see .claude/skills/tailor-resume/format-rules.md):
//   - Single column. No grid, table, or absolute positioning anywhere, so the PDF
//     text layer extracts in strict linear reading order.
//   - Right-aligned dates use #h(1fr) inside a normal paragraph, which stays linear
//     under extraction, unlike a two-cell grid.
//   - Standard fonts only, to avoid character substitution during parsing.

// Toggle: thin rule under section headings. Aids the F-pattern scan; some
// institutional guidance prefers no rules at all. Set to false to remove.
#let SECTION_RULE = true

// Toggle: how dates and locations are placed in an entry.
//
//   false (default) - right-aligned on the org/title lines. This is what recruiters
//     expect: eye-tracking shows they saccade to the right margin to check dates.
//     Cost is that a stream-order PDF text extractor may emit the right-aligned runs
//     after the entry's bullets rather than beside the org, because a wide whitespace
//     gap reads to a naive extractor like a column boundary.
//
//   true - dates and locations run inline after the org and title. Strictly linear in
//     every extraction mode, at the cost of the right-margin date scan.
//
// Default is false: position-aware parsers (the majority) handle right alignment
// correctly, and the human scan pattern is worth more than the residual risk.
// Flip to true when applying through a known-strict parser such as Workday or Taleo.
#let LINEAR_DATES = false

#let BODY_SIZE = 10pt
#let MARGIN = 0.5in

// Vertical rhythm. Every gap must be larger than the gap one level below it. The reader
// infers structure entirely from relative gap size, so any inversion makes two units
// merge visually. Both inversions below were real bugs found by eye, not by any
// automated check:
//
//   - entry gap < bullet gap  =>  consecutive jobs merge into one block
//   - bullet gap < line leading  =>  one wrapped bullet reads as two bullets
//
// The full ordering, loosest to tightest:
//
//   SPACE_SECTION > SPACE_ENTRY > SPACE_BULLET > SPACE_ENTRY_BODY >= LEADING
//
// LEADING is the gap between wrapped lines *inside* one bullet. It must stay the
// tightest value on the page, because those lines are a single sentence.
#let SPACE_SECTION = 14pt // above a section heading
#let SPACE_ENTRY = 9pt // between entries within a section
#let SPACE_BULLET = 0.68em // between bullets in the same entry
#let SPACE_ENTRY_BODY = 5pt // between an entry's header lines and its bullets
#let LEADING = 0.58em // between wrapped lines within a single bullet

#let resume(body) = {
  set page(paper: "us-letter", margin: MARGIN)
  set text(
    font: ("Helvetica", "Arial"),
    size: BODY_SIZE,
    lang: "en",
  )
  set par(justify: false, leading: LEADING, spacing: 0.65em)

  // Straight quotes only. Curly quotes are a character-substitution risk on older
  // parsers, and gain nothing on a resume.
  set smartquote(enabled: false)

  set list(marker: [•], indent: 0pt, body-indent: 7pt, spacing: SPACE_BULLET)

  // The rule hugs the heading text so the two read as one unit, then a clear gap
  // separates that unit from the content it introduces.
  show heading.where(level: 2): it => {
    v(SPACE_SECTION, weak: true)
    text(size: BODY_SIZE + 1.5pt, weight: "bold", upper(it.body))
    if SECTION_RULE {
      v(1.5pt, weak: true)
      line(length: 100%, stroke: 0.5pt + rgb("#000000"))
    }
    v(4pt, weak: true)
  }

  body
}

// Contact header. Name, then one delimited line of contact fields.
// Plain text only, never icons: parsers strip images and the field is lost.
//
// The name and the contact line are separate blocks on purpose. Joining them with a
// `linebreak()` puts both on lines of one paragraph, where spacing comes from
// `par.leading` — sized for 10pt body text, far too tight beneath a 19pt name, so the
// name's descenders crowd the contact line. Separate blocks each size to their own
// content and the gap below is set explicitly.
#let header(name: "", contact: ()) = {
  block(width: 100%, below: 6pt)[
    #align(center)[#text(size: 19pt, weight: "bold")[#name]]
  ]
  block(width: 100%, below: 3pt)[
    #align(center)[#text(size: BODY_SIZE)[#contact.join("  |  ")]]
  ]
}

// One experience, project, or education entry.
// Line 1: organization (bold), dates right-aligned.
// Line 2: title, location right-aligned.
// Bullets follow in the generated file as a native Typst list.
#let entry(org: "", title: "", location: "", dates: "") = {
  block(above: SPACE_ENTRY, below: SPACE_ENTRY_BODY, breakable: false)[
    #if LINEAR_DATES [
      #text(weight: "bold")[#org]#if dates != "" [, #dates]
      #if title != "" or location != "" [
        #linebreak()
        #title#if location != "" [, #location]
      ]
    ] else [
      #text(weight: "bold")[#org] #h(1fr) #dates
      #if title != "" or location != "" [
        #linebreak()
        #title #h(1fr) #location
      ]
    ]
  ]
}

// Categorized skills. Takes a dictionary of category -> comma-separated items.
// Ordered by relevance to the job description, most relevant first.
#let skills(categories) = {
  for (category, items) in categories {
    block(spacing: 0.35em)[#text(weight: "bold")[#category:] #items]
  }
}

// Optional summary, mid-level and above only. Max four lines.
#let summary(body) = {
  block(spacing: 0.5em)[#body]
}
