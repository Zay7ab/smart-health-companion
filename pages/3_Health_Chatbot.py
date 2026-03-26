import streamlit as st
from groq import Groq

st.title("🤖 Health Chatbot")
st.write("Describe your symptoms and get health guidance.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Chat input
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])

            system_prompt = """You are a Smart Health Companion AI assistant.
            Your job is to:
            - Listen to the user's symptoms
            - Suggest possible conditions (always remind them to see a doctor)
            - Give general health advice
            - Answer health-related questions clearly and compassionately
            Always end with: 'Please consult a qualified doctor for proper diagnosis.'
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
                temperature=0.7,
                max_tokens=500
            )

            reply = response.choices[0].message.content
            st.chat_message("assistant").write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"Error: {e}")
