import pandas as pd
import os
import json
from datasets import Dataset
from sklearn.utils import shuffle
import ast

pd.set_option("display.max_colwidth", None)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
path_to_training_csv = f"{__location__}/prosocial/training_dataset.csv"
path_to_validation_csv = f"{__location__}/prosocial/validation_dataset.csv"

class QuestionDataset:
    @staticmethod
    def __prepare_dataset(df, dataset):
        position = 0
        for data in dataset:
            tag, patterns = data["safety_label"].replace("__", ""), data["context"]
            responses = [data["response"]] + [response for response in data["rots"] if response]
            df.loc[position] = [tag] + [patterns] + [responses]
            position += 1

    @staticmethod
    def __read_dataset(path):
        with open(path) as f:
            dataset = [json.loads(line) for line in f.readlines() if line]
        
        return dataset

    @staticmethod
    def load_dataset(path_to_training_json, path_to_test_json):
        training_dataset = Dataset.from_list(QuestionDataset.__read_dataset(path_to_training_json))
        testing_dataset = Dataset.from_list(QuestionDataset.__read_dataset(path_to_test_json))

        return training_dataset, testing_dataset

    @staticmethod
    def prepare():
        # Load Dataset
        path_to_training_json = f"{__location__}/train.json"
        path_to_test_json = f"{__location__}/validation.json"

        training_dataset, validation_dataset = QuestionDataset.load_dataset(path_to_training_json, path_to_test_json)

        # Create Training & Validation DataFrames
        df_training = pd.DataFrame(columns=['tag', 'patterns', 'responses'])
        df_validation = pd.DataFrame(columns=['tag', 'patterns', 'responses'])

        # Prepare Training & Validation Datasets
        QuestionDataset.__prepare_dataset(df_training, training_dataset)
        QuestionDataset.__prepare_dataset(df_validation, validation_dataset)

        # Shuffle Dataset
        df_training = shuffle(df_training)
        df_validation = shuffle(df_validation)

        # Save To CSV Files
        df_training.to_csv(path_to_training_csv, index=False)
        df_validation.to_csv(path_to_validation_csv, index=False)
    
    @staticmethod
    def convert_to_intent_json():
        training_dataset = pd.read_csv(path_to_training_csv)
        with open(f"{__location__}/prosocial/prosocial_intent.json", 'w') as f:
            json.dump({
                "intents": [{
                "tag": training_dataset.loc[i, "tag"],
                "patterns": [training_dataset.loc[i, "patterns"]],
                "responses": ast.literal_eval(training_dataset.loc[i, "responses"]),
                "context_set": "" } for i in range(len(training_dataset))]}, f)


if __name__ == "__main__":
    QuestionDataset.convert_to_intent_json()