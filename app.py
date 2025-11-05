import streamlit as st
from project_builder import build_and_run
from ai_agent import handle_user_prompt

st.set_page_config(page_title="AI Code Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Integrated Code Agent")
st.subheader("Generate, modify, commit & push code — with natural language")

st.markdown("---")

mode = st.radio("Choose Mode:", ["Generate Project", "Agent Mode"])

prompt = st.text_area(
    "🧠 Enter your prompt:",
    height=150,
    placeholder="Example: create a flask app with login and a product page"
)

auto_run = False
if mode == "Generate Project":
    auto_run = st.checkbox("Run the main file after generation?")

if st.button("🚀 Execute"):
    if not prompt.strip():
        st.error("⚠️ Please enter a prompt before executing")
    else:
        with st.spinner("Processing..."):
            if mode == "Generate Project":
                build_and_run(prompt, auto_run)
                st.success("✅ Project generated in VS Code workspace")
            else:
                result = handle_user_prompt(prompt)

                if isinstance(result, dict):  # GitHub result dictionary
                    st.success("✅ Successfully pushed code to GitHub")

                    if result.get("repo_url"):
                        st.markdown(f"🔗 **GitHub Repo:** [{result['repo_url']}]({result['repo_url']})")

                    if result.get("zip_url"):
                        st.markdown(f"⬇️ **Download ZIP:** [{result['zip_url']}]({result['zip_url']})")

                    if result.get("codespaces_url"):
                        st.markdown(
                            f"[🚀 Open in GitHub Codespaces]({result['codespaces_url']})",
                            unsafe_allow_html=True
                        )
                else:
                    st.success(result)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini + LangChain")
