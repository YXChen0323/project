from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained("./llm/tokenizer")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained("./llm/model")