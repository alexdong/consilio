from pathlib import Path
from typing import List, Dict
import xml.etree.ElementTree as ET

from .state import WorkflowState
from ai.prompts import load_prompt_template, render_prompt
from ai.claude import query_claude


def extract_perspectives(xml_content: str) -> List[Dict[str, str]]:
    """Extract perspectives from observation XML"""
    root = ET.fromstring(xml_content)
    perspectives = []

    for p in root.findall(".//perspective"):
        perspectives.append(
            {"title": p.find("title").text, "question": p.find("question").text}
        )

    return perspectives


def run_consultation(state: WorkflowState, cloud_config: Dict) -> List[str]:
    """Run perspective consultation stage"""
    print("[💭] Starting consultation phase...")

    # Load previous content
    statement = (state.decision_dir / "Statement.md").read_text()
    observation = (state.decision_dir / "Observation.xml").read_text()

    # Extract perspectives
    perspectives = extract_perspectives(observation)

    # Load prompt templates
    prompts = load_prompt_template(state.stage.value)

    responses = []
    for p in perspectives:
        print(f"[🗣️] Consulting {p['title']}...")

        # Format prompts
        system_prompt = render_prompt(prompts.system, {"perspective": p["title"]})
        user_prompt = render_prompt(
            prompts.user,
            {
                "FOUNDER_SITUATION": statement,
                "ADVISOR_OBSERVATION": observation,
                "questions": p["question"],
            },
        )

        # Query Claude
        response = query_claude(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            api_key=cloud_config["claude_key"],
        )
        responses.append(response.content)

    # Save perspectives
    perspectives_xml = "<perspectives>\n" + "\n".join(responses) + "\n</perspectives>"
    perspectives_path = state.decision_dir / "Perspectives.xml"
    perspectives_path.write_text(perspectives_xml)

    print("[✅] Consultation complete")
    return responses
