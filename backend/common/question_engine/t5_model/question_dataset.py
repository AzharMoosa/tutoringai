import pandas as pd
from torch.utils.data import Dataset
import copy

class QuestionDataset(Dataset):
    def __init__(self, tokenizer, dataset_path: str, max_input_length: int = 512, max_output_length: int = 96) -> None:
        self.dataset_path = dataset_path
        self.dataset = pd.read_csv(dataset_path)
        self.max_input_length = max_input_length
        self.max_output_length = max_output_length
        self.tokenizer = tokenizer
        self.inputs = []
        self.targets = []

        self.__create()
    
    def __len__(self):
        return len(self.inputs)
    
    def __getitem__(self, index):
        source_input_ids = self.inputs[index]["input_ids"].squeeze()
        target_input_ids = self.targets[index]["input_ids"].squeeze()

        source_attention_mask = self.inputs[index]["attention_mask"].squeeze()
        target_attention_mask = self.targets[index]["attention_mask"].squeeze()

        labels = copy.deepcopy(target_input_ids)
        labels[labels == 0] = -100

        return { "source_input_ids" : source_input_ids, "target_input_ids": target_input_ids, "source_attention_mask": source_attention_mask, "target_attention_mask": target_attention_mask, "labels": labels }

    def __create(self):
        def is_greater_than_max_length(input):
            input_encoding = self.tokenizer.encode_plus(input, truncation=False, return_tensors="pt")
            input_encoding_length = len(input_encoding["input_ids"][0])
            return input_encoding_length > self.max_input_length

        for i in range(len(self.dataset)):
            context = self.dataset.loc[i, "context"]
            answer = self.dataset.loc[i, "answer"]
            question = self.dataset.loc[i, "question"]

            input = f"context: {context}  answer: {answer} </s>"
            target = f"question: {str(question)} </s>"

            if is_greater_than_max_length(input):
                continue

            input_tokenized = self.tokenizer.batch_encode_plus([input], max_length=self.max_input_length, padding="max_length", return_tensors="pt")
            targets_tokenized = self.tokenizer.batch_encode_plus([target], max_length=self.max_output_length, padding="max_length", return_tensors="pt")

            self.inputs.append(input_tokenized)
            self.targets.append(targets_tokenized)
