from google import genai

def get_initial_topic_list(topic: str) -> list:
    with open(".env", "r") as f:
        api_key = f.read()
    with open("./prompt_structures/initial_topic.txt", "r") as f:
        prompt = f.read()
    prompt = prompt.replace("TOPIC", topic)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(f"Gemini response: \n<{response.text}>")
    response_text = response.text
    if response_text[0:3] == "```":
        response_text = response_text[3:-4].strip()
    if response_text[0:6] == "python":
        response_text = response_text[6:].strip()
    print(f"Cleaned Response text: \n<{response_text}>")
    return eval(response_text)

def get_topic_lesson(topic: str, node: str, parent: list) -> str:
    with open(".env", "r") as f:
        api_key = f.read()
    with open("./prompt_structures/topic_lesson.txt", "r") as f:
        prompt = f.read()
    prompt = prompt.replace("CONTEXT", topic)
    prompt = prompt.replace("TOPIC", node)
    prompt = prompt.replace("PARENT", parent)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(f"Gemini response: \n<{response.text}>")
    response_text = response.text
    return response_text