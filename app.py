import streamlit as st
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="مساعد الملازم")
st.markdown('<style>body{direction:rtl;text-align:right;}</style>', unsafe_allow_html=True)

pwd = st.text_input("أدخل الباسورد (4455)", type="password")

if pwd == "4455":
    st.title("📚 مساعد الملازم الذكي")
    f = st.file_uploader("ارفع الملزمة (PDF)", type="pdf")
    if f is not None:
        try:
            reader = PyPDF2.PdfReader(f)
            text = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
            if text:
                st.success("✅ تم قراءة الملزمة بنجاح!")
                q = st.chat_input("اسألني أي سؤال عن الملزمة...")
                if q:
                    genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g")
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"أجب بالعربية بناءً على المادة العلمية: {text[:10000]}\nالسؤال: {q}"
                    res = model.generate_content(prompt)
                    st.write(res.text)
            else:
                st.warning("⚠️ الملف قد يكون صوراً فقط (Scanner) ولا يحتوي نص.")
        except Exception as e:
            st.error("حدث خطأ في قراءة الملف.")
