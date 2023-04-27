import torch
torch.cuda.empty_cache()
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

path_to_tokenizer = f"{__location__}/../trained_model/"
path_to_model = f"{__location__}/../trained_model/"

tokenizer = AutoTokenizer.from_pretrained(path_to_tokenizer)
model = AutoModelForSeq2SeqLM.from_pretrained(path_to_model)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device: ", device)
model = model.to(device)

def answer_question(question):
    encoded_text = tokenizer.encode(question, return_tensors="pt").cuda()
    model_output = model.generate(encoded_text, do_sample=True, top_p=0.9, max_length=512).cpu()
    answer = tokenizer.decode(model_output[0], skip_special_tokens=True)
    return answer

def answer_test_set():
    pass