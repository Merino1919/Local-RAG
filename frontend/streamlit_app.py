import streamlit as st
import requests

st.set_page_config(page_title="IA Local - Analista de Documentos", layout="wide")

st.title("📂 Analista de Documentos Sensibles (Privado)")
st.sidebar.header("Configuración")
api_url = st.sidebar.text_input("URL de la API", "http://localhost:8000/api/v1")

# --- Sección de Carga ---
st.subheader("1. Subir Documentación")
uploaded_file = st.file_uploader("Sube un PDF o Excel", type=["pdf", "xlsx", "xls"])

if st.button("Procesar Documento"):
    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        with st.spinner("Analizando y vectorizando..."):
            res = requests.post(f"{api_url}/upload", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
            if res.status_code == 200:
                st.success("¡Documento listo para consultas!")
            else:
                st.error("Error al procesar.")

# --- Sección de Chat ---
st.divider()
st.subheader("2. Consultar Información")
user_input = st.text_input("Haz una pregunta sobre los documentos:")

if st.button("Preguntar"):
    if user_input:
        with st.spinner("Pensando..."):
            res = requests.post(f"{api_url}/query", params={"question": user_input})
            if res.status_code == 200:
                data = res.json()
                st.markdown(f"**Respuesta:** {data['answer']}")
                
                with st.expander("Ver fuentes consultadas"):
                    for source in set(data['sources']):
                        st.caption(f"- {source}")
            else:
                st.error("La API no pudo responder.")