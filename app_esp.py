# Importamos las bibliotecas necesarias
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import streamlit.components.v1 as components


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
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Animación suave */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Animación de pulso */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Botón de micrófono personalizado */
    #micButton {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        font-size: 3rem;
        cursor: pointer;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        margin: 20px auto;
        display: block;
    }
    
    #micButton:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
    }
    
    #micButton.recording {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        animation: pulse 1s infinite;
    }
    
    #status {
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
        font-size: 1.1rem;
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
        return "😄", "Muy Positivo", "#10b981", "¡Excelente! Tu mensaje irradia felicidad y optimismo."
    elif polaridad > 0.1:
        return "😊", "Positivo", "#34d399", "Tu mensaje tiene un tono positivo y agradable."
    elif polaridad < -0.5:
        return "😢", "Muy Negativo", "#dc2626", "Tu mensaje refleja emociones negativas muy fuertes."
    elif polaridad < -0.1:
        return "😔", "Negativo", "#ef4444", "Tu mensaje tiene un tono negativo o de preocupación."
    else:
        return "😐", "Neutral", "#f59e0b", "Tu mensaje es neutral, sin emociones marcadas."


def mostrar_resultados(texto, polaridad, subjetividad, texto_ingles):
    """Muestra los resultados del análisis de forma visual"""
    
    emoji, sentimiento, color, descripcion = obtener_emoji_sentimiento(polaridad)
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1f2937; margin: 2rem 0;'>📊 Resultados del Análisis</h2>", unsafe_allow_html=True)
    
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
        <div style='font-size: 5rem; margin-bottom: 1rem; line-height: 1;' class='pulse'>{emoji}</div>
        <h2 style='margin: 0; font-weight: 700; font-size: 2.5rem; color: {color};'>
            {sentimiento}
        </h2>
        <p style='margin: 1rem 0 0.5rem 0; color: #6b7280; font-size: 1rem; line-height: 1.6;'>
            {descripcion}
        </p>
        <p style='margin: 0.5rem 0 0 0; color: #9ca3af; font-size: 0.875rem;'>
            Nivel de confianza: <strong>{abs(polaridad):.2f}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas en columnas
    col1, col2 = st.columns(2)
    
    with col1:
        valor_normalizado = int((polaridad + 1) * 50)
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); 
                    border: 1px solid #f3f4f6;' class='fade-in'>
            <p style='margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.875rem; 
                       font-weight: 600;'>
                📊 POLARIDAD EMOCIONAL
            </p>
            <div style='background: #f3f4f6; border-radius: 999px; height: 12px; 
                        overflow: hidden; margin: 0.75rem 0;'>
                <div style='background: {color}; height: 100%; width: {valor_normalizado}%; 
                            transition: width 1s ease;'></div>
            </div>
            <p style='margin: 0.5rem 0 0 0; color: #111827; font-weight: 700; 
                       font-size: 2.25rem;'>
                {polaridad:.3f}
            </p>
            <p style='margin: 0.5rem 0 0 0; color: #9ca3af; font-size: 0.75rem; 
                       line-height: 1.4;'>
                -1.0 (muy negativo) → +1.0 (muy positivo)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        porcentaje = int(subjetividad * 100)
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); 
                    border: 1px solid #f3f4f6;' class='fade-in'>
            <p style='margin: 0 0 0.75rem 0; color: #6b7280; font-size: 0.875rem; 
                       font-weight: 600;'>
                🎭 SUBJETIVIDAD
            </p>
            <div style='background: #f3f4f6; border-radius: 999px; height: 12px; 
                        overflow: hidden; margin: 0.75rem 0;'>
                <div style='background: linear-gradient(90deg, #8b5cf6, #6d28d9); 
                            height: 100%; width: {porcentaje}%; 
                            transition: width 1s ease;'></div>
            </div>
            <p style='margin: 0.5rem 0 0 0; color: #111827; font-weight: 700; 
                       font-size: 2.25rem;'>
                {porcentaje}%
            </p>
            <p style='margin: 0.5rem 0 0 0; color: #9ca3af; font-size: 0.75rem; 
                       line-height: 1.4;'>
                0% = objetivo → 100% = opinión
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interpretación
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 📖 Interpretación")
    
    if polaridad > 0.5:
        st.success("🎉 **Mensaje Muy Positivo:** Tu texto transmite mucha energía positiva y optimismo.")
    elif polaridad > 0.1:
        st.success("😊 **Mensaje Positivo:** Tu texto tiene un tono agradable y favorable.")
    elif polaridad < -0.5:
        st.error("😢 **Mensaje Muy Negativo:** Tu texto refleja emociones negativas fuertes.")
    elif polaridad < -0.1:
        st.warning("😔 **Mensaje Negativo:** Tu texto tiene un tono de preocupación.")
    else:
        st.info("😐 **Mensaje Neutral:** Tu texto es objetivo y no expresa emociones marcadas.")
    
    if subjetividad > 0.7:
        st.info("💭 **Muy Subjetivo:** Tu mensaje es principalmente una opinión personal.")
    elif subjetividad > 0.4:
        st.info("🤔 **Mixto:** Tu mensaje combina opiniones con hechos.")
    else:
        st.info("📊 **Objetivo:** Tu mensaje está basado en hechos y datos.")
    
    with st.expander("🔬 Ver detalles técnicos"):
        st.markdown("**🌐 Traducción al inglés:**")
        st.code(texto_ingles, language=None)
        st.json({
            "Polaridad": round(polaridad, 4),
            "Subjetividad": round(subjetividad, 4),
            "Clasificación": sentimiento
        })


# Componente HTML para reconocimiento de voz del navegador
def speech_recognition_component():
    html_code = """
    <div style="text-align: center; padding: 20px;">
        <button id="micButton" onclick="toggleRecording()">🎤</button>
        <div id="status" style="color: #667eea;">Presiona el micrófono para hablar</div>
        <div id="transcript" style="margin-top: 20px; padding: 15px; background: #f3f4f6; border-radius: 12px; min-height: 60px; display: none;">
            <strong>Texto reconocido:</strong>
            <p id="transcriptText" style="margin: 10px 0 0 0; color: #1f2937;"></p>
        </div>
    </div>
    
    <script>
        let recognition;
        let isRecording = false;
        
        // Verificar soporte del navegador
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                document.getElementById('status').textContent = '🎙️ Escuchando... Habla ahora';
                document.getElementById('status').style.color = '#ef4444';
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('transcriptText').textContent = transcript;
                document.getElementById('transcript').style.display = 'block';
                document.getElementById('status').textContent = '✅ Texto capturado exitosamente';
                document.getElementById('status').style.color = '#10b981';
                
                // Enviar el texto a Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: transcript
                }, '*');
            };
            
            recognition.onerror = function(event) {
                let errorMsg = 'Error al reconocer voz';
                if (event.error === 'no-speech') {
                    errorMsg = '❌ No se detectó voz. Intenta de nuevo';
                } else if (event.error === 'not-allowed') {
                    errorMsg = '❌ Permiso denegado. Permite el acceso al micrófono';
                }
                document.getElementById('status').textContent = errorMsg;
                document.getElementById('status').style.color = '#ef4444';
                document.getElementById('micButton').classList.remove('recording');
                isRecording = false;
            };
            
            recognition.onend = function() {
                document.getElementById('micButton').classList.remove('recording');
                isRecording = false;
                if (document.getElementById('status').style.color !== '#10b981') {
                    document.getElementById('status').textContent = 'Presiona el micrófono para hablar';
                    document.getElementById('status').style.color = '#667eea';
                }
            };
        } else {
            document.getElementById('status').textContent = '❌ Tu navegador no soporta reconocimiento de voz';
            document.getElementById('status').style.color = '#ef4444';
            document.getElementById('micButton').disabled = true;
        }
        
        function toggleRecording() {
            if (!recognition) return;
            
            if (isRecording) {
                recognition.stop();
                document.getElementById('micButton').classList.remove('recording');
                isRecording = false;
            } else {
                recognition.start();
                document.getElementById('micButton').classList.add('recording');
                isRecording = true;
            }
        }
    </script>
    """
    
    return components.html(html_code, height=300)


# ================================
# INICIALIZAR ESTADO
# ================================

if 'texto_espanol' not in st.session_state:
    st.session_state.texto_espanol = "¡Estoy muy feliz de aprender inteligencia artificial con esta aplicación!"


# ================================
# INTERFAZ PRINCIPAL
# ================================

# Título
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
        Habla o escribe en español y la IA detectará el tono emocional
    </p>
    <p style='color: #9ca3af; font-size: 0.95rem;'>
        👨‍💻 Desarrollado por <strong style='color: #667eea;'>Joel Pesantez</strong>
    </p>
</div>
""", unsafe_allow_html=True)


# Tabs
tab1, tab2 = st.tabs(["🎙️ Hablar por Micrófono", "✍️ Escribir Texto"])

# TAB 1: VOZ
with tab1:
    st.markdown("""
    <div style='background: #f0f9ff; padding: 1.5rem; border-radius: 12px; 
                border-left: 4px solid #667eea; margin-bottom: 1.5rem;'>
        <p style='margin: 0 0 0.75rem 0; color: #1e40af; font-weight: 600;'>
            🎙️ Instrucciones:
        </p>
        <ol style='margin: 0; color: #4b5563; line-height: 1.8;'>
            <li>Presiona el botón del <strong>micrófono 🎤</strong></li>
            <li><strong>Permite el acceso</strong> al micrófono en tu navegador</li>
            <li><strong>Habla claramente</strong> en español</li>
            <li>El texto se capturará <strong>automáticamente</strong></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Componente de reconocimiento de voz
    texto_reconocido = speech_recognition_component()
    
    # Si hay texto reconocido, guardarlo
    if texto_reconocido:
        st.session_state.texto_espanol = texto_reconocido
        st.success(f"✅ Texto capturado: **{texto_reconocido}**")
        st.info("👇 Desplázate hacia abajo y presiona 'Analizar Sentimiento'")

# TAB 2: TEXTO
with tab2:
    st.markdown("""
    <div style='background: #fef3c7; padding: 1.25rem; border-radius: 12px; 
                border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #92400e; font-weight: 500;'>
            ✍️ Escribe tu mensaje y presiona "Analizar Sentimiento"
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


# Botón de análisis
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
        st.warning("⚠️ Por favor, habla o escribe un mensaje para analizar.")


# Footer
st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 3rem; padding: 2rem; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; text-align: center;'>
    <p style='margin: 0; color: white; font-size: 1.2rem; font-weight: 600;'>
        🚀 Analizador de Sentimientos con IA
    </p>
    <p style='margin: 0.5rem 0; color: rgba(255,255,255,0.95); font-size: 1rem;'>
        Desarrollado por <strong>Joel Pesantez</strong>
    </p>
    <p style='margin: 1rem 0 0 0; color: rgba(255,255,255,0.85); font-size: 0.85rem;'>
        🧠 TextBlob • 🌐 GoogleTranslator • 🎤 Web Speech API
    </p>
</div>
""", unsafe_allow_html=True)
