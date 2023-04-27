import json
import re
from datasets import Dataset
import os
from backend.common.marc.training.model_tuner import ModelTuner
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

# Load GSM8K Dataset
class MathDataset:
    @staticmethod
    def __process_answer(answer):
        # Process Answer From GSM8K Dataset
        CALCULATOR_PATTERN = r"<<.*?>>"
        SOLUTION_PATTERN = "####"
        answer = re.sub(CALCULATOR_PATTERN, "", answer)
        answer = answer.replace(SOLUTION_PATTERN, "The answer is")
        return answer

    @staticmethod
    def __read_dataset(path):
        with open(path) as f:
            dataset = [json.loads(line) for line in f.readlines() if line]
        
        for data in dataset:
           data["answer"] = MathDataset.__process_answer(data["answer"])
        
        return dataset
    
    @staticmethod
    def process_data(dataset, tokenizer):
        # Generate Inputs and Targets
        inputs, targets = dataset["question"][:3], dataset["answer"][:3]

        # Tokenize Input
        model_inputs = tokenizer(inputs, max_length=1024, padding="max_length", truncation=True)
        model_labels = tokenizer(text=targets, max_length=256, padding="max_length", truncation=True)

        model_inputs["labels"] = model_labels["input_ids"]
        return model_inputs

    @staticmethod
    def load_dataset(path_to_training_json, path_to_test_json):
        training_dataset = Dataset.from_list(MathDataset.__read_dataset(path_to_training_json))
        testing_dataset = Dataset.from_list(MathDataset.__read_dataset(path_to_test_json))

        return training_dataset, testing_dataset

def train_model():
    output_directory = f"{__location__}/../trained_model"
    path_to_training_json = f"{__location__}/../datasets/gsm8k_training.jsonl"
    path_to_test_json = f"{__location__}/../datasets/gsm8k_test.jsonl"
    model_name = "google/flan-t5-base"

    # Load Dataset
    training_dataset, testing_dataset = MathDataset.load_dataset(path_to_training_json, path_to_test_json)
    
    # Tune Model
    ModelTuner.tune_model(training_dataset, testing_dataset, MathDataset.process_data, model_name, output_directory)

if __name__ == "__main__":
    train_model()