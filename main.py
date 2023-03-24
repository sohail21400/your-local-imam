import requests
import streamlit as st
from streamlit_chat import message
import json
# TODO: add a button to clear the chat. DONE
# TODO: auto first letter capitalization for user input. DONE
# TODO: add temperature slider inside an expandable section. DONE

st.set_page_config(
    page_title="Local Imam",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# storing the chat
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
    {"role": "system",
        "content": "Act as a Muslim imam who gives me guidance and advice on how to deal with life problems. Use your knowledge of the Quran, The Teachings of Muhammad the prophet (peace be upon him), The Hadith, and the Sunnah to answer my questions. Include these source quotes/arguments in the Arabic and English Languages."},
    ]

# TODO: show these demo questions when user taps qustion mark icon
demo_questions = ["What is the meaning of life?", "Who is the best person in the world?", "Who is prophet Muhammed?"]

# this prints the full json data which is given for OpenAI completion
def print_messages():
    print("\n\n")
    for json_data in st.session_state.messages:
        pretty_json = json.dumps(json_data, indent=4, sort_keys=True)
        print(pretty_json)
    print("\n\n")

# TODO: make the text box pinned on top or bottom
# TODO: add auto save the messages as cache
# TODO: put custom avathar
# TODO: temprature is not working
# this returns the user input taken from the text box and adds the user message to the messages json list
def get_user_input():
    user_input = st.text_area("Ask me anything", "", key="user_input", placeholder="What is the meaning of life?").capitalize()
    
    if user_input != "":
        st.session_state.messages.append({"role": "user", "content": user_input})
    # todo: clear the text input after hitting enter
    return user_input

# this generates the response from the OpenAI API and adds the response to the messages json list
def generate_response(temperature):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": st.session_state.messages,
        "stream": False,
        'temperature': temperature,
    }
    response = requests.post(
        'https://chatgpt-api.shn.hk/v1/', headers=headers, json=data)
    # TODO: do you need other response codes?
    reply = response.json()
    print(reply)
    reply = response.json()['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "assistant", "content": reply})

    print_messages()
    return reply


st.title("Your Local Imam")
with st.expander("Configure"):
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider('Temperature', 0.0, 2.0, 0.0)
    with col2:
        clear_chat = st.button("Clear chat")
        if clear_chat:
            st.session_state.messages = []

col1, col2 = st.columns([3,9])
with col1:
    user_input = get_user_input()
    if user_input != "":
        output = generate_response(temperature)
with col2:
    # TODO: first put a default hardcoded message in a message window
    if st.session_state.messages:
        # for i in range(len(st.session_state['generated'])-1, -1, -1):
        #     message(st.session_state['past'][i],
        #             is_user=True, key=str(i) + '_user')
        #     message(st.session_state["generated"][i], key=str(i))
            
            
        for i in range(len(st.session_state.messages)-1, -1, -1):
            # if the message is from the system, don't show the message
            if st.session_state.messages[i]['role'] == 'system':
                continue
            message(st.session_state.messages[i]['content'], key=str(i), is_user=st.session_state.messages[i]['role'] == 'user')

        # todo: you can use this below code is there is auto scroll and the text box is below like in a normal messaging app
        # for i in range(0, len(st.session_state['generated'])):
        #     message(st.session_state["generated"][i], key=str(i))
        #     message(st.session_state['past'][i],
        #             is_user=True, key=str(i) + '_user')

with st.sidebar:
    st.text("Made with love")