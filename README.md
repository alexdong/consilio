# Consilio: A Personal Decision Making Tool

> "Consilio" is a Latin term that embodies concepts such as counsel,
> deliberation, and wisdom. In ancient times, "consilium" referred to a group
> of advisors or a council that deliberated on important decisions, reflecting
> a process of careful consideration and planning. The term is associated with
> strategic thinking and prudent decision-making, emphasizing the use of good
> judgment, experience, and advice.

## Overview

Consilio helps you make better decisions by having LLM asking
independent and multi-perspective questions. Think of it as a vast
support network of advisors.  It asks you questions like "Have you thought about ...",  "What if ...", "Let's
stress test it this way ...".  The kind of questions you often pay your
advisors or boards for.

Think of Consilio as the "formal scientific method" described by Robert Pirsig.
It can be "slow, tedious, lumbering, laborious but invincible".

> “Actually I've never seen a cycle-maintenance problem complex enough really
> to require full-scale formal scientific method. Repair problems are not that
> hard. When I think of formal scientific method an image sometimes comes to
> mind of an enormous juggernaut, a huge bulldozer-slow, tedious, lumbering,
> laborious, but invincible. It takes twice as long, five times as long, maybe
> a dozen times as long as informal mechanic's techniques, but you know in the
> end you're going to get it. There's no fault isolation problem in motorcycle
> maintenance that can stand up to it. When you've hit a really tough one,
> tried everything, racked your brain and nothing works, and you know that this
> time Nature has really decided to be difficult, you say, "Okay, Nature,
> that's the end of the nice guy," and you crank up the formal scientific
> method.”

Consilio is intentionally minimal. It is designed to be used
in a command-line environment with a text editor (e.g., vim).

The core artefact Consilio works around is a single `DECISION.md` document. As
you go through the thinking process, you will revise this document by answering
the questions posed by Consilio.

All intermediate steps are preserved in structured format within a date-stamped
directory, creating a detailed record of the decision-making process. This
allows for both immediate reference and retrospective review of how important
decisions were made.

## The Decision Making Process

1. **Observe**: understand the situation by asking clarifying questions and explore alternatives

   You start by providing a document that captures the decision context,
   available options, and current considerations in a structured format;

   Consilio reviews this information, asking clarifying questions. You may want
   to go back and address these questions by revising your initial document.

   When you feel that the clarifying questions coming from Consilio is no longer
   adding much value. You are ready to proceed to the next step.

2. **Assemble**:

   At this step, you work with Consilio to identify the additional perspectives
   to bring to the table.

   Consilio will suggest a list of perspectives, followed by questions for each
   of them and explains why the answer matters.

3. **Consult**: systematically examines the options from multiple perspectives and weight the evidence

   Consilio will pass the observation and the questions to each perspective to
   allow in-depth exploration from each perspective.

   You may want to go back to the previous two steps based on the questions
   asked in these discussions.

## 3. Under the Hood

### 3.0 Define Context

Create a new `.consilio.yml` file in the root directory with the following
structure:

```yaml
domain:"a NZ-based B2C iOS app startup that are pre-product-market-fit"
perspective:"an bootstrapped B2C founder, who successfully navigated pre-PMF phase with limited capital. , living outside of US but your main market is US."
user_role:"Solo Founder"
```

Consilio can load different context through the command line option.

```bash
consilio --context marketing.consilio.yml
```

Further, the yaml settings can be overridden by the user at the start of the session.

### 3.1 Start Consilio

```bash
$ consilio
> Please define the type of decision: business
> Please enter the title of the decision: Bank Loan

```

1. Create new decision directory: `Decisions/YYYYMMDD-{decision_title|slug}/`
2. Open `Statement.md` in vim with template:

```markdown
# Decision: [Title]

## Summary
[What needs to be decided?]

## Options
[Available choices]

## Context
[Background information]

## Considerations
[What's been thought about]

## Unknowns
[What's unclear]
```

### 3.2 Initial Analysis & Observation

1. Read `Statement.md`
2. Load prompts from `1-Observe/`
3. Send to Claude with the following process:
   - Claude analyzes the situation from an expert advisor perspective
   - Performs detailed analysis of key elements, risks, opportunities
   - Formulates impactful questions to guide decision-making
   - Identifies relevant perspectives to consult
4. Save response to `Observation.xml`:

   ```xml
   <analysis>
      [Detailed analysis of situation including:]
      - Key elements breakdown
      - Potential risks and opportunities 
      - Alternative approaches
      - Key stakeholders
      - Short/long-term implications
   </analysis>
   <consult>
      <perspective>
         <title>[Perspective description]</title>
         <question>[Information seeking details]</question>
      </perspective>
      [Additional perspectives...]
   </consult>
   ```

5. User reviews and can either:
   - Edit `Statement.md` and retry
   - Continue to next stage

### 3.3 Multiple Perspectives Consultation

1. Parse `Observation.xml` to extract identified perspectives
2. For each perspective:
   - Create new Claude session with specific perspective expertise
   - Load prompts from `2-Consult/`
   - Include original situation, advisor observations, and specific questions
3. Save responses to `Perspectives.xml`:

   ```xml
   <perspectives>
      <perspective>
         <thought_process>
               - Key points summary
               - Potential solutions analysis
               - Reasoning explanation
         </thought_process>
         <answer>
               [Concrete, actionable answers to questions]
         </answer>
      </perspective>
      [Additional perspectives...]
   </perspectives>
   ```

4. User reviews and can either:
   - Edit `Statement.md` and restart
   - Continue to the synthesis step

### 3.4 Final Synthesis & Advice

1. Load prompts from `3-Advise/`
2. Send all previous documents to Claude for:
   - Comprehensive analysis of all gathered information
   - Identification of patterns, conflicts, and gaps
   - Risk and opportunity assessment
   - Synthesis of critical insights
3. Save final output to `Memo.md` with:
   - Comprehensive situation summary
   - Synthesis of critical information
   - Expert insights on potential impacts
   - Up to 7 important questions for consideration, each with:
     - Importance rating (1-9)
     - Brief explanation of relevance
     - Connection to synthesized information
