import streamlit as st
from openai import OpenAI

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- OPENAI CLIENT -----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
/* Your existing CSS here */
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
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a trend-aware headline generator."},
                        {"role": "user", "content": f"Generate 5 trendy, engaging, SEO-friendly headlines about: {keywords}. Keep them short and catchy."}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )

                text = response.choices[0].message.content
                headlines = [hl.strip("- ").strip() for hl in text.split("\n") if hl.strip()]

                # Display headlines
                for hl in headlines:
                    st.markdown(f"<div class='result-box'><h2>{hl}</h2></div>", unsafe_allow_html=True)
                    st.markdown(f"<button class='copy-btn' onclick='navigator.clipboard.writeText(\"{hl}\")'>📋 Copy Headline</button>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
    else:
        st.warning("⚠️ Please enter some keywords.")
