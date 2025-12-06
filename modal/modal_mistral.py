import modal

# Create Modal app
app = modal.App("detoxifyai-mistral")

# Define GPU image with dependencies
image = modal.Image.debian_slim(python_version="3.10").pip_install(
    "torch", "transformers", "accelerate", "bitsandbytes", "sentencepiece"
)


# Deploy Mistral-7B with 4-bit quantization
@app.cls(
    gpu="A10G",  # GPU type
    image=image,
    timeout=600,
    container_idle_timeout=300,  # Keep warm for 5 min
)
class MistralModel:
    @modal.enter()
    def load_model(self):
        """Load model once when container starts"""
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        import torch

        print("Loading Mistral-7B with 4-bit quantization...")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.1"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.1",
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )

        print("✅ Model loaded!")

    @modal.method()
    def generate(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7):
        """Generate text from prompt"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
