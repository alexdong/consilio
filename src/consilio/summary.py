import click
from .models import Topic

def generate_summary(topic: Topic) -> None:
    """Generate a summary of all discussion rounds"""
    if not topic.discussion_file.exists():
        click.echo("No discussion file found.")
        return

    rounds: List[Round] = []
    
    # Gather all rounds
    current_round = 1
    while True:
        input_file = topic.round_input_file(current_round)
        response_file = topic.round_response_file(current_round)
        
        if not input_file.exists() or not response_file.exists():
            break
            
        rounds.append(Round(
            number=current_round,
            input=input_file.read_text(),
            response=response_file.read_text()
        ))
        current_round += 1

    if not rounds:
        click.echo("No discussion rounds found.")
        return

    # Generate summary using template
    prompt = render_template("summary.j2", topic=topic, rounds=rounds)
    system_prompt = render_template("system.j2")

    try:
        summary = get_llm_response(prompt, system_prompt=system_prompt)
        
        # Save summary
        summary_file = topic.directory / "summary.md"
        summary_file.write_text(summary)
        click.echo(f"Summary generated and saved to: {summary_file}")
        
    except Exception as e:
        click.echo(f"Error generating summary: {str(e)}")
