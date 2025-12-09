import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Chart Wizard AI", layout="wide", page_icon="🧙‍♂️")

# --- CSS İLE GÖRSELLİĞİ ARTIRMA ---
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1 {color: #ff4b4b;}
    .stButton>button {width: 100%; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧙‍♂️ Chart Wizard: AI Destekli Veri Analisti")
st.markdown("---")

# --- API AYARLARI (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.header("🔑 Erişim Ayarları")
    api_key = st.text_input("Google Gemini API Key", type="password")
    
    st.info("Bu proje şunları yapabilir:\n1. 👁️ Grafiği Görür\n2. 📊 Veriyi Çizer\n3. 🧠 Analiz Yapar")
    
    if api_key:
        genai.configure(api_key=api_key)

# --- SESSION STATE (HAFIZA) ---
if 'detected_type' not in st.session_state:
    st.session_state.detected_type = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# --- SEKME YAPISI ---
tab1, tab2 = st.tabs(["👁️ 1. Adım: Grafik Tanıma", "🚀 2. Adım: Otomatik Çizim ve Analiz"])

# ==========================================
# 1. MODÜL: VISION (GÖRÜNTÜ İŞLEME)
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Grafik Yükle")
        uploaded_img = st.file_uploader("Örnek bir grafik yükle", type=["png", "jpg", "jpeg"])
    
    with col2:
        if uploaded_img:
            image = Image.open(uploaded_img)
            st.image(image, caption="Analiz Edilecek Görsel", width=500)
            
            if st.button("📸 Grafik Türünü Tespit Et", type="primary"):
                if not api_key:
                    st.error("Lütfen önce API Anahtarını gir.")
                else:
                    try:
                        with st.spinner("Yapay zeka görseli tarıyor..."):
                            # Senin çalışan modelin: gemini-2.5-flash
                            model = genai.GenerativeModel('models/gemini-2.5-flash')
                            
                            prompt = """
                            Bu görseldeki grafik türü nedir? 
                            Sadece şu seçeneklerden birini yaz: 'Bar Chart', 'Line Chart', 'Scatter Plot', 'Histogram', 'Pie Chart'.
                            Başka hiçbir kelime ekleme.
                            """
                            response = model.generate_content([prompt, image])
                            yanit = response.text.strip()
                            
                            st.session_state.detected_type = yanit
                            st.success(f"✅ Tespit Edildi: **{yanit}**")
                            st.info("Hafızaya alındı! Şimdi yandaki sekmeye geçip kendi verini yükleyebilirsin.")
                            
                    except Exception as e:
                        st.error(f"Hata: {e}")

# ==========================================
# 2. MODÜL: WIZARD (VERİDEN GRAFİĞE)
# ==========================================
with tab2:
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("📂 Veri Seti Yükle")
        uploaded_file = st.file_uploader("CSV veya Excel", type=["csv", "xlsx"])
        
        if st.session_state.detected_type:
            st.warning(f"💡 AI Önerisi: **{st.session_state.detected_type}**")

    # Veri yüklendiyse işlemleri başlat
    if uploaded_file:
        # Dosya okuma
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Kolon Tipleri
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64', 'datetime']).columns.tolist()
        
        # --- OTOMATİK SEÇİMLER ---
        chart_type = st.session_state.detected_type if st.session_state.detected_type else "Bar Chart"
        x_col, y_col = None, None
        
        # Akıllı Kolon Atama
        if chart_type == "Line Chart":
            x_col = date_cols[0] if date_cols else (num_cols[0] if num_cols else None)
            y_col = num_cols[1] if len(num_cols) > 1 else (num_cols[0] if num_cols else None)
        else:
            x_col = cat_cols[0] if cat_cols else (num_cols[0] if num_cols else None)
            y_col = num_cols[0] if num_cols else None

        # Kullanıcı Kontrol Paneli
        with col_left:
            st.divider()
            st.markdown("### 🛠️ Grafik Ayarları")
            selected_chart = st.selectbox("Grafik Tipi", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart"], index=["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart"].index(chart_type) if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart"] else 0)
            
            x_axis = st.selectbox("X Ekseni", df.columns, index=df.columns.get_loc(x_col) if x_col in df.columns else 0)
            y_axis = st.selectbox("Y Ekseni", df.columns, index=df.columns.get_loc(y_col) if y_col in df.columns else 0)
            
            # YENİ ÖZELLİK: AI YORUM BUTONU
            st.divider()
            if st.button("🧠 Veriyi Yorumla (AI)", type="secondary"):
                if not api_key:
                    st.error("API Anahtarı gerekli.")
                else:
                    with st.spinner("AI veriyi okuyor ve rapor yazıyor..."):
                        try:
                            # Verinin özetini çıkarıp LLM'e gönderme
                            data_summary = df.head(10).to_string()
                            stats = df.describe().to_string()
                            
                            model_text = genai.GenerativeModel('models/gemini-2.5-flash')
                            prompt_text = f"""
                            Sen kıdemli bir veri analistisin. Aşağıdaki veriye bakarak yönetici özeti çıkar.
                            Önemli trendleri, en yüksek/en düşük değerleri ve dikkat çeken noktaları 3 madde halinde yaz.
                            Türkçe cevap ver.
                            
                            Veri Örneği:
                            {data_summary}
                            
                            İstatistikler:
                            {stats}
                            """
                            res_text = model_text.generate_content(prompt_text)
                            st.session_state.analysis_result = res_text.text
                        except Exception as e:
                            st.error(f"Analiz Hatası: {e}")

        # Sağ Taraf: Grafik ve Rapor
        with col_right:
            st.subheader(f"📊 {selected_chart} Sonucu")
            
            # Grafik Çizimi
            fig = None
            if selected_chart == "Bar Chart": fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis)
            elif selected_chart == "Line Chart": fig = px.line(df, x=x_axis, y=y_axis, markers=True)
            elif selected_chart == "Scatter Plot": fig = px.scatter(df, x=x_axis, y=y_axis, size=y_axis, color=x_axis)
            elif selected_chart == "Histogram": fig = px.histogram(df, x=x_axis, y=y_axis)
            elif selected_chart == "Pie Chart": fig = px.pie(df, names=x_axis, values=y_axis)
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # AI Analiz Sonucunu Göster
            if st.session_state.analysis_result:
                st.info("🤖 **AI Analiz Raporu:**")
                st.markdown(st.session_state.analysis_result)
        # --- YENİ ÖZELLİK: VERİYLE SOHBET (CHAT WITH DATA) ---
        st.divider()
        st.subheader("💬 Veriyle Sohbet Et")
        
        user_query = st.text_input("Veriye bir soru sor veya filtre iste:", placeholder="Örn: Sadece 'Elektronik' kategorisindeki satışları göster")
        
        if st.button("Sorgula ve Çiz") and user_query:
            if not api_key:
                st.error("API Key gerekli.")
            else:
                with st.spinner("Yapay zeka sorgunu koda çeviriyor..."):
                    try:
                        # 1. Gemini'ye Veri Yapısını ve Soruyu Veriyoruz
                        columns_info = ", ".join(df.columns)
                        sample_data = df.head(3).to_string()
                        
                        prompt_code = f"""
                        Sen bir Python Pandas uzmanısın. Elimde şu kolonlara sahip bir dataframe (df) var: {columns_info}
                        Veriden örnekler:
                        {sample_data}
                        
                        Kullanıcı isteği: "{user_query}"
                        
                        GÖREVİN: Kullanıcının isteğini yerine getiren bir Python Pandas filtresi yaz.
                        Sadece filtreleme kodunu ver. Değişken ataması yapma.
                        Örnek Çıktılar:
                        - df[df['Satis'] > 500]
                        - df[df['Sehir'] == 'Ankara']
                        - df.groupby('Kategori')['Satis'].sum().reset_index()
                        
                        Lütfen sadece tek satırlık çalıştırılabilir Python kodu ver. Markdown veya açıklama yok.
                        """
                        
                        model_coder = genai.GenerativeModel('models/gemini-2.5-flash')
                        response_code = model_coder.generate_content(prompt_code)
                        generated_code = response_code.text.strip().replace("`", "").replace("python", "")
                        
                        st.caption(f"🔧 Çalıştırılan Kod: `{generated_code}`")
                        
                        # 2. Kodu Güvenli Şekilde Çalıştır (eval)
                        # Not: Gerçek prodüksiyonda eval tehlikelidir ama demo/proje için harikadır.
                        filtered_df = eval(generated_code)
                        
                        if isinstance(filtered_df, pd.DataFrame):
                            st.write(f"Sonuç: {len(filtered_df)} satır bulundu.")
                            st.dataframe(filtered_df.head())
                            
                            # Filtrelenmiş veri ile otomatik grafik
                            st.subheader("🎯 Sorgu Sonucu Grafiği")
                            
                            # Otomatik X ve Y seçimi (Basit mantık)
                            new_num = filtered_df.select_dtypes(include=['number']).columns
                            new_cat = filtered_df.select_dtypes(include=['object']).columns
                            
                            if len(new_cat) > 0 and len(new_num) > 0:
                                fig_query = px.bar(filtered_df, x=new_cat[0], y=new_num[0], title=f"Analiz: {user_query}")
                                st.plotly_chart(fig_query, use_container_width=True)
                            else:
                                st.warning("Grafik için uygun kolon bulunamadı, tabloyu inceleyin.")
                                
                        else:
                            st.write("Sonuç (Tablo değil):", filtered_df)
                            
                    except Exception as e:
                        st.error(f"Sorgu anlaşılamadı veya kod hatası: {e}")

    else:
        with col_right:
            st.info("👈 Başlamak için sol taraftan dosya yükleyin.")