# Consilio: AI-Facilitated Panel Discussions

Consilio[^1] is a CLI tool that facilitates System-2 Reasoning with the help of 
AI. 

Solutions to real world problems are rarely generated in a single, sequential
way. The process can be messy with many missed turns and back tracks. Consilio
provides the thinking tools like panel discussion and one-on-one interview to
faciliate a real-world decision making process. For those technical minded,
Consilio gives you the buttons and knobs to control the Monte Carlo Tree Search
process. 

Compare to inference time reasoning models like OpenAI's o1, Gemini Flash
Thinking or DeepSeek R1, Consilio is particularly strong in externalising tacit
knowledge Like personal preferences, values or biases, things you don't know
that you know. It's also great at providing the entry points for you to
discover and explore areas you are unfamiliar or even unaware of, things "you
don't know what you don't know." 

Consilio is a file-centric program. There is no database involved. Every
interaction, inputs from you or responses from LLMs, is saved as a text file.
This comes with a few benefits. Check the documents into your version control
system to maintain a record of your decision-making process. Use your unix
power tools to review responses and locate particular discussions on one topic.
Or feed the discussions into another LLM to gradually develop and solidify a
more accurate and holistic view of your decision making process.


## Installation

Consilio assumes that you have.

### Prerequisites

- python 3.9 or above
- `pipx` or `uv` installed in your system.
- `$EDITOR` or `$VISUAL` set in your environment.
- `$GEMINI_API_KEY` set in your environment. [^2]


### Steps

```bash
# Install Consilio
pipx install consilio  # or: uv install consilio

# After installation, create a new decision folder and check it into git
mkdir -p ~/Decisions/MyDecision
cd ~/Decisions/MyDecision
git init
```

## Usage

### Initialise Project

`cons init`: initialize a new Consilio project in the specified directory (defaults to
current directory) and open README.md in your default editor. 


### Clarify Goals

`cons clarify`: **Rubber duck your README.md file**. This command generate a
set of clarifying questions based on the README.md file. I often use this
command at the beginning of a thinking session to get the idea out "onto the
paper". These questions are great catalysts to externalise thoughts in a
structured manner.


### Manage Perspectives

`cons perspectives [subcommand]`: **Invite different experts to the table**.
This comand generate or add perspectives into your thinking session. The
perspectives can be different stakeholders, advisors from distinct backgrounds
or experts in different fields into your decision making process. 

Available subcommands:

- `generate`: Generate a new set of perspectives. You'll be prompted for the
  number of perspectives you'd like to include. For each question, you may want
  to have a play with the numbers to see what the optimal number is for the
  problem you are trying to tackle. The output perspectives will be saved to a
  `perspectives.json` file. Subsequent `generate` calls with overwrite the
  file. Once you are happy with the numbers, sometime it's a lot faster to just
  edit this file to focus on a small number of perspectives you feel is
  relevant. This is the default subcommand if run without a subcommand. 
- `add`: Interactively add a single new perspective. You'll be prompted to
  describe the questions you seek to answer. The LLM will generate a
  perspective based on your input and append it to the `perspectives.json`
  file.


### Facilitate Group Discussion

`cons discuss`: **Start a new round of group discussion**. You will be prompted
to give your input at the beginning of the discussion. Use this opportunity to
answer questions from the previous round of discussions or specify areas you'd
like to the group to focus on next. Responses from the previous round will be
automatically included in your `input.md` file with `> ` prefixed to each line.
A helpful mental model is to think of the input file as a Reply-to-All email. 
The responses from the group discussion will be saved in an `output.md` file.


### Conduct Interviews

`cons interview [subcommand]`: **Start an one-on-one interview session with a
chosen perspective**. This allows a more focused session to go deep with an
individual perspective. 

Available subcommands:

- `start`: You'll be prompted for the index number of the perspective you'd
  like to interview. The perspective will be loaded from the
  `perspectives.json` file. Use `cons perspectives add` to introduce a new one.
- `next`: Continue the interview with the most recent perspective.


### Additional Commands

- `cons completion [shell]` to generate shell completion scripts. Supported shells are `bash`, `zsh` and `fish`.
- `cons --version` to get the version of the program.
- `cons --help` to get the help message.


## Example Thinking Session 

Our family has been dreaming about getting a weekend getaway house near the
beach. Or a bach as we call it in New Zealand. We weren't clear where it
should be, whether to build or buy, and of course how we can finance it. 

The following is the file structure we have after a few days of thinking.

```bash
ls -lhT | awk 'BEGIN { printf "%-50s %-15s %-30s %-30s\n", "Name", "Size", "Last Modified", "Created" }
{
    cmd = "stat -f \"%SB\" \"" $10 "\" 2>/dev/null || stat -c \"%W\" \"" $10 "\" 2>/dev/null"
    cmd | getline created
    close(cmd)
    printf "%-50s %-15s %-30s %-30s\n", $10, $5, $6 " " $7 " " $8, created
}'
Name                                               Size            Last Modified                  Created
-------------------------------                    ------          ---------------                 -------------------
README.md                                          7.1K            22 Jan 10:58:50                Jan 21 09:28:50 2025
perspectives.json                                  5.4K            25 Jan 09:32:02                Jan 21 10:04:27 2025
discussion-r1-response.md                          8.3K            21 Jan 09:39:10                Jan 22 09:39:10 2025
discussion-r2-input.md                             1.4K            23 Jan 11:35:37                Jan 23 11:35:37 2025
discussion-r2-response.md                          8.2K            23 Jan 11:59:07                Jan 23 11:59:07 2025
discussion-r3-input.md                             10K             23 Jan 12:22:21                Jan 23 12:22:21 2025
discussion-r3-response.md                          9.4K            23 Jan 12:43:45                Jan 23 12:43:45 2025
discussion-r4-input.md                             6.5K            23 Jan 13:08:13                Jan 23 13:08:13 2025
discussion-r4-response.md                          6.2K            23 Jan 16:56:12                Jan 23 16:56:12 2025
interview-p11-r1-input.md                          331B            22 Jan 12:32:58                Jan 22 12:32:58 2025
interview-p11-r1-response.md                       6.8K            22 Jan 12:33:07                Jan 22 12:33:07 2025
interview-p11-r2-input.md                          1.4K            22 Jan 12:35:02                Jan 22 12:32:40 2025
interview-p11-r2-response.md                       7.3K            22 Jan 12:35:16                Jan 22 12:35:16 2025
interview-p11-r3-input.md                          1.8K            22 Jan 16:25:13                Jan 22 16:23:31 2025
interview-p11-r3-response.md                       12K             22 Jan 16:25:34                Jan 22 16:25:34 2025
interview-p11-r4-input.md                          130B            23 Jan 11:15:50                Jan 23 11:15:50 2025
interview-p11-r4-response.md                       11K             23 Jan 11:16:10                Jan 23 11:16:10 2025
```

A few things to note that hopefully gives you a sense of the process:

* On 21st, we started talking about this idea at the breakfast table. I created
  the README.md file to capture the inputs from 

* 22nd, the next day. We provided more input, particularly around our personal
  preferences using the `cons clarify`. Things like we just want a quiet place
  to read and connect as a family; off-the-grid, without utility is not an
  issue for us; our limited budget, we prefer it to be low maintainence and
  don't mind building it ourselves in stages. This step really helped to
  clarify our thoughts and set the direction for the perspectives we want to
  explore. We settled on 10 different perspectives and the `discuss` command
  became to take shape.

* 22nd afternoon, we added a new perspective "Low-maintanence Eco-friendly Bach
  Architect", as perspective #11, to help us understand the house design and its
  impact on the budget. I entered all the patterns we love from Christopher
  Alexander's "A Pattern Language" book to round 2, `interview-p11-r2-input.md`
  and asked for a staged build-out plan.

* 23rd, we reviewed the staged build plan and asked for one more round of
  targeted questions. Once we were satisfied with the cost and the kind of
  house we want to build, we returned to the group discussion to share the plan
  and get further feedback on the financial side.


## See Also

- [CONTRIBUTING.md](CONTRIBUTING.md) document for the contribution guidelines.
- [Python.md](Python.md) document for the coding style guide.
- [Issues](https://github.com/alexdong/consilio/issues) for the list of issues and feature requests.

[^1]: Consilio is a Latin term that embodies concepts such as counsel, deliberation, and wisdom. In ancient times, "consilium" referred to a group of advisors or a council that deliberated on important decisions, reflecting a process of careful consideration and planning. The term is associated with strategic thinking and prudent decision-making, emphasizing the use of good judgment, experience, and advice.
[^2]: Consilio only works with the Gemini API for now. More specifically, we are using `gemini-2.0-flash-exp`. This may appear to be a rather unusual choice but there are two main reasons that took us down this path. First is Gemini's **Structured output** makes it much easier to parse and understand the output. Second is that we need a large context window size to fully explore the problem space, Gemini's 1M token limit is an excellent fit for this.
[^3]: Just like LISP's `cons`, Consilio builds up structures that you can manipulate, shape and transform. A tool that helps you to construct your thoughts, opinions, and decisions in a structured manner.
