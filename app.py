import streamlit as st
import google.generativeai as genai
# ⚠️ THE FIX: Import Client directly from the client submodule 
from google.generativeai.client import Client 

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="📰 Trend-Aware Headline Generator",
    page_icon="✨",
    layout="centered",
)

# ----------------- GEMINI CLIENT SETUP -----------------
# 1. Configure the API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Instantiate the Client using the correctly imported class
try:
    # Use the imported Client class
    client = Client() 
except Exception as e:
    st.error(f"Failed to initialize Gemini Client. Check your API key and environment setup. Details: {e}")
    # Stop the app execution if the client can't be initialized
    st.stop()


# ----------------- CUSTOM CSS: Futuristic/Cyberpunk Aesthetic -----------------
st.markdown("""
<style>
/* 1. Global: Dark Mode Base, Futuristic Font */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0c1d; /* Deep Purple-Black Background */
    color: #E0E0E0;
    font-family: 'Space Mono', monospace; /* Futuristic/Monospace Font */
}

/* 2. Headers: Neon Accents & Bold Typography */
h1, h2 {
    color: #00FFFF; /* Electric Cyan Accent */
    text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF; /* Subtle Neon Glow */
    font-weight: 800;
}
.st-emotion-cache-1wivap2 {
    color: #FF00FF !important; /* Neon Magenta Subheader */
}

/* 3. Input Field (The Generator) */
[data-testid="textInputRoot"] {
    border: 2px solid #330055; /* Purple Border */
    background-color: #1a1930; 
    border-radius: 12px;
    padding: 10px;
    transition: all 0.3s ease-in-out;
}
[data-testid="textInputRoot"]:focus-within {
    border-color: #00FFFF; /* Cyan on focus */
    box-shadow: 0 0 15px #00FFFF40; /* Subtle hover glow */
}

/* 4. Generate Button: Motion UI/Liquid Feel */
.stButton>button {
    background-color: #FF00FF; /* Neon Magenta Button */
    color: #0d0c1d; /* Dark text for contrast */
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* Liquid transition */
    box-shadow: 0 4px 15px #FF00FF60;
}
.stButton>button:hover {
    background-color: #00FFFF; /* Swap to Cyan on hover */
    color: #0d0c1d;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px #00FFFF60;
}

/* 5. Result Box: The Headline Display (Bento/Modular Feel) */
.result-box {
    background-color: #1a1930; 
    border: 1px solid #330055;
    border-left: 5px solid #00FFFF; /* Highlight bar */
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
    margin-bottom: 5px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    animation: fadeIn 0.5s ease-out; /* Seamless entry animation */
}
.result-box h2 {
    color: #E0E0E0; /* White text for readability */
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
                # Use client.models.generate_content for the generation call
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
                    # Escape quotes for JavaScript function
                    safe_hl = hl.replace('"', '\\"') 
                    
                    st.markdown(f"""
                        <div class='result-box'>
                            <h2>{hl}</h2>
                            <button class='copy-btn' onclick='navigator.clipboard.writeText("{safe_hl}")'>
                                📋 Copy Headline
                            </button>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Simple separator for style
                st.markdown("---")

            except Exception as e:
                # A more informative error for the user
                st.error(f"❌ Gemini API Error: The generation failed. Details: {e}")
    else:
        st.warning("⚠️ Please enter some keywords into the input field above.")

# ----------------- FOOTER/CALL TO ACTION -----------------
st.markdown("---")
st.markdown("This tool uses the **Gemini 2.5 Flash** model for rapid trend analysis and headline generation.")
