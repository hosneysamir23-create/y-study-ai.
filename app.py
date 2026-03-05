import streamlit as st
import google.generativeai as genai
from supabase import create_client
import tempfile
import os

# إعدادات الربط من Secrets
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("تأكد من إعداد الـ Secrets بشكل صحيح (SUPABASE_URL, SUPABASE_KEY, GOOGLE_API_KEY)")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="المساعد الدائم", layout="centered")
st.title("📚 مساعد المذاكرة (الحفظ الدائم)")

# نظام تسجيل الدخول
if "auth" not in st.session_state:
    st.session_state.auth = False

def check():
    if st.session_state.pwd == "Hh1112007@":
        st.session_state.auth = True

if not st.session_state.auth:
    st.text_input("كلمة السر", type="password", key="pwd", on_change=check)
    st.stop()

# رفع الملف
f = st.file_uploader("ارفع درسك هنا", type=["pdf", "png", "jpg", "jpeg"])

if f:
    # 1. حفظ الملف في Supabase (عشان يفضل معاك للأبد)
    file_path = f"study_files/{f.name}"
    try:
        supabase.storage.from_("files").upload(file_path, f.getvalue(), {"content-type": f.type})
    except:
        pass # الملف موجود مسبقاً

    st.success(f"✅ الملف '{f.name}' محفوظ في خزنتك.")

    # 2. تحضير الملف لجوجل (عشان نصلح خطأ InvalidArgument)
    q = st.chat_input("اسأل أي سؤال...")
    if q:
        with st.spinner("جاري التحليل..."):
            try:
                # إنشاء ملف مؤقت محلي عشان جوجل تقرأه صح
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{f.name.split('.')[-1]}") as tmp:
                    tmp.write(f.getvalue())
                    tmp_path = tmp.name
                
                # رفع الملف لجوجل
                google_file = genai.upload_file(tmp_path)
                
                # إرسال السؤال
                response = model.generate_content([q, google_file])
                
                st.markdown(f"### الرد:\n{response.text}")
                
                # مسح الملف المؤقت
                os.remove(tmp_path)
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {str(e)}")

st.divider()
st.info("💡 ملفاتك الآن تُحفظ تلقائياً في Supabase ويمكنك الوصول إليها من Dashboard الموقع.")
