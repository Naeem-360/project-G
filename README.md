# 🚀 ChatMate AI: Your Adaptive Conversational Companion 🤖

## 📖 Project Overview

ChatMate AI (G) is an intelligent, highly adaptable conversational assistant designed to provide personalized and engaging user experiences. Powered by Python, OpenAI's GPT-4o-mini, and sentiment analysis, it dynamically adjusts its behavior based on user input, emotions, and context. Whether you're seeking advice, troubleshooting tech, or just chatting for fun, ChatMate AI is your go-to companion! 🌟

**This project helps users by**:
- **Offering tailored responses that match their mood and intent** 😊.
- **Opening applications like Notepad or Draw.io with simple commands** 🖥️.
- **Providing domain-specific expertise (e.g., bikes, tech, personal growth)** 🚴‍♂️💻.
- **Saving conversation history for context-aware interactions** 📜.

## 🚀 Features

1. **✅ Dynamic Behavior Adaptation: Switches between 8 personas (e.g., Curious Explorer, Witty Jokester) based on user mood and intent.😄**
2. **✅ Application Integration: Opens apps like Notepad, Draw.io, Calculator, or Chrome with natural language commands.** 🖥️
3. **✅ Domain-Specific Modes: Specialized AI for bikes, tech, personal growth, or emotional support.** 🚴‍♂️💻
4. **✅ Conversation Persistence: Saves and summarizes chat history in chat_data.json for seamless interactions.** 📜
5. **✅ Customizable Framework: Easily tweak behaviors, apps, or domains via dictionaries.** ⚙️
6. **✅ Sentiment & Mood Detection: Analyzes tone and intensity for precise responses.** 😊😔


## Domain-Specific Modes 🔍:

- **BikeMaster AI: Expert in Bangladesh's bicycle market.**
- **TechGuru AI: Tech trends and troubleshooting.**
- **LifeCoach AI: Personal growth and productivity tips.**
- **UserSync AI: Emotion-driven, empathetic conversations.**
- **Customizable Prompts ⚙️: Easily extend behavior prompts or app integrations by editing the behavior_prompts dictionary or apps dictionary.**
- **Sentiment & Mood Detection 😄😔: Uses TextBlob to gauge sentiment (positive, negative, neutral) and mood intensity for precise persona selection.**
- **Error Handling 🚨: Gracefully manages app-opening errors and invalid inputs.**
- **Conversation Persistence 💾: Saves chat history to chat_data.json for continuity.**


## 🛠️ Installation
To get started with **ChatMate AI (G)**, follow these steps:

1. **Clone the Repository** 📂:
 ```bash
   git clone https://github.com/Naeem-360/project-G.git
   cd main1.py
 ```
2. **Set Up a Virtual Environment(optional)** 🐍:
 ```bash
 python -m venv venv
 ```
 ```bash
source venv/bin/activate 
 ```
 ```bash
# On Windows:
venv\Scripts\activate
 ```
3. **Install Required Modules** 📦:
 ```bash
pip install openai textblob python-dotenv colored re
 ```
4. **Set Up Environment Variables** 🔑: Create a .env file in the project root and add your OpenAI API key:
 ```bash
GITHUB_TOKEN=your_openai_api_key
 ```
5. **Run the Application** 🚀:
 ```bash
python main1.py
 ```


## 🔧 Customization
**ChatMate AI is highly customizable! Here’s how you can tailor it to your needs**:
- **Add New Behaviors** 🧑‍🎤: Edit the behavior_prompts dictionary in chatmate.py to introduce new personas. Example:
```bash
"Creative Muse": {
    "prompt": "Inspire with bold, imaginative ideas.",
    "keywords": ["inspire", "create", "art", "idea"],
    "sentiment": "positive",
    "context": ["creative", "brainstorm"]
}
 ```

- **Expand App Integrations** 💻: Update the apps dictionary to include new applications:
 ```bash
apps["firefox"] = r"C:\Program Files\Mozilla Firefox\firefox.exe"
 ```
- **Tweak Sentiment Analysis** ⚖️: Modify the analyze_user_behavior function to adjust keyword weights or context detection logic.
- **Change Domain Modes** 🌐: Add new triggers in process_base_prompt for specialized AI modes (e.g., FitnessCoach AI for workout plans).

## 📡 Cloning the Repository
To **contribute** or **experiment** with **ChatMate AI(G)**, clone the repo:
 ```bash
git clone https://github.com/Naeem-360/project-G.git
cd chatmate-ai
 ```
- **Replace your-username with the actual GitHub username hosting the project. Don’t have it yet? Fork it and make it your own**! 🍴

## 🤝 Contribute to ChatMate AI
**I welcome contributions to make ChatMate AI even better! Here’s how you can get involved**:
1. **Add New Features** 🌈: Implement new behaviors, app integrations, or AI modes.
2. **Improve Sentiment Analysis** 📊: Enhance mood detection with advanced NLP techniques.
3. **Optimize Performance**⚡: Reduce token usage or improve response times.
4. **Fix Bugs** 🐞: Spot and squash issues in the code.
5. **Share Ideas** 💡: Open an issue to suggest enhancements or new use cases.

## To contribute:
- **Fork the repository** 🍴.
- **Create a feature branch (git checkout -b feature/awesome-feature)**.
- **Commit your changes (git commit -m "Add awesome feature")**.
- **Push to the branch (git push origin feature/awesome-feature)**.
## Open a Pull Request 📬.
 **Let’s build the ultimate conversational AI together! 🚀 Your creativity and expertise can take ChatMate AI to new heights.** 🌍


## 📜 License
- This project is licensed under the MIT License. See the LICENSE file for details.



## ⭐ Star the repo if you love ChatMate AI! Let’s make conversations smarter and more fun! 😎
## project-G
- This project is a behavior-aware AI assistant that adapts its responses based on user emotion, sentiment, and context. It can chat, open apps, and shift personalities dynamically
