from transformers import AutoTokenizer, AutoModelForCausalLM

# Specify the model name to be used from the Hugging Face Model Hub
model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"

# Load the tokenizer associated with the specified model
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Save the loaded tokenizer to a local directory
tokenizer.save_pretrained("D:/project/transformer_model/Qwen2_5-Coder-3B/tokenizer")
# Load the causal language model from the specified model
model = AutoModelForCausalLM.from_pretrained(model_name)
# Save the loaded model to a local directory
model.save_pretrained("D:/project/transformer_model/Qwen2_5-Coder-3B/model")