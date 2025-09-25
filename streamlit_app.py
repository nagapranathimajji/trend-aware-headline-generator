import streamlit as st
from transformers import pipeline
from huggingface_hub import HfApi

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    body {
        background: #f5f7fa;
        font-family: 'Inter', sans-serif;
    }
    .headline-card {
        background: white;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .headline-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    .headline-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a202c;
    }
    .copy-btn {
        font-size: 0.9rem;
        background: #2563eb;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 0.5rem;
        cursor: pointer;
        margin-top: 0.5rem;
        border: none;
    }
    .copy-btn:hover {
        background: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- APP -----------------
st.title("📰 Trend-Aware Headline Generator")
st.write("Generate **catchy, trend-aware headlines** powered by Hugging Face ✨")

# Input box
user_prompt = st.text_area(
    "Enter your news/article content:",
    placeholder="Paste your news article here..."
)

# Hugging Face API setup
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]  # store in Streamlit secrets
generator = pipeline(
    "text-generation",
    model="PeftModelForCausalLM",  # you can choose any suitable model
    use_auth_token=HF_API_TOKEN,
)

if st.button("🚀 Generate Headlines"):
    if user_prompt.strip():
        try:
            # Generate text
            outputs = generator(
                f"Generate 3 catchy headlines for this news article:\n{user_prompt}",
                max_length=100,
                num_return_sequences=3
            )

            st.subheader("✨ Generated Headlines")
            for i, o in enumerate(outputs, start=1):
                headline = o['generated_text'].strip()
                st.markdown(
                    f"""
                    <div class="headline-card">
                        <div class="headline-text">{headline}</div>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText('{headline}')">📋 Copy</button>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"⚠️ Hugging Face API Error: {str(e)}")
    else:
        st.warning("Please enter some text first!")
