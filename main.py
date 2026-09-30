# ============================================================
#         🤖 SHUVO AI - MULTI-ENGINE V16 ULTIMATE (KIVY GUI)
#   Buildozer / Android Ready | Multi-AI Engine Integration
# ============================================================

import datetime
import random
import re
import math
import json
import urllib.request
import urllib.parse
import urllib.error
import os
import webbrowser
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock

AI_NAME = "Shuvo AI"
CREATOR_NAME = "Shuvo"
MEMORY_FILE = "shuvo_ai_v16_memory.json"

# ============================================================
# 🔑 API Keys (নিরাপদ উপায়: Environment Variable থেকে নেওয়া হবে)
# ============================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")

ACTIVE_ENGINE = "1"
SYSTEM_PROMPT = f"You are {AI_NAME}, a smart & friendly AI created by {CREATOR_NAME}. Answer naturally in Bangla, Banglish, or English depending on user input."

# ------------------------------------------------------------
# 1. NETWORK & INTERNET CONNECTIVITY CHECKER
# ------------------------------------------------------------
def check_internet():
    test_urls = ["https://1.1.1.1", "https://8.8.8.8", "https://www.google.com"]
    for url in test_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4):
                return True
        except Exception:
            continue
    return False

# ------------------------------------------------------------
# 2. 5-ENGINE AI INTEGRATION FUNCTIONS
# ------------------------------------------------------------
def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = json.dumps({"contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\nUser Query: {prompt}"}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode())
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception: return None

def call_groq(prompt):
    if not GROQ_API_KEY: return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())["choices"][0]["message"]["content"]
    except Exception: return None

def call_openai(prompt):
    if not OPENAI_API_KEY: return None
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())["choices"][0]["message"]["content"]
    except Exception: return None

def call_deepseek(prompt):
    if not DEEPSEEK_API_KEY: return None
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())["choices"][0]["message"]["content"]
    except Exception: return None

def call_claude(prompt):
    if not CLAUDE_API_KEY: return None
    url = "https://api.anthropic.com/v1/messages"
    headers = {"x-api-key": CLAUDE_API_KEY, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "claude-3-haiku-20240307", "max_tokens": 1000,
        "system": SYSTEM_PROMPT, "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())["content"][0]["text"]
    except Exception: return None

def ask_ai_engines(prompt):
    if not check_internet():
        return "⚠️ Network connection paowa jayni! Wi-Fi/Mobile Data check করুন।"

    engine_map = {
        "1": ("Gemini", call_gemini),
        "2": ("Groq (Llama 3)", call_groq),
        "3": ("OpenAI", call_openai),
        "4": ("DeepSeek", call_deepseek),
        "5": ("Claude", call_claude)
    }

    current_name, func = engine_map.get(ACTIVE_ENGINE, ("Gemini", call_gemini))
    try:
        res = func(prompt)
        if res: return res
    except Exception: pass

    for eng_id, (name, engine_func) in engine_map.items():
        if eng_id != ACTIVE_ENGINE:
            try:
                res = engine_func(prompt)
                if res: return f"[{name} Fallback]:\n{res}"
            except Exception: continue

    return None

# ------------------------------------------------------------
# 3. WEB BROWSER & LINK INTEGRATION
# ------------------------------------------------------------
def open_in_browser(url):
    try:
        webbrowser.open(url)
        return f"🌐 Browser open kora hocche: {url}"
    except Exception as e:
        return f"⚠️ Browser open korte somossa: {e}"

def google_search_web(query):
    encoded = urllib.parse.quote(query)
    open_in_browser(f"https://www.google.com/search?q={encoded}")
    return f"🔎 Google-e search kora hocche: '{query}'"

def search_wikipedia(query):
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
        req = urllib.request.Request(url, headers={'User-Agent': 'ShuvoAI/16.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if "extract" in data:
                return f"🌐 Wikipedia ({data.get('title', query)}):\n{data['extract']}"
    except Exception: pass
    return None

# ------------------------------------------------------------
# 4. UTILITY & MATHEMATICS
# ------------------------------------------------------------
def calculate_math(expr):
    expr = expr.lower().replace("×", "*").replace("÷", "/").replace("^", "**")
    try:
        if "sqrt" in expr: return math.sqrt(float(expr.replace("sqrt", "").strip()))
        if re.fullmatch(r"[0-9+\-*/().%\s*]+", expr): return eval(expr, {"__builtins__": None}, {})
    except Exception: return None
    return None

def get_time(): return datetime.datetime.now().strftime("%I:%M:%S %p")
def get_date(): return datetime.datetime.now().strftime("%d-%m-%Y (%A)")

# ------------------------------------------------------------
# 5. PERSISTENT MEMORY MANAGEMENT
# ------------------------------------------------------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception: pass
    return {"expenses": [], "todos": []}

def save_memory(mem_data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(mem_data, f, ensure_ascii=False, indent=2)
    except Exception: pass

memory = load_memory()

# ------------------------------------------------------------
# 6. MAIN HYBRID BRAIN CONTROLLER
# ------------------------------------------------------------
def ai_reply(user):
    global ACTIVE_ENGINE
    text = user.lower().strip()

    if text in ["bye", "exit", "quit", "bondho", "viday"]:
        save_memory(memory)
        return "Bye Boss! All data saved."

    clean_input = text.replace(" ", "")
    if clean_input.startswith("engine") or clean_input.startswith("engin"):
        eng_num = ''.join(filter(str.isdigit, clean_input))
        if eng_num in ["1", "2", "3", "4", "5"]:
            ACTIVE_ENGINE = eng_num
            engines = {"1": "Google Gemini", "2": "Meta Llama 3", "3": "OpenAI", "4": "DeepSeek", "5": "Claude"}
            return f"✅ Active Engine Set To {eng_num}: {engines[eng_num]}"

    if text.startswith("open "):
        site = text.replace("open ", "").strip()
        if site == "facebook": return open_in_browser("https://www.facebook.com")
        if site == "youtube": return open_in_browser("https://www.youtube.com")
        if site in ["google", "chrome"]: return open_in_browser("https://www.google.com")
        if site == "chatgpt": return open_in_browser("https://chatgpt.com")
        return open_in_browser(f"https://www.{site}.com")

    if text.startswith("google search:") or text.startswith("google "):
        q = text.replace("google search:", "").replace("google ", "").strip()
        return google_search_web(q)

    if "wifi" in text or "internet" in text or "net" in text:
        status = "✅ Connected" if check_internet() else "❌ Disconnected"
        return f"🌐 Network Status: {status}"

    if text.startswith("todo:"):
        memory["todos"].append(text.replace("todo:", "").strip())
        save_memory(memory)
        return "✅ Todo List-e jog kora hoyeche!"

    if text in ["show todo", "my todo", "todo"]:
        return "📋 Todo List:\n" + "\n".join([f"{i+1}. {t}" for i, t in enumerate(memory["todos"])]) if memory["todos"] else "Kono Todo khunje paowa jayni."

    if text in ["time", "date", "somoy", "shomoy", "tarikh"]:
        return f"🕐 Bortoman somoy: {get_time()}" if any(x in text for x in ["time", "somoy", "shomoy"]) else f"📅 Ajker tarikh: {get_date()}"

    m_ans = calculate_math(text)
    if m_ans is not None: return f"🧮 Ganitik folafol: {m_ans}"

    if any(w in text for w in ["kemon aso", "kemon acho", "how are you"]):
        return "Ami khub bhalo achi, Boss! 😄 Apni kemon achen?"

    if any(p in text for p in ["banaise", "created you", "creator"]):
        return f"Amake toiri korechen {CREATOR_NAME}! 👑"

    if any(w in text for w in ["hello", "hi", "hey"]):
        return f"Hello Boss! 😄 Ami {AI_NAME}। Bolun apnake kivabe shahajjo korte pari?"

    # Try AI Engine first
    ai_res = ask_ai_engines(user)
    if ai_res: return ai_res

    # Wikipedia search fallback
    if any(k in text for k in ["wiki", "wikipedia", "what is", "who is", "ki", "kake bole"]):
        wiki_res = search_wikipedia(user)
        if wiki_res: return wiki_res

    return f"Dukhito Boss, ami '{user}' bujhte parini. API key set na thakle AI engine kaj korbe na."

# ------------------------------------------------------------
# 7. KIVY APPLICATION INTERFACE (THREADED & AUTO-WRAPPED)
# ------------------------------------------------------------
class MainApp(App):
    def build(self):
        self.title = AI_NAME

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_logs = Label(
            text=f"🤖 {AI_NAME} System Online!\nCreated by {CREATOR_NAME}\n" + "="*30 + "\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )
        # Fix for Text Wrapping on Mobile Screen
        self.chat_logs.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.chat_logs.bind(texture_size=self.update_label_height)
        
        self.scroll.add_widget(self.chat_logs)
        main_layout.add_widget(self.scroll)

        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=5)
        self.user_input = TextInput(hint_text="Type a message...", multiline=False)
        self.send_btn = Button(text="Send", size_hint=(0.25, 1))
        self.send_btn.bind(on_press=self.send_message)

        input_layout.add_widget(self.user_input)
        input_layout.add_widget(self.send_btn)
        main_layout.add_widget(input_layout)

        return main_layout

    def update_label_height(self, instance, value):
        instance.height = instance.texture_size[1]
        self.scroll.scroll_y = 0

    def append_response(self, response_text):
        self.chat_logs.text += f"{AI_NAME}: {response_text}\n\n"
        self.send_btn.disabled = False

    def process_ai_in_background(self, text):
        response = ai_reply(text)
        Clock.schedule_once(lambda dt: self.append_response(response))

    def send_message(self, instance):
        text = self.user_input.text.strip()
        if not text: return

        self.chat_logs.text += f"\nYou: {text}\n"
        self.user_input.text = ""
        self.send_btn.disabled = True

        threading.Thread(target=self.process_ai_in_background, args=(text,), daemon=True).start()

if __name__ == '__main__':
    MainApp().run()
