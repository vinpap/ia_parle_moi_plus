"""
Code de l'application Streamlit. Pour lancer l'appli, utiliser la commande suivante :
streamlit run app.py
"""

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


print_conv = True # Affiche la conversation dans le terminal ou non
lang = "fr" # L'anglais et le français sont gérés
bot_is_rude = False # À mettre à True pour activer le mode toxique du chatbot
use_azure = True # Utilisation d'Azure Speech ou du modèle alternatif (pas encore implémenté)

chatbot = Chatbot(language=lang, print_conversation=print_conv, rude_mode=bot_is_rude, use_azure=use_azure)
st.balloons()
st.markdown("<h1 style='text-align: center; color: black; font-size:60px'>Votre ami imaginaire</h1>", unsafe_allow_html=True)
st.image("meme.jpg")
st.markdown("<h2 style='text-align: center; color: black; font-size:30px'>Pas d'amis ? Pas de problème ! Découvrez nos amis imaginaires (presque) sympathiques disponibles 24h/24 et 7j7 !</h2>", unsafe_allow_html=True)
if not bot_is_rude:
    st.markdown("<h2 style='text-align: center; color: black; font-size:16px; font-style: italic bold'>Astuce : votre vie manque de négativité ? Activez le mode toxique pour discuter avec l'ami toxique que vous avez toujours rêvé d'avoir !</h2>", unsafe_allow_html=True)


if bot_is_rude: 
    st.markdown("<h3 style='text-align: center; color: red; font-size:20px'>Mode toxique activé</h3>", unsafe_allow_html=True)


st.session_state["continue"] = True



while True:
    if "continue" in st.session_state:
        conv = chatbot.listen()
        if print_conv: 
            if "continue" not in st.session_state: break
            st.markdown(f"<p class='conversation user_sentence'>{conv[0]}</p>", unsafe_allow_html=True)
            display_answer(conv[1])



    

