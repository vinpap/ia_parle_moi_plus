from vocal_assistant.chatbot import Chatbot

assistant = Chatbot(language="fr")

# Amélioration possible : Faire en sorte de quitter la boucle quand on dit au revoir au chatbot
while True:
    sentence = input()
    print(assistant.ask(sentence))