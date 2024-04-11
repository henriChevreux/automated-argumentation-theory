import pandas as pd
import pickle
import os
        

def process_excel_file(filename):
    columns = ["argumentAttacked", "argumentAttacking", "relationship"]
    df = pd.read_excel(filename, header=None, names=columns)
    return df

def process_csv_file(filename):
    columns = ["argumentAttacked", "argumentAttacking", "relationship"]
    df = pd.read_csv(filename, header=None, names=columns)
    return df

def construct_af(df):
    # only keep attacks
    df_attack = df.loc[df["relationship"] == 'a']
    args = {}
    af = []

    # abstract away the arguments
    for index, relationship in df_attack.iterrows():
        if not args.get(relationship["argumentAttacked"]):
            arg_code = str(len(args) + 1)
            args[relationship["argumentAttacked"]] = arg_code

        if not args.get(relationship["argumentAttacking"]):
            arg_code = str(len(args) + 1)
            args[relationship["argumentAttacking"]] = arg_code

    # We have our abstracted arguments list, we now construct the graph
    for index, relationship in df_attack.iterrows():
        argumentAttackedcode = args.get(relationship["argumentAttacked"])
        argumentAttackingcode = args.get(relationship["argumentAttacking"])
        if argumentAttackedcode and argumentAttackingcode:
            af.append(argumentAttackingcode + " " + argumentAttackedcode)

    return af, args

def display_net_format(args, af):
    print("*Vertices " + str(len(args)))
    for i in range(1, len(args) + 1):
        print(str(i) + " " + "\"" + str(i) + "\"")

    print("*Arcslist ")
    for edge in af:
        print(edge)

def display_af_format(args, af):
    print("p af " + str(len(args)))

    for edge in af:
        print(edge)

def save_af_format(filename, args, af):
    basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    args_filename = f"output/{basename_without_ext}_args.pkl"
    graph_filename = f"output/{basename_without_ext}_graph.af"
    # Save arguments abstraction dictionary
    with open(args_filename, 'wb') as f:
        pickle.dump(args, f)
    # Save graph in net format
    f = open(graph_filename, "w")
    f.write("p af " + str(len(args)) + "\n")
    for edge in af:
        f.write(edge + "\n")
    f.close()
    
    return args_filename, graph_filename

def save_net_format(filename, args, af):
    basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    args_filename = f"output/{basename_without_ext}_args.pkl"
    graph_filename = f"output/{basename_without_ext}_graph.net"
    # Save arguments abstraction dictionary
    with open(args_filename, 'wb') as f:
        pickle.dump(args, f)
    # Save graph in net format
    f = open(graph_filename, "w")
    f.write("*Vertices " + str(len(args))+"\n")
    for i in range(1, len(args) + 1):
        f.write(str(i) + " " + "\"" + str(i) + "\"" + "\n")

    f.write("*Arcslist \n")
    for edge in af:
        f.write(edge + "\n")
    f.close()
    
    return args_filename, graph_filename

def unabstract_extension(extension:list, args_filepath):
    # Load arguments dictionary
    import pickle
        
    with open(f'{args_filepath}', 'rb') as f:
        args = pickle.load(f)
    
    # Calculate inverse arguments dictionary
    args_inv = {v: k for k, v in args.items()}
    
    # Retrieve arguments from dictionary
    args_plain = []
    for arg in extension:
        args_plain.append(args_inv.get(arg))

    return args_plain

def get_arguments(args_filepath)->dict:
    # Load arguments dictionary
    import pickle
    
    args = None
        
    with open(f'{args_filepath}', 'rb') as f:
        args = pickle.load(f)

    return args

def run_construct_AF_subprocess(filename):
    # Assume csv file
    df_processed = process_csv_file(filename)
    af, args = construct_af(df_processed)
    inv_args = {v: k for k, v in args.items()}
    # Save in af file format
    args_filename, graph_filename = save_af_format(filename, args, af)
    
    return args_filename, graph_filename
