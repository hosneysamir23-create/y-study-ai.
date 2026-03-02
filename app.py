import streamlit as st
import PyPDF2
import google.generativeai as genai
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="مساعد الملازم الذكي")

# --- ميزة حفظ تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if st.session_state["pwd_input"] == "Hh1112007@":
        st.session_state["authenticated"] = True
        # --- ميزة تسجيل مين دخل ---
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"تم دخول مستخدم بنجاح في: {datetime.now()}\n")
    else:
        st.error("❌ الباسورد غلط يا بطل!")

# --- واجهة الدخول ---
if not st.session_state["authenticated"]:
    st.title("🔐 تسجيل الدخول")
    st.text_input("أدخل كلمة المرور", type="password", key="pwd_input", on_change=check_password)
    st.stop() # بيوقف البرنامج هنا لحد ما يدخل الباسورد صح

# --- لو الباسورد صح، بقية البرنامج بيظهر هنا ---
st.title("📚 مساعد الملازم (صور + PDF)")

# زرار لمشاهدة السجل (ليك أنت بس)
if st.sidebar.button("عرض سجل الدخول"):
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            st.sidebar.text(f.read())
    except:
        st.sidebar.write("لا يوجد سجلات بعد.")

f = st.file_uploader("ارفع الملزمة أو صورة الصفحة", type=["pdf", "jpg", "jpeg", "png"])

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
