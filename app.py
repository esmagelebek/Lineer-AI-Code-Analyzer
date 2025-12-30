import streamlit as st
import pandas as pd
from analyzer import CodeDebtAnalyst

st.set_page_config(page_title="Lineer AI Assistant", layout="wide")
st.title("🚀 Lineer: AI Destekli Mimari ve Kod Analizi")

with st.sidebar:
    st.header("Ayarlar")
    api_key = st.secrets["GROQ_API_KEY"]

uploaded_files = st.file_uploader("Python dosyalarınızı yükleyin", type="py", accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for f in uploaded_files:
        content = f.read().decode("utf-8")
        all_data.extend(CodeDebtAnalyst.analyze_source(f.name, content))
    
    if all_data:
        df = pd.DataFrame(all_data)
        st.subheader("📊 Analiz Raporu")
        st.dataframe(df.drop(columns=["Kod"]), use_container_width=True)

        st.divider()
        st.subheader("🤖 AI Mimari & Kod Önerisi")
        
        # Seçim: Dosya mı yoksa tek bir fonksiyon mu?
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
                    st.warning("Lütfen sidebar'dan API anahtarını girin.")
