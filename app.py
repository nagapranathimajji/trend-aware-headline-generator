import streamlit as st
# ⚠️ New Import Strategy: Import Client directly from its canonical location.
from google.generativeai.client import Client 

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- GEMINI CLIENT SETUP -----------------
# 1. Access the API Key directly from secrets
API_KEY = None
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Configuration Error: Ensure your GEMINI_API_KEY is set in st.secrets.")
    st.stop()

# 2. Instantiate the Client using the explicitly imported Client class
try:
    # We pass the API_KEY directly into the client constructor for maximum robustness
    client = Client(api_key=API_KEY) 
except Exception as e:
    # This should be the final block to catch any remaining initialization errors
    st.error(f"Failed to initialize Gemini Client. Details: {e}")
    st.stop()
    
# ----------------- CUSTOM CSS: Futuristic/Cyberpunk Aesthetic -----------------
st.markdown("""
<style>
/* ... (Your CSS is here and is correct) ... */
/* 1. Global: Dark Mode Base, Futuristic Font */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0c1d;
    color: #E0E0E0;
    font-family: 'Space Mono', monospace;
}
/* 2. Headers: Neon Accents & Bold Typography */
h1, h2 {
    color: #00FFFF;
    text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF;
    font-weight: 800;
}
.st-emotion-cache-1wivap2 {
    color: #FF00FF !important;
}
/* 3. Input Field (The Generator) */
[data-testid="textInputRoot"] {
    border: 2px solid #330055;
    background-color: #1a1930; 
    border-radius: 12px;
    padding: 10px;
    transition: all 0.3s ease-in-out;
}
[data-testid="textInputRoot"]:focus-within {
    border-color: #00FFFF;
    box-shadow: 0 0 15px #00FFFF40;
}
/* 4. Generate Button: Motion UI/Liquid Feel */
.stButton>button {
    background-color: #FF00FF;
    color: #0d0c1d;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 0 4px 15px #FF00FF60;
}
.stButton>button:hover {
    background-color: #00FFFF;
    color: #0d0c1d;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px #00FFFF60;
}
/* 5. Result Box: The Headline Display (Bento/Modular Feel) */
.result-box {
    background-color: #1a1930; 
    border: 1px solid #330055;
    border-left: 5px solid #00FFFF;
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
    margin-bottom: 5px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    animation: fadeIn 0.5s ease-out;
}
.result-box h2 {
    color: #E0E0E0;
    font-size: 1.2em;
    text-shadow: none;
    margin: 0;
}
/* 6. Copy Button (Micro-Interaction) */
.copy-btn {
    background: none;
    border: 1px solid #FF00FF;
    color: #FF00FF;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 5px;
    float: right;
    font-size: 0.8em;
    transition: background-color 0.2s, color 0.2s;
}
.copy-btn:hover {
    background-color: #FF00FF;
    color: #0d0c1d;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.title("📰 Trend-Aware Headline Generator")
st.subheader("Generate multiple catchy, SEO-friendly headlines with AI ⚡")

# ----------------- INPUT -----------------
keywords = st.text_input("🔍 Enter a topic, keywords, or trend:")

# Initialize prompt context for the AI
PROMPT = (
    "You are an expert Digital Marketer and Trend Analyst. "
    "Analyze current digital marketing trends and generate 5 trendy, engaging, SEO-friendly headlines "
    "about the user's topic. Use power words, curiosity gaps, and number lists where appropriate. "
    "Keep each headline short, catchy, and format each as a bullet point."
)

# ----------------- GENERATE BUTTON -----------------
if st.button("✨ Generate Headlines"):
    if keywords:
        with st.spinner("Scanning social trends... ⚡"):
            try:
                # 💥 FINAL CALL: Using the instantiated client object 💥
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        PROMPT, 
                        f"Topic to generate headlines for: {keywords}"
                    ]
                )
                
                # Extract and display the generated headlines
                text = response.text
                headlines = [hl.strip("*- ").strip() for hl in text.split("\n") if hl.strip()]

                for hl in headlines:
                    safe_hl = hl.replace('"', '\\"') 
                    
                    st.markdown(f"""
                        <div class='result-box'>
                            <h2>{hl}</h2>
                            <button class='copy-btn' onclick='navigator.clipboard.writeText("{safe_hl}")'>
                                📋 Copy Headline
                            </button>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")

            except Exception as e:
                # Catch API-specific errors
                st.error(f"❌ Gemini API Error: The generation failed. Details: {e}")
    else:
        st.warning("⚠️ Please enter some keywords into the input field above.")

# ----------------- FOOTER/CALL TO ACTION -----------------
st.markdown("---")
st.markdown("This tool uses the **Gemini 2.5 Flash** model for rapid trend analysis and headline generation.")
