import streamlit as st
import requests

st.set_page_config(page_title="IA Local - Analista de Documentos", layout="wide")

st.title("Sensitive documents analyst (private deployment)")
st.sidebar.header("Config")
api_url = st.sidebar.text_input("API URL", "http://localhost:8000/api/v1")

# --- Upload section ---
st.subheader("1. Documentation upload")
uploaded_file = st.file_uploader("Upload a PDF or an Excel file", type=["pdf", "xlsx", "xls"])

if st.button("Process document"):
    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        with st.spinner("Analyzing and vectorizing..."):
            res = requests.post(f"{api_url}/upload", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
            if res.status_code == 200:
                st.success("Document ready for queries!")
            else:
                st.error("Error while processing.")

# --- Chat section ---
st.divider()
st.subheader("2. Information checking")
user_input = st.text_input("Ask a question about the provided documents:")

if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            res = requests.post(f"{api_url}/query", params={"question": user_input})
            if res.status_code == 200:
                data = res.json()
                st.markdown(f"**Answer:** {data['answer']}")
                
                with st.expander("Check employed sources"):
                    for source in set(data['sources']):
                        st.caption(f"- {source}")
            else:
                st.error("API was not reachable.")