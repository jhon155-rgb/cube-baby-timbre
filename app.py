import streamlit as st
import librosa
import numpy as np
import tempfile

timbres_por_estilo = {
    'rock': 'British Crunch',
    'metal': 'Heavy Distortion',
    'blues': 'Clean Blues',
    'jazz': 'Warm Clean',
    'funk': 'Funky Wah',
    'pop': 'Bright Clean',
    'reggae': 'Dub Clean Delay',
}

def detectar_estilo(audio_path):
    y, sr = librosa.load(audio_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()

    if tempo > 130 and spectral_centroid > 3000:
        return 'metal'
    elif tempo > 110 and spectral_centroid > 2000:
        return 'rock'
    elif tempo < 90 and spectral_centroid < 1500:
        return 'jazz'
    elif 90 <= tempo <= 110 and spectral_centroid < 1800:
        return 'blues'
    elif 100 < tempo < 120 and 1800 <= spectral_centroid < 2500:
        return 'pop'
    elif 70 < tempo < 100 and spectral_centroid > 2500:
        return 'funk'
    elif tempo < 80 and spectral_centroid < 1200:
        return 'reggae'
    else:
        return 'rock'

def sugerir_timbre(estilo):
    return timbres_por_estilo.get(estilo, 'Clean Standard')

st.title("Detector de Timbre para Cube Baby")
st.write("Envie uma música para sugerirmos o melhor timbre para a sua Cube Baby.")

audio_file = st.file_uploader("Escolha um arquivo de áudio (MP3, WAV)", type=['mp3', 'wav'])

if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    estilo = detectar_estilo(tmp_path)
    timbre = sugerir_timbre(estilo)

    st.success(f"Estilo detectado: **{estilo}**")
    st.info(f"Sugestão de timbre para Cube Baby: **{timbre}**")
