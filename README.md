# Consilio: AI-Facilitated Panel Discussions

Consilio[^1] is a command-line tool that helps you make better decisions through System-2 Reasoning.

For complex problems, solutions are not generated in a single, sequential way, but through a latent, iterative exploration process. Consilio provides a set of thinking tools, like debate, panel discussion, stress test and one-on-one interview, to faciliate this process. Or, to put it more simply, Consilio gives you with the tools to execute a Monte Carlo Tree Search by providing inputs every step of the way.

## Quick Start

```bash
# Install Consilio
pipx install consilio  # or: uv install consilio

# Start a new discussion
cons

# Follow the interactive prompts to:
# 1. Describe your situation
# 2. Generate expert perspectives
# 3. Engage in structured discussion rounds
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pipx or uv package manager

### Install Steps

```bash
# Using pipx (recommended)
pipx install consilio

# Or using uv
uv install consilio
```

## Basic Usage

1. Start a new discussion with `cons`
2. Enter your topic or decision when prompted
3. Choose number of expert perspectives (1-10)
4. Guide the discussion through multiple rounds

All interactions are automatically saved as text files for future reference.

## Features

### Core Capabilities

- Generate diverse expert perspectives on your topic
- Facilitate structured multi-round discussions
- Save all interactions for review and reference
- Edit and refine discussions using your preferred editor
- Switch between multiple ongoing discussions

### `cons` Command

`cons` is the main command that you will interact with.

Under the hook, it delegates to a set of subcommands depends on the state of the topic directory.

- `cons topics`. If there is no `topic` in the configuration file or there is no `discussion.md` file in the topic directory, you will be prompted to describe the topic of the discussion. A slug will be generated from the topic and the file is saved as `~/.consilio/YYYY-MM-DD-{Topic-Slug}/discussion.md`.

- `cons perspectives`. If there is a `discussion.md` file in the topic directory but no `perspectives.md` file, you will be prompted to enter the number of perspectives you would like to include in the discussion. Consilio will then generate a list of perspectives based on the topic and save it as `~/.consilio/YYYY-MM-DD-{Topic-Slug}/perspectives.md`. You can reload the perspectives or open up this file to add or remove perspectives.

- `cons discuss`. If both the `discussion.md` and `perspectives.md` files exist, Consilio will start the discussion process. Each round of discussion will be saved as `~/.consilio/YYYY-MM-DD-{Topic-Slug}/round-{n}.md`.

### `topics`

$ cons topics [flags]

This command will prompt you to enter the topic you'd like to discuss. The topic will be saved as `discussion.md` in the topic directory. You can use this command to start a new discussion or to switch to a different topic.

The topic directory will be set as `topic` in the config.toml file through the `cons config set topic YYYY-MM-DD-{Topic_Slug}` command.

Flags:

- `-l`, `--list`: List all the topic directories in the `~/.consilio` directory.
- `-t`, `--topic-number <number in the list>`: Switch to a different topic. This will update the `topic` in the config file.
- `-o`, `--open`: Open the topic directory in the default file explorer.

### `perspectives`

$ cons perspectives [flags]

Reload available perspectives. This will overwrite the existing `perspectives.md` file in the topic directory and request a new set of perspectives. If there is no topic or decision file, this command will quietly exit with a message to start a new topic.

I find this useful after a couple of rounds of discussions when I want to update the discussion document or want to focus on a particular area.

Flags:

- `-e`, `--edit`: Open the perspectives.md file in the default editor

### `discuss`

$ cons discuss [flags]

Start a new round of discussion. You will be prompted to provide guidance for the discussion. You can answer questions from the previous round of discussions or specify a particular area you'd like to focus on next.

Flags:

- `-e`, `--edit [round number]`: Open the specified round of discussions in the default editor. You can use this to add more context or clarifications to the discussion document. Once you are done editing, save and close the file. Consilio will provide you with the next steps.
- `-r`, `--round [round number]`: Restart the discussion from the specified round number. This is useful if you want to revisit a previous round of discussions or if you have saved the discussion document and want to continue from where you left off.

### `interview`

$ cons interview [perspective_index] [flags]

Start an interview session with a specific perspective. This allows for focused discussions with individual perspectives, getting deeper insights from their particular viewpoint.

Flags:

- `-r`, `--round [round number]`: Start from a specific interview round number.

### `summary`

$ cons summary

Generate a comprehensive summary of the discussion. This will compile all the rounds of discussions, perspectives, and other relevant information into a single document for easy review and reference.

### `config`

$ cons config

Create a initial configuration file  `~/.config/consilio/config.toml` with
default options, then open the configuration file in the default editor.

The following configuration options are available:

```toml
# The current topic being discussed
topic = "~/.consilio/YYYY-MM-DD-{Topic-Slug}"

# Key bindings for input (default: "emacs")
key_bindings = "vi"  

# LLM model to use (default: "claude-3-sonnet-20240229")
model = "claude-3-sonnet-20240229"

# Temperature for LLM responses (0.0-1.0, brainstorm: 0.8, meeting: 0.2)
temperature = 1.0
```

### Misc

- `cons completion [shell]` to generate shell completion scripts. Supported shells are `bash`, `zsh` and `fish`.
- `cons --version` to get the version of the program.
- `cons --help` to get the help message.

### Key Commands

- `cons` - Start or continue a discussion
- `cons topics` - Manage discussion topics
- `cons summary` - Generate comprehensive discussion summary
- `cons perspectives` - Generate or edit expert perspectives
- `cons discuss` - Start a new discussion round
- `cons interview` - Interview a specific perspective
- `cons config` - Configure settings

See detailed command options below.

## Demo Session

The main command is `cons` [^2].

Following is a session where:

- `$` is the shell prompt
- `>>>` is the consilio prompt
- `>` is the response

```bash
$ cons
Please enter the topic you'd like to discuss** (Press E to edit the topic in your default editor):
>>>
My daughter is 10 years old. She has a very busy schedule:

Ballet on Monday 4:30-5:30 and Thursday 4:00-5:00; 
Jazz on Friday 4:00-5:00; 
Karate on Wednesday 6:00-8:00 and Friday same time.
Violin on Saturday morning 10:30 - 11:30.

She just earned her Junior Black Belt in Karate and she is Grade 3 in Ballet
with a distinction. She will go to intermediate school and she has decided to
add Fencing to her schedule on Monday from 3:30-4:30.  

On the personal note, My wife has been doing karate with her since she was 5.
They spent a lot of time together. I'm a fencer and I am really excited about
her starting fencing. 

However, she was very tired towards the end of this year and started to get
tired and sick more often. Her academic performance has also dropped.

Both my wife and I think she is doing too much and we are looking for advices
on how to handle this. We are both worried about her overcrowded schedule and
the impact it is having on her health and academic performance.
<<<

CTRL+C received. The file is saved as ~/.consilio/2024-12-25-My-daughter-schedule/discussion.md. 

Next step: 
* `cons` again to generate perspectives based on the topic.



$ cons
Please enter the number of perspectives you would like to include (1-10):
>>> 5

Generating perspectives based on the topic ...

> 1. The Pediatric Exercise Physiologist
>    - Expertise: The science of how exercise and physical activity affect
>      children's growth, development, and overall health. This includes
>      understanding energy expenditure, recovery, and the impact of intense
>      training on young bodies.
>    - Goal: To optimize your daughter's physical activity schedule to ensure
>      it supports her health, well-being, and long-term athletic development
>      without causing burnout or injury.
>    - Role: To analyze your daughter's current activity load, considering the
>      intensity, duration, and frequency of each activity. They would assess
>      the potential for overtraining, recommend strategies for recovery and
>      rest, and advise on how to balance her physical activities with her
>      developmental needs and energy levels.
> 
> 2. The Child Educational Psychologist
>     - Expertise: The study of how children learn, develop cognitively, and
>       navigate the social and emotional aspects of schooling. They understand
>       the impact of stress, fatigue, and extracurricular activities on
>       academic performance and mental well-being.
>     - Goal: To optimize your daughter's overall schedule to support her
>       academic success, cognitive development, and emotional well-being,
>       ensuring a healthy balance between schoolwork, extracurriculars, and
>       rest.
>     - Role: To assess the impact of your daughter's busy schedule on her
>       academic performance, attention span, and motivation. They would
>       provide recommendations on time management strategies, stress reduction
>       techniques, and how to create a more supportive and balanced learning
>       environment at home. They might also consider the social and emotional
>       implications of her commitments.
> 
> 3. The Youth Sports Coach (Generalist)
>     - Expertise: Experience in coaching and developing young athletes across
>       various disciplines. They understand the importance of fun, skill
>       development, and fostering a love for movement while also recognizing
>       the signs of burnout and the need for a balanced approach.
>     - Goal: To help your daughter maintain her enjoyment of her activities
>       and continue to develop her skills and passions without sacrificing her
>       health or well-being.
>     - Role: To provide a perspective on the overall volume and intensity of
>       your daughter's activities. They would likely advocate for open
>       communication with your daughter about her enjoyment levels and suggest
>       considering her personal preferences and intrinsic motivation as key
>       factors in her schedule. They might also emphasize the importance of
>       unstructured play and free time.
> 
> 4. The Family Wellness Consultant
>     - Expertise: Understanding the dynamics of family well-being and the
>       importance of creating a supportive and healthy home environment. They
>       focus on the interplay between individual needs and family harmony.
>     - Goal: To help your family create a schedule that supports not only your
>       daughter's individual interests but also the overall well-being and
>       balance of the entire family unit, including parental needs and time
>       for connection.
>     - Role: To facilitate discussions about family priorities and values.
>       They might help you identify areas where the schedule is creating
>       stress for everyone and guide you in making decisions that prioritize
>       your daughter's health and well-being while also considering the impact
>       on family time and dynamics. They might encourage a collaborative
>       approach to adjusting the schedule.
> 
> 5. The Child Sleep Specialist
>     - Expertise: The science of sleep in children, understanding its crucial
>       role in physical and cognitive development, mood regulation, and
>       overall health. They can assess sleep patterns and the impact of
>       external factors on sleep quality.
>     - Goal: To ensure your daughter is getting adequate and high-quality
>       sleep to support her physical recovery, academic performance, and
>       emotional well-being.
>     - Role: To analyze your daughter's sleep schedule in relation to her
>       activities. They would assess the potential for sleep deprivation and
>       its contribution to her tiredness and increased susceptibility to
>       illness. They would provide recommendations for optimizing her sleep
>       environment, establishing healthy sleep routines, and potentially
>       adjusting her activity schedule to prioritize sufficient sleep.


The file is saved as ~/.consilio/2024-12-25-My-daughter-schedule/perspectives.md.

Next step: 
* `cons` again to start the first round of discussions.
* `cons perspectives -e` to edit the perspectives file.
* `cons edit` to edit the discussion file if you want to add more context or clarifications.
* `cons perspectives` to generate a new set of perspectives based on the topic.


$ cons
Please provide guidance for the discussion. (Answer questions from the previous round of discussions, or specify a particular area you'd like to focus on next. CTRL+D when you finish.)
>>>
Starting discussions (Round #1) ...

> ## Round 1: Team Meeting - Addressing the Overcrowded Schedule
> 
> Here's how each perspective might contribute to the first round of the
> meeting:
> 
> **1. The Pediatric Exercise Physiologist:**
> 
> *   **Presentation:** "My primary concern is the potential for physical
>     overtraining and insufficient recovery. With ballet, jazz, karate, and
>     now fencing, she's engaging in a significant amount of structured
>     physical activity. Each discipline requires specific muscle groups and
>     has its own demands. The reported tiredness and increased sickness are
>     red flags from a physiological standpoint. We need to consider the
>     intensity and duration of each activity. For example, Karate twice a week
>     for two hours each time, especially after earning her black belt, likely
>     involves high-intensity training."
> *   **Guiding Question:** "Can we get a sense of the intensity level of each
>     activity?  Is the karate focused on drills and sparring, or more on
>     technique?  How much active time is involved in each session, versus
>     downtime?"
> *   **Addressing Others:** "I agree with the Sleep Specialist that inadequate
>     sleep exacerbates the physical stress. The body repairs and recovers
>     during sleep, and with this level of activity, it's crucial."
> 
> **2. The Child Educational Psychologist:**
> 
> *   **Presentation:** "From an academic and cognitive perspective, chronic
>     fatigue significantly impacts concentration, memory, and motivation. The
>     drop in academic performance is a direct consequence we often see with
>     overloaded schedules. The cognitive load of switching between different
>     activities, combined with potential sleep deprivation, can be
>     overwhelming for a 10-year-old. The transition to intermediate school
>     will also add new academic pressures."
> *   **Guiding Question:** "Has there been any noticeable change in her
>     engagement with schoolwork or her attitude towards learning?  Are there
>     specific subjects where the decline is more pronounced?"
> *   **Addressing Others:** "The Family Wellness Consultant's point about
>     family dynamics is important. Stress and tiredness can affect her
>     interactions at home, and it's vital to create a supportive environment
>     that prioritizes well-being over constant achievement."
> 
> **3. The Youth Sports Coach (Generalist):**
> 
> *   **Presentation:** "While it's fantastic that she's passionate and
>     talented, enjoyment is key at this age. Burnout is a real risk when kids
>     feel pressured or lose the fun aspect of their activities. The fact that
>     she's getting tired and sick more often suggests the balance has tipped
>     too far towards obligation rather than pure enjoyment. We need to ensure
>     she still has time for unstructured play and simply being a kid."
> *   **Guiding Question:** "Does she express excitement about going to all
>     these activities, or are there any signs of reluctance or resistance? Has
>     she ever mentioned wanting to cut back on anything?"
> *   **Addressing Others:** "I appreciate the Pediatric Exercise
>     Physiologist's focus on physical strain, but we also need to consider the
>     emotional toll of constantly being on the go. Even activities she loves
>     can become stressors if there's no downtime."
> 
> **4. The Family Wellness Consultant:**
> 
> *   **Presentation:** "My concern lies in the overall family system. An
>     overloaded child often means an overloaded family. Parents become taxi
>     drivers and schedulers, and family time can become fragmented and focused
>     solely on the child's commitments. We need to consider the impact on
>     family meals, quality time together, and the parents' well-being as well.
>     The excitement about fencing is understandable, but we need to assess if
>     adding another commitment is sustainable for everyone."
> *   **Guiding Question:** "How is this schedule impacting family routines and
>     the time you spend together as a family unit?  Are there moments of
>     stress or conflict related to managing the schedule?"
> *   **Addressing Others:** "The Educational Psychologist's point about the
>     transition to intermediate school is crucial. That in itself will be a
>     significant adjustment, and adding more to her plate might be
>     counterproductive to her success in that new environment."
> 
> **5. The Child Sleep Specialist:**
> 
> *   **Presentation:** "Adequate sleep is the foundation for a child's
>     physical and cognitive health. With this level of activity, sufficient
>     sleep is non-negotiable. Tiredness and increased susceptibility to
>     illness are classic signs of sleep deprivation. The brain needs time to
>     consolidate learning and the body needs time to repair. A 10-year-old
>     generally needs 9-11 hours of sleep per night. With her current schedule,
>     I'm concerned about whether she's consistently achieving that."
> *   **Guiding Question:** "What is her typical bedtime and wake-up time on
>     school nights and weekends?  Are there any difficulties falling asleep or
>     staying asleep?"
> *   **Addressing Others:** "I agree with the Youth Sports Coach that burnout
>     is a risk, and lack of sleep significantly contributes to it. When a
>     child is sleep-deprived, even enjoyable activities can feel like a
>     burden."
> 
> **Synthesis and Summary of Round 1:**
> 
> The initial round of discussion reveals a consensus that the daughter's
> current schedule is likely unsustainable and negatively impacting her health,
> academic performance, and potentially her overall well-being. Key themes
> emerging include:
> 
> *   **Physical Overtraining and Insufficient Recovery:** The sheer volume and
>     intensity of her activities raise concerns about physical strain and the
>     body's ability to recover adequately.
> *   **Cognitive Overload and Academic Impact:**  Fatigue and a busy schedule
>     are likely contributing to the observed decline in academic performance
>     and engagement.
> *   **Risk of Burnout and Loss of Enjoyment:**  While passion is positive,
>     the current schedule might be pushing her past the point of genuine
>     enjoyment into a realm of obligation and stress.
> *   **Impact on Family Dynamics:** The demands of the schedule are likely
>     affecting family routines, quality time, and potentially creating stress
>     for the parents as well.
> *   **Potential Sleep Deprivation:** There's a strong indication that she
>     might not be getting enough sleep, which exacerbates all the other
>     concerns.
> 
> The guiding questions raised by each expert highlight the need to gather more
> specific information about the intensity of each activity, her personal
> feelings about the schedule, its impact on family life, and her sleep
> patterns. The team agrees that a re-evaluation of the schedule is necessary,
> with a focus on finding a healthier balance that prioritizes her well-being
> while still allowing her to pursue her passions.

The file is saved as ~/.consilio/2024-12-25-My-daughter-schedule/round-1.md.

Next step:
* `cons` to start the next round of discussions.

$ cons
Please provide guidance for the discussion. (Answer questions from the previous round of discussions, or specify a particular area you'd like to focus on next. CTRL+D when you finish.)
>>> We have had discussions with her for a few times. She is not willing to give up any of her activities. How do we approach this?
Starting discussions (Round #2) ...

> ## Round 2: Team Meeting - Addressing Resistance to Change 
> 
> ...
> ...
```

## Decision Philosophy

Consilio is a file-centric program. Every interaction is saved as
a text file. Use your unix power tools to review responses and search
for discussions from past decisions.

Check this document into your version control system to maintain a record of your decision-making process.

All intermediate steps are preserved in structured format within a date-stamped
directory, creating a detailed record of the decision-making process. This
allows for both immediate reference and retrospective review of how important
decisions were made.

## Inspiration

- [Virtual Lab](https://github.com/zou-group/virtual-lab): The Virtual Lab is an AI-human collaboration for science research. [x.com](https://x.com/james_y_zou/status/1856729107045982607)
- [tenx](https://github.com/cortesi/tenx): For the idea of encouraging the use of editors for fine control over the context.

## See Also

- [CONTRIBUTING.md](CONTRIBUTING.md) document for the contribution guidelines.
- [Python.md](Python.md) document for the coding style guide.
- [Issues](https://github.com/alexdong/consilio/issues) for the list of issues and feature requests.

[^1]: Consilio is a Latin term that embodies concepts such as counsel, deliberation, and wisdom. In ancient times, "consilium" referred to a group of advisors or a council that deliberated on important decisions, reflecting a process of careful consideration and planning. The term is associated with strategic thinking and prudent decision-making, emphasizing the use of good judgment, experience, and advice.
[^2]: The name `cons` is a shortcut for `consilio`. It's called `cons` because just like LISP's `cons`, it constructs structures that you can manipulate, shape and transform. This is what I envision Consilio to be - a tool that helps you construct your thoughts, opinions, and decisions in a structured manner.
