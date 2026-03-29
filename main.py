import streamlit as st
import time
import os
from groq import Groq

# API
client = Groq(api_key = os.environ["GROQ_API_KEY"])

# page config
st.set_page_config(page_title="bot-gpt")

if 'chats' not in st.session_state:
    st.session_state.chats = []
if 'system_instruction_change' not in st.session_state:
    st.session_state.system_instruction_change = "You are a generalized helpful assistant that helps with users' tasks."
if 'console_output' not in st.session_state:
    st.session_state.console_output = []
if 'disclaimer_finish' not in st.session_state:
    st.session_state.disclaimer_finish = False

# Title
st.title("bot-gpt")

# DISCLAIMER SCREEN
if not st.session_state.disclaimer_finish:
    st.text("DISCLAIMER: Please do not abuse this AI in any way that is in violation of school policy. ")
    dis_text = "Type 'I solemnly swear that I will abide by these rules' to continue."
    
    with st.form(key="input_dis", clear_on_submit=True):  
        user_input_dis = st.text_input(dis_text, key="user_input_dis")    
        submit_button_dis = st.form_submit_button("Submit", type="primary")
    
    if submit_button_dis and user_input_dis:
        if user_input_dis == "I solemnly swear that I will abide by these rules":
            st.session_state.disclaimer_finish = True
            st.session_state.console_output.append("Accepted! Starting schbot...")
            time.sleep(.5)
            st.session_state.console_output = []
            st.session_state.console_output.append("Welcome to schbot!")
            st.session_state.console_output.append("Press 'M' to manage chats, 'S' for settings, and 'Q' to quit.")
            time.sleep(.5)
            st.session_state.console_output.append("\nHow may schbot help you today?")
            st.rerun()
        else:
            st.error("Please type the exact statement: 'I solemnly swear that I will abide by these rules'")

# MAIN SCREEN
else:
    # Console output
    console_container = st.container()
    with console_container:
        for line in st.session_state.console_output:
            st.text(line)

    # Clear Console Button
    if st.button("Clear Console"):
        st.session_state.console_output = []
        st.rerun()

    
    # Input area - ONLY SHOW AFTER DISCLAIMER
    if len(st.session_state.chats) != 0:
        prompt_text = "What would you like to do? \n(Ask Something, Manage Chats (M), Settings (S), Quit (Q))"
    else:
        prompt_text = "Type here:"
    
    with st.form(key="input_form", clear_on_submit=True):  
        user_input = st.text_input(prompt_text, key="user_input")    
        submit_button = st.form_submit_button("Submit", type="primary")

    if submit_button and user_input:
        st.session_state.console_output.append(f"\n{user_input}")

        # New Chat
        if user_input.lower() == "m":
            time.sleep(.5)
            st.session_state.console_output.append("\n Welcome to Chat Management. What would you like to do? View Chats (V), Create a New Chat (N), or Delete a Chat (X)")

            # Delete Chat
            chat_text = ""
            with st.form(key="chat_form", clear_on_submit=True):  
                user_chat = st.text_input(chat_text, key="user_chat")    
                submit_button = st.form_submit_button("Submit", type="primary")
            if user_chat.lower() == "v":
                time.sleep(.5)
                if len(st.session_state.chats) == 0:
                    st.session_state.console_output.append("You have no chats to view!")
                else:
                    st.session_state.console_output.append(str(st.session_state.chats))
                st.rerun()
            elif user_chat.lower() == "n":
                time.sleep(.5)
                st.session_state.console_output.append("\nInput the name of your chat?\n")
                st.session_state.chats.append(user_input)
                st.rerun()
            elif user_chat.lower() == "x":
                if len(st.session_state.chats) != 0:
                    st.session_state.console_output.append("\nWhich chat would you like to delete?\n")
                    st.session_state.console_output.append(str(st.session_state.chats))
                    time.sleep(.5)
                    st.session_state.console_output.append("\nInput the number of the chat.")
                    st.session_state.chats.remove(user_input)
                else:
                    time.sleep(.5)
                    st.session_state.console_output.append("\nYou have no chats to delete!")
                st.rerun()
               

        # Settings
        elif user_input.lower() == "s":
            time.sleep(.5)
            st.session_state.console_output.append("\nWelcome to Settings!")
            st.session_state.console_output.append("Here you can give schbot certain instructions for his responses.\n Press 1 for a faster model and 2 for a more thorough model.")
            st.session_state.console_output.append("Input your settings or press 'X' to exit.")
            if st.button("1"):
                st.session_sate.ai_model = "llama-3.1-8b-instant"
                st.session_state.console_output.append("Your settings have been changed.")
                st.rerun()
            if st.button("2"):
                st.session_sate.ai_model = "llama-3.3-70b-versatile"
                st.session_state.console_output.append("Your settings have been changed.")
                st.rerun()

        # Quit command (added missing)
        elif user_input.lower() == "q":
            time.sleep(.5)
            st.session_state.console_output.append("\nThank you for using schbot!")

        # Regular query
        else:
            if len(st.session_state.chats) == 0:
                st.session_state.console_output.append(f"\nNew chat automatically created! — {user_input}")
                st.session_state.chats.append(user_input)
                time.sleep(.5)
                st.session_state.console_output.append("Loading...")
                chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "user", "content": user_input}
                            ],
                            model="llama-3.1-8b-instant"
                        )
                response = chat_completion.choices[0].message.content
                st.session_state.console_output.pop()
                st.session_state.console_output.append(f"\nAnswer: \n{response}\n")

    st.rerun()
