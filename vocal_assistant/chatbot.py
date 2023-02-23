"""Classe utilisée pour parler au chatbot via l'API et récupérer sa réponse"""

import openai
import vocal_assistant.keys as keys

class Chatbot:

    def __init__(self, language="en"):

        openai.api_key = keys.OPENAI_API_KEY
        self.language = language
    
    def ask(self, sentence):

        if self.language=="en":
            sentence = f"""If someone told an artificial intelligence this: '{sentence}', the AI would answer this:"""
        elif self.language=="fr":
            sentence = f"""Si on disait ceci à une intelligence artificielle : '{sentence}', elle répondrait ceci : """

        else: raise ValueError("Unsupported language, only French and English are supported")

        answer = openai.Completion.create(engine="text-davinci-003", 
                                          prompt=sentence, 
                                          max_tokens=2048)["choices"][0]["text"]
        
        return answer.replace('"', "").replace("'", "")
