# Importamos las bibliotecas necesarias
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import speech_recognition as sr
import av
import queue
import pydub


# ================================
# CONFIGURACIÓN DE LA PÁGINA
# ================================

st.set_page_config(
    page_title="Analizador de Sentimientos - Joel Pesantez",
    page_icon="🎤",
    layout="centered"
)

# CSS personalizado
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        max-width: 900px;
    }
    
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        padding: 0.75rem 2rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        font-size: 16px;
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
</style>
""", unsafe_allow_html=True)


# ================================
# FUNCIONES AUXILIARES
# ================================

def analizar_sentimiento(texto):
    """Analiza el sentimiento de un texto en español"""
    try:
        traductor = GoogleTranslator(source='es', target='en')
        texto_ingles = traductor.translate(texto)
        
        blob = TextBlob(texto_ingles)
        polaridad = blob.sentiment.polarity
        subjetividad = blob.sentiment.subjectivity
        
        return polaridad, subjetividad, texto_ingles
    except Exception as e:
        st.error(f"❌ Error al analizar: {str(e)}")
        return None, None, None


def obtener_emoji_sentimiento(polaridad):
    """Retorna emoji y clasificación según la polaridad"""
    if polaridad > 0.5:
        return "😄", "Muy Positivo", "#10b981", "¡Excelente! Tu mensaje irradia felicidad."
    elif polaridad > 0.1:
        return "😊", "Positivo", "#34d399", "Tu mensaje tiene un tono positivo."
    elif polaridad < -0.5:
        return "😢", "Muy Negativo", "#dc2626", "Tu mensaje refleja emociones muy negativas."
    elif polaridad < -0.1:
        return "😔", "Negativo", "#ef4444", "Tu mensaje tiene un tono negativo."
    else:
        return "😐", "Neutral", "#f59e0b", "Tu mensaje es neutral."


def mostrar_resultados(texto, polaridad, subjetividad, texto_ingles):
    """Muestra los resultados del análisis"""
    
    emoji, sentimiento, color, descripcion = obtener_emoji_sentimiento(polaridad)
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1f2937; margin: 2rem 0;'>📊 Resultados del Análisis</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 16px; margin: 1.5rem 0; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);' class='fade-in'>
        <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 0.875rem; 
                   font-weight: 600; text-transform: uppercase;'>
            📝 Texto Analizado
        </p>
        <p style='margin: 0.75rem 0 0 0; color: white; font-size: 1.25rem; 
                   font-weight: 500; line-height: 1.6;'>
            "{texto}"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: white; padding: 3rem 2rem; border-radius: 20px; 
                text-align: center; margin: 2rem 0; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.1); 
                border-top: 6px solid {color};' class='fade-in'>
        <div style='font-size: 5rem; margin-bottom: 1rem;' class='pulse'>{emoji}</div>
        <h2 style='margin: 0; font-weight: 700; font-size: 2.5rem; color: {color};'>
            {sentimiento}
        </h2>
        <p style='margin: 1rem 0; color: #6b7280; font-size: 1rem;'>
            {descripcion}
        </p>
        <p style='color: #9ca3af; font-size: 0.875rem;'>
            Confianza: <strong>{abs(polaridad):.2f}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        valor_normalizado = int((polaridad + 1) * 50)
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);' class='fade-in'>
            <p style='margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.875rem; 
                       font-weight: 600;'>
                📊 POLARIDAD
            </p>
            <div style='background: #f3f4f6; border-radius: 999px; height: 12px; 
                        overflow: hidden; margin: 0.75rem 0;'>
                <div style='background: {color}; height: 100%; width: {valor_normalizado}%; 
                            transition: width 1s ease;'></div>
            </div>
            <p style='margin: 0.5rem 0; color: #111827; font-weight: 700; font-size: 2rem;'>
                {polaridad:.3f}
            </p>
            <p style='color: #9ca3af; font-size: 0.75rem;'>
                -1.0 (negativo) → +1.0 (positivo)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        porcentaje = int(subjetividad * 100)
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);' class='fade-in'>
            <p style='margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.875rem; 
                       font-weight: 600;'>
                🎭 SUBJETIVIDAD
            </p>
            <div style='background: #f3f4f6; border-radius: 999px; height: 12px; 
                        overflow: hidden; margin: 0.75rem 0;'>
                <div style='background: #8b5cf6; height: 100%; width: {porcentaje}%; 
                            transition: width 1s ease;'></div>
            </div>
            <p style='margin: 0.5rem 0; color: #111827; font-weight: 700; font-size: 2rem;'>
                {porcentaje}%
            </p>
            <p style='color: #9ca3af; font-size: 0.75rem;'>
                0% (objetivo) → 100% (opinión)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📖 Interpretación")
    
    if polaridad > 0.5:
        st.success("🎉 **Muy Positivo:** Tu mensaje transmite mucha energía positiva.")
    elif polaridad > 0.1:
        st.success("😊 **Positivo:** Tu mensaje tiene un tono agradable.")
    elif polaridad < -0.5:
        st.error("😢 **Muy Negativo:** Tu mensaje refleja emociones negativas fuertes.")
    elif polaridad < -0.1:
        st.warning("😔 **Negativo:** Tu mensaje tiene un tono de preocupación.")
    else:
        st.info("😐 **Neutral:** Tu mensaje es objetivo.")
    
    if subjetividad > 0.6:
        st.info("💭 **Muy Subjetivo:** Principalmente opinión personal.")
    elif subjetividad > 0.3:
        st.info("🤔 **Mixto:** Combina opiniones y hechos.")
    else:
        st.info("📊 **Objetivo:** Basado en hechos.")
    
    with st.expander("🔬 Detalles técnicos"):
        st.code(texto_ingles, language=None)
        st.json({"Polaridad": round(polaridad, 4), "Subjetividad": round(subjetividad, 4)})


# Cola para procesar audio
audio_queue = queue.Queue()

class AudioProcessor:
    def __init__(self):
        self.frames = []
    
    def recv(self, frame):
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels),
        )
        self.frames.append(sound)
        return frame


# ================================
# INICIALIZAR ESTADO
# ================================

if 'texto_espanol' not in st.session_state:
    st.session_state.texto_espanol = "¡Estoy muy feliz de aprender inteligencia artificial!"


# ================================
# INTERFAZ PRINCIPAL
# ================================

st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='font-weight: 300; margin-bottom: 0; color: #374151;'>
        🎤 Analizador de
    </h1>
    <h1 style='font-weight: 700; font-size: 3.5rem; margin-top: -10px; 
               background: linear-gradient(90deg, #667eea, #764ba2); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        Sentimientos con IA
    </h1>
    <p style='color: #6b7280; font-size: 1.1rem; margin: 1rem 0 0.5rem 0;'>
        Habla o escribe en español para detectar el tono emocional
    </p>
    <p style='color: #9ca3af; font-size: 0.95rem;'>
        👨‍💻 Desarrollado por <strong style='color: #667eea;'>Joel Pesantez</strong>
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎙️ Grabar Audio", "✍️ Escribir Texto"])

# TAB 1: AUDIO
with tab1:
    st.markdown("""
    <div style='background: #f0f9ff; padding: 1.5rem; border-radius: 12px; 
                border-left: 4px solid #667eea; margin-bottom: 1.5rem;'>
        <p style='margin: 0 0 0.75rem 0; color: #1e40af; font-weight: 600;'>
            🎙️ Instrucciones:
        </p>
        <ol style='margin: 0; color: #4b5563; line-height: 1.8;'>
            <li>Presiona <strong>"START"</strong> para iniciar la grabación</li>
            <li><strong>Habla claramente</strong> en español</li>
            <li>Presiona <strong>"STOP"</strong> cuando termines</li>
            <li>Presiona <strong>"Transcribir Audio"</strong> para convertir a texto</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Grabador WebRTC
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": False, "audio": True},
        audio_frame_callback=AudioProcessor().recv,
    )
    
    st.info("💡 **Tip:** Después de grabar, presiona el botón de abajo para transcribir")
    
    if st.button("🎤 Transcribir Audio Grabado", type="primary", use_container_width=True):
        if webrtc_ctx.audio_processor and webrtc_ctx.audio_processor.frames:
            with st.spinner("🔄 Procesando audio..."):
                try:
                    # Combinar todos los frames de audio
                    combined_audio = sum(webrtc_ctx.audio_processor.frames)
                    
                    # Guardar temporalmente
                    combined_audio.export("temp_audio.wav", format="wav")
                    
                    # Reconocer con SpeechRecognition
                    recognizer = sr.Recognizer()
                    with sr.AudioFile("temp_audio.wav") as source:
                        audio_data = recognizer.record(source)
                        texto = recognizer.recognize_google(audio_data, language="es-ES")
                        
                        st.session_state.texto_espanol = texto
                        st.success(f"✅ **Texto reconocido:** {texto}")
                        st.info("👇 Desplázate y presiona 'Analizar Sentimiento'")
                        
                except sr.UnknownValueError:
                    st.error("❌ No pude entender el audio. Intenta hablar más claro.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Primero graba audio presionando START")

# TAB 2: TEXTO
with tab2:
    st.markdown("""
    <div style='background: #fef3c7; padding: 1.25rem; border-radius: 12px; 
                border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #92400e; font-weight: 500;'>
            ✍️ Escribe tu mensaje
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.texto_espanol = st.text_area(
        "Ingresa tu texto:",
        value=st.session_state.texto_espanol,
        height=180,
        placeholder="Ejemplo: Hoy fue un día increíble..."
    )

# Botón análisis
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Analizar Sentimiento", type="primary", use_container_width=True):
        if st.session_state.texto_espanol and st.session_state.texto_espanol.strip():
            with st.spinner("🧠 Analizando..."):
                polaridad, subjetividad, texto_ingles = analizar_sentimiento(
                    st.session_state.texto_espanol
                )
                
                if polaridad is not None:
                    mostrar_resultados(
                        st.session_state.texto_espanol,
                        polaridad,
                        subjetividad,
                        texto_ingles
                    )
        else:
            st.warning("⚠️ Escribe o graba un mensaje primero.")

# Footer
st.markdown("""
<div style='margin-top: 4rem; padding: 2rem; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; text-align: center;'>
    <p style='margin: 0; color: white; font-size: 1.2rem; font-weight: 600;'>
        🚀 Analizador de Sentimientos con IA
    </p>
    <p style='margin: 0.5rem 0; color: rgba(255,255,255,0.95);'>
        Desarrollado por <strong>Joel Pesantez</strong>
    </p>
    <p style='margin: 1rem 0 0 0; color: rgba(255,255,255,0.85); font-size: 0.85rem;'>
        🧠 TextBlob • 🌐 GoogleTranslator • 🎤 WebRTC
    </p>
</div>
""", unsafe_allow_html=True)
