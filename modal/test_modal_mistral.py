import modal

# Connect to deployed app
app = modal.App.lookup("detoxifyai-mistral", create_if_missing=False)
MistralModel = modal.Cls.from_name("detoxifyai-mistral", "MistralModel")

# Test the model
test_prompt = """You are a professional communication expert. Rephrase this toxic message professionally:

Toxic: You're an idiot for making that mistake
Professional:\n"""

print("🧪 Testing Modal Mistral-7B...")
print("Calling endpoint (first call may take 30s to spin up GPU)...\n")

# Correct syntax - no context manager
response = MistralModel().generate.remote(test_prompt, max_tokens=100, temperature=0.7)


print("✅ Response received!")
print(f"\n{response}")
