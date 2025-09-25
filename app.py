import streamlit as st
import google.generativeai as genai

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- GEMINI CLIENT SETUP -----------------
API_KEY = None
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Configuration Error: Ensure your GEMINI_API_KEY is set in st.secrets.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    st.error(f"Failed to initialize Gemini Client. Details: {e}")
    st.stop()

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
/* Dark cyberpunk theme */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0c1d;
    color: #E0E0E0;
    font-family: 'Space Mono', monospace;
}
/* Neon headers */
h1, h2 {
    color: #00FFFF;
    text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF;
    font-weight: 800;
}
/* Input field */
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
/* Button */
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
/* Result box */
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
    margin: 0;
}
/* Copy button */
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

# ----------------- GENERATE BUTTON -----------------
if st.button("✨ Generate Headlines"):
    if keywords:
        with st.spinner("Scanning social trends... ⚡"):
            try:
                # Let Gemini handle both system context + user input
                response = model.generate_content([
                    {"role": "system", "parts": [
                        "You are an expert Digital Marketer and Trend Analyst. "
                        "Generate 5 trendy, engaging, SEO-friendly headlines. "
                        "Use power words, curiosity gaps, and number lists where appropriate. "
                        "Each headline should be short, catchy, and formatted as a bullet point."
                    ]},
                    {"role": "user", "parts": [f"Topic: {keywords}"]}
                ])
                
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
                st.error(f"❌ Gemini API Error: The generation failed. Details: {e}")
    else:
        st.warning("⚠️ Please enter some keywords into the input field above.")

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown("This tool uses the **Gemini 2.5 Flash** model for rapid trend analysis and headline generation.")
