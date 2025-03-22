from google import genai

with open(".env", "r") as f:
    api_key = f.read()

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how PPO works"
)
print(response.text)