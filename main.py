import sys
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear
from typing import Optional

from utils import load_context, get_random_decision_quote
from workflow import State
from storage import create_decision_dir
import observe
import consult

def display_welcome():
    """Display welcome message and random quote"""
    clear()
    print("Welcome to Consilio.\n")
    print(get_random_decision_quote())
    print("\nMay you make wise decisions.\n")

def run_repl(state: State):
    """Run the interactive REPL"""
    session = PromptSession()
    
    while True:
        try:
            command = session.prompt("\nEnter command (observe/consult) or Ctrl+C to exit: ")
            
            if command == "observe":
                result = observe.observe(state.doc_path, state.context)
                print(result)
            elif command == "consult": 
                result = consult.consult(state.doc_path, "", state.context)
                print(result)
            else:
                print("Invalid command. Please use 'observe' or 'consult'")
                
        except KeyboardInterrupt:
            print("\nExiting Consilio...")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {str(e)}")

def main(context_path: Optional[Path] = None, doc_path: Optional[Path] = None):
    """Main entry point for Consilio"""
    display_welcome()

    # Load context
    context = load_context(context_path)
    
    if not doc_path:
        doc_path = Path(input("Enter path to decision document: "))
    
    # Create decision directory
    decision_dir = create_decision_dir(doc_path.stem)
    
    # Initialize state
    state = State(
        decision_dir=decision_dir,
        context={"domain": context.domain, 
                "user_role": context.user_role,
                "perspective": context.perspective},
        stage="observe",
        doc_path=doc_path
    )
    
    # Start REPL
    run_repl(state)


if __name__ == "__main__":
    main()
