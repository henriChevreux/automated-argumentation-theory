import typer
import subprocess
from rich import print as rprint

# CLI commands

app = typer.Typer()

@app.command()
def credits():
    rprint(f"[green bold]This software is being developed in the context of an undergraduate research project, under the supervision of Dr. Odinaldo Rodrigues at King's College London.[green bold]")
        
@app.command()
def run_pipeline(filepath:str):
    import build_pairs
    import predict_relationships
    from InquirerPy import prompt
    import construct_AF
    
    rprint(f"[green bold]Starting the pipeline with input data {filepath}.[green bold]")
    pairs_filename = build_pairs.build_pairs(filepath)
    rprint(f"[green bold]Pairs of arguments successfully saved at {pairs_filename}.[green bold]")
    relationships_filename = predict_relationships.run_pipeline_subprocess(filepath)
    rprint(f"[green bold]Relationships successfully saved in file {relationships_filename}.[green bold]")
    rprint(f"[green bold]Constructing argumentation framework...[green bold]")
    args_filename, graph_filename = construct_AF.run_construct_AF_subprocess(relationships_filename)
    rprint(f"[green bold]Graph successfully saved at {graph_filename}.[green bold]")
    rprint(f"[green bold]Abstraction dictionary successfully saved at {args_filename}.[green bold]")
    
    # Prompt whether user wants to perform reasoning tasks
    reasoning_task_question = questions = [
        {
            'type': 'list',
            'name': 'reasoning_bool',
            'message': 'Proceed with a reasoning task?',
            'choices': ['Yes', 'No'],
        },
    ]
    proceed_prompt = prompt(reasoning_task_question)
    launch_reasoning_pipeline = proceed_prompt['reasoning_bool']
    if launch_reasoning_pipeline == 'Yes':
        rprint(f"[green bold]Proceeding to reasoning task...[green bold]")
        calculate_extensions(graph_filepath = graph_filename, args_filepath = args_filename)
    else:
        rprint(f"[green bold]Closing pipeline.[green bold]")


@app.command()
def calculate_extensions(
    graph_filepath: str,
    args_filepath: str,
):
    import subprocess
    from InquirerPy import prompt
    import construct_AF
    import os
    
    # The task and semantics to be sent to the solver, according to ICCMA norms
    solver_task = ""
    
    problems_codes = {
        "Calculate a single extension": "SE",
        "Calculate credulous acceptance of an argument": "DC",
        "Calculate skeptical acceptance of an argument": "DS",
    }
    
    semantics_codes = {
        "Grounded": "GR",
        "Preffered": "PR",
        "Stable": "ST",
        "Semi-stable": "SST",
        "Complete": "CO",
        "Ideal": "ID",
    }
    
    subtrack_selection_questions = questions = [
        {
            'type': 'list',
            'name': 'problem_selection',
            'message': 'Select a reasoning task: ',
            'choices': problems_codes.keys(),
        },
        {
            'type': 'list',
            'name': 'semantics_selection',
            'message': 'Select an argumentation semantics: ',
            'choices': semantics_codes.keys(),
        }
    ]

    subtrack_prompt = prompt(subtrack_selection_questions)
    problem_code = problems_codes.get(subtrack_prompt['problem_selection'])
    semantics_code = semantics_codes.get(subtrack_prompt['semantics_selection'])
    
    subtrack = problem_code + "-" + semantics_code
    rprint("[yellow]=============================================[yello]")
    
    
    if problem_code == "SE":
        solver_command = f"./crustabri/target/release/crustabri solve -p {subtrack} -f {graph_filepath}"
        # Run solver with params
        output = subprocess.check_output(
            solver_command, 
            shell=True,
        )
            
        output = output.decode("utf-8")
        output = output.split("\n")
        # extract extension from output and remove prefix
        extension = output[-3][2:]
        # Convert to list of abstract arguments
        abstract_ext = list(extension.split(" "))
        # un-abstract extension
        args_plain = construct_AF.unabstract_extension(extension=abstract_ext, args_filepath=args_filepath)
            
        print(args_plain)

    if problem_code == "DS" or problem_code == "DC":
        args = construct_AF.get_arguments(args_filepath=args_filepath)
        print(args)
        
        arg_selection_question = questions = [
            {
                'type': 'list',
                'name': 'arg_selection',
                'message': 'Select an argument: ',
                'choices': args.keys(),
            },
        ]
        arg_prompt = prompt(arg_selection_question)
        arg_code = args.get(arg_prompt['arg_selection'])
        
        solver_command = f"./crustabri/target/release/crustabri solve -p {subtrack} -f {graph_filepath} -a {arg_code}"
        # Run solver with params
        output = subprocess.check_output(
            solver_command,
            shell=True,
        )
            
        output = output.decode("utf-8")
        output = output.split("\n")
        # extract response from output
        result = output[-3]

        print(result)

if __name__ == "__main__":
    app()
