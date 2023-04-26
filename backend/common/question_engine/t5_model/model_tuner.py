from torch.utils.data import DataLoader
import pytorch_lightning as pl
from transformers import (
    AdamW
)

class ModelTuner(pl.LightningModule):
    def __init__(self, model, tokenizer, hyper_parameters, training_dataset, validation_dataset):
        super(ModelTuner, self).__init__()
        self.model = model
        self.tokenizer = tokenizer
        self.hyper_parameters = hyper_parameters
        self.training_dataset = training_dataset
        self.validation_dataset = validation_dataset
    
    def forward(self, input_ids, attention_mask=None, decoder_input_ids=None, decoder_attention_mask=None, labels=None):
        return self.model(input_ids=input_ids, attention_mask=attention_mask, decoder_attention_mask=decoder_attention_mask, labels=labels)
    
    def training_step(self, batch, batch_index):
        output = self.forward(input_ids=batch["source_input_ids"], attention_mask=batch["source_attention_mask"], decoder_input_ids=batch["target_input_ids"], decoder_attention_mask=batch["target_attention_mask"], labels=batch["labels"])
        training_loss = output[0]
        return training_loss

    def validation_step(self, batch, batch_index):
        output = self.forward(input_ids=batch["source_input_ids"], attention_mask=batch["source_attention_mask"], decoder_input_ids=batch["target_input_ids"], decoder_attention_mask=batch["target_attention_mask"], labels=batch["labels"])
        validation_loss = output[0]
        return validation_loss
    
    def train_dataloader(self):
        return DataLoader(self.training_dataset, batch_size=self.hyper_parameters.batch_size, num_workers=4)
    
    def val_dataloader(self):
        return DataLoader(self.validation_dataset, batch_size=self.hyper_parameters.batch_size, num_workers=4)
    
    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=3e-4, eps=1e-8)