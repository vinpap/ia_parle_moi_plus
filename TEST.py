"""Ce fichier contient les modèles à utiliser pour remplacer Azure Speech pour la reconnaissance vocale.
Ils n'ont pas encore été intégrés à l'application."""


###########################################################################
# Modèle de reconnaissance vocale pour l'anglais
###########################################################################
import torch
import librosa
import numpy as np
import soundfile as sf
from scipy.io import wavfile
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


file_name = 'TEST/example.wav'

data = wavfile.read(file_name)
framerate = data[0]
sounddata = data[1]
time = np.arange(0,len(sounddata))/framerate
print('Sampling rate:',framerate,'Hz')

input_audio, _ = librosa.load(file_name, sr=16000)


input_values = tokenizer(input_audio, return_tensors="pt").input_values
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = tokenizer.batch_decode(predicted_ids)[0]
print(transcription)

###########################################################################
# Modèle de reconnaissance vocale pour le français
###########################################################################
from speechbrain.pretrained import EncoderDecoderASR
asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-commonvoice-fr", savedir="pretrained_models/asr-crdnn-commonvoice-fr", run_opts={"device":"cuda"})
text = asr_model.transcribe_file("TEST/example_FR.wav")
print(text)





