# ============================================================
#         🤖 SHUVO AI - MULTI-ENGINE V16 ULTIMATE
#   Pydroid 3 | 5 AI Engines + Wifi Check + Hybrid Brain
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

AI_NAME = "Shuvo AI"
CREATOR_NAME = "Shuvo"

MEMORY_FILE = "shuvo_ai_v16_memory.json"

# ============================================================
# 🔑 Apnar 5-ti API Key
# ============================================================
GEMINI_API_KEY = "AQ.Ab8RN6KL4INQNKIog_JUi7xzdRgpxZSLGapV68ex3amWbUGX8g"
GROQ_API_KEY = "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"
OPENAI_API_KEY = "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"
DEEPSEEK_API_KEY = "Sk-f3daff53d53642f294b132c372d5cbcf"
CLAUDE_API_KEY = "Sk-ant-api03-rSTFywkDScxy-agWh6rrPzspt_nFqrBBFu8_5a_wm7v6UErNqiEzc1fj7uyjFIRqLdVkkFxOF7zpRXt7CBKbeg-YSRZJAAA"

# Active Engine Selector (1=Gemini, 2=Groq, 3=OpenAI, 4=DeepSeek, 5=Claude)
ACTIVE_ENGINE = "1"

SYSTEM_PROMPT = f"You are {AI_NAME}, a smart & friendly AI created by {CREATOR_NAME}. Answer naturally in Bangla, Banglish, or English depending on user input."

# ------------------------------------------------------------
# 1. NETWORK & INTERNET CONNECTIVITY CHECKER (UPDATED)
# ------------------------------------------------------------
def check_internet():
    # Wi-Fi ev Mobile Data ubhoyer jonno multi-server fallback check
    test_urls = [
        "https://1.1.1.1",
        "https://8.8.8.8",
        "https://www.google.com"
    ]
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

# 1. Google Gemini
def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = json.dumps({"contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\nUser Query: {prompt}"}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method='POST')
    with urllib.request.urlopen(req, timeout=15) as response:
        res_data = json.loads(response.read().decode())
        return res_data['candidates'][0]['content']['parts'][0]['text']

# 2. Meta Llama 3 via Groq
def call_groq(prompt):
    if not GROQ_API_KEY: return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())["choices"][0]["message"]["content"]

# 3. OpenAI ChatGPT
def call_openai(prompt):
    if not OPENAI_API_KEY: return None
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())["choices"][0]["message"]["content"]

# 4. DeepSeek
def call_deepseek(prompt):
    if not DEEPSEEK_API_KEY: return None
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())["choices"][0]["message"]["content"]

# 5. Anthropic Claude
def call_claude(prompt):
    if not CLAUDE_API_KEY: return None
    url = "https://api.anthropic.com/v1/messages"
    headers = {"x-api-key": CLAUDE_API_KEY, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "claude-3-haiku-20240307", "max_tokens": 1000,
        "system": SYSTEM_PROMPT, "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())["content"][0]["text"]

# MASTER AI BRAIN ROUTER (WITH HYBRID FALLBACK)
def ask_ai_engines(prompt):
    if not check_internet():
        return "⚠️ Network connection paowa jayni! Onugroh kore Wi-Fi ba Mobile Data on korun."

    engine_map = {
        "1": ("Gemini", call_gemini),
        "2": ("Groq (Llama 3)", call_groq),
        "3": ("OpenAI", call_openai),
        "4": ("DeepSeek", call_deepseek),
        "5": ("Claude", call_claude)
    }

    # 1st Priority: Selected Active Engine
    current_name, func = engine_map.get(ACTIVE_ENGINE, ("Gemini", call_gemini))
    try:
        res = func(prompt)
        if res: return res
    except Exception: pass

    # Auto Fallback to other engines if preferred one fails
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
        return f"🌐 Chrome / Browser-e open kora hocche: {url}"
    except Exception as e:
        return f"⚠️ Browser open korte somossa hoyeche: {e}"

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
                return f"🌐 **Wikipedia Knowledge ({data.get('title', query)})**:\n{data['extract']}"
    except: pass
    return f"🔍 '{query}' somporke kono tothyo paowa jayni."

# ------------------------------------------------------------
# 4. UTILITY & MATHEMATICS
# ------------------------------------------------------------
def calculate_math(expr):
    expr = expr.lower().replace("×", "*").replace("÷", "/").replace("^", "**")
    try:
        if "sqrt" in expr: return math.sqrt(float(expr.replace("sqrt", "").strip()))
        if re.fullmatch(r"[0-9+\-*/().%\s*]+", expr): return eval(expr, {"__builtins__": None}, {})
    except: return None
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
        except: pass
    return {"expenses": [], "todos": []}

def save_memory(mem_data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(mem_data, f, ensure_ascii=False, indent=2)
    except: pass

memory = load_memory()

# ------------------------------------------------------------
# 6. MAIN HYBRID BRAIN CONTROLLER
# ------------------------------------------------------------
def ai_reply(user):
    global ACTIVE_ENGINE
    text = user.lower().strip()

    if text in ["bye", "exit", "quit", "bondho", "viday", "allah hafiz"]:
        save_memory(memory)
        return "__EXIT__"

    # ENGINE SWITCHING
    clean_input = text.replace(" ", "")
    if clean_input.startswith("engine") or clean_input.startswith("engin"):
        eng_num = ''.join(filter(str.isdigit, clean_input))
        if eng_num in ["1", "2", "3", "4", "5"]:
            ACTIVE_ENGINE = eng_num
            engines = {"1": "Google Gemini", "2": "Meta Llama 3 (Groq)", "3": "OpenAI ChatGPT", "4": "DeepSeek", "5": "Claude"}
            return f"✅ Active Engine Set To {eng_num}: {engines[eng_num]}"

    # CHROME & WEB OPEN COMMANDS
    if text.startswith("open "):
        site = text.replace("open ", "").strip()
        if site == "facebook": return open_in_browser("https://www.facebook.com")
        if site == "youtube": return open_in_browser("https://www.youtube.com")
        if site in ["google", "chrome"]: return open_in_browser("https://www.google.com")
        if site == "chatgpt": return open_in_browser("https://chatgpt.com")
        return open_in_browser(f"https://www.{site}.com")

    # GOOGLE SEARCH COMMAND
    if text.startswith("google search:") or text.startswith("google "):
        q = text.replace("google search:", "").replace("google ", "").strip()
        return google_search_web(q)

    # WI-FI & NETWORK STATUS
    if "wifi" in text or "internet" in text or "net" in text:
        status = "✅ Connected" if check_internet() else "❌ Disconnected"
        return f"🌐 **Network Status**: {status}"

    # TODO LIST MANAGEMENT
    if text.startswith("todo:"):
        memory["todos"].append(text.replace("todo:", "").strip())
        save_memory(memory)
        return "✅ Todo List-e jog kora hoyeche!"

    if text in ["show todo", "my todo", "todo"]:
        return "📋 **Todo List**:\n" + "\n".join([f"{i+1}. {t}" for i, t in enumerate(memory["todos"])]) if memory["todos"] else "Kono Todo khunje paowa jayni."

    # TIME & DATE
    if text in ["time", "date", "somoy", "shomoy", "tarikh"]:
        return f"🕐 Bortoman somoy: {get_time()}" if any(x in text for x in ["time", "somoy", "shomoy"]) else f"📅 Ajker tarikh: {get_date()}"

    # MATH EVALUATION
    m_ans = calculate_math(text)
    if m_ans is not None: return f"🧮 **Ganitik folafol**: {m_ans}"

    # 🌟 PRIMARY BRAIN: 5 MULTI-ENGINE AI (Prioritized)
    ai_res = ask_ai_engines(user)
    if ai_res:
        return ai_res

    # LOCAL QUICK FALLBACK RESPONSES
    if any(w in text for w in ["kemon aso", "kemon acho", "how are you"]):
        return f"Ami khub bhalo achi, Boss! 😄 Apni kemon achen?"

    if any(p in text for p in ["banaise", "created you", "creator", "ke banaiyeche"]):
        return f"Amake toiri korechen {CREATOR_NAME}! 👑"

    if any(w in text for w in ["hello", "hi", "hey"]):
        return f"Hello Boss! 😄 Ami {AI_NAME}। Bolun apnake kivabe shahajjo korte pari?"

    # FINAL FALLBACK TO WIKIPEDIA
    return search_wikipedia(user)

# ============================================================
#                     START AI V16 SYSTEM
# ============================================================
net_status = "Connected ✅" if check_internet() else "Disconnected ❌"
print("\n" + "=" * 60)
print(f"      🤖 {AI_NAME} - MULTI-ENGINE V16 ULTIMATE")
print(f"      Created by: {CREATOR_NAME} | Network: {net_status}")
print("      Commands: 'engine 1' to 'engine 5' to switch AI Engine")
print("=" * 60)
print(f"\nAI: Hello Boss! System is online and fully connected.\n")

while True:
    try:
        user = input("You: ")
        if not user.strip(): continue

        response = ai_reply(user)

        if response == "__EXIT__":
            print("\nAI: Bye Boss! All data saved automatically. 👋")
            break

        print(f"\nAI: {response}\n")

    except (KeyboardInterrupt, Exception):
        save_memory(memory)
        print("\nAI: Bye! 👋")
        break
