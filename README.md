# Consilio: A Personal Decision Support Tool

> "Consilio" is a Latin term that embodies concepts such as counsel,
> deliberation, and wisdom. In ancient times, "consilium" referred to a group
> of advisors or a council that deliberated on important decisions, reflecting
> a process of careful consideration and planning. The term is associated with
> strategic thinking and prudent decision-making, emphasizing the use of good
> judgment, experience, and advice.


## 1. Overview

Consilio is a personal command-line tool that augments decision-making by
having structured conversations with Claude through a deliberate context-aware
perspective analysis process. 

Consider it as a thoughtful advisor who first understands your situation, asks
clarifying questions, then systematically examines the decision from multiple
perspectives before providing advice as recommendations and further questions. 

The tool enforces a deliberate decision-making process:

1. You first document the decision context, available options, and current
   considerations in a structured format;
2. Consilio reviews this information, asking clarifying questions, identifies
   what are the most impactful perpsectives to consider;
3. Consilio then explores the decision in depth from each perspective (e.g., financial, operational, strategic) in focused conversations;
4. Consilio synthesizes insights from all perspectives into concrete
   recommendations and further questions to consider.

All interactions are preserved in a structured format (markdown and XML) within
a date-stamped directory, creating a detailed record of the decision-making
process. This allows for both immediate reference and retrospective review of
how important decisions were made. 

The tool is intentionally minimal and personal. The tool is designed to be used
in a command-line environment, with excellent support to iterate on the
decision context and perspectives. It is intended to be used in conjunction
with a text editor (e.g., vim) and version control system (e.g., git) to manage
the decision-making process.


## 2. File Structure

```
.
├── Decisions/
│   └── 20241204-bank-loan/        # Date-slugged decision directory
│       ├── Statement.md           # Problem definition
│       ├── Observation.xml        # Initial analysis with structured output
│       ├── Perspectives.xml       # Multiple viewpoint analysis
│       └── Memo.md                # Final synthesis
├── Prompts/
│   ├── 1-Observe/
│   │   ├── SystemPrompt.md
│   │   └── UserPrompt.md
│   ├── 2-Consult/
│   │   ├── SystemPrompt.md
│   │   └── UserPrompt.md
│   └── 3-Advise/
│       ├── SystemPrompt.md
│       └── UserPrompt.md
├── editor.py                   
├── main.py                      
└── requirements.txt
```

## 3. Workflow

### 3.0 Define Context
Create a new `.consilio.yml` file in the root directory with the following
structure:

```yaml
domain:"a NZ-based B2C iOS app startup that are pre-product-market-fit"
consilio_role:"an bootstrapped B2C founder, who successfully navigated pre-PMF phase with limited capital. , living outside of US but your main market is US."
user_role:"Solo Founder"
```

### 3.1 Problem Definition

The yaml settings can be overridden by the user at the start of the session.

```bash
$ consilio --decision-type financial
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
