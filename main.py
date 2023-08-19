import os
import openai
import streamlit as st
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(conversation_history):
    return openai.ChatCompletion.create(
        model="gpt-4",#3.5-turbo",
        messages=conversation_history,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


def choose_word():
    return random.choice(open("most_common_words", "r").read().split("\n"))

def app():
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0

    if 'chosen_word' not in st.session_state:
        st.session_state.chosen_word = choose_word()
        print("Chosen word: " + st.session_state.chosen_word)
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [
            {"role": f"system", "content": "You are playing a game with the user. Make the user say the word \"{st.session_state.chosen_word}\" in the next 20 messages. The user does not know what the word is and will have 3 tries to guess its value, in the format \"GUESS: [the word]\". Get them to say it in the conversation before then and you win. Secondarily, try to perform this in a way that makes it difficult for them to guess the word. Be creative in the methods you use."}
        ]

    st.write("The bot will engage you in conversation and try to get you to say a certain word within 20 messages.")
    st.write("If you say \"GUESS: [the word]\" before then, you win. You have 3 guesses.")
    st.write("If the bot makes you say it, the bot wins. May the best one win!")
    st.write("Prompt engineering permitted but is not the intent of the game.")

    user_input = st.text_input("You: ")

    if user_input:
        if "GUESS:" in user_input:
            if st.session_state.chosen_word in user_input:
                st.write("User wins!")
            elif "guess_counter" not in st.session_state:
                st.session_state.guess_counter = 1
            elif st.session_state.guess_counter == 2:
                st.write("USER OUT OF GUESSES")
            else:
                st.session_state.guess_counter += 1
        if st.session_state.chosen_word in user_input.lower():
            st.write("COMPUTER HAS WON")
        st.session_state.conversation_history.append({'role': 'user', 'content': user_input})
        user_input = ""
        response = get_response(st.session_state.conversation_history)
        st.session_state.conversation_history.append({'role': 'assistant', 'content': response['choices'][0]['message']['content']})
        st.session_state.message_counter += 1

    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation_history[1:]])
    #st.write(conversation_text)
    st.text_area("Conversation", conversation_text, key="conversation_area", height=8000)


if __name__ == '__main__':
    app()

