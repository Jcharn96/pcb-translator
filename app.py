import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PCB Translator",
    page_icon="🌏"
)

st.title("🌏 PCB Translator")

api_key = st.secrets["GEMINI_API_KEY"]

text = st.text_area("Enter text", height=150)

# ---------------- COPY FUNCTION ----------------
def copy_button(text, label):
    components.html(f"""
        <button onclick="navigator.clipboard.writeText(`{text}`)"
        style="padding:6px 10px;margin:4px 0;cursor:pointer;">
            📋 Copy {label}
        </button>
    """, height=40)

# ---------------- INIT SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ---------------- TRANSLATE ----------------
if st.button("Translate"):

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a professional PCB translator.

Expertise:
- Lithography
- Exposure
- Developing
- Photoresist
- Alignment
- SPC
- Yield Analysis

Return EXACT format:

Thai:
...

English:
...

Chinese:
...

Pinyin:
...

Text:
{text}
"""

    response = model.generate_content(prompt)
    result = response.text

    st.session_state["last_input"] = text

    # save history
    st.session_state.history.append({
        "input": text,
        "output": result
    })

    st.markdown("## Translation Result")

    try:
        thai = result.split("English:")[0].replace("Thai:", "").strip()
        english = result.split("English:")[1].split("Chinese:")[0].strip()
        chinese = result.split("Chinese:")[1].split("Pinyin:")[0].strip()
        pinyin = result.split("Pinyin:")[1].strip()

        st.text_area("🇹🇭 Thai", thai, height=80)
        copy_button(thai, "Thai")

        st.text_area("🇬🇧 English", english, height=80)
        copy_button(english, "English")

        st.text_area("🇨🇳 Chinese", chinese, height=80)
        copy_button(chinese, "Chinese")

        st.text_area("🔤 Pinyin", pinyin, height=80)
        copy_button(pinyin, "Pinyin")

        # favorite button
        if st.button("⭐ Add to Favorite"):
            st.session_state.favorites.append(text)
            st.success("Added to favorite")

    except:
        st.text_area("Raw Output", result, height=300)

# ---------------- MORE INFO ----------------
if "last_input" in st.session_state:

    if st.button("📖 More Information"):

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        info_prompt = f"""
You are a senior PCB Process Engineer.

Text:
{st.session_state["last_input"]}

Explain:
1. Meaning
2. Causes
3. Corrective actions
4. Related process
"""

        info_response = model.generate_content(info_prompt)

        st.markdown("## 📖 More Information")
        st.write(info_response.text)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📚 History")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history[-10:])):
        if st.sidebar.button(f"{i+1}. {item['input'][:20]}"):
            st.sidebar.write(item["output"])

st.sidebar.title("⭐ Favorites")

for fav in st.session_state.favorites:
    st.sidebar.write("• " + fav)

# ---------------- FACTORY REPLY ----------------
st.sidebar.title("💬 Factory Reply")

if st.button("Generate Reply (Chinese)"):

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    reply_prompt = f"""
You are a PCB engineer replying to Chinese factory.

Write short professional reply in:

1. English
2. Chinese

Message:
{st.session_state.get("last_input", "")}
"""

    reply = model.generate_content(reply_prompt)

    st.markdown("## 💬 Factory Reply")
    st.write(reply.text)