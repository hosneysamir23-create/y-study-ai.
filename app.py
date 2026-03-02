import streamlit as st
import PyPDF2
import google.generativeai as genai
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="AI Study")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

def check():
    p = st.session_state.get("p_in", "")
    pw = st.session_state.get("pw_in", "")
    if pw == "Hh1112007@":
        st.session_state["auth"] = True
        with open("log.txt", "a") as f:
            f.write(f"{p} - {datetime.now()}\n")
    else:
        st.error("Wrong Password")

if not st.session_state["auth"]:
    st.title("Login")
    st.text_input("Phone", key="p_in")
    st.text_input("Password", type="password", key="pw_in")
    st.button("Login", on_click=check)
    st.stop()

st.title("Study Assistant")
f = st.file_uploader("Upload", type=["pdf", "jpg", "png"])
if f:
    genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g")
    model = genai.GenerativeModel('gemini-1.5-flash')
    if f.type == "application/pdf":
        reader = PyPDF2.PdfReader(f)
        txt = "".join([p.extract_text() for p in reader.pages])
        q = st.chat_input("Ask...")
        if q:
            r = model.generate_content(f"Answer in Arabic: {txt[:10000]} \n Q: {q}")
            st.write(r.text)
    else:
        img = Image.open(f)
        st.image(img, width=300)
        q = st.chat_input("Ask...")
        if q:
            r = model.generate_content(["Explain in Arabic:", img, q])
            st.write(r.text)
