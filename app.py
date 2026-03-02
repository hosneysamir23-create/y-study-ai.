import PyPDF2
import google.generativeai as genai
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="AI Study")

BANNED = ["01000000000"]

if "auth" not in st.session_state:
st.session_state["auth"] = False

def check():
p = st.session_state["p_in"]
pw = st.session_state["pw_in"]
if p in BANNED:
st.error("Access Denied")
elif pw == "Hh1112007@":
st.session_state["auth"] = True
with open("log.txt", "a") as f:
f.write(f"{p} - {datetime.now()}\n")
else:
st.error("Wrong Password")

if not st.session_state["auth"]:
st.title("Login Page")
st.text_input("Mobile Number", key="p_in")
st.text_input("Password", type="password", key="pw_in")
st.button("Login", on_click=check)
st.stop()

st.title("Student Assistant")
if st.sidebar.button("Show Logs"):
try:
with open("log.txt", "r") as f: st.sidebar.text(f.read())
except: st.sidebar.write("No logs.")

f = st.file_uploader("Upload PDF or Photo", type=["pdf", "jpg", "png"])
if f:
genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g")
model = genai.GenerativeModel('gemini-1.5-flash')
if f.type == "application/pdf":
reader = PyPDF2.PdfReader(f)
txt = "".join([p.extract_text() for p in reader.pages])
q = st.chat_input("Ask in Arabic...")
if q:
res = model.generate_content(f"Answer in Arabic: {txt[:10000]}\nQuestion: {q}")
st.write(res.text)
else:
img = Image.open(f)
st.image(img, width=300)
q = st.chat_input("Ask in Arabic...")
if q:
res = model.generate_content(["Answer in Arabic:", img, q])
st.write(res.text)
