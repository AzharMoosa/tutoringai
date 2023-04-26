import os
import argparse
import torch
torch.cuda.empty_cache()
import pytorch_lightning as pl
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
)
from backend.common.question_engine.t5_model.question_dataset import QuestionDataset
from backend.common.question_engine.t5_model.model_tuner import ModelTuner

pl.seed_everything(42)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
path_to_training_csv = f"{__location__}/dataset/training_dataset.csv"
path_to_validation_csv = f"{__location__}/dataset/validation_dataset.csv"
path_to_tokenizer = f"{__location__}/tokenizer/"
path_to_model = f"{__location__}/model/"
tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device {device}")
model = model.to(device)


training_dataset = QuestionDataset(tokenizer, path_to_training_csv)
validation_dataset = QuestionDataset(tokenizer, path_to_validation_csv)

class QuestionGenerationModel:
    def train():
        args_dict = dict(
            batch_size=2,
        )
        hyper_parameters = argparse.Namespace(**args_dict)
        tuned_model = ModelTuner(model, tokenizer, hyper_parameters, training_dataset, validation_dataset)
        model_trainer = pl.Trainer(max_epochs=1, enable_progress_bar=True)
        model_trainer.fit(tuned_model)

        tuned_model.model.save_pretrained(path_to_model)
        tokenizer.save_pretrained(path_to_tokenizer)

if __name__ == "__main__":
    QuestionGenerationModel.train()