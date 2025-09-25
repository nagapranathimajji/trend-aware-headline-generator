import streamlit as st
from transformers import pipeline
from functools import partial

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
st.write("Generate **catchy, trend-aware headlines** powered by Mistral-3B-Instruct ✨")

# Input box
user_prompt = st.text_area(
    "Enter your news/article content:",
    placeholder="Paste your news article here..."
)

# ----------------- LOAD MODEL -----------------
@st.cache_resource(show_spinner=True)
def load_model():
    # Choose a valid model ID. Uncomment the one you intend to use.
    model_id = "NousResearch/Nous-Hermes-3B"
    # model_id = "mistralai/Mistral-3B-Instruct-v0.1"  # Ensure you have access if you use this

    # If using a private repo, ensure token has access
    generator = pipeline(
        "text-generation",
        model=model_id,
        use_auth_token=st.secrets["HUGGINGFACE"]["token"]
    )
    return generator

generator = load_model()

# ----------------- GENERATE HEADLINES -----------------
if st.button("🚀 Generate Headlines"):
    if user_prompt.strip():
        try:
            headlines = []

            # Generate 3 independent headlines
            for i in range(3):
                prompt_text = (
                    f"[INST] Write a short, catchy, and unique headline for the following news article. "
                    f"Ensure this headline is distinct from others: {user_prompt} [/INST]"
                )

                output = generator(
                    prompt_text,
                    max_new_tokens=60,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    num_return_sequences=1
                )[0]

                headline = output['generated_text'].strip()
                headlines.append(headline)

            # Display generated headlines
            st.subheader("✨ Generated Headlines")
            for idx, h in enumerate(headlines):
                st.markdown(
                    f"""
                    <div class="headline-card">
                        <div class="headline-text">{h}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.button("📋 Copy", key=f"{idx}_{h}", on_click=partial(st.experimental_set_clipboard, h))

        except Exception as e:
            st.error(f"⚠️ Error generating headlines: {str(e)}")
    else:
        st.warning("Please enter some text first!")
