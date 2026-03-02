import PyPDF2
import google.generativeai as genai
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="AI Study Assistant")

BANNED_NUMBERS = ["01000000000"]

if "authenticated" not in st.session_state:
st.session_state["authenticated"] = False

def check_login():
phone = st.session_state["phone_input"]
pwd = st.session_state["pwd_input"]
if phone in BANNED_NUMBERS:
st.error("🚫 هذا الرقم محظور")
elif pwd == "Hh1112007@":
st.session_state["authenticated"] = True
with open("log.txt", "a", encoding="utf-8") as f:
f.write(f"Phone: {phone} | Time: {datetime.now()}\n")
else:
st.error("❌ كلمة المرور خطأ")

if not st.session_state["authenticated"]:
st.title("🔐 تسجيل الدخول")
st.text_input("رقم الموبايل", key="phone_input")
st.text_input("كلمة المرور", type="password", key="pwd_input")
st.button("دخول", on_click=check_login)
st.stop()

st.title("📚 مساعد الملازم الذكي")

with st.sidebar:
if st.button("سجل الدخول"):
try:
with open("log.txt", "r", encoding="utf-8") as f:
st.text(f.read())
except:
st.write("لا يوجد سجل.")

f = st.file_uploader("ارفع الملف", type=["pdf", "jpg", "jpeg", "png"])

if f:
genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g")
model = genai.GenerativeModel('gemini-1.5-flash')
if f.type == "application/pdf":
pdf = PyPDF2.PdfReader(f)
content = "".join([p.extract_text() for p in pdf.pages if p.extract_text()])
is_image = False
else:
content = Image.open(f)
is_image = True
st.image(content, width=300)
