import streamlit as st
import openai

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
body {
    background-color: #0D0B1E;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
}
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    color: #00F5FF;
    text-shadow: 0 0 10px #00F5FF, 0 0 20px #8A2BE2;
}
.stButton button {
    background: linear-gradient(90deg, #00F5FF, #8A2BE2);
    border: none;
    color: white;
    padding: 0.6em 1.2em;
    border-radius: 12px;
    font-size: 1.1em;
    font-weight: bold;
    transition: all 0.3s ease;
    cursor: pointer;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px #00F5FF, 0 0 35px #8A2BE2;
}
.result-box {
    border: 2px solid #FF00E6;
    border-radius: 12px;
    padding: 1em;
    margin-top: 1em;
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 20px #FF00E6;
    text-align: center;
    transition: transform 0.3s ease;
}
.result-box:hover {
    transform: scale(1.02);
}
.copy-btn {
    margin-top: 0.5em;
    padding: 0.4em 0.8em;
    background: linear-gradient(90deg, #FF00E6, #FF6FFF);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}
.copy-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #FF00E6, 0 0 25px #FF6FFF;
}
input, textarea {
    background-color: #1A1A2E;
    color: #FFFFFF;
    border: 2px solid #00F5FF;
    border-radius: 8px;
    padding: 0.5em;
}
</style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.title("📰 Trend-Aware Headline Generator")
st.subheader("Generate multiple catchy, SEO-friendly headlines with AI ⚡")

# ----------------- INPUT -----------------
keywords = st.text_input("🔍 Enter a topic, keywords, or trend:")

# ----------------- GENERATE BUTTON -----------------
if st.button("✨ Generate Headlines"):
    if keywords:
        with st.spinner("Scanning social trends... ⚡"):
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Generate 5 trendy, engaging, SEO-friendly headlines about: {keywords}. Keep them short and catchy.",
                    max_tokens=60,
                    temperature=0.7
                )
                headlines = response.choices[0].text.strip().split("\n")
                headlines = [hl.strip("- ").strip() for hl in headlines if hl.strip()]
                
                # Display headlines with copy buttons
                for i, hl in enumerate(headlines, 1):
                    st.markdown(f"<div class='result-box'><h2>{hl}</h2></div>", unsafe_allow_html=True)
                    st.markdown(f"<button class='copy-btn' onclick='navigator.clipboard.writeText(\"{hl}\")'>📋 Copy Headline</button>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
    else:
        st.warning("⚠️ Please enter some keywords.")

# ----------------- OPTIONAL: HISTORY -----------------
if "history" not in st.session_state:
    st.session_state.history = []

if keywords:
    st.session_state.history.append(keywords)

if st.session_state.history:
    st.markdown("### 🕹️ Your Recent Keywords")
    st.markdown(", ".join(st.session_state.history[-5:]))
