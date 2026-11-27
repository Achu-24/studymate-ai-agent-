import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from agent_core import make_llm, run_agent

st.set_page_config(page_title="StudyMate AI", page_icon="📚")
st.title("📚 StudyMate AI")
st.caption("Your personal AI study-planning assistant")

if "history" not in st.session_state:
    st.session_state.history = []

if "turns" not in st.session_state:
    st.session_state.turns = []

api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password"
)

if st.sidebar.button("Clear Chat"):
    st.session_state.history = []
    st.session_state.turns = []
    st.rerun()

st.sidebar.info("Your chat is kept only in this session.")

for turn in st.session_state.turns:
    with st.chat_message("user"):
        st.markdown(turn["user"])

    with st.chat_message("assistant"):
        st.markdown(turn["answer"])

    if turn["trace"]:
        with st.expander("View agent steps"):
            for step in turn["trace"]:
                st.write(step)

prompt = st.chat_input("Ask me about your study plan...")

if prompt:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar.")
    else:
        st.session_state.history.append(
            HumanMessage(content=prompt)
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    llm = make_llm(api_key)
                    answer, trace, limit_hit = run_agent(
                        llm,
                        st.session_state.history
                    )

                    st.markdown(answer)

                    if limit_hit:
                        st.warning("The agent reached its step limit.")

                    st.session_state.history.append(
                        AIMessage(content=answer)
                    )

                    st.session_state.turns.append({
                        "user": prompt,
                        "answer": answer,
                        "trace": trace
                    })

                except Exception as error:
                    st.error(f"Error: {str(error)[:300]}")
                    st.session_state.history.pop()