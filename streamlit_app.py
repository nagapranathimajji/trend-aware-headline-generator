import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

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
st.write("Generate **catchy, trend-aware headlines** powered by Flan-T5 ✨")

# Input box
user_prompt = st.text_area(
    "Enter your news/article content:",
    placeholder="Paste your news article here..."
)

# ----------------- LOAD FLAN-T5 -----------------
@st.cache_resource(show_spinner=True)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    return generator

generator = load_model()

# ----------------- GENERATE HEADLINES -----------------
if st.button("🚀 Generate Headlines"):
    if user_prompt.strip():
        try:
            prompt_text = f"Generate 3 catchy and accurate headlines for this news article:\n{user_prompt}"

            outputs = generator(
                prompt_text,
                do_sample=True,   # allow creative variation
                top_k=50,
                top_p=0.95,
                num_return_sequences=3
            )

            st.subheader("✨ Generated Headlines")
            for o in outputs:
                headline = o['generated_text'].strip()
                st.markdown(f"""
                    <div class="headline-card">
                        <div class="headline-text">{headline}</div>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText('{headline}')">📋 Copy</button>
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Flan-T5 Error: {str(e)}")
    else:
        st.warning("Please enter some text first!")
