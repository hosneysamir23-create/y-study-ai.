import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="مساعد الملازم")
st.markdown('<style>body{direction:rtl;text-align:right;}</style>', unsafe_allow_html=True)

pwd = st.text_input("أدخل كلمة المرور (4455)", type="password")

if pwd == "4455":
st.title("📚 مساعد الملازم الذكي")
f = st.file_uploader("ارفع الملزمة (PDF)", type="pdf")
if f is not None:
try:
reader = PyPDF2.PdfReader(f)
text = ""
for page in reader.pages:
text += page.extract_text()
