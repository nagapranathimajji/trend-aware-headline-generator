import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline

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
st.write("Generate **catchy, trend-aware headlines** powered by GPT-2 ✨")

# Input box
user_prompt = st.text_area(
    "Enter your news/article content:",
    placeholder="Paste your news article here..."
)

# ----------------- LOAD GPT-2 -----------------
@st.cache_resource(show_spinner=True)
def load_gpt2():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

generator = load_gpt2()

# ----------------- GENERATE HEADLINES -----------------
if st.button("🚀 Generate Headlines"):
    if user_prompt.strip():
        try:
            prompt_text = f"Generate a catchy headline for this news article:\n{user_prompt}\nHeadline:"

            headlines = []
            # Generate 3 unique headlines
            for _ in range(3):
                o = generator(
                    prompt_text,
                    max_new_tokens=30,  # short headline
                    do_sample=True,
                    top_k=50,
                    top_p=0.95
                )[0]

                # Remove the prompt from generated text
                headline = o['generated_text'].replace(prompt_text, "").strip()
                headlines.append(headline)

            st.subheader("✨ Generated Headlines")
            for h in headlines:
                st.markdown(f"""
                    <div class="headline-card">
                        <div class="headline-text">{h}</div>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText('{h}')">📋 Copy</button>
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ GPT-2 Error: {str(e)}")
    else:
        st.warning("Please enter some text first!")
