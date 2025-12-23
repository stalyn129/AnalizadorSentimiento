# Importamos las bibliotecas necesarias
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import tempfile
import os


# ================================
# CONFIGURACIÓN DE LA PÁGINA
# ================================

st.set_page_config(
    page_title="Analizador de Sentimientos - Joel Pesantez",
    page_icon="🎤",
    layout="centered"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Espaciado general */
    .block-container {
        padding-top: 2rem !important;
        max-width: 900px;
    }
    
    /* Botones */
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        font-size: 16px;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Animación suave */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Cards personalizados */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ================================
# FUNCIONES AUXILIARES
# ================================

def analizar_sentimiento(texto):
    """Analiza el sentimiento de un texto en español"""
    try:
        # Traduce de español a inglés
        traductor = GoogleTranslator(source='es', target='en')
        texto_ingles = traductor.translate(texto)
        
        # Analiza el sentimiento
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
        return "😄", "Muy Positivo", "#10b981"
    elif polaridad > 0.1:
        return "😊", "Positivo", "#34d399"
    elif polaridad < -0.5:
        return "😢", "Muy Negativo", "#dc2626"
    elif polaridad < -0.1:
        return "😔", "Negativo", "#ef4444"
    else:
        return "😐", "Neutral", "#f59e0b"


def mostrar_resultados(texto, polaridad, subjetividad, texto_ingles):
    """Muestra los resultados del análisis de forma visual"""
    
    emoji, sentimiento, color = obtener_emoji_sentimiento(polaridad)
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1f2937;'>📊 Resultados del Análisis</h2>", unsafe_allow_html=True)
    
    # Texto analizado
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 16px; margin: 1.5rem 0; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);' class='fade-in'>
        <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 0.875rem; 
                   font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>
            📝 Texto Analizado
        </p>
        <p style='margin: 0.75rem 0 0 0; color: white; font-size: 1.25rem; 
                   font-weight: 500; line-height: 1.6;'>
            "{texto}"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Card principal del sentimiento
    st.markdown(f"""
    <div style='background: white; padding: 3rem 2rem; border-radius: 20px; 
                text-align: center; margin: 2rem 0; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.1); 
                border-top: 6px solid {color};' class='fade-in'>
        <div style='font-size: 5rem; margin-bottom: 1rem; line-height: 1;'>{emoji}</div>
        <h2 style='margin: 0; font-weight: 700; font-size: 2.5rem; color: {color};'>
            {sentimiento}
        </h2>
        <p style='margin: 0.5rem 0 0 0; color: #6b7280; font-size: 1.125rem;'>
            Confianza: {abs(polaridad):.2f}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas en columnas
    col1, col2 = st.columns(2)
    
    with col1:
        valor_normalizado = int((polaridad + 1) * 50)
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <p style='margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.875rem; 
                       font-weight: 600;'>
                📊 POLARIDAD
            </p>
            <div style='background: #f3f4f6; border-radius: 999px; height: 10px; 
                        overflow: hidden; margin: 0.75rem 0;'>
                <div style='background: {color}; height: 100%; width: {valor_normalizado}%; 
                            transition: width 0.8s ease;'></div>
            </div>
            <p style='margin: 0.5rem 0 0 0; color: #111827; font-weight: 700; 
                       font-size: 2rem;'>
                {polaridad:.3f}
            </p>
            <p style='margin: 0.25rem 0 0 0; color: #9ca3af; font-size: 0.75rem;'>
                -1.0 (negativo) → +1.0 (positivo)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        porcentaje = int(subjetividad * 100)
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <p style='margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.875rem; 
                       font-weight: 600;'>
                🎭 SUBJETIVIDAD
            </p>
            <div style='background: #f3f4f6; border-radius: 999px; height: 10px; 
                        overflow: hidden; margin: 0.75rem 0;'>
                <div style='background: #8b5cf6; height: 100%; width: {porcentaje}%; 
                            transition: width 0.8s ease;'></div>
            </div>
            <p style='margin: 0.5rem 0 0 0; color: #111827; font-weight: 700; 
                       font-size: 2rem;'>
                {porcentaje}%
            </p>
            <p style='margin: 0.25rem 0 0 0; color: #9ca3af; font-size: 0.75rem;'>
                0% (objetivo) → 100% (opinión)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interpretación detallada
    st.markdown("### 📖 Interpretación Detallada:")
    
    if polaridad > 0.5:
        mensaje = "🎉 Tu mensaje transmite **mucha energía positiva** y optimismo."
        tipo = "success"
    elif polaridad > 0.1:
        mensaje = "😊 Tu mensaje tiene un **tono positivo** y agradable."
        tipo = "success"
    elif polaridad < -0.5:
        mensaje = "😢 Tu mensaje refleja **emociones negativas muy fuertes**."
        tipo = "error"
    elif polaridad < -0.1:
        mensaje = "😔 Tu mensaje tiene un **tono negativo** o de preocupación."
        tipo = "warning"
    else:
        mensaje = "😐 Tu mensaje es **neutral**, sin emociones marcadas."
        tipo = "info"
    
    if tipo == "success":
        st.success(mensaje)
    elif tipo == "error":
        st.error(mensaje)
    elif tipo == "warning":
        st.warning(mensaje)
    else:
        st.info(mensaje)
    
    # Análisis de subjetividad
    if subjetividad > 0.7:
        st.info("💭 Tu mensaje es **muy subjetivo** (opinión personal fuerte).")
    elif subjetividad > 0.4:
        st.info("🤔 Tu mensaje mezcla opiniones con algunos hechos.")
    else:
        st.info("📊 Tu mensaje es **mayormente objetivo** (basado en hechos).")
    
    # Expander con traducción
    with st.expander("🌐 Ver traducción al inglés"):
        st.code(texto_ingles, language=None)


# ================================
# INICIALIZAR ESTADO
# ================================

if 'texto_espanol' not in st.session_state:
    st.session_state.texto_espanol = "¡Estoy muy feliz de aprender inteligencia artificial!"

# Reconocedor de voz
recognizer = sr.Recognizer()


# ================================
# INTERFAZ PRINCIPAL
# ================================

# Título con nombre del autor
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
        Escribe o habla en español y la IA detectará el tono emocional
    </p>
    <p style='color: #9ca3af; font-size: 0.95rem;'>
        👨‍💻 Desarrollado por <strong style='color: #667eea;'>Joel Pesantez</strong>
    </p>
</div>
""", unsafe_allow_html=True)


# ================================
# TABS: TEXTO Y VOZ
# ================================

tab1, tab2 = st.tabs(["✍️ Escribir Texto", "🎙️ Hablar por Micrófono"])

# --- TAB 1: ENTRADA DE TEXTO ---
with tab1:
    st.markdown("""
    <div style='background: #fef3c7; padding: 1.25rem; border-radius: 12px; 
                border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #92400e; font-weight: 500;'>
            ✍️ Escribe tu mensaje y presiona <strong>"Analizar Sentimiento"</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.texto_espanol = st.text_area(
        "Ingresa tu texto aquí:",
        value=st.session_state.texto_espanol,
        height=180,
        key="text_input",
        placeholder="Ejemplo: Hoy fue un día increíble, aprendí muchas cosas nuevas..."
    )


# --- TAB 2: ENTRADA DE VOZ ---
with tab2:
    st.markdown("""
    <div style='background: #f0f9ff; padding: 1.5rem; border-radius: 12px; 
                border-left: 4px solid #667eea; margin-bottom: 1.5rem;'>
        <p style='margin: 0 0 0.75rem 0; color: #1e40af; font-weight: 600; 
                   font-size: 1.1rem;'>
            🎙️ Instrucciones de Grabación:
        </p>
        <ol style='margin: 0.5rem 0 0 1.25rem; color: #4b5563; line-height: 1.8;'>
            <li><strong>Presiona el botón rojo</strong> para iniciar la grabación</li>
            <li><strong>Habla claramente</strong> en español hacia tu micrófono</li>
            <li><strong>Presiona "Stop"</strong> cuando termines de hablar</li>
            <li>El texto será <strong>transcrito automáticamente</strong></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Grabador de audio
    audio_bytes = audio_recorder(
        text="🎤 Haz clic para grabar",
        recording_color="#e74c3c",
        neutral_color="#667eea",
        icon_name="microphone",
        icon_size="3x",
        pause_threshold=2.0,
        sample_rate=16000
    )
    
    # Procesar audio grabado
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        with st.spinner("🔄 Transcribiendo tu voz... Por favor espera"):
            try:
                # Guardar audio en archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_bytes)
                    tmp_file_path = tmp_file.name
                
                # Reconocer el audio
                with sr.AudioFile(tmp_file_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    
                    texto_reconocido = recognizer.recognize_google(
                        audio_data,
                        language="es-ES"
                    )
                    
                    st.session_state.texto_espanol = texto_reconocido
                    
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                                padding: 1.25rem; border-radius: 12px; margin: 1rem 0;'>
                        <p style='margin: 0; color: white; font-weight: 600;'>
                            ✅ Transcripción exitosa:
                        </p>
                        <p style='margin: 0.5rem 0 0 0; color: white; font-size: 1.125rem;'>
                            "{texto_reconocido}"
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Eliminar archivo temporal
                os.unlink(tmp_file_path)
                
            except sr.UnknownValueError:
                st.error("❌ No pude entender el audio. Intenta hablar más claro y cerca del micrófono.")
            except sr.RequestError as e:
                st.error(f"❌ Error de conexión con el servicio de Google: {e}")
            except Exception as e:
                st.error(f"❌ Error inesperado al procesar el audio: {str(e)}")
    
    # Consejos para mejor grabación
    st.markdown("---")
    st.markdown("**💡 Consejos para mejor reconocimiento:**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- ✅ Habla claro y pausado")
        st.markdown("- ✅ Mantén el micrófono cerca")
    with col2:
        st.markdown("- ✅ Evita ruidos de fondo")
        st.markdown("- ✅ Usa un ambiente silencioso")


# ================================
# BOTÓN DE ANÁLISIS
# ================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analizar_btn = st.button(
        "🔍 Analizar Sentimiento",
        type="primary",
        use_container_width=True
    )

if analizar_btn:
    if st.session_state.texto_espanol and st.session_state.texto_espanol.strip():
        with st.spinner("🧠 Analizando el sentimiento..."):
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
        st.warning("⚠️ Por favor, escribe o graba un mensaje para analizar.")


# ================================
# FOOTER
# ================================

st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 3rem; padding: 2rem; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; text-align: center;'>
    <p style='margin: 0; color: white; font-size: 1.1rem; font-weight: 600;'>
        🚀 Analizador de Sentimientos con IA
    </p>
    <p style='margin: 0.5rem 0; color: rgba(255,255,255,0.95); font-size: 0.95rem;'>
        Desarrollado por <strong>Joel Pesantez</strong>
    </p>
    <p style='margin: 1rem 0 0 0; color: rgba(255,255,255,0.85); font-size: 0.8rem;'>
        🧠 TextBlob | 🌐 GoogleTranslator | 🎤 SpeechRecognition
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e5e7eb; 
            text-align: center; color: #9ca3af; font-size: 0.875rem;'>
    © 2024 Joel Pesantez - Todos los derechos reservados
</div>
""", unsafe_allow_html=True)