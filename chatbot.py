import streamlit as st
from mistralai import Mistral
import os
from dotenv import load_dotenv
import random

load_dotenv()

# List of Dad Jokes
DAD_JOKES = [
    "Why don’t skeletons fight each other? They don’t have the guts!",
    "I’m afraid for the calendar. Its days are numbered.",
    "Remember, kiddo, a job well done is better than a job half done!",
    "I used to play piano by ear, but now I use my hands.",
    "You can’t trust stairs… they’re always up to something!",
    "Why did the old man fall down the well? He couldn’t see that well.",
    "Why did the egg have a day off? Because it was Fryday.",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "If your house is cold, just stand in the corner. It’s always 90 degrees there"
]

def get_dad_joke():
    return random.choice(DAD_JOKES)

# Page Config
st.set_page_config(page_title='Daddy GPT', layout='centered', page_icon='🧔🏾')

# Function
def main(userInput):
    with st.chat_message("user", avatar="🧑🏽"):
        st.write(userInput)
    
    st.session_state.messages.append({"role": "human", "avatar": "🧑🏽", "content": userInput})
    
    with st.chat_message("assistant", avatar='🧔🏾'):
        with st.spinner('So Listen...'):
            agent_id = os.getenv('agent_id')
            api_key = os.getenv('api_key')
            model = 'mistral-large-2411'
            client = Mistral(api_key=api_key)
            ai_response = client.agents.complete(
                agent_id=agent_id,
                messages=[
                    {"role": "user", "content": userInput}
                ]
            )
            
        # Append dad joke to the response
        response_text = ai_response.choices[0].message.content
        response_text += f"\n\n💡 I have a JOKE : {get_dad_joke()}"
        st.write(response_text)
        st.session_state.messages.append({"role": "ai", "avatar": "🧔🏾", "content": response_text})

# Some Stylings
css="""
<style>
    .title {
        text-align: center;
        background: linear-gradient(60deg, rgb(255, 255, 255), rgb(49, 13, 13), rgb(255, 255, 255));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        margin-bottom: 1px;
    }
    
    .subtext {
        background: linear-gradient(60deg, rgb(199, 153, 153), rgb(156, 139, 139), rgb(68, 27, 27));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 1rem;
        margin-top: 0;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)
st.markdown('<h1 class="title">Daddy GPT</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Treat me like Daddy, do not make me DIRTY!</p>', unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.input = 'Hi, Daddy..'
    st.markdown("<div style='height: 2vh'></div>", unsafe_allow_html=True)
  
# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.text(message["content"])
      
# React to User Input
if userInput := st.chat_input('Write your wish SON'):
    st.session_state.input = userInput

if userInput != '':
    main(userInput=st.session_state.input)
