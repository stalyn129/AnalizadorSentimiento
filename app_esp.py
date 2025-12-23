# Importamos las bibliotecas necesarias
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator


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
    
    /* Animación de pulso para resultados */
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
    
    # Card principal del sentimiento con animación
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
    
    # Métricas en columnas con barras de progreso animadas
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
                Rango: -1.0 (muy negativo)<br>
                hasta +1.0 (muy positivo)
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
                0% = objetivo/factual<br>
                100% = opinión personal
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interpretación detallada con iconos
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 📖 Interpretación Completa")
    
    # Análisis de polaridad
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
    with col2:
        if polaridad > 0.5:
            st.success("🎉 **Mensaje Muy Positivo:** Tu texto transmite mucha energía positiva, alegría y optimismo. Las palabras elegidas reflejan entusiasmo.")
        elif polaridad > 0.1:
            st.success("😊 **Mensaje Positivo:** Tu texto tiene un tono agradable y favorable. Expresa satisfacción o aprobación.")
        elif polaridad < -0.5:
            st.error("😢 **Mensaje Muy Negativo:** Tu texto refleja emociones negativas fuertes como tristeza, enojo o decepción.")
        elif polaridad < -0.1:
            st.warning("😔 **Mensaje Negativo:** Tu texto tiene un tono de preocupación, descontento o crítica.")
        else:
            st.info("😐 **Mensaje Neutral:** Tu texto es objetivo y no expresa emociones marcadas. Es informativo o descriptivo.")
    
    # Análisis de subjetividad
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    if subjetividad > 0.7:
        st.info("💭 **Muy Subjetivo:** Tu mensaje es principalmente una **opinión personal** con juicios de valor. Refleja tus sentimientos y perspectiva.")
    elif subjetividad > 0.4:
        st.info("🤔 **Mixto:** Tu mensaje combina **opiniones personales con algunos hechos**. Hay elementos tanto subjetivos como objetivos.")
    else:
        st.info("📊 **Objetivo:** Tu mensaje está basado principalmente en **hechos y datos**, con poca opinión personal. Es informativo y neutral.")
    
    # Expander con detalles técnicos
    with st.expander("🔬 Detalles Técnicos del Análisis"):
        st.markdown("**🌐 Traducción al inglés:**")
        st.code(texto_ingles, language=None)
        
        st.markdown("**📐 Valores numéricos:**")
        st.json({
            "Polaridad": round(polaridad, 4),
            "Subjetividad": round(subjetividad, 4),
            "Polaridad (%)": f"{valor_normalizado}%",
            "Clasificación": sentimiento
        })
        
        st.markdown("**ℹ️ Cómo funciona:**")
        st.markdown("""
        - El texto se traduce de español a inglés usando Google Translator
        - TextBlob analiza el sentimiento del texto en inglés
        - La **polaridad** mide si el texto es positivo o negativo
        - La **subjetividad** mide si el texto es opinión u objetivo
        """)


# ================================
# INICIALIZAR ESTADO
# ================================

if 'texto_espanol' not in st.session_state:
    st.session_state.texto_espanol = "¡Estoy muy feliz de aprender inteligencia artificial con esta aplicación!"

if 'historial' not in st.session_state:
    st.session_state.historial = []


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
        Escribe en español y la IA detectará el tono emocional de tu mensaje
    </p>
    <p style='color: #9ca3af; font-size: 0.95rem;'>
        👨‍💻 Desarrollado por <strong style='color: #667eea;'>Joel Pesantez</strong>
    </p>
</div>
""", unsafe_allow_html=True)


# ================================
# ÁREA DE ENTRADA DE TEXTO
# ================================

st.markdown("""
<div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
            padding: 1.25rem; border-radius: 12px; 
            border-left: 4px solid #f59e0b; margin-bottom: 1.5rem;'>
    <p style='margin: 0; color: #92400e; font-weight: 500; font-size: 0.95rem;'>
        ✍️ <strong>Escribe tu mensaje</strong> y presiona el botón "Analizar Sentimiento" para obtener los resultados
    </p>
</div>
""", unsafe_allow_html=True)

st.session_state.texto_espanol = st.text_area(
    "Ingresa tu texto aquí:",
    value=st.session_state.texto_espanol,
    height=200,
    key="text_input",
    placeholder="Ejemplo: Hoy fue un día increíble, aprendí muchas cosas nuevas y conocí gente maravillosa. Me siento muy motivado para seguir adelante...",
    help="Escribe en español. Puedes usar emojis y puntuación para expresarte mejor."
)

# Contador de caracteres
char_count = len(st.session_state.texto_espanol)
if char_count > 0:
    st.caption(f"📝 {char_count} caracteres | {'✅ Listo para analizar' if char_count > 10 else '⚠️ Escribe al menos 10 caracteres'}")


# ================================
# EJEMPLOS RÁPIDOS
# ================================

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
st.markdown("**💡 Ejemplos rápidos:**")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😊 Ejemplo Positivo", use_container_width=True):
        st.session_state.texto_espanol = "¡Qué día tan maravilloso! Logré terminar mi proyecto y recibí excelentes comentarios. Me siento muy orgulloso del trabajo que hice."
        st.rerun()

with col2:
    if st.button("😐 Ejemplo Neutral", use_container_width=True):
        st.session_state.texto_espanol = "El seminario comenzó a las 9 de la mañana. Participaron 50 personas. Se discutieron temas de tecnología e innovación."
        st.rerun()

with col3:
    if st.button("😔 Ejemplo Negativo", use_container_width=True):
        st.session_state.texto_espanol = "Estoy muy decepcionado con los resultados. Nada salió como esperaba y me siento frustrado con todo el proceso."
        st.rerun()


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
        if len(st.session_state.texto_espanol.strip()) < 10:
            st.warning("⚠️ Por favor, escribe un mensaje más largo (al menos 10 caracteres)")
        else:
            with st.spinner("🧠 Analizando el sentimiento de tu mensaje..."):
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
                    
                    # Guardar en historial
                    st.session_state.historial.insert(0, {
                        'texto': st.session_state.texto_espanol[:100] + "...",
                        'sentimiento': obtener_emoji_sentimiento(polaridad)[1],
                        'polaridad': polaridad
                    })
                    if len(st.session_state.historial) > 5:
                        st.session_state.historial.pop()
    else:
        st.warning("⚠️ Por favor, escribe un mensaje para analizar.")


# ================================
# HISTORIAL (SI HAY)
# ================================

if st.session_state.historial:
    st.markdown("---")
    st.markdown("### 📜 Historial de Análisis")
    
    for i, item in enumerate(st.session_state.historial):
        emoji_hist = obtener_emoji_sentimiento(item['polaridad'])[0]
        st.markdown(f"""
        <div style='background: #f9fafb; padding: 0.75rem 1rem; border-radius: 8px; 
                    margin: 0.5rem 0; border-left: 3px solid #e5e7eb;'>
            <span style='font-size: 1.5rem;'>{emoji_hist}</span>
            <strong>{item['sentimiento']}</strong> - {item['texto']}
        </div>
        """, unsafe_allow_html=True)


# ================================
# FOOTER
# ================================

st.markdown("<div style='margin-top: 4rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 3rem; padding: 2rem; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
    <p style='margin: 0; color: white; font-size: 1.2rem; font-weight: 600;'>
        🚀 Analizador de Sentimientos con IA
    </p>
    <p style='margin: 0.5rem 0; color: rgba(255,255,255,0.95); font-size: 1rem;'>
        Desarrollado por <strong>Joel Pesantez</strong>
    </p>
    <p style='margin: 1rem 0 0 0; color: rgba(255,255,255,0.85); font-size: 0.85rem;'>
        🧠 TextBlob • 🌐 GoogleTranslator • ⚡ Streamlit
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e5e7eb; 
            text-align: center; color: #9ca3af; font-size: 0.875rem;'>
    © 2024 Joel Pesantez - Análisis de Sentimientos con Inteligencia Artificial
</div>
""", unsafe_allow_html=True)
