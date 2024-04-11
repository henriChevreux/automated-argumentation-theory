def build_pairs(fp):
    import pandas as pd
    import os
    
    from nltk.tokenize import sent_tokenize 

    # Get sentences from text
    f = open(fp, "r")
    text = f.read()
    tokens = sent_tokenize(text)

    # Pre-process arguments
    tokens = pre_process(tokens)
    
    pairs = []
    # Cartesian product of arguments
    for i in range(0,len(tokens)):
        for j in range(0,len(tokens)):
            if (i!=j):
                pairs.append((tokens[i],tokens[j]))
    df = pd.DataFrame(data=pairs)

    basename_without_ext = os.path.splitext(os.path.basename(fp))[0]
    out_path = f"out/{basename_without_ext}_pairs.csv"
    df.to_csv(out_path, header=False)

    return out_path

def pre_process(args):
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    temp_args = remove_stopwords(args)
    temp_args = to_lowercase(temp_args)
    temp_args = remove_non_alpha(temp_argss)

    return temp_args

"""
helper methods for pre-processing arguments, inspired by methods in https://www.geeksforgeeks.org/text-preprocessing-in-python-set-1/
"""

def remove_stopwords(args):
    proc_args = []
    stop_words = set(stopwords.words("english"))
    for arg in args:
        word_tokens = word_tokenize(arg)
        filtered_text = [word for word in word_tokens if word not in stop_words]
        proc_args.append(' '.join(filtered_text))

    return proc_args
        

def to_lowercase(args):
    proc_args = []
    for arg in args:
        proc_args.append(arg.lower())

    return proc_args

def remove_non_alpha(args):
    import re
    re_args = []
    for arg in args:
        temp = re.sub(r'[\W]+', ' ', arg)
        temp = "".join(x for x in arg if x.isalpha() or x.isspace()).strip()
        temp = re.sub(' +', ' ', temp)
        re_args.append(temp)

    return re_args
