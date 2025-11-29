import streamlit as st
import ollama

# Model set karo
desiredModel = 'llama3.1:8b'

st.title("MindFlow — Local AI Chat UI")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Reset button at top
if st.button("Reset Chat"):
    st.session_state.chat_history = []

# Display existing chat history in GPT-style bubbles
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["question"])
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Call Ollama model
        response = ollama.chat(
            model=desiredModel,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response["message"]["content"]

        # Display assistant message
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save to session history
        st.session_state.chat_history.append({"question": prompt, "answer": answer})

    except Exception as e:
        st.error(f"Error: {e}")

# -----------------------------
# Show Chat History in Sidebar
# -----------------------------
if st.sidebar.button("Show Chat History"):
    st.sidebar.subheader("Chat History")
    for i, chat in enumerate(st.session_state.chat_history, start=1):
        st.sidebar.markdown(f"**Q{i}:** {chat['question']}")
        st.sidebar.markdown(f"**A{i}:** {chat['answer']}")
        st.sidebar.markdown("---")
