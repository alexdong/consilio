# Consilio: AI-Facilitated Panel Discussions

Consilio[^1] is a command-line power tool that helps you make better decisions
through System-2 Reasoning. 

Solutions to real world problems are rarely generated in a single, sequential
way. The process can be messy with many missed turns and back tracks. Consilio
provides the thinking tools like panel discussion and one-on-one interview to
faciliate a real-world decision making process. For those technical minded,
Consilio gives you the buttons and knobs to control the Monte Carlo Tree Search
process. 

Compare to inference time reasoning models like OpenAI's o1 or Gemini Flash
Thinking, Consilio is particularly strong in externalising tacit knowledge that
you don't know what you know. It's also great at providing the entry points for
you to discover and explore areas "you don't know what you don't know." 

Consilio is a file-centric program. Every interaction is saved as a text file.
Use your unix power tools to review responses and search for discussions from
past decisions. Check the documents into your version control system to
maintain a record of your decision-making process. 

Consilio assumes that you have 

- `$EDITOR` or `$VISUAL` set in your environment.
- `pipx` or `uv` installed in your system.
- `$GEMINI_API_KEY` set in your environment. [^2]


## Quick Start

```bash
# Install Consilio
pipx install consilio  # or: uv install consilio

# Create a new folder
mkdir ~/Decisions/MyDecision
cd ~/Decisions/MyDecision

# Start a new discussion [^3]
cons init

# Follow the interactive prompts to:
# 1. Describe your situation
# 2. Generate expert perspectives
# 3. Engage in structured discussion rounds
```

### `init`

$ cons init

Initialize a new Consilio project in the specified directory (defaults to current directory) and open README.md in your default editor. If README.md already exists, it will be opened for editing.

The editor will be pre-populated with a template if creating a new file, or the existing content if the file already exists.

This step will also creates a `cons.toml` file with default settings.

The following configuration options are available in cons.toml:

```toml
# Key bindings for input (default: "emacs")
key_bindings = "vi"

# Temperature for LLM responses (0.0-1.0, brainstorm: 0.8, meeting: 0.2)
temperature = 1.0

### `perspectives`

$ cons perspectives [subcommand]

Generate or manage perspectives for your discussion. If no subcommand is specified, generates a new set of perspectives (1-25) based on your topic.

Available subcommands:

- `generate`: Same as running without a subcommand. Generate a new set of perspectives. You'll be prompted for the number of perspectives you'd like to include. The perspectives will be saved to `perspectives.json`.

- `add`: Interactively add a single new perspective. You'll be prompted to describe the new perspective, and the LLM will generate appropriate details while considering the existing perspectives.

- `edit`: Open the perspectives file in your default editor to modify or remove perspectives. The file will be validated for proper JSON format after editing.

### `discuss`

$ cons discuss [flags]

Start a new round of discussion. You will be prompted to provide guidance for the discussion. You can answer questions from the previous round of discussions or specify a particular area you'd like to focus on next.

If both the `discussion.md` and `perspectives.md` files exist, Consilio will start the discussion process. Each round of discussion will be saved as `~/.consilio/YYYY-MM-DD-{Topic-Slug}/round-{n}.md`.

Flags:

- `-r`, `--round [round number]`: Restart the discussion from the specified round number. This is useful if you want to revisit a previous round of discussions or if you have saved the discussion document and want to continue from where you left off.

### `interview`

$ cons interview [flags]

Start an interview session with a specific perspective. This allows for focused discussions with individual perspectives, getting deeper insights from their particular viewpoint.

Flags:

- `-r`, `--round [round number]`: Start from a specific interview round number.


### Misc

- `cons completion [shell]` to generate shell completion scripts. Supported shells are `bash`, `zsh` and `fish`.
- `cons --version` to get the version of the program.
- `cons --help` to get the help message.


## Inspiration

- [Virtual Lab](https://github.com/zou-group/virtual-lab): The Virtual Lab is an AI-human collaboration for science research. [x.com](https://x.com/james_y_zou/status/1856729107045982607)

## See Also

- [CONTRIBUTING.md](CONTRIBUTING.md) document for the contribution guidelines.
- [Python.md](Python.md) document for the coding style guide.
- [Issues](https://github.com/alexdong/consilio/issues) for the list of issues and feature requests.

[^1]: Consilio is a Latin term that embodies concepts such as counsel, deliberation, and wisdom. In ancient times, "consilium" referred to a group of advisors or a council that deliberated on important decisions, reflecting a process of careful consideration and planning. The term is associated with strategic thinking and prudent decision-making, emphasizing the use of good judgment, experience, and advice.
[^2]: Consilio only works with the Gemini API for now. More specifically, we are using `gemini-2.0-flash-exp`. This may appear to be a rather unusual choice but there are two main reasons that took us down this path. First is Gemini's **Structured output** makes it much easier to parse and understand the output. Second is that we need a large context window size to fully explore the problem space, Gemini's 1M token limit is an excellent fit for this.
[^3]: The command `cons` is a shortcut for `consilio`. It's called `cons` because just like LISP's `cons`, it constructs structures that you can manipulate, shape and transform. This is what I envision Consilio to be - a tool that helps you construct your thoughts, opinions, and decisions in a structured manner.
