# Consilio: A Personal Decision Making Tool

> "Consilio" is a Latin term that embodies concepts such as counsel,
> deliberation, and wisdom. In ancient times, "consilium" referred to a group
> of advisors or a council that deliberated on important decisions, reflecting
> a process of careful consideration and planning. The term is associated with
> strategic thinking and prudent decision-making, emphasizing the use of good
> judgment, experience, and advice.

## Overview

Consilio helps you make better decisions by doing two things:

1. clarify: asking independent questions like "Have you thought about ...",  "What if ...", "Let's
   stress test it this way ...".  The kind of questions you often pay your advisors or boards for.

2. consult: assemble a group of relevant perspectives and seek out
   detailed, targeted opinions from them. Think of it as a vast
   support network of advisors.  

To get started, you need to create a decision document. This document
captures the context of the decision, the questions you need to answer, and the
opinions you gather and any other relevant information. This is a structured way to think through important decisions, with consilio or not.

As you interact with consilio, you will keep coming back to this document by addressing
the questions posed by Consilio as well as giving feedback to the opinions gathered.
I strongly recommend checking this file into your version control system so you have a
record of the decision-making process.

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

Get get started, please select one of the following actions: observe, consult.
CTRL+C to exit.

> observe
[Response in Markdown format]
{You noticed that you need to provide more context. You update the document in your editor.  Now, let's try again.}
> observe
[...]
{You are happy with the quality of the questions and decide to proceed.}
> consult
[Response from the assembly step]
Are you ready to proceed to the consult step? (Y/n) Y
[Opinions from each perspectives]
{You noticed a gap in the information and decide to go back to the observe step.}
> consult
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

Consilio can load different context through the command line option.

```bash
consilio --context marketing.consilio.yml
```

### Paper Trail

All intermediate steps are preserved in structured format within a date-stamped
directory, creating a detailed record of the decision-making process. This
allows for both immediate reference and retrospective review of how important
decisions were made.

## Contributing

Contributions are welcome! Here's how you can help:

### Development Setup

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/your-username/consilio.git
   cd consilio
   ```

3. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

### Development Workflow

1. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

2. Make your changes
3. Run the linter:

   ```bash
   make lint
   ```

4. Run the test suite with coverage:

   ```bash
   # Run tests with coverage report
   pytest --cov=consilio --cov-report=term-missing

   # Generate HTML coverage report
   pytest --cov=consilio --cov-report=html
   ```

   The HTML report will be generated in the `htmlcov` directory. Open `htmlcov/index.html` in your browser to view detailed coverage information.

5. Commit your changes:

   ```bash
   git commit -m "feat: Add new feature"
   ```

6. Push to your fork:

   ```bash
   git push origin feature-name
   ```

7. Open a Pull Request

### Code Style

Please refer to the [Python.md](Python.md) document for the coding style guide.
