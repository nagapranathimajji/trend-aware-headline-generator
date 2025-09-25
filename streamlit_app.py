import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

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
st.write("Generate **catchy, trend-aware headlines** powered by Mistral-7B-Instruct ✨")

# Input box
user_prompt = st.text_area(
    "Enter your news/article content:",
    placeholder="Paste your news article here..."
)

# ----------------- LOAD MISTRAL-7B-INSTRUCT -----------------
@st.cache_resource(show_spinner=True)
def load_model():
    model_id = "mistralai/Mistral-7B-Instruct-v0.3"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

generator = load_model()

# ----------------- GENERATE HEADLINES -----------------
if st.button("🚀 Generate Headlines"):
    if user_prompt.strip():
        try:
            headlines = []

            # Generate 3 independent headlines with modified prompts for diversity
            for i in range(3):
                prompt_text = (
                    f"[INST] Write a short, catchy, and unique headline for the following news article. "
                    f"Ensure this headline is distinct from others: {user_prompt} [/INST]"
                )
                
                output = generator(prompt_text, max_length=60, num_return_sequences=1)[0]
                headline = output['generated_text'].strip()
                headlines.append(headline)

            st.subheader("✨ Generated Headlines")
            for i, h in enumerate(headlines):
                # Display headline card
                st.markdown(
                    f"""
                    <div class="headline-card">
                        <div class="headline-text">{h}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # Copy button with unique key
                st.button("📋 Copy", key=f"{i}_{h}", on_click=lambda text=h: st.experimental_set_clipboard(text))

        except Exception as e:
            st.error(f"⚠️ Mistral-7B-Instruct Error: {str(e)}")
    else:
        st.warning("Please enter some text first!")
