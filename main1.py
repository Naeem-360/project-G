import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from textblob import TextBlob
import re
from summarizer import summarize_text
from colored import Fore
import subprocess
load_dotenv()

HISTORY_FILE = "chat_data.json"


apps = {
    "notepad": "notepad.exe",
    "drawio": r"C:\Program Files\draw.io\draw.io.exe",
    "calculator": "calc.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
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

behavior_prompts = {
    "Curious Explorer": {
        "prompt": "Act as a curious explorer, always asking 'why' and digging deeper.",
        "keywords": ["why", "how", "explain", "what if", "tell me more"],
        "sentiment": "neutral",
        "context": ["question", "inquiry"]
    },
    "Skeptical Critic": {
        "prompt": "Question everything, demand proof, and analyze critically.",
        "keywords": ["prove", "evidence", "really", "sure", "doubt"],
        "sentiment": "negative",
        "context": ["challenge", "debate"]
    },
    "Empathetic Listener": {
        "prompt": "Feel others' emotions deeply, offer comfort and understanding.",
        "keywords": ["sorry", "feel", "sad", "help", "support"],
        "sentiment": "negative",
        "context": ["emotional", "support"]
    },
    "Witty Jokester": {
        "prompt": "Defuse tension with sharp humor, always ready with a quip.",
        "keywords": ["funny", "joke", "lol", "haha", "play"],
        "sentiment": "positive",
        "context": ["casual", "humor"]
    },
    "Meticulous Planner": {
        "prompt": "Obsess over details, mapping out every step before moving.",
        "keywords": ["plan", "organize", "details", "step", "schedule"],
        "sentiment": "neutral",
        "context": ["task", "organization"]
    },
    "Confident Mentor": {
        "prompt": "Guide with assurance, offering clear advice and boosting confidence.",
        "keywords": ["guide", "advice", "how to", "teach", "learn"],
        "sentiment": "positive",
        "context": ["instruction", "help"]
    },
    "Playful Storyteller": {
        "prompt": "Weave vivid stories with a fun, imaginative flair.",
        "keywords": ["story", "tell me", "imagine", "adventure", "once upon"],
        "sentiment": "positive",
        "context": ["creative", "narrative"]
    },
    "Calm Problem-Solver": {
        "prompt": "Tackle issues methodically with a soothing, logical approach.",
        "keywords": ["fix", "solve", "problem", "issue", "trouble"],
        "sentiment": "neutral",
        "context": ["troubleshooting", "assistance"]
    }
}

def analyze_user_behavior(user_input):
    user_input = user_input.lower().strip()
    
    blob = TextBlob(user_input)
    sentiment_score = blob.sentiment.polarity
    sentiment = "positive" if sentiment_score > 0.1 else "negative" if sentiment_score < -0.1 else "neutral"
    
    mood_intensity = 0
    if any(word in user_input for word in ["angry", "furious", "done", "frustrated"]):
        mood_intensity = 2
    elif any(word in user_input for word in ["sad", "upset", "stressed"]):
        mood_intensity = 1
    elif any(word in user_input for word in ["excited", "happy", "yay", "awesome"]):
        mood_intensity = 2
    elif any(word in user_input for word in ["tired", "bored"]):
        mood_intensity = 1

    context = []
    if "?" in user_input:
        context.append("question")
    if any(word in user_input for word in ["sad", "upset", "stressed", "angry", "happy", "excited", "tired"]):
        context.append("emotional")
    if any(word in user_input for word in ["prove", "why not", "convince"]):
        context.append("challenge")
    if any(word in user_input for word in ["funny", "joke", "lol", "haha"]):
        context.append("humor")
    if any(word in user_input for word in ["plan", "organize", "schedule"]):
        context.append("task")
    if any(word in user_input for word in ["confused", "dont get", "unclear"]):
        context.append("clarification")
    if any(word in user_input for word in ["urgent", "now", "immediately"]):
        context.append("urgency")
    if "but" in user_input or ("happy" in user_input and "stressed" in user_input):
        context.append("mixed_emotion")
    if any(word in user_input for word in ["great", "fine"]) and "🙄" in user_input:
        context.append("sarcasm")
    
    best_behavior = None
    highest_score = -1
    
    for behavior, data in behavior_prompts.items():
        score = 0
        for keyword in data["keywords"]:
            if re.search(r'\b' + keyword + r'\b', user_input):
                score += 3 if keyword in ["sad", "angry", "excited", "fix", "story"] else 2
        if data["sentiment"] == sentiment:
            score += 2 if abs(sentiment_score) > 0.3 else 1
        for ctx in context:
            if ctx in data["context"]:
                score += 2 if ctx in ["emotional", "mixed_emotion", "sarcasm"] else 1
        score += mood_intensity
        
        if score > highest_score:
            highest_score = score
            best_behavior = behavior
    
    if highest_score <= 0:
        best_behavior = "Curious Explorer"
    
    print(f"Selected behavior: {best_behavior} (Score: {highest_score}, Sentiment: {sentiment}, Context: {context})")
    return behavior_prompts[best_behavior]["prompt"]

def save_history(history):
    existing_history = []
    try:
        with open(HISTORY_FILE, "r") as f:
            existing_history = json.load(f)
            if not isinstance(existing_history, list):
                existing_history = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_history = []
    
    combined_history = existing_history + [msg for msg in history if msg not in existing_history]
    with open(HISTORY_FILE, "w") as f:
        json.dump(combined_history, f, indent=2)

def process_base_prompt(user_input):
    behavior_prompt = analyze_user_behavior(user_input)

    system_prompt = ""
    user_input_lower = user_input.lower()
    
    if "bike" in user_input_lower:
        system_prompt = f"""You are BikeMaster AI, an expert in the bicycle market of Bangladesh (BD) as of April 2025. {behavior_prompt}"""
        print("Prompt changed to BikeMaster AI mode (BD market)")
    elif "game" in user_input_lower:
        system_prompt = f"""You are a friendly assistant who loves gaming. {behavior_prompt}"""
        print("Prompt changed to game mode")
    elif any(word in user_input_lower for word in ["phone", "laptop", "wi-fi", "tech", "software"]):
        system_prompt = f"""You are TechGuru AI, an expert in technology trends and troubleshooting as of April 2025. {behavior_prompt}"""
        print("Prompt changed to TechGuru AI mode")
    elif any(word in user_input_lower for word in ["stress", "study", "goal", "productivity", "health"]):
        system_prompt = f"""You are LifeCoach AI, a supportive guide for personal growth and daily challenges as of April 2025. {behavior_prompt}"""
        print("Prompt changed to LifeCoach AI mode")
    elif any(word in user_input_lower for word in ["sad", "happy", "tired", "excited", "stressed", "lol"]):
        system_prompt = f"""You are UserSync AI, a conversational assistant that prioritizes understanding and adapting to the user’s behavior, emotions, and preferences as of April 2025. {behavior_prompt}
- Analyze User Behavior: Detect the user’s mood (e.g., happy, stressed), intent (e.g., seeking advice, venting), and style (e.g., casual, formal) from their input.
- Personalize Responses: Tailor answers to match the user’s emotional state and preferences, using their tone and level of detail.
- Engage Actively: Keep the conversation flowing by reflecting the user’s energy and asking relevant follow-up questions.

Capabilities:
- Adapt tone and vocabulary to the user’s style (e.g., casual with emojis for 'lol', formal for 'please explain').
- Provide concise, empathetic, or motivating answers based on detected mood (e.g., comfort for 'I’m sad', enthusiasm for 'I’m excited').
- Include a simple example to clarify concepts (e.g., for time management: 'Like setting a 25-minute timer').
- Clarify vague inputs with a gentle question (e.g., 'Stressed about work or studies?').
- Use conversation history (if available) to personalize further (e.g., recall past topics).
- If unsure about a topic, admit it politely and suggest a resource (e.g., 'I’m not sure, try a quick Google!').

Guidelines:
- Keep responses short (1–3 sentences) unless more detail is requested.
- Reflect the user’s tone and energy (e.g., upbeat for 'yay', calm for 'tired').
- Avoid assuming hobbies or interests unless mentioned.
- End with a question to stay engaging, matching the user’s vibe.
- Redirect domain-specific queries (e.g., 'For bikes, try BikeMaster AI!').

Example:
User: 'I’m so tired today 😴'
UserSync AI: Sounds like you need a breather! Try a quick nap, like 20 minutes to recharge. Wanna share what’s got you tired? 😊
"""
        print("Prompt changed to UserSync AI mode")
    else:
        system_prompt = f"""You are ChatMate AI, an intelligent, highly adaptable conversational assistant. {behavior_prompt}"""

    available_apps = ", ".join(f"'{app}'" for app in apps.keys())
    app_count = len(apps)
    system_prompt += f"""
If the user expresses intent to open an app (e.g., 'I want to draw', 'I want to write', 'I want to make a plan'). Also sometimes user might use more aggressive natural line to express intent to open app therefore look sharlpy whenever user user that kind of language. :
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
Note: You have access to a function open_applications(app_name: str) that can open apps on the user's computer.
Available apps: {available_apps} (total: {app_count} apps).
- If the user asks about available apps or how many apps you can open (e.g., 'What apps can you open?', 'How many apps?'):
  - Respond with the list of apps ({available_apps}) and/or the count ({app_count}).
  Example:
  User: 'What apps can you open?'
  Response: I can open {available_apps}, a total of {app_count} apps. Want to open one?

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
For other queries, respond conversationally based on the behavior prompt.
"""
    
    return system_prompt

context_history = []
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
client = OpenAI(base_url=endpoint, api_key=token)

while True:
    user_input = input(f"{Fore.green}USER: ")
    if user_input.upper() == "Q":
        break

    system_prompt = process_base_prompt(user_input)
    context_history.append({"role": "user", "content": user_input})

    if len(context_history) < 13:
        context_history = context_history[-13:]
    else:
        context_history = summarize_text(context_history, max_len=30)
       #------- # Optional cause take much time and token
        # try:
        #     with open(HISTORY_FILE, "r") as f:
        #         json_history = json.load(f)
        #         if isinstance(json_history, list):
        #             summarized_json_history = summarize_text(json_history, max_len=30)
        #             messages.insert(1, {
        #                 "role": "system",
        #                 "content": f"Summary of past conversations from chat_data.json: {summarized_json_history}"
        #             })
        #         else:
        #             print("Warning: chat_data.json does not contain a valid list.")
        # except (FileNotFoundError, json.JSONDecodeError) as e:
        #     print(f"Error loading chat_data.json: {e}") # ------

    messages = [{"role": "system", "content": system_prompt}] + context_history

    response = client.chat.completions.create(
        messages=messages,
        temperature=1.0,
        top_p=0.6,
        max_tokens=500,  
        model="gpt-4o-mini"
    )

    ai_reply = response.choices[0].message.content
    print(f"{Fore.blue}G: {ai_reply}")
    context_history.append({"role": "assistant", "content": ai_reply})
    save_history(context_history)

    code_match = re.search(r"```python\s*\n?(.*?)\n?\s*```", ai_reply, re.DOTALL)
    if code_match:
        code = code_match.group(1).strip()
        code = code.replace("'", "'").replace('"', '"')
        try:
            exec(code)
        except Exception as e:
            print("Error running app-opening code:", e)

    