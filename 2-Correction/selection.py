from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("CIDAS/clipseg-rd64-refined")
model = AutoModelForSeq2SeqLM.from_pretrained("CIDAS/clipseg-rd64-refined")