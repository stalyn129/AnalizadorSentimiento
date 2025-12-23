import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import tempfile
import os

# Configuración principal
st.set_page_config(
    page_title="Detector de Emociones IA",
    page_icon="🧠",
    layout="wide"
)

# Header personalizado
st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>
            🧠 Detector Inteligente de Emociones
        </h1>
        <p style='color: white; text-align: center; margin-top: 10px; opacity: 0.9;'>
            Analiza el sentimiento de cualquier texto con IA avanzada
        </p>
    </div>
""", unsafe_allow_html=True)

# Inicialización
rec = sr.Recognizer()
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Layout en columnas
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 💬 Entrada de Datos")
    
    modo = st.radio(
        "Selecciona el modo de entrada:",
        ["📝 Texto Manual", "🎙️ Grabación de Voz"],
        horizontal=True
    )
    
    if modo == "📝 Texto Manual":
        texto_usuario = st.text_area(
            "Escribe tu mensaje:",
            value=st.session_state.input_text,
            height=200,
            placeholder="Ejemplo: Me siento increíble hoy, todo va muy bien..."
        )
        st.session_state.input_text = texto_usuario
        
    else:
        st.markdown("**Presiona el botón y comienza a hablar:**")
        audio_data = audio_recorder(
            text="",
            recording_color="#667eea",
            neutral_color="#764ba2",
            icon_name="microphone-lines",
            icon_size="2x"
        )
        
        if audio_data:
            st.audio(audio_data, format="audio/wav")
            
            with st.spinner("Procesando audio..."):
                try:
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    temp_file.write(audio_data)
                    temp_file.close()
                    
                    with sr.AudioFile(temp_file.name) as audio_source:
                        rec.adjust_for_ambient_noise(audio_source)
                        recorded_audio = rec.record(audio_source)
                        transcription = rec.recognize_google(recorded_audio, language="es-ES")
                        
                        st.session_state.input_text = transcription
                        st.success(f"✨ Transcripción: **{transcription}**")
                    
                    os.unlink(temp_file.name)
                    
                except sr.UnknownValueError:
                    st.error("⚠️ No se pudo reconocer el audio. Intenta hablar más claro.")
                except Exception as error:
                    st.error(f"Error: {error}")

with col_right:
    st.markdown("### ℹ️ Información")
    st.info("""
    **¿Cómo funciona?**
    
    1. Ingresa texto o graba tu voz
    2. La IA traduce y analiza
    3. Obtienes resultados instantáneos
    
    **Métricas:**
    - 😊 Polaridad emocional
    - 🎯 Nivel de subjetividad
    - 📈 Intensidad del sentimiento
    """)

# Botón de análisis
st.markdown("---")
if st.button("🚀 Analizar Sentimiento Ahora", use_container_width=True, type="primary"):
    if st.session_state.input_text.strip():
        with st.spinner("Analizando..."):
            try:
                # Traducción
                translator = GoogleTranslator(source='es', target='en')
                english_text = translator.translate(st.session_state.input_text)
                
                # Análisis
                analysis = TextBlob(english_text)
                polarity_score = analysis.sentiment.polarity
                subjectivity_score = analysis.sentiment.subjectivity
                
                # Resultados
                st.markdown("---")
                st.markdown("## 📊 Resultados del Análisis")
                
                # Tarjeta de texto
                st.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 20px; 
                            border-left: 5px solid #667eea; border-radius: 5px;'>
                    <strong>Texto analizado:</strong><br>
                    {st.session_state.input_text}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Métricas visuales
                metric1, metric2, metric3 = st.columns(3)
                
                with metric1:
                    if polarity_score > 0.15:
                        emoji = "😄"
                        label = "POSITIVO"
                        color = "#2ecc71"
                    elif polarity_score < -0.15:
                        emoji = "😢"
                        label = "NEGATIVO"
                        color = "#e74c3c"
                    else:
                        emoji = "😐"
                        label = "NEUTRAL"
                        color = "#95a5a6"
                    
                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background-color: {color}20; 
                                border-radius: 10px;'>
                        <h1 style='margin: 0; font-size: 3em;'>{emoji}</h1>
                        <h3 style='margin: 10px 0; color: {color};'>{label}</h3>
                        <p style='margin: 0; font-size: 1.5em;'>{polarity_score:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric2:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background-color: #3498db20; 
                                border-radius: 10px;'>
                        <h3 style='margin: 0; color: #3498db;'>POLARIDAD</h3>
                        <p style='margin: 10px 0; font-size: 2em; font-weight: bold;'>
                            {polarity_score:.3f}
                        </p>
                        <p style='margin: 0; font-size: 0.9em; color: #666;'>Rango: -1 a +1</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric3:
                    percentage = int(subjectivity_score * 100)
                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background-color: #9b59b620; 
                                border-radius: 10px;'>
                        <h3 style='margin: 0; color: #9b59b6;'>SUBJETIVIDAD</h3>
                        <p style='margin: 10px 0; font-size: 2em; font-weight: bold;'>
                            {percentage}%
                        </p>
                        <p style='margin: 0; font-size: 0.9em; color: #666;'>
                            {subjectivity_score:.2f}/1.00
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Interpretación detallada
                st.markdown("---")
                st.markdown("### 🔍 Análisis Detallado")
                
                interpretation_col1, interpretation_col2 = st.columns(2)
                
                with interpretation_col1:
                    st.markdown("**📉 Polaridad Emocional:**")
                    normalized = (polarity_score + 1) / 2
                    st.progress(normalized)
                    
                    if polarity_score > 0.5:
                        st.success("Emoción extremadamente positiva detectada")
                    elif polarity_score > 0.15:
                        st.info("Tono positivo identificado")
                    elif polarity_score < -0.5:
                        st.error("Emoción fuertemente negativa")
                    elif polarity_score < -0.15:
                        st.warning("Tono negativo presente")
                    else:
                        st.info("Tono neutral y equilibrado")
                
                with interpretation_col2:
                    st.markdown("**🎯 Nivel de Subjetividad:**")
                    st.progress(subjectivity_score)
                    
                    if subjectivity_score > 0.7:
                        st.write("Texto altamente subjetivo (opinión personal)")
                    elif subjectivity_score > 0.4:
                        st.write("Balance entre opinión y hechos")
                    else:
                        st.write("Texto mayormente objetivo")
                
            except Exception as e:
                st.error(f"❌ Error durante el análisis: {str(e)}")
    else:
        st.warning("⚠️ Debes ingresar texto o grabar audio antes de analizar")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p style='margin: 5px;'>🎓 Desarrollado por <strong>Tu Nombre Aquí</strong></p>
    <p style='margin: 5px; font-size: 0.9em;'>
        Tecnologías: Streamlit • TextBlob • Deep Translator • Speech Recognition
    </p>
</div>
""", unsafe_allow_html=True)
