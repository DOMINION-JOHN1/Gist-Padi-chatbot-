import streamlit as st
import openai

st.title('Gist Padi')

client = openai.OpenAI(api_key="your-api-key")  # Replace "your-api-key" with your actual OpenAI API key

if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# start chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.container():  # Changed from `st.chat_message` to `st.container`
        st.markdown(f"{message['role']}: {message['content']}")

# Accept user input
if prompt := st.text_input('You:'):
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.container():  # Changed from `st.chat_message` to `st.container`
        st.markdown(f"You: {prompt}")

    # Display response in container
    with st.container():  # Changed from `st.chat_message` to `st.container`
        message_placeholder = st.empty()
        full_response = ""
        for response in client.ChatCompletion.create(
            model=st.session_state['openai_model'],
            messages=[
                {"role": m['role'], "content": m['content']}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].message['content'] or "")
            message_placeholder.markdown(f"Assistant: {full_response} | ")
        message_placeholder.markdown(f"Assistant: {full_response}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})
