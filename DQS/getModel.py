from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained("D:/project/transformer_model/Qwen2_5-Coder-3B/tokenizer")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained("D:/project/transformer_model/Qwen2_5-Coder-3B/model")