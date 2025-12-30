import streamlit as st
import pandas as pd
import json
from analyzer import CodeDebtAnalyst

st.set_page_config(page_title="Lineer AI Assistant", layout="wide")
st.title("🚀 Lineer: AI Destekli Mimari ve Kod Analizi")

# 1. Notebook dosyalarını okumak için yardımcı fonksiyon (Fonksiyon tanımları en üstte olur)
def get_code_from_ipynb(file_content):
    try:
        data = json.loads(file_content)
        code_cells = [
            "".join(cell["source"]) 
            for cell in data["cells"] 
            if cell["cell_type"] == "code"
        ]
        return "\n\n".join(code_cells)
    except Exception:
        return ""

# API Anahtarını güvenli alandan çekiyoruz
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("API Anahtarı bulunamadı! Lütfen Secrets kısmını kontrol edin.")
    api_key = None

# 2. Dosya yükleyici kısmında tipi genişlettik
uploaded_files = st.file_uploader("Python (.py) veya Notebook (.ipynb) dosyalarınızı yükleyin", 
                                  type=["py", "ipynb"], 
                                  accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for f in uploaded_files:
        # Karakter bozulmalarını önlemek için güvenli okuma yapıyoruz
        try:
            content_raw = f.read().decode("utf-8")
        except UnicodeDecodeError:
            f.seek(0) # Dosya imlecini başa sar
            content_raw = f.read().decode("latin-1")
        
        # 3. Dosya tipine göre içeriği işleme
        if f.name.endswith(".ipynb"):
            content = get_code_from_ipynb(content_raw)
        else:
            content = content_raw
        
        if content.strip():
            all_data.extend(CodeDebtAnalyst.analyze_source(f.name, content))
    
    if all_data:
        df = pd.DataFrame(all_data)
        st.subheader("📊 Analiz Raporu")
        st.dataframe(df.drop(columns=["Kod"]), use_container_width=True)

        st.divider()
        st.subheader("🤖 AI Mimari & Kod Önerisi")
        
        selection = st.selectbox("İncelemek istediğiniz birimi seçin:", df['İsim'].unique())
        selected_row = df[df['İsim'] == selection].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Mevcut İçerik ({selected_row['Tip']}):**")
            st.code(selected_row['Kod'], language='python')
        
        with col2:
            if st.button("AI Analizini Başlat ✨", type="primary"):
                if api_key:
                    with st.spinner("AI mimariyi inceliyor..."):
                        suggestion = CodeDebtAnalyst.get_ai_refactor_suggestion(
                            selected_row['Kod'], 
                            api_key, 
                            mode=selected_row['Tip']
                        )
                        st.markdown(suggestion)
                else:
                    st.warning("API anahtarı sistemde tanımlı değil.")
