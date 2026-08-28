// Shared cover letter styling. Generated letters import this and contain content only.
//
// Design constraints (see agents/write-cover-letter/format-rules.md):
//   - Single column. No grid, table, or absolute positioning anywhere, so the PDF text
//     layer extracts in strict linear reading order.
//   - Contact details live in the document body, never in a page header. Some parsers
//     drop headers and footers wholesale.
//   - Standard fonts only, to avoid character substitution during parsing.
//   - Same font stack and contact-line delimiter as resume-style.typ, so a resume and a
//     letter submitted together read as one packet.

#let BODY_SIZE = 10.5pt
#let MARGIN = 1in

// A letter is short, so it can spend space the resume cannot. Dense text triggers
// immediate negative bias, and the whole document is one screen either way.
// Vertical rhythm, same principle as the resume: the reader infers structure from
// relative gap size, so every gap must clearly exceed the one below it.
//
//   SPACE_BLOCK > SPACE_PARA > LEADING
//
// SPACE_PARA at 0.95em was a real bug found by eye: it sat close enough to LEADING that
// a new paragraph read as another wrapped line of the previous one.
#let LEADING = 0.72em // between wrapped lines inside a paragraph
#let SPACE_PARA = 1.25em // between body paragraphs, must clearly exceed LEADING
#let SPACE_BLOCK = 16pt // between letter blocks (address, date, salutation, body)

#let letter(body) = {
  set page(paper: "us-letter", margin: MARGIN)
  set text(
    font: ("Helvetica", "Arial"),
    size: BODY_SIZE,
    lang: "en",
  )

  // Ragged right, never justified. Justification produces uneven word spacing that reads
  // as a template, and adds nothing at this line length.
  set par(justify: false, leading: LEADING, spacing: SPACE_PARA)

  // Straight quotes only, matching the resume. Curly quotes are a character-substitution
  // risk on older parsers.
  set smartquote(enabled: false)

  body
}

// Sender block. Name, then one delimited line of contact fields.
// Mirror the resume's contact line exactly: same fields, same order.
#let letterhead(name: "", contact: ()) = {
  block(width: 100%, below: 4pt)[
    #text(size: BODY_SIZE + 5pt, weight: "bold")[#name]
  ]
  block(width: 100%, below: SPACE_BLOCK)[
    #text(size: BODY_SIZE)[#contact.join("  |  ")]
  ]
}

// Dateline. Written out in full ("August 20, 2026"), not MM/YYYY. This is the one place
// in the system that does not use the numeric date convention: a numeric dateline on a
// letter reads as a generated document.
#let dateline(date) = {
  block(width: 100%, below: SPACE_BLOCK)[#date]
}

// Optional recipient block. Include only with a verified name or a real team from
// company-research.md. Each line is its own block so extraction stays linear.
#let recipient(lines: ()) = {
  block(width: 100%, below: SPACE_BLOCK)[
    #lines.join(linebreak())
  ]
}

// "Dear <someone>,". Never "To Whom It May Concern".
#let salutation(greeting) = {
  block(width: 100%, below: SPACE_BLOCK)[#greeting]
}

// Closing and signature. No title line, no elaborate valediction.
#let signoff(closing: "Sincerely,", name: "") = {
  block(width: 100%, above: SPACE_BLOCK, below: 0pt)[
    #closing
    #linebreak()
    #linebreak()
    #name
  ]
}

// The T-Chart format and its `requirement()` helper were removed 08/2026. A letter is
// prose; the requirement-mapping job belongs to match-analysis.md and the resume.
//
// One lesson from that helper is worth keeping, because it applies to any spacing value
// added here later: its bold label sat 2pt above its evidence line, and the two lines'
// ascenders and descenders collided in the rendered PDF. Text extraction did not reveal
// it, because extraction reports order, not position. Always look at the page as an image
// as well as through pdftotext.
