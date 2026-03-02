import streamlit as st
import PyPDF2
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="مساعد الملازم")

# غير الرقم اللي تحت ده لأي باسورد تحبه
pwd = st.text_input("أدخل كلمة المرور الجديدة", type="password")

if pwd == "اكتب_الباسورد_الجديد_هنا": 
    st.title("📚 مساعد الملازم (صور + PDF)")
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

        q = st.chat_input("اسألني أي سؤال عن الصورة أو الملف...")
        if q:
            if source_type == "text":
                res = model.generate_content(f"أجب بالعربية: {content[:10000]}\nالسؤال: {q}")
            else:
                res = model.generate_content(["اشرح الصورة وجاوب بالعربي:", content, q])
            st.write(res.text)
