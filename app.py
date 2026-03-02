import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="مساعد الملازم")
st.markdown('<style>body{direction:rtl;text-align:right;}</style>', unsafe_allow_html=True)

pwd = st.text_input("أدخل كلمة المرور (4455)", type="password")

if pwd == "4455": st.title("📚 مساعد الملازم الذكي") f = st.file_uploader("ارفع الملزمة (PDF)", type="pdf") if f is not None: try: reader = PyPDF2.PdfReader(f) text = "" for page in reader.pages: extracted = page.extract_text() if extracted: text += extracted if text: st.success("✅ تم قراءة الملزمة بنجاح!") q = st.chat_input("اسألني أي سؤال عن الملزمة...") if q: genai.configure(api_key="AIzaSyDETNhoieNKbhhq_zF_W0AVaGlCBrMct0g") model = genai.GenerativeModel('gemini-1.5-flash') prompt = f"أجب بالعربية بناءً على المادة العلمية المرفقة: {text[:15000]}\n\nالسؤال: {q}" res = model.generate_content(prompt) with st.chat_message("assistant"): st.write(res.text) else: st.warning("⚠️ الملف قد يكون عبارة عن صور فقط ولا يحتوي على نص قابل للقراءة.") except Exception as e: st.error("حدث خطأ أثناء معالجة الملف، تأكد أنه PDF سليم.")
