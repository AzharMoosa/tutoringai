from datasets import Dataset
import datasets
import numpy as np
import transformers
from datasets import Dataset
from functools import partial
import torch
torch.cuda.empty_cache()
from datetime import datetime

class ModelTuner:
    @staticmethod
    def __prepare_training_testing_dataset(process_dataset, training_dataset, testing_dataset):
        training_dataset = training_dataset.map(
            process_dataset,
            batched=True,
            remove_columns=training_dataset.column_names,
            load_from_cache_file=False,
            desc="Tokenizing Training Dataset"
        )

        testing_dataset = testing_dataset.map(
            process_dataset,
            batched=True,
            num_proc=8,
            remove_columns=testing_dataset.column_names,
            load_from_cache_file=False,
            desc="Tokenizing Test Dataset"
        )

        return training_dataset, testing_dataset

    @staticmethod
    def __get_training_arguments(output_directory):
        return transformers.TrainingArguments(
            output_dir=output_directory,
            evaluation_strategy="steps",
            eval_steps=20,
            do_train=True,
            num_train_epochs=1,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            gradient_accumulation_steps=4,
            eval_accumulation_steps=1
        )

    @staticmethod
    def tune_model(training_dataset, testing_dataset, process_data, model_name, output_directory):
        tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
        model = transformers.AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        process_dataset = partial(process_data, tokenizer=tokenizer)

        training_dataset, testing_dataset = ModelTuner.__prepare_training_testing_dataset(process_dataset, training_dataset, testing_dataset)
        training_arguments = ModelTuner.__get_training_arguments(output_directory)

        trainer = transformers.Trainer(
            model=model,
            args=training_arguments,
            train_dataset=training_dataset,
            eval_dataset=testing_dataset
        )

        trainer.train()

        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S").replace(" ", "-")

        trainer.save_model(f"{output_directory}/model/{timestamp}")
        tokenizer.save_pretrained(f"{output_directory}/tokenizer/{timestamp}")

        print("Model Trained Successfully")