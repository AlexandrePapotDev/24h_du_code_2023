from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("stabilityai/stable-diffusion-2-inpainting")
model = AutoModelForSeq2SeqLM.from_pretrained("stabilityai/stable-diffusion-2-inpainting")