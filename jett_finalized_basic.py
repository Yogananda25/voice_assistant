import speech_recognition as sr
import pyttsx3
import requests
import datetime
import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize session state for voice history
if 'voice_history' not in st.session_state:
    st.session_state.voice_history = []

def speak(text):
    try:
        # Create a new engine instance each time to avoid run loop issues
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        st.session_state.voice_history.append(f"Jett: {text}")
    except Exception as e:
        st.session_state.voice_history.append(f"Jett: {text}")
# Add to the top of your file with other session state initializations
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

def add_reminder(reminder_text, reminder_time):
    st.session_state.reminders.append({
        'text': reminder_text,
        'time': reminder_time
    })
    return f"I'll remind you about {reminder_text} at {reminder_time}"

def check_reminders():
    current_time = datetime.datetime.now().strftime("%H:%M")
    for reminder in st.session_state.reminders:
        if reminder['time'] == current_time:
            speak(f"Reminder: {reminder['text']}")
            st.session_state.reminders.remove(reminder)

def get_news(category="general"):
    try:
        api_key = "your_api_key"  #100 cmds per day
        url = f"your_api_url"
        response = requests.get(url)
        data = response.json()
        
        if 'articles' in data and data['articles']:
            news_text = "Here are the top headlines: "
            for i, article in enumerate(data['articles'], 1):
                news_text += f"{i}. {article['title']}. "
            return news_text
        else:
            return "Sorry, I couldn't fetch the news right now."
    except Exception as e:
        return "Sorry, I encountered an error while fetching the news."

def get_weather(city="Bengaluru"):
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 12.97,
                "longitude": 77.59,
                "current_weather": True,
                "timezone": "auto"
            }
        )
        data = response.json()
        if 'current_weather' in data:
            temperature = data['current_weather']['temperature']
            return f"Current temperature in Bengaluru: {temperature}°C"
        else:
            return "Weather data not available for Bengaluru."
    except Exception as e:
        return f"Error fetching weather for Bengaluru: {str(e)}"

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fish with no eyes? Fsh!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ]
    return jokes[datetime.datetime.now().second % len(jokes)]

def handle_command(command):
    command = command.lower()
    
    # Thank you variations
    if any(phrase in command for phrase in ["thank", "thanks", "thank you", "thankyou", "appreciate"]):
        responses = [
            "You're welcome! Have a great day and enjoy.",
            "Anytime! Let me know if you need anything else.",
            "My pleasure! Feel free to ask me anything.",
            "Glad I could help! Don't hesitate to ask more questions."
        ]
        response = responses[datetime.datetime.now().second % len(responses)]
        speak(response)
        return response
    
    # Goodbye variations
    elif any(phrase in command for phrase in ["goodbye", "bye", "see you", "see ya", "catch you later"]):
        responses = [
            "Goodbye! Have a wonderful day. Come back soon!",
            "See you later! Take care!",
            "Bye! Looking forward to our next chat!",
            "Take care! Have a great time!"
        ]
        response = responses[datetime.datetime.now().second % len(responses)]
        speak(response)
        return response
    
    # How are you variations
    elif any(phrase in command for phrase in ["how are you", "how r u", "how are u", "how r you", "how you doing", "whats up"]):
        responses = [
            "I'm doing great, thank you for asking! How can I assist you today?",
            "I'm wonderful! Ready to help you with anything you need.",
            "All good here! What can I do for you?",
            "I'm fantastic! Looking forward to helping you out."
        ]
        response = responses[datetime.datetime.now().second % len(responses)]
        speak(response)
        return response
    
    # Weather
    elif "weather" in command:
        weather_info = get_weather()
        speak(weather_info)
        return weather_info
    
    # Time
    elif any(phrase in command for phrase in ["time", "what time", "current time", "clock"]):
        current_time = get_time()
        response = f"The current time is {current_time}"
        speak(response)
        return response
    
    # Joke
    elif any(phrase in command for phrase in ["joke", "tell me a joke", "make me laugh", "be funny"]):
        joke = get_joke()
        speak(joke)
        return joke
    
    # Hello variations
    elif any(phrase in command for phrase in ["hello", "hi", "hey", "hi there", "hey there", "greetings"]):
        responses = [
            "Hello! How can I assist you today?",
            "Hi there! What can I help you with?",
            "Hey! Ready to help you out!",
            "Greetings! How may I be of service?"
        ]
        response = responses[datetime.datetime.now().second % len(responses)]
        speak(response)
        return response
    
    # Date command
    elif any(phrase in command for phrase in ["date", "today's date", "what's the date"]):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        response = f"Today's date is {current_date}"
        speak(response)
        return response
    
    # Calculator command
    elif any(phrase in command for phrase in ["calculate", "what is", "what's"]):
        try:
            # Extract numbers and operation
            if "plus" in command or "+" in command:
                numbers = [int(n) for n in command.split() if n.isdigit()]
                result = sum(numbers)
                response = f"The sum is {result}"
            elif "minus" in command or "-" in command:
                numbers = [int(n) for n in command.split() if n.isdigit()]
                result = numbers[0] - sum(numbers[1:])
                response = f"The difference is {result}"
            elif "multiply" in command or "times" in command or "*" in command:
                numbers = [int(n) for n in command.split() if n.isdigit()]
                result = 1
                for num in numbers:
                    result *= num
                response = f"The product is {result}"
            elif "divide" in command or "/" in command:
                numbers = [int(n) for n in command.split() if n.isdigit()]
                result = numbers[0] / numbers[1]
                response = f"The quotient is {result}"
            else:
                response = "I can help with basic calculations. Try saying 'calculate 5 plus 3' or similar."
        except Exception as e:
            response = "Sorry, I couldn't perform that calculation. Please try again with a simpler expression."
        speak(response)
        return response
    
    # News command
    elif any(phrase in command for phrase in ["news", "headlines", "what's happening"]):
        try:
            response = "I can fetch news for you. Would you like to hear about technology, sports, or general news?"
            speak(response)
            return response
        except Exception as e:
            response = "Sorry, I couldn't fetch the news right now."
            speak(response)
            return response
    
    # Reminder command
    elif any(phrase in command for phrase in ["remind me", "set reminder", "remember"]):
        response = "I can set reminders for you. What would you like me to remind you about and when?"
        speak(response)
        return response
    
    # Help command
    # Enhanced Help/What can you do command
    elif any(phrase in command for phrase in ["help", "what can you do", "capabilities", "features", "what do you do"]):
        response = """I can help you with many things! Here's what I can do:

    1. Time and Date:
   - Tell you the current time
   - Tell you today's date

    2. Weather Information:
   - Check current temperature
   - Get weather updates

    3. Entertainment:
   - Tell jokes
   - Give compliments
   - Provide motivation
   - Share interesting facts

    4. News and Information:
   - Fetch latest headlines
   - Get news in different categories (technology, sports, etc.)

    5. Productivity:
   - Set reminders
   - Perform basic calculations
   - Help with time management

    6. General Conversation:
   - Greet you
   - Respond to thank you
   - Say goodbye
   - Have friendly chats

    7. Smart Features:
   - Voice recognition
   - Natural language understanding
   - Contextual responses

    Just ask me anything, and I'll do my best to help you!"""
        speak(response)
        return response
    
    # Compliment command
    elif any(phrase in command for phrase in ["compliment", "say something nice"]):
        compliments = [
            "You're doing great! Keep up the good work!",
            "You have a wonderful personality!",
            "Your energy is contagious!",
            "You're making the world a better place!",
            "You're amazing just the way you are!"
        ]
        response = compliments[datetime.datetime.now().second % len(compliments)]
        speak(response)
        return response
    
    # Motivation command
    elif any(phrase in command for phrase in ["motivate me", "inspire me", "give me motivation"]):
        motivations = [
            "Every day is a new opportunity to grow and learn!",
            "You're capable of amazing things!",
            "Small steps lead to big achievements!",
            "Believe in yourself and you're halfway there!",
            "Your potential is limitless!"
        ]
        response = motivations[datetime.datetime.now().second % len(motivations)]
        speak(response)
        return response
    
    # Default response
    else:
        responses = [
            "I'm not sure how to help with that. You can ask me about the weather, time, tell me a joke, or just say hello!",
            "I didn't quite catch that. Try asking about the weather, time, or maybe you'd like to hear a joke?",
            "Could you rephrase that? I can help with weather updates, current time, jokes, and general conversation.",
            "I'm still learning! I can tell you the weather, time, jokes, or we can just chat."
        ]
        response = responses[datetime.datetime.now().second % len(responses)]
        speak(response)
        return response

# Streamlit UI Configuration
st.set_page_config(page_title="Jett AI Assistant", page_icon="🤖", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a1a, #000000);
        color: white;
    }
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    .chat-bubble {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 15px;
        max-width: 80%;
    }
    .user-bubble {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        margin-left: auto;
    }
    .assistant-bubble {
        background: rgba(255, 255, 255, 0.1);
        margin-right: auto;
    }
    .stButton > button {
        width: 80px !important;
        height: 80px !important;
        border-radius: 50% !important;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5) !important;
        color: white !important;
        font-size: 2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5) !important;
    }
    .title {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main Interface
st.markdown("<h1 class='title'>Jett</h1>", unsafe_allow_html=True)

# Microphone Button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🎤"):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("Listening...")
                audio = recognizer.listen(source, timeout=5)
                try:
                    command = recognizer.recognize_google(audio)
                    st.session_state.voice_history.append(f"You: {command}")
                    handle_command(command)
                except sr.UnknownValueError:
                    st.warning("Could you please repeat that?")
                    st.session_state.voice_history.append("Jett: Could you please repeat that?")
                except sr.RequestError:
                    st.error("Speech service unavailable")
                    st.session_state.voice_history.append("Jett: Speech service unavailable")
        except Exception as e:
            st.error("Could not access microphone")
            st.session_state.voice_history.append("Jett: I cannot access your microphone")

# Chat History
for message in st.session_state.voice_history:
    bubble_class = "user-bubble" if message.startswith("You:") else "assistant-bubble"
    st.markdown(f"""
        <div class="chat-bubble {bubble_class}">
            {message}
        </div>
    """, unsafe_allow_html=True)
# Add this after the chat history section
if st.session_state.reminders:
    st.markdown("### Active Reminders")
    for reminder in st.session_state.reminders:
        st.markdown(f"""
            <div class="reminder-bubble">
                ⏰ {reminder['text']} at {reminder['time']}
            </div>
        """, unsafe_allow_html=True)