import streamlit as st
from project_builder import build_and_run
from ai_agent import handle_user_prompt

st.set_page_config(page_title="AI Code Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Integrated Code Agent")
st.subheader("Generate, modify, commit & push code — all with natural language")

st.markdown("---")

mode = st.radio("Choose Mode:", ["Generate Project", "Agent Mode"])

prompt = st.text_area("🧠 Enter your prompt:", height=150, placeholder="Example: create a flask app with login page")

col1, col2 = st.columns([1, 3])

auto_run = False
if mode == "Generate Project":
    auto_run = col1.checkbox("Run the main file after generation?")

if col2.button("🚀 Execute"):
    if not prompt.strip():
        st.error("⚠️ Please enter a prompt before executing")
    else:
        with st.spinner("Processing..."):
            if mode == "Generate Project":
                build_and_run(prompt, auto_run)
                st.success("✅ Project generated in VS Code workspace")
            else:
                result = handle_user_prompt(prompt)
                st.success(result)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini + LangChain")
