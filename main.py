import streamlit as st
import openai

# Set up your OpenAI API key here
openai.api_key = "API_KEY"


def main():
    st.title("GABE-GPT - Generative AI-Based Entity")

    # Initialize chat history as an empty list
    chat_history = []

    # User input for token length
    token_length = st.slider("Select Token Length", min_value=50, max_value=1000, value=150, step=10)

    # GPT Engine options (GPT-3 and GPT-4)
    engine_options_gpt_3 = ["text-davinci-002", "text-davinci-003"]
    engine_options_gpt_4 = ["gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613"]
    selected_engine = st.selectbox("Select GPT Engine", engine_options_gpt_3 + engine_options_gpt_4)

    # User input
    user_input = st.text_input("You: ", "")

    # Clear conversation button
    if st.button("Clear Conversation"):
        chat_history.clear()
        st.text("Conversation history cleared.")

    if user_input:
        # Add user input to the chat history
        chat_history.append(("User", user_input))

        # Get GPT response
        response_text = generate_response(chat_history, selected_engine, token_length)
        chat_history.append(("GABE-GPT", response_text))

        # Pagination to handle longer responses
        while len(response_text.split()) >= token_length and len(
                chat_history) <= 20:  # Max 20 tokens to avoid excessive API usage
            response_text = generate_response(chat_history, selected_engine, token_length)
            chat_history.append(("GABE-GPT", response_text))

    # Display the chat history
    st.text_area("Chat History", value=format_chat_history(chat_history), height=500, max_chars=None)


def generate_response(chat_history, engine, token_length):
    prompt_text = format_chat_history(chat_history)
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt_text,
        max_tokens=token_length,
        temperature=0,  # Set temperature to 0 for deterministic output
    )
    return response.choices[0].text.strip()


def format_chat_history(chat_history):
    formatted_history = "\n".join([f"{name}: {message}" for name, message in chat_history])
    return formatted_history


if __name__ == "__main__":
    main()