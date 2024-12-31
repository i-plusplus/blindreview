import openai

# Configure OpenAI API key
openai.api_key = "your_openai_api_key"

def moderate_feedback(feedback_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Moderate the following feedback for inappropriate content: {feedback_text}",
        max_tokens=50
    )
    return response.choices[0].text.strip()



