import streamlit as st
import google.generativeai as genai

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- GEMINI CLIENT -----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])  # Store your key in Streamlit secrets

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
                # Gemini text generation
                response = genai.chat.create(
                    model="gemini-1.5-t",  # Latest Gemini chat model
                    messages=[
                        {"author": "user", "content": f"Generate 5 trendy, engaging, SEO-friendly headlines about: {keywords}. Keep them short and catchy."}
                    ],
                    temperature=0.7,
                    max_output_tokens=150
                )

                # Extract generated text
                text = response.choices[0].content[0].text
                headlines = [hl.strip("- ").strip() for hl in text.split("\n") if hl.strip()]

                # Display headlines
                for hl in headlines:
                    st.markdown(f"<div class='result-box'><h2>{hl}</h2></div>", unsafe_allow_html=True)
                    st.markdown(f"<button class='copy-btn' onclick='navigator.clipboard.writeText(\"{hl}\")'>📋 Copy Headline</button>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
    else:
        st.warning("⚠️ Please enter some keywords.")
