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

### 3.1 Problem Definition
1. Create new decision directory: `Decisions/YYYYMMDD-{decision}/`
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

### 3.2 Initial Analysis

1. Read `Statement.md`
2. Load prompts from `1-Observe/`
3. Send to Claude
4. Save response to `Observation.xml`:
```xml
<observation>
    <summary>
        [Initial analysis summary]
    </summary>
    <clarifications>
        <question>...</question>
        <question>...</question>
    </clarifications>
    <perspectives>
        <perspective>
            <name>Financial</name>
            <questions>
                <question>What's the ROI timeline?</question>
                <question>What are the cash flow implications?</question>
            </questions>
        </perspective>
        <perspective>
            <name>Operational</name>
            <questions>
                <question>How will this affect daily operations?</question>
                <question>What resources are needed?</question>
            </questions>
        </perspective>
    </perspectives>
</observation>
```
5. User reviews and can either:
   - Edit `Statement.md` and retry
   - Continue to next stage

### 3.3 Multiple Perspectives

1. Parse `Observation.xml` to extract perspectives and their questions
2. For each perspective in the XML:
   - Create new Claude session
   - Load prompts from `2-Consult/`
   - Include `Statement.md` and perspective questions
3. Save all responses to `Perspectives.xml`:
```xml
<perspectives>
    <perspective>
        <name>Financial</name>
        <analysis>
            [Claude's analysis from financial perspective]
        </analysis>
        <recommendations>
            [Specific recommendations]
        </recommendations>
    </perspective>
    <perspective>
        <name>Operational</name>
        <analysis>
            [Claude's analysis from operational perspective]
        </analysis>
        <recommendations>
            [Specific recommendations]
        </recommendations>
    </perspective>
</perspectives>
```
4. User reviews and can either:
   - Edit `Statement.md` and restart
   - Continue to the synthesis step

### 3.4 Final Synthesis

1. Load prompts from `3-Advise/`
2. Send all previous documents to Claude
3. Save final advice directly to `Memo.md`
