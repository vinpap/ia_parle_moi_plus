import time
import streamlit as st
from vocal_assistant.chatbot import Chatbot

st.set_page_config(page_title="Votre ami imaginaire",
                   page_icon="favicon.png"
                   )

st.markdown(
    """
    <style>
    .conversation {
        border:1px solid black;
        max-width: 70%;
        width: fit-content;
        border-radius: 10px;
        padding: 5px 10px;
    }
    .user_sentence {
        margin-left: auto;
        background-color: #3170a9;
        margin-right: 0;
    }
    .bot_sentence {
        margin-right: auto; 
        background-color: #444444;
        color: white;
        margin-left: 0;
    }
    .conversation * {
        padding: 5px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def display_answer(answer):

    t = st.empty()
    for i in range(len(answer) + 1):
        if i == len(answer): t.markdown(f"<div class='conversation bot_sentence'>{answer[0:i]}</div>", unsafe_allow_html=True)
        else: t.markdown(f"<div class='conversation bot_sentence'>{answer[0:i]}...</div>", unsafe_allow_html=True)
        time.sleep(0.05)


print_conv = True
lang= "fr"
bot_is_rude = False

chatbot = Chatbot(language=lang, print_conversation=print_conv, rude_mode=bot_is_rude)
st.balloons()
st.markdown("<h1 style='text-align: center; color: black; font-size:60px'>Votre ami imaginaire</h1>", unsafe_allow_html=True)
st.image("meme.jpg")
st.markdown("<h2 style='text-align: center; color: black; font-size:30px'>Pas d'amis ? Pas de problème ! Découvrez nos amis imaginaires (presque) sympathiques disponibles 24h/24 et 7j7 !</h2>", unsafe_allow_html=True)
if not bot_is_rude:
    st.markdown("<h2 style='text-align: center; color: black; font-size:16px; font-style: italic bold'>Astuce : votre vie manque de négativité ? Activez le mode no-respect pour discuter avec l'ami toxique dont vous avez toujours rêvé !</h2>", unsafe_allow_html=True)

if bot_is_rude: 
    st.markdown("<h3 style='text-align: center; color: red; font-size:20px'>Mode no-respect activé</h3>", unsafe_allow_html=True)


st.session_state["continue"] = True

if lang == "fr": answer = chatbot.ask_ai("Qui es-tu ?")
elif lang == "en": answer = chatbot.ask_ai("Who are you?")
chatbot.say(answer)
if print_conv: display_answer(answer)

while True:
    if "continue" in st.session_state:
        conv = chatbot.listen()
        if print_conv: 
            if "continue" not in st.session_state: break
            st.markdown(f"<p class='conversation user_sentence'>{conv[0]}</p>", unsafe_allow_html=True)
            display_answer(conv[1])



    

