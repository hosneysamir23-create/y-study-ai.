import streamlit as st
import PyPDF2
import google.generativeai as genai
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="مساعد الملازم الذكي")

# --- قائمة الأرقام المحظورة (ضيف هنا أي رقم عايز تحظره) ---
BANNED_NUMBERS = ["01000000000", "0123456789"] 

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_login():
    phone = st.session_state["phone_input"]
    pwd = st.session_state["pwd_input"]
    
    # 1. التأكد من الحظر
    if phone in BANNED_NUMBERS:
        st.error("🚫 عذراً، هذا الرقم محظور من استخدام التطبيق.")
        return

    # 2. التأكد من الباسورد
    if pwd == "Hh1112007@":
        st.session_state["authenticated"] = True
        # تسجيل الدخول بالرقم والوقت
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"دخول: {phone} | التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    else:
        st.error("❌ الباسورد غلط!")

# --- واجهة الدخول المعدلة ---
if not st.session_state["authenticated"]:
    st.title("🔐 تسجيل دخول الطلاب")
    st.text_input("رقم الموبايل", key="phone_input", placeholder="01xxxxxxxxx")
    st.text_input("كلمة المرور", type="password", key="pwd_input")
    st.button("دخول", on_click=check_login)
    st.stop()

# --- البرنامج الرئيسي ---
st.title("📚 مساعد الملازم الذكي")

# لوحة تحكم ليك أنت (مخفية في الجنب)
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    if st.button("عرض سجل المستخدمين"):
        try:
            with open("log.txt", "r", encoding="utf-8") as f:
                st.text(f.read())
        except:
            st.write("لا يوجد سجلات.")

f = st.file_uploader("ارفع الملزمة أو الصورة", type=["pdf", "jpg", "jpeg", "png"])

if f:
    genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if f.type == "application/pdf":
        pdf = PyPDF2.PdfReader(f)
        content = "".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        source_type = "text"
    else:
        content = Image.open(f)
        source_type = "image"
        st.image(content, caption="تم رفع الصورة", width=300)

    q = st.chat_input("اسألني أي سؤال...")
    if q:
        if source_type == "text":
            res = model.generate_content(f"أجب بالعربية: {content[:10000]}\nالسؤال: {q}")
        else:
            res = model.generate_content(["اشرح الصورة وجاوب بالعربي:", content, q])
        st.write(res.text)
