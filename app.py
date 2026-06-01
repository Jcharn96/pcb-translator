import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ---------------- APP CONFIG (APP-LIKE UI) ----------------
st.set_page_config(
    page_title="PCB Translator",
    page_icon="👽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# hide sidebar completely
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.title("👽 PCB Translator")

# ---------------- API KEY ----------------
api_key = st.secrets["GEMINI_API_KEY"]

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# ---------------- COPY FUNCTION ----------------
def copy_button(text, label):
    components.html(f"""
        <button onclick="navigator.clipboard.writeText(`{text}`)"
        style="
            padding:8px 12px;
            margin:5px 0;
            border-radius:8px;
            border:1px solid #ccc;
            cursor:pointer;
            width:100%;
        ">
        📋 Copy {label}
        </button>
    """, height=45)

# ---------------- CARD UI ----------------
def card(title, content):
    st.markdown(f"""
    <div style="
        padding:12px;
        border-radius:10px;
        border:1px solid #ddd;
        margin-bottom:10px;
        background-color:#fafafa;
    ">
    <b>{title}</b><br>{content}
    </div>
    """, unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown("### Input (PCB Term)")
text = st.text_area("", height=140, placeholder="Enter PCB / Lithography / defect term...")

col1, col2 = st.columns(2)

translate_btn = col1.button("👽 Translate")
info_btn = col2.button("📖 More Info")

# ---------------- TRANSLATE ----------------
if translate_btn:

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are a professional PCB manufacturing translator.

Expertise:
- Lithography
- Exposure
- Developing
- Photoresist
- Alignment
- SPC
- Yield analysis
- Etching

Return EXACT format:

Thai:
...

English:
...

Traditional Chinese (Taiwan):
...

Pinyin:
...

Text:
{text}
"""

    with st.spinner("Translating..."):
        response = model.generate_content(prompt)
        result = response.text

    st.session_state.last_input = text
    st.session_state.history.append(text)

    try:
        thai = result.split("English:")[0].replace("Thai:", "").strip()
        english = result.split("English:")[1].split("Traditional Chinese (Taiwan):")[0].strip()
        chinese = result.split("Traditional Chinese (Taiwan):")[1].split("Pinyin:")[0].strip()
        pinyin = result.split("Pinyin:")[1].strip()

        st.markdown("## 👽 Result")

        card("🇹🇭 Thai", thai)
        copy_button(thai, "Thai")

        card("🇬🇧 English", english)
        copy_button(english, "English")

        card("🇨🇳 Chinese", chinese)
        copy_button(chinese, "Chinese")

        card("🔤 Pinyin", pinyin)
        copy_button(pinyin, "Pinyin")

    except:
        st.error("Parsing error - raw output shown below")
        st.write(result)

# ---------------- MORE INFO ----------------
if info_btn and st.session_state.last_input:

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    info_prompt = f"""
You are a senior PCB Process Engineer.

Analyze this term:

{text}

Provide:
1. Meaning in PCB context
2. Possible causes
3. Corrective actions
4. Related process step
"""

    with st.spinner("Analyzing..."):
        info = model.generate_content(info_prompt)

    st.markdown("## 📖 PCB Engineer Insight")
    st.write(info.text)

# ---------------- HISTORY ----------------
st.markdown("## History")

if st.button("Clear History"):
    st.session_state.history = []
    st.session_state.last_input = ""
    st.success("History cleared")
    
if st.session_state.history:
    for i, h in enumerate(reversed(st.session_state.history[-10:])):
        st.write(f"{i+1}. {h}")
