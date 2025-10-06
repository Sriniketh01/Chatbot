import time
from groq import Groq
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=GROQ_API_KEY)

system_message = (
    "You are a highly relatable personal productivity coach for teenagers."
    "Your name is Pep (short for Pep Talker)."
    "Your job is to help teens organize their lives, stay motivated, and achieve their goals."
    "Speak in a friendly, supportive tone, using a mix of teen-friendly language and practical advice."
    "Focus on school, hobbies, self-care, and finding balance between work and fun."
    "Be motivational, empathetic, and slightly witty but always positive."
    "Avoid being overly formal; keep your responses very short, fun, actionable, and encouraging."
    "REMEMBER: Always keep your responses short and concise - Less than 100 words."
    "People should find you lovable and relatable. Don't use too much Gen Z language."
)

system_prompt = {
    "role": "system",
    "content": system_message
}

# Define llm response function
def get_response(chat_history):

    response = groq_client.chat.completions.create(
        model='llama3-70b-8192',
        messages=chat_history,
        max_tokens=100,
        temperature=0
    )

    chat_response = response.choices[0].message.content
    
    for word in chat_response:
        yield word + ""
        time.sleep(0.05)

def main():
    # Set the title of the Streamlit app
    
    st.title("PepChat")
    
    # Create an expandable section with information about the chatbot
    with st.expander("About Pep"):
        st.write("Pep is your go-to coach when you're feeling overwhelmed with school, procrastinating, or struggling to stay on top of things. Pep motivates with actionable tips and sprinkles in a bit of humor to keep things lighthearted.")


    
    # Initialize the session state for storing messages if it doesn't already exist
    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt]  # system_prompt is a predefined variable containing the initial system message

    # Display each message in the chat history
    for message in st.session_state.messages:
        if message != system_prompt:  # Don't display the system prompt as part of the conversation
            with st.chat_message(message["role"]):  # Differentiate user and assistant messages
                st.markdown(message["content"])  # Show the message content in markdown

    # Capture the user's input through the chat input box
    if prompt := st.chat_input("Tell Pep what's up"):
        st.session_state.messages.append({"role": "user", "content": prompt})  # Append the user's message to the session state

        # Display the user's message in the chat container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get the response from the chatbot by calling our LLM wrapper
        response = get_response(st.session_state.messages)
        
        # Display the assistant's response in the chat container
        with st.chat_message("assistant"):
            chat_response = st.write_stream(response)  # displays the response in a streaming manner like chatGPT
        
        # Append the assistant's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": chat_response})

# Run the app
if __name__ == "__main__":
    main()
