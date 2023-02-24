"""Classe utilisée pour parler au chatbot via l'API et récupérer sa réponse"""
import azure.cognitiveservices.speech as speechsdk
import openai
import vocal_assistant.keys as keys

class Chatbot:
    """
    Chatbot qui convertit les paroles de l'utilisateur en texte puis les envoie à l'API
    d'OpenAI. La réponse de l'API est ensuite lue par une voix artificielle.
    Voix disponibles == voix françaises :

    fr-FR-AlainNeural
    fr-FR-BrigitteNeural
    fr-FR-CelesteNeural
    fr-FR-ClaudeNeural
    fr-FR-CoralieNeural
    fr-FR-DeniseNeural1
    fr-FR-EloiseNeural
    fr-FR-HenriNeural
    fr-FR-JacquelineNeural
    fr-FR-JeromeNeural
    fr-FR-JosephineNeural
    fr-FR-MauriceNeural
    fr-FR-YvesNeural
    fr-FR-YvetteNeural
    fr-BE-CharlineNeural
    fr-BE-GerardNeural
    fr-CA-AntoineNeural
    fr-CA-JeanNeural
    fr-CA-SylvieNeural
    fr-CH-ArianeNeural
    fr-CH-FabriceNeural
    ...
    
    voix anglaises :

	en-US-AIGenerate1Neural
    en-US-AIGenerate2Neural
    en-US-AmberNeural
    en-US-AnaNeural
    en-US-AriaNeural
    en-US-AshleyNeural
    en-US-BrandonNeural
    en-US-ChristopherNeural
    en-US-CoraNeural
    en-US-DavisNeural
    en-US-ElizabethNeural
    en-US-EricNeural
    en-US-GuyNeural
    en-US-JacobNeural
    en-US-JaneNeural
    en-US-JasonNeural
    en-US-JennyMultilingualNeural
    en-US-JennyNeural
    en-US-MichelleNeural
    en-US-MonicaNeural
    en-US-NancyNeural
    en-US-RogerNeural1
    en-US-SaraNeural
    en-US-SteffanNeural
    en-US-TonyNeural
    ...

    (liste complète sur https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts)
    """

    def __init__(self, language="en", print_conversation=False, rude_mode=False):
        """
        - language : "fr" ou "en"
        - print_conversation : toute la conversation avec le chatbot sera affichée à l'écran si 
        cette valeur vaut True
        """

        self.language = language
        self.print_conversation = print_conversation
        self.rude_mode = rude_mode

        openai.api_key = keys.OPENAI_API_KEY

        speech_config = speechsdk.SpeechConfig(subscription=keys.SPEECH_KEY, region=keys.SPEECH_REGION)
        if self.language == "en": 
            speech_config.speech_recognition_language="en-US"
            speech_config.speech_synthesis_language = "en-US" 
            speech_config.speech_synthesis_voice_name ="en-US-JennyMultilingualNeural"
        elif self.language == "fr": 
            speech_config.speech_recognition_language= "fr-FR"
            speech_config.speech_synthesis_language = "fr-FR"
            speech_config.speech_synthesis_voice_name = "fr-CA-AntoineNeural"

        else: raise ValueError("Unsupported language, only French and English are supported")

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)
        
    
    def listen(self):
        """
        Écoute le micro de l'utilisateur et réagit en conséquence
        """

        while(True):

            speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
            if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                if self.print_conversation: print(speech_recognition_result.text)
                if self.language == "en" and "exit program" in speech_recognition_result.text.lower():
                    self.say("Have a nice day!")
                    return (speech_recognition_result.text, "Have a nice day!")
                elif self.language == "fr" and "ferme l'application" in speech_recognition_result.text.lower():
                    self.say("À plus tard !")
                    return (speech_recognition_result.text, "À plus tard !")
                
                if self.language == "en" and "tais-toi" in speech_recognition_result.text.lower():
                    self.stop_talking()
                    return (speech_recognition_result.text)
                elif self.language == "fr" and "tais-toi" in speech_recognition_result.text.lower():
                    self.stop_talking()
                    return (speech_recognition_result.text)
                answer = self.ask_ai(speech_recognition_result.text)
                self.say(answer)
                return (speech_recognition_result.text, answer)

            
    
    def say(self, sentence):
        """
        Prononce la phrase 'sentence'
        """
        self.speech_synthesizer.speak_text_async(sentence)
        if self.print_conversation: print(sentence)

    def ask_ai(self, sentence):
        """
        Envoie une requête à l'API d'OpenAI
        """

        if self.language=="en":
            if self.rude_mode:
                sentence = f"""If someone told "{sentence}" to a haughty and rude AI, the AI would answer this:"""
            else:
                sentence = f"""If someone told "{sentence}" to an AI, the AI would answer this:"""
        elif self.language=="fr":
            if self.rude_mode:
                sentence = f"""Si on disait "{sentence}" à un ami particulièrement méprisant, grossier et désagréable, il répondrait ceci : """
            else:
                sentence = f"""Si on disait "{sentence}" à un bon ami il répondrait ceci : """

            

        else: raise ValueError("Unsupported language, only French and English are supported")

        answer = openai.Completion.create(engine="text-davinci-003", 
                                          prompt=sentence, 
                                          max_tokens=2048)["choices"][0]["text"]
        
        return answer.replace('"', "").replace("'", "")
    
    def stop_talking():

        self.speech_synthesizer.stop_speaking()