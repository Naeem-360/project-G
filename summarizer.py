from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")  

def summarize_text(text, max_len=100):
    try:
        endpoint = "https://models.inference.ai.azure.com"
        client = OpenAI(base_url=endpoint, api_key=token)

        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Summarize the following text in {max_len} words or fewer:\n\n{text}"}
        ]

        response = client.chat.completions.create(
            messages=messages,
            temperature=0.5,
            top_p=0.5,
            max_tokens=max_len * 2,
            model="gpt-4o-mini"
        )
        summary = response.choices[0].message.content.strip()
        return [{"role": "user", "content": f"Summary of previous conversation: {summary}"}]
    except Exception as e:
        print("API Error:", str(e)) 
        return f"Error: {str(e)}"



sum_text = "An AI article explores the capabilities and potential applications of artificial intelligence. AI systems can mimic human learning, comprehension, and decision-making processes, enabling them to perform tasks that typically require human intelligence. These tasks include object recognition, natural language processing, and problem-solving. AI is being integrated across various industries, transforming how businesses operate and impacting society as a whole."



if __name__ == "__main__":
    summary = summarize_text(sum_text, max_len=30)

