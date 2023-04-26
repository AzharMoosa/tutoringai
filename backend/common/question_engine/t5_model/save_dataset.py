import pandas as pd
import os
from datasets import load_dataset
from sklearn.utils import shuffle

pd.set_option("display.max_colwidth", None)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
path_to_training_csv = f"{__location__}/dataset/training_dataset.csv"
path_to_validation_csv = f"{__location__}/dataset/validation_dataset.csv"

class QuestionDataset:
    @staticmethod
    def __prepare_dataset(df, dataset, answer_length_limit=7):
        position = 0
        for data in dataset:
            context, question = data["context"], data["question"]
            answer = data["answers"]["text"][0]
            answer_length = len(answer.split())

            if answer_length >= answer_length_limit:
                continue

            df.loc[position] = [context] + [answer] + [question]
            position += 1

    @staticmethod
    def prepare():
        # Load Squad Dataset
        training_dataset = load_dataset("squad", split="train")
        validation_dataset = load_dataset("squad", split="validation")

        # Create Training & Validation DataFrames
        df_training = pd.DataFrame(columns=['context', 'answer', 'question'])
        df_validation = pd.DataFrame(columns=['context', 'answer', 'question'])

        # Prepare Training & Validation Datasets
        QuestionDataset.__prepare_dataset(df_training, training_dataset)
        QuestionDataset.__prepare_dataset(df_validation, validation_dataset)

        # Shuffle Dataset
        df_training = shuffle(df_training)
        df_validation = shuffle(df_validation)

        # Save To CSV Files
        df_training.to_csv(path_to_training_csv, index=False)
        df_validation.to_csv(path_to_validation_csv, index=False)

if __name__ == "__main__":
    QuestionDataset.prepare()