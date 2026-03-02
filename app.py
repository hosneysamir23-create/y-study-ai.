import streamlit as st
st.markdown('<style>body{direction:rtl;text-align:right;}</style>', unsafe_allow_html=True)
pwd = st.text_input("أدخل الباسورد", type="password")
if pwd == "4455":
  st.title("📚 مساعد الملازم الذكي")
  f = st.file_uploader("ارفع الملزمة (PDF)", type="pdf")
  import PyPDF2
   import google.generativeai as genai
    pdf = PyPDF2.PdfReader(f)
      text = "".join([p.extract_text() for p in pdf.pages])
       st.success("تم تحميل الملف")
         q = st.chat_input("اسألني أي سؤال...")
          genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g")
            model = genai.GenerativeModel('gemini-1.5-flash')
             res = model.generate_content(f"أجب بالعربية: {text[:10000]}\nالسؤال: {q}")
              st.write(res.text)
