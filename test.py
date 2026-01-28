import streamlit as st
import os
from app.core.engine import RAGEngine

# Configuración de la página
st.set_page_config(page_title="IA Local - Modo Directo", layout="wide")

# 1. Inicializar motor
if "rag_engine" not in st.session_state:
    with st.spinner("Iniciando motor de IA..."):
        st.session_state.rag_engine = RAGEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

engine = st.session_state.rag_engine

st.title("📂 Analista de Documentos (Directo)")

# --- Sidebar: Gestión de Archivos y Chat ---
st.sidebar.header("Panel de Control")
uploaded_file = st.sidebar.file_uploader("Sube un PDF o Excel", type=["pdf", "xlsx", "xls"])

# Botones de acción en la sidebar
col_proc, col_clear = st.sidebar.columns(2)

with col_proc:
    if st.button("🚀 Procesar"):
        if uploaded_file:
            os.makedirs("./temp", exist_ok=True)
            file_path = os.path.join("./temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Indexando..."):
                msg = engine.ingest_document(file_path)
                st.sidebar.success(msg)
        else:
            st.sidebar.error("Falta archivo")

with col_clear:
    if st.button("🗑️ Limpiar Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Sección de Chat Principal ---
st.subheader("Consultas sobre tus documentos")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input y Lógica de Respuesta
if prompt := st.chat_input("¿Qué quieres saber?"):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos..."):
            # OJO: Asegúrate que tu engine devuelva un dict con 'answer' y 'sources'
            response = engine.get_response(prompt)
            
            # Si el engine devuelve un string directamente (por usar LangGraph), 
            # ajusta estas líneas:
            full_response = response["answer"] if isinstance(response, dict) else response
            
            # Manejo de fuentes
            if isinstance(response, dict) and response.get("sources"):
                sources = "\n\n**Fuentes:**\n" + "\n".join([f"- {os.path.basename(s)}" for s in set(response["sources"]) if s])
                full_response += sources
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})