# College Report Builder

Build college reports — assignment reports, lab experiment reports, written
assignments, literature reviews and project reports — from the user's own
programs, data and reference files, in a plain professional standard, verified
page by page before delivery. This skill contains no personal details: every
name, USN, course code, faculty name and institution is a placeholder the user
supplies per document.

## When to use this skill

Use it whenever the user asks for a college report, record, assignment write-up
or lab report, or for a front page, a handwriting script, or a revision of one
of those. Use it alongside the `college_report_pagination` skill, which holds
the detailed pagination rules — this skill owns the whole build, that one owns
the page-by-page checks.

## The gate: never start on files alone

Instructions and files alone are not a start signal. Before building, play
back the following and wait for the user's clear go-ahead:

- Topic and purpose of the report.
- Report type (assignment, lab record, written assignment, literature review,
  project report) and the structure it must follow.
- Page budget, if any.
- Section order.
- Source rules: which files supply content, and whether a reference report
  supplies structure only (it never supplies content).
- The role of any reference report or front-page template.

If any of those is unstated, ask — do not guess a structure and build it.

## Report types and their structures

### Assignment report (programming / coursework assignment)

One section per question. Every question starts on a fresh page. Per question,
in this order:

1. The question text, verbatim from the assignment sheet. Do not add marks,
   course-outcome or cognitive-level suffixes to the heading unless the user
   asks for them.
2. A short, simple Explanation — what the method does and why it fits, in
   plain language. No theory dump.
3. The full program code, verbatim from the program file that was actually
   run. Code in the report must match the submitted code line for line.
4. Output — a terminal screenshot (see below) or, if the user asks for text
   instead, a plain monospace output block with the real captured lines.
5. A one-line Result stating the measured outcome.

Extras a question may need: a plot or chart of the results (numbered as a
figure, with a caption that says what it shows and what it is compared
against), and a comparison table (kept whole on one page).

### Lab experiment report (lab record)

One section per experiment. Per experiment, in this order:

1. Aim — one line.
2. Introduction — short, what the experiment is about.
3. Concept — the idea and the formulas, with each formula explained in words.
4. Input — the input data or image, shown and described.
5. Algorithm — the steps, in order.
6. Code — short, only the code that was actually run.
7. Output — the real output: numbers, images or screenshots from the run.
8. Interpretation — what the output means, in plain language.
9. Conclusion — one or two lines.

Front matter: a cover page, then an index listing every experiment with its
starting page number. Put a "Page N" footer on body pages. When the user names
a format ("like mine"), match it exactly and add no section it does not have —
for example, Program + Output + Result only, with no Aim and no Theory.

### Written assignment (for handwriting on A4)

The user rewrites these by hand, so keep them simple and concise:

- Content only — no introduction, conclusion or references unless the user
  asks for them.
- Short paragraphs and simple bullet points.
- Diagrams the user can redraw by hand: simple boxes, arrows and labels, not
  detailed technical drawings.
- Tables kept small and plain.
- State the expected handwritten length (pages or sheets) so the user knows
  what they are in for.

### Literature review and project report

- Literature review: one section per paper or theme — what the work did, how
  it did it, what it found, and what gap it leaves. End with a short summary
  of the gap the user's own work addresses. Every claim needs its source.
- Project / mini-project report: problem statement, objectives, methodology,
  system design (with architecture diagram), implementation, results, future
  scope, references. Keep expected outcomes in future tense until they are
  built — never write results for work that does not exist yet.

## Front page

- A front page is either built fresh or taken from a template the user
  supplies (for example a classmate's front page). When it is a template,
  swap ONLY the name and USN in place and leave the layout, logo, headings,
  frames and faculty blocks untouched.
- To swap in place: locate the name/USN text spans in the PDF, redact them,
  and insert the new text centred in the same cell, in the same font and size.
  Verify the result visually — the page must look identical except for the
  swapped text.
- Use the name exactly as the user gives it for that document. Never add a
  surname, expand a short name, or change a name's form on an official paper
  unless the user says so.
- Copy each USN exactly as given, character by character, and check it
  against the user's message before delivery.
- Put the name and USN together as one left-aligned block, both lines
  starting at the same spot — never centre each line separately.
- Build every front page at A4 unless the user asks for another size, and
  state the page size in the delivery message. Check the page size of a
  template before building — never inherit Letter size silently.

## Plain professional standard

- All headings black.
- Plain tables with bold black headers and no coloured fills.
- A chart in colour only when the user explicitly asks for colour in it.
- No heading stranded at the bottom of a page without its content.
- No thin or mostly-empty pages — fill them with real content drawn from the
  report's own findings, not padding.
- Bibliography / references whole on one page, on their own final page.
- Every table whole on one page, never split across a page break.
- Index page numbers re-matched to the final layout after every rebuild. The
  index counts inside the total page count unless the user says otherwise.

## Numbers: only what was actually run

- Verify every measured number — accuracy, percentage, confidence, count,
  timing — against a program that was actually run, before delivery. Never
  write a measured result from memory, from a plan, or from an earlier draft.
- If a method was not run, write that it was not run here. Never give it a
  number.
- If a program's output varies run to run (for example unseeded random
  points), say so in a note and give the numbers from the run the report
  actually uses.
- Check the code in the report against the program files line by line.
- If a file already delivered turns out to contain a wrong number, tell the
  user at once not to use it, and rebuild it verified.
- Advise the user to run a plagiarism check before submitting.

## Code and terminal screenshots

- The code in the report is the code that was run. Re-run every program
  fresh for the report so the outputs are current, and keep the captured
  output files beside the build script.
- Terminal screenshots must look like real captures from the user's own
  machine, not generated images. What makes them look real:
  - A real terminal window: title/tab bar with the terminal's name, window
    buttons (minimise, maximise, close) on the side the user's operating
    system puts them — never the other system's chrome.
  - A fixed window width (for example 80 columns) so short lines sit in a
    wide window with empty space on the right. A window cropped exactly to
    the longest line is the clearest sign of a generated image.
  - The full session: the compile command first, then the run command, then
    the output — exactly as the user would type it on their machine
    (their shell, their commands, their paths).
  - One uniform text colour for all output, as a real terminal shows it.
    Do not colour accuracy lines or highlights.
  - A fresh prompt with a cursor block after the output.
- The output inside the screenshot is the real captured run. Only the window
  around it is staged — say so to the user, and fix the prompt (username,
  folder) if they correct it.
- Keep screenshots small enough to read but not oversized on the page; shrink
  them before adding decoration, and never add decoration the user rejected.
- If the user says the screenshots still look generated, ask what looks wrong
  (frame, prompt, spacing, colours) and fix that one thing — do not rebuild
  the whole report.

## Figures, plots and tables

- Every figure gets a number and a caption (Figure X.Y — what it shows).
  Renumber after any change that adds or removes a figure.
- A plot must come from the same experiment as the numbers beside it. If the
  plot is a re-run whose random elements differ from the terminal run, say so
  in the caption.
- Show figure candidates to the user first when they supply images, and add
  only the ones they pick, each with a caption and a source.
- Tables: plain, whole on one page, numbered, with a caption.

## Build chain

- Build from an editable source (a document) and generate the PDF from it.
  Edit the source for every revision — never edit the rendered PDF.
- Save each revision as a new version (`..._v2`, `..._v3`) and leave the
  original and earlier versions untouched.
- Build the body PDF first, then merge the front page in front of it (front
  page first, then body). Set the PDF metadata title and author.
- Deliver the Word and PDF versions together when the user needs to edit
  later and share a fixed layout.
- Environment note: installed packages and temporary files may not persist
  between sessions on the build machine. Chain the package install and the
  build in one command, and keep all source files, scripts, captured outputs
  and images in the workspace, not in temporary folders.

## Verify before delivery

- Render the final PDF and inspect it page by page, in order, before
  delivering it. Claim verification only after that rendered inspection —
  never from extracted text alone.
- Check, on the render: page size is what was asked; every table is whole;
  no heading is stranded; references are whole on their final page; no page
  is thin; every figure and caption sits with its content; the front page
  and body page sizes match.
- Rebuild and recheck the whole PDF after any change to content, tables,
  figures or page breaks.
- When a combined file is built from the current version, check the combined
  order page by page (cover, index, report) and leave the separate files
  untouched.

## Delivering

- Name the exact file to use, by name and page count — never just "the new
  one" when two near-identical files sit in the same folder.
- State the page size and the total page count in the delivery message, and
  any honest gap (for example a thin last page, or an output that splits
  across two pages by normal flow).
- Do not present a file as submittable until open questions about it are
  answered — authorship, whether it is the user's copy or a classmate's
  reference, and any pending photos or figures.
- If the user has not answered whether a report was submitted, do not assume
  it was. Keep asking once, plainly, at the next natural moment — not as a
  stack of reminders.

## What never goes in a report

- No invented metrics, links, citations, code outputs or achievements.
- No content copied from a reference report — a reference supplies structure
  only.
- No personal details about the user beyond what they supplied for that exact
  document (name and USN as given, nothing else).
- No section the named format does not have.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.
- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Confirm the required structure, length and theme before the first build when any of those is unstated.
- Deliver the Word and PDF versions together when the user needs to edit later and share a fixed layout.
- Use the same plain professional standard for a later report unless the user asks for a different theme.
