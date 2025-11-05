import streamlit as st
from project_builder import build_and_run
from ai_agent import handle_user_prompt

st.set_page_config(page_title="AI Code Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Integrated Code Agent")
st.subheader("Generate, modify, upload to GitHub")

st.markdown("---")

mode = st.radio("Choose Mode:", ["Generate Project", "Agent Mode"])

prompt = st.text_area("🧠 Enter your prompt:", height=150,
                      placeholder="Example: create a flask app with login page")

github_enabled = st.checkbox("Upload to GitHub after generation?")

if github_enabled:
    st.markdown("### 🔑 GitHub Credentials (User enters)")
    github_username = st.text_input("GitHub Username")
    github_reponame = st.text_input("GitHub Repository Name")
    github_pat = st.text_input("GitHub Personal Access Token (PAT)", type="password")

col1, col2 = st.columns([1, 3])
auto_run = False

if mode == "Generate Project":
    auto_run = col1.checkbox("Run main file (local VS Code only)?")

if col2.button("🚀 Execute"):
    with st.spinner("Processing..."):
        if mode == "Generate Project":
            zip_bytes = build_and_run(prompt, auto_run, github_enabled,
                                      github_username, github_reponame, github_pat)
            if zip_bytes:
                st.download_button(
                    "⬇️ Download Generated Project",
                    data=zip_bytes,
                    file_name="project.zip",
                    mime="application/zip"
                )
        else:
            result = handle_user_prompt(prompt)
            st.success(result)
