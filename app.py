import streamlit as st
import openai

# Page config
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# Custom CSS for Futuristic Cyberpunk Look
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
    text-shadow: 0 0 10px #00F5FF;
}
.stButton button {
    background: linear-gradient(90deg, #00F5FF, #8A2BE2);
    border: none;
    color: white;
    padding: 0.6em 1.2em;
    border-radius: 8px;
    font-size: 1.1em;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00F5FF;
}
.result-box {
    border: 2px solid #FF00E6;
    border-radius: 8px;
    padding: 1em;
    margin-top: 1em;
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 15px #FF00E6;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("📰 Trend-Aware Headline Generator")
st.subheader("Generate catchy, SEO-friendly headlines with AI ⚡")

# Input field
keywords = st.text_input("🔍 Enter a topic, keywords, or trend:")

# Generate button
if st.button("✨ Generate Headline"):
    if keywords:
        with st.spinner("Scanning social trends... ✨"):
            # Use your OpenAI key stored in Streamlit secrets
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Generate an engaging, trend-aware, SEO-friendly headline about: {keywords}",
                max_tokens=20,
                temperature=0.7
            )
            headline = response.choices[0].text.strip()
        
        st.markdown(f"<div class='result-box'><h2>{headline}</h2></div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some keywords.")
