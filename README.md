# Consilio: A Personal Decision Making Tool

> "Consilio" is a Latin term that embodies concepts such as counsel,
> deliberation, and wisdom. In ancient times, "consilium" referred to a group
> of advisors or a council that deliberated on important decisions, reflecting
> a process of careful consideration and planning. The term is associated with
> strategic thinking and prudent decision-making, emphasizing the use of good
> judgment, experience, and advice.

## Overview

Consilio helps you make better decisions by focusing on two key actions:

1. **Clarify**: Asking independent questions like:
   - "Have you thought about ...?"
   - "What if ...?"
   - "Let's stress test it this way ..."

   These are the kinds of questions you might expect from trusted advisors or boards.

2. **Consult**: Assembling a group of relevant perspectives and seeking detailed, targeted opinions from them. Think of it as a vast support network of advisors.

To get started, create a **decision document**. This document captures:

- The context of the decision
- The questions you need to answer
- The opinions you gather
- Any other relevant information

It provides a structured way to think through important decisions, with or without Consilio.

As you interact with Consilio, you will refine this document by addressing the questions it poses and giving feedback on the gathered opinions.  
**Tip**: Check this document into your version control system to maintain a record of your decision-making process.

## Demo Session

Following is an example session:

```bash
# Create a new decision document
$ consilio Decisions/BankLoan.md
Welcome to Consilio
-------------------

Decision document: Decisions/BankLoan.md
Domain: "a NZ-based B2C iOS app startup that are pre-product-market-fit"
Advisor Perspective: "an bootstrapped B2C founder, who successfully navigated pre-PMF phase with limited capital. , living outside of US but your main market is US."
User Role:"Solo Founder"

Enter command C(larify), P(erspectives) or Ctrl+C to exit.
> C
[Response in Markdown format]
{You noticed that you need to provide more context. You update the document in your editor.  Now, let's try again.}
> C
[...]
{You are happy with the quality of the questions and decide to proceed.}
> P
[Response from the assembly step]
Are you ready to proceed to the consult step? (Y/n) Y
[Opinions from each perspectives]
{You noticed a gap in the information and decide to go back to the observe step.}
> C
[...]

{When you gut feel tells you that you have enough information to make a decision. }

CTRL+C received.  Exiting.
```

## Get Started

### Install

```bash
# Using `pipx` ... 
pipx install consilio

# or, if you prefer `uv`
uv install consilio
```

### Configuration

Create a new `.consilio.yml` file in the root directory with the following
structure:

```yaml
domain:"a NZ-based B2C iOS app startup that are pre-product-market-fit"
perspective:"an bootstrapped B2C founder, who successfully navigated pre-PMF phase with limited capital. , living outside of US but your main market is US."
user_role:"Solo Founder"
```

If you don't have a `.consilio.yml` file, Consilio will create one for you
when you run the command.

If you have multiple contexts, you can create a separate context file and load it through the command line option.

```bash
consilio --context marketing.consilio.yml
```

### Paper Trail

All intermediate steps are preserved in structured format within a date-stamped
directory, creating a detailed record of the decision-making process. This
allows for both immediate reference and retrospective review of how important
decisions were made.

## Contributing Guide

Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) document for the contribution guidelines.
Please refer to the [Python.md](Python.md) document for the coding style guide.
