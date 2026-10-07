
import torch
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify
from pyngrok import ngrok

login(token="APNA_TOKEN_YAHAN_PASTE_KAR")

model_name = "meta-llama/Meta-Llama-3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=200)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response})

public_url = ngrok.connect(5000)
print(f"Aapka live API URL yeh raha: {public_url}")
app.run(port=5000)
  
