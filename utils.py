import os
from pathlib import Path
import random
from typing import Dict, Optional

import yaml
from dataclasses import dataclass
from jinja2 import Template

import anthropic


# XML Utils
def escape_xml_string(xml_string):
    # Common XML escapes
    replacements = {
        "&": "&amp;",
    }

    # Replace special characters with their escaped versions
    for char, escape in replacements.items():
        xml_string = xml_string.replace(char, escape)

    return xml_string.strip()


# Claude Integration
@dataclass
class ClaudeResponse:
    content: str
    raw: Dict  # Store raw API response


def query_claude(
    user_prompt: str,
    system_prompt: Optional[str] = None,
    assistant: Optional[str] = None,
    temperature: float = 0.7,
) -> ClaudeResponse:
    """Send query to Claude and get response"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=temperature,
        system=system_prompt if system_prompt else "",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant}] if assistant else [],
            },
        ],
    )
    content = "".join(block.text for block in message.content if block.type == "text")
    return ClaudeResponse(content=content, raw=message.model_dump())


# Config Management
@dataclass
class Context:
    domain: str
    perspective: str
    user_role: str


def load_context(config_path: Optional[Path] = None) -> Context:
    """Load context from yaml file"""
    if not config_path:
        config_path = Path(".consilio.yml")

    with open(config_path) as f:
        data = yaml.safe_load(f)

    return Context(**data)


# Prompt Management
@dataclass
class PromptTemplate:
    system: str
    user: str


def load_prompt_template(stage: str) -> PromptTemplate:
    """Load system and user prompts for a given stage"""
    base_path = Path("Prompts")
    system = (base_path / "SystemPrompt.md").read_text()
    user = (base_path / f"UserPrompt-{stage}.md").read_text()
    return PromptTemplate(system=system, user=user)


def render_prompt(template_str: str, context: Dict[str, str]) -> str:
    """Use Jinja2 template to replace placeholders with context values"""
    template = Template(template_str)
    return template.render(context)


# Quotes


def get_random_decision_quote():
    quotes = [
        (
            "Every decision you make reflects your evaluation of who you are.",
            "Marianne Williamson",
        ),
        ("Decision making is easy when your values are clear.", "Roy Disney"),
        (
            "Life is about choices. Some we regret, some we're proud of. Some will haunt us forever. The message: we are what we chose to be.",
            "Graham Brown",
        ),
        (
            "Some of our important choices have a time line. If we delay a decision, the opportunity is gone forever. Sometimes our doubts keep us from making a choice that involves change. Thus an opportunity may be missed.",
            "James E. Faust",
        ),
        (
            "We may think that our decisions are guided purely by logic and rationality, but our emotions always play a role in our good decision making process.",
            "Salma Stockdale",
        ),
        (
            "The quality of your life is built on the quality of your decisions.",
            "Wesam Fawzi",
        ),
        ("Decision is a risk rooted in the courage of being free.", "Paul Tillich"),
        ("Decision making is the specific executive task.", "Peter Drucker"),
        ("May your choices reflect your hopes, not your fears.", "Nelson Mandela"),
        (
            "All of us start from zero. We take the right decision and become a hero.",
            "Govinda",
        ),
        ("You cannot make progress without making decisions.", "Jim Rohn"),
        ("There's no wrong time to make the right decision.", "Dalton McGuinty"),
        (
            "Every decision brings with it some good, some bad, some lessons, and some luck. The only thing that's for sure is that indecision steals many years from many people who wind up wishing they'd just had the courage to leap.",
            "Doe Zantamata",
        ),
        (
            "Decision making is power. Most people don't have the guts to make 'tough decision' because they want to make the 'right decision' and so they make 'no decision'. Remember, live is short, so do things that matter the most and have the courage to make 'tough decision' and to chase your dreams.",
            "Yama Mubtakeraker",
        ),
        ("A good decision is based on knowledge and not on numbers.", "Plato"),
        (
            "There are times when delaying a decision has benefit. Often, allowing a set period of time to mull something over so your brain can work it through generates a thoughtful and effective decision.",
            "Nancy Morris",
        ),
        ("A decision clouded with doubt is never a good decision.", "Steven Aitchison"),
        ("The art of decision making includes the art of questioning.", "Pearl Zhu"),
        (
            "When faced with a decision, choose the path that feeds your soul.",
            "Dorothy Mendoza Row",
        ),
        (
            "Be open about your thoughts, ideas, and desires and you will be right with your decisions.",
            "Auliq Ice",
        ),
        (
            "Never make a decision when you are upset, sad, jealous or in love.",
            "Mario Teguh",
        ),
        (
            "Think 100 times before you take a decision, but once that decision is taken, stand by it as one man.",
            "Muhammad Ali Jinnah",
        ),
        (
            "Whenever you're making an important decision, first ask if it gets you closer to your goals or farther away. If the answer is closer, pull the trigger. If it's farther away, make a different choice. Conscious choice making is a critical step in making your dreams a reality.",
            "Jillian Michaels",
        ),
        (
            "Always make decisions that prioritize your inner peace.",
            "Izey Victoria Odiase",
        ),
        (
            "The goal shouldn't be to make the perfect decision every time but to make less bad decisions than everyone else.",
            "Spencer Fraseur",
        ),
        (
            "Don't let adverse facts stand in the way of a good decision.",
            "Colin Powell",
        ),
        (
            "Great decision-making comes from the ability to create the time and space to think rationally and intelligently about the issue at hand.",
            "Graham Allcot",
        ),
        (
            "Poor decision making I think, is the number one cause for most of our mistakes. So to make fewer mistakes means to make better decisions, and to make better decisions you must train yourself to think more clearly.",
            "Rashard Royster",
        ),
        (
            "Make decisions with the long term in mind. If you were truly the owner of your company and the success or failure of your business hinged on the performance of your team, you would dedicate yourself to constant improvement.",
            "David Miller",
        ),
        (
            "Whenever you see a successful business, someone once made a courageous decision.",
            "Peter F Drucker",
        ),
        (
            "Great leaders don't lead others with bitterness or resentfulness of past mistakes, they lead with hope and knowledge of the past to inform greater decision making in the future.",
            "Spencer Fraseur",
        ),
    ]

    quote, author = random.choice(quotes)
    return f'"{quote}" - {author}'


# Example usage:
# print(get_random_decision_quote())
