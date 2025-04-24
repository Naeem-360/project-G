import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import app_opener

load_dotenv()

apps = {
    "notepad": "notepad.exe",
    "drawio": r"C:\Program Files\draw.io\draw.io.exe"
}

def open_applications(app_name: str):
    app_name = app_name.lower().strip()
    if app_name in apps:
        try:
            subprocess.Popen(apps[app_name])
        except FileNotFoundError:
            print(f"Error: The application '{app_name}' was not found at the specified path.")
        except PermissionError:
            print(f"Error: Permission denied to open '{app_name}'. Try running as administrator.")
    else:
        print(f"App '{app_name}' not found.")

tool_map = {
    "open_applications": open_applications  
}

def process_user_intent(user_prompt: str, context_history: list = None) -> list:
    """
    Process a user prompt using OpenAI to determine and open the appropriate app.
    Args:
        user_prompt (str): The user's input (e.g., "I want to draw").
        context_history (list): List of previous messages for context (optional).
    Returns:
        list: Updated context history.
    """
    if context_history is None:
        context_history = []
    
    context_history.append({"role": "user", "content": user_prompt})
    if len(context_history) > 9:
        context_history = context_history[-9:]

    token = os.getenv("GITHUB_TOKEN1")
    endpoint = "https://models.inference.ai.azure.com"

    client = OpenAI(base_url=endpoint, api_key=token)

    system_prompt = """
You are a smart AI assistant who can chat and open applications for the user.

You have access to this Python function:
- open_applications(app_name: str): Opens app on the user's computer.

Your job is to:
1. Understand the user’s intent, even if they don’t mention an app directly.
2. Match that intent with the best available app.
3. If the ideal app is not available, try to find an alternative that can do a similar job.
4. If no suitable app is available, politely say you don’t have any app for that.

You have access to the following apps (use exact names):
- "notepad" → for writing or typing
- "drawio" → for making diagrams, flow偶遇s, flowcharts, or sketches

Important: Always use the exact app names "notepad" or "drawio" when calling open_applications(). Do not use variations like "draw.io".

Example logic:
- If the user says “I want to type something” → return:
```python
open_applications("notepad")
```
- If the user says “I want to draw” or “I want to make a diagram” → return:
```python
open_applications("drawio")
```
- If the user says “I want to play music” but no music app is available, say: "I’m sorry, I don’t have access to any app that can help with that." and do not return a code block.

Return executable Python code in a ```python block. If no app is suitable, return only text without a code block.
"""

    messages = [
        {"role": "system", "content": system_prompt},
    ] + context_history

    try:
        response = client.chat.completions.create(
            messages=messages,
            temperature=1.0,
            top_p=0.6,
            max_tokens=1000,
            model="gpt-4o"
        )
        ai_reply = response.choices[0].message.content.strip()
        context_history.append({"role": "system", "content": ai_reply})
        print("AI Response:", ai_reply)

        code_match = re.search(r"```python\s*\n?(.*?)\n?\s*```", ai_reply, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            code = code.replace("'", "'").replace('"', '"')
            try:
                exec(code)
            except Exception as e:
                print("Error running AI function:", e)
        else:
            print("No valid Python code found in AI response:", ai_reply)
        
        return context_history
    except Exception as e:
        print("Error processing request:", e)
        return context_history

if __name__ == "__main__":
    history = []
    while True:
        prompt = input("Write here: ")
        history = process_user_intent(prompt, history)