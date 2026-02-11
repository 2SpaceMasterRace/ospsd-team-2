# Design Document

**Date:**   
**Day:**   
**Time:**   
**Status:** 

---

## Context and Scope

A very general overview of what is being built or worked on. This section should bring anyone up to speed on the objective quickly and clearly. Keep it concise.

---

## Goals and Non-Goals

A clear list of goals and expected outcomes.

### Goals

- Explicitly state what is to be done.
- Focus on delivering the MVP.
- Define measurable outcomes where possible.

### Non-Goals

- Features or improvements that are out of scope for now.
- Ideas that can be revisited in future iterations.

This separation helps prevent scope creep and keeps execution focused.

---

## Learnings and Progress

**Note:** Prototyping itself is part of the design doc creation. "I tried it out and it works" is one of the strongest arguments for choosing a design.

Start with a high-level overview, then dive into details.

**Given:**
- Context (facts)
- Goals
- Non-goals (requirements)

**This section should:**
- Discuss problems faced.
- Document solutions attempted.
- Explain why a particular solution best satisfies the goals.
- Record what has been implemented so far.
- Save valuable references for future debugging.

**Include:**
- System context diagrams
- APIs
- Datasets used
- Pseudocode (only when novel algorithms are involved)

The goal is to give the reader a clear view of the broader technical landscape and contextualize what is happening at every step.

---

## Alternatives Considered

List reasonable alternative approaches that could have achieved similar outcomes.

For each alternative:
- Be succinct.
- Highlight trade-offs.
- Explain why it was not selected.

For the chosen design:
- Explicitly state why it is the best fit for the project goals.
- Clarify trade-offs introduced by other solutions.
- Include relevant details such as accuracy, performance, complexity, etc., where helpful.

This section should help future readers understand the decision-making process.

---

## Cross-Cutting Concerns

A short section describing:
- Problems faced during implementation.
- Potential future risks or issues arising from the design.
- Constraints or dependencies that may impact scaling or maintenance.

---

## Review & Suggestions

**Reserved for:** The Professors and the TA's.

**Purpose:**
- Share feedback.
- Discuss scope improvements.
- Suggest refinements.

Instead of meeting every week, use this shared document for asynchronous discussion. Save meetings for decisions that truly require live discussion. Over time, this document may evolve more like the U.S. Constitution — with amendments and clarifications — rather than being replaced entirely. These amendments can be incredibly helpful for future maintainers performing "design doc archaeology."
