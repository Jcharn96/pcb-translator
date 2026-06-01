import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ---------------- APP CONFIG ----------------
st.set_page_config(
    page_title="Translator",
    page_icon="👽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("👽 Translator")

# ---------------- API KEY ----------------
api_key = st.secrets["GEMINI_API_KEY"]

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=api_key)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- COPY BUTTON ----------------
def copy_button(text, label):
    components.html(
        f"""
        <button onclick="navigator.clipboard.writeText(`{text}`)"
        style="
            width:100%;
            padding:8px;
            border-radius:8px;
            border:1px solid #ccc;
            cursor:pointer;
        ">
        📋 Copy {label}
        </button>
        """,
        height=45
    )

# ---------------- CARD ----------------
def card(title, content):
    st.markdown(
        f"""
        <div style="
            padding:12px;
            border-radius:10px;
            border:1px solid #ddd;
            margin-bottom:10px;
            background-color:#fafafa;
        ">
        <b>{title}</b><br>
        {content}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- INPUT ----------------
text = st.text_area(
    "Enter PCB term or sentence",
    height=150,
    placeholder="Example: Under Exposure"
)

translate_btn = st.button("👽 Translate")

# ---------------- TRANSLATE ----------------
if translate_btn:

    if not text.strip():
        st.warning("Please enter text.")
        st.stop()

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a professional PCB manufacturing translator.

Expertise:
- PCB Manufacturing
- Lithography
- SES Process
- DES Process
- Exposure
- Developing
- Photoresist
- Alignment
- SPC
- Yield Analysis
- Etching

Translate using terminology commonly used in Taiwan PCB factories.

Return EXACTLY in this format:

Thai:
<translation>

English:
<translation>

Traditional Chinese (Taiwan):
<translation>

Pinyin:
<translation>

Text:
{text}
"""

    try:

        with st.spinner("Translating..."):

            response = model.generate_content(prompt)

        result = response.text

        st.session_state.history.append(text)

        try:

            thai = result.split("English:")[0].replace(
                "Thai:", ""
            ).strip()

            english = result.split(
                "English:"
            )[1].split(
                "Traditional Chinese (Taiwan):"
            )[0].strip()

            chinese = result.split(
                "Traditional Chinese (Taiwan):"
            )[1].split(
                "Pinyin:"
            )[0].strip()

            pinyin = result.split(
                "Pinyin:"
            )[1].strip()

            st.markdown("## Translation Result")

            card("🇹🇭 Thai", thai)
            copy_button(thai, "Thai")

            card("🇬🇧 English", english)
            copy_button(english, "English")

            card("🇹🇼 Traditional Chinese", chinese)
            copy_button(chinese, "Chinese")

            card("🔤 Pinyin", pinyin)
            copy_button(pinyin, "Pinyin")

        except Exception:

            st.warning(
                "Translation format changed. Showing raw response."
            )

            st.write(result)

    except Exception as e:

        error_text = str(e)

        if "429" in error_text:

            st.warning(
                """
⚠️ Gemini API usage limit reached.

Please wait approximately 1 minute and try again.

Free Gemini API has a request-per-minute limit.
"""
            )

        elif "404" in error_text:

            st.error(
                "Model not found. Please check Gemini model name."
            )

        else:

            st.error(
                f"Gemini Error:\n\n{error_text}"
            )

# ---------------- HISTORY ----------------
st.markdown("---")
st.markdown("### History")

if st.button("🗑 Clear History"):

    st.session_state.history = []

    st.success("History cleared.")

if st.session_state.history:

    for i, item in enumerate(
        reversed(st.session_state.history[-10:]),
        start=1
    ):
        st.write(f"{i}. {item}")
