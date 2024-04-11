import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import pandas as pd
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Flatten, Dense
from rich import print as rprint

def load_csv(filepath):
    # Import csv dataset
    features = ["argument1", "argument2"]
    df = pd.read_csv(filepath, usecols=features)    
    df = shuffle(df).reset_index(drop=True)
    # Split features and labels
    X = df[features]
    
    return X

def load_tokenizer():
    tokenizer = []
    with open('Predict_relationships/saved_tokenizers/tokenizer_full.json') as f:
        data = f.read()
        tokenizer = tokenizer_from_json(data)

    return tokenizer

def process_data(X):
    # Split pairs of sentences
    sentences_1 = X["argument1"].to_numpy()
    sentences_2 = X["argument2"].to_numpy()

    # Load tokenizer
    tokenizer = load_tokenizer()
    
    # Encode data
    sequences_1 = tokenizer.texts_to_sequences(sentences_1)
    sequences_2 = tokenizer.texts_to_sequences(sentences_2)

    # Padding sequences to have the same length
    max_len = 50
    padded_sequences_1 = pad_sequences(sequences_1, maxlen=max_len, padding='post')
    padded_sequences_2 = pad_sequences(sequences_2, maxlen=max_len, padding='post')
    
    return [padded_sequences_1, padded_sequences_2]

def predict_relationships(X, padded_sequences, model):
    # Load model
    model = tf.keras.models.load_model(f"Predict_relationships/saved_models/{model}")
   
    y = model.predict(padded_sequences)

    label_map = {
        '1': 'n',
        '0': 'a',
        '2': 's',
    }

    predictions_labels = []

    # Get labels of predictions
    for i in range(len(y)):
        arg = str(np.argmax(y[i]))
        arg_dec = label_map.get(arg)
        predictions_labels.append(arg_dec)
        
    X['relationship'] = predictions_labels
    
    return X

def save_csv(df, filepath):
    directory_out = "out/predict_relationships_sp"
    if not os.path.exists(directory_out):
        os.makedirs(directory_out)
    
    basename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
    output_filename = f"{directory_out}/{basename_without_ext}.csv"
    df.to_csv(output_filename)
    
    return output_filename

def run_predict_relationships_subprocess(filepath, model):
    X =load_csv(filepath=filepath)
    sequences = process_data(X)
    relationships = predict_relationships(X, sequences, model)
    output_filename = save_csv(df=relationships, filepath=filepath)
    
    return output_filename