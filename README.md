# 🧙‍♂️ Chart Wizard AI: Akıllı Veri Görselleştirme Asistanı

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange)
![Plotly](https://img.shields.io/badge/Plotly-Express-green)

**Chart Wizard AI**, veri analizi ve görselleştirme süreçlerini otomatize eden, **Google Gemini (Vision & LLM)** destekli yeni nesil bir veri asistanıdır.

Kullanıcıların grafik türlerini tanımasına, kod yazmadan veri görselleştirmesine ve verileriyle doğal dilde sohbet etmesine olanak tanır.

---

## 🚀 Özellikler

### 1. 👁️ Grafik Tanıma (Computer Vision)

Kullanıcı bir grafik görseli (JPG/PNG) yükler. Yapay zeka, görüntüyü analiz eder ve grafiğin türünü (Bar, Line, Scatter, vb.) tespit ederek hafızasına alır.

### 2. 📊 Otomatik Çizim Sihirbazı (Auto-Plot)

CSV veya Excel dosyası yüklendiğinde, sistem kolon tiplerini otomatik analiz eder. Eğer öncesinde bir grafik fotoğrafı yüklendiyse o stili, yüklenmediyse veriye en uygun grafik türünü otomatik seçip çizer.

### 3. 💬 Veriyle Sohbet (Chat with Data) - _BETA_

Veri setinizle konuşun! Dropdown menülerle uğraşmak yerine:

- _"Satışları 5000'den büyük olan şehirleri göster"_
- _"Elektronik kategorisindeki ürünleri filtrele"_
  gibi komutlar verin, AI sizin için Python kodu yazıp sonucu görselleştirsin.

### 4. 🧠 AI Veri Analisti

Tek bir tıklama ile verinizin istatistiksel özetini çıkarır ve Gemini LLM modelini kullanarak size **"Yönetici Özeti"** formatında bir rapor sunar.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler

- Python 3.8 veya üzeri
- Google Cloud API Key (Gemini erişimi için)

### Adım 1: Projeyi Klonlayın

```bash
git clone [https://github.com/KULLANICI_ADIN/Chart-Wizard-AI.git](https://github.com/KULLANICI_ADIN/Chart-Wizard-AI.git)
cd Chart-Wizard-AI
Adım 2: Gerekli Kütüphaneleri YükleyinBashpip install -r requirements.txt
Adım 3: Uygulamayı BaşlatınBashpython -m streamlit run app.py
📂 Proje Mimarisiapp.py: Uygulamanın ana dosyası. Streamlit arayüzü ve tüm mantık burada döner.requirements.txt: Gerekli Python kütüphaneleri.Google Gemini API: Görüntü işleme ve doğal dil işleme (NLP) motoru.Pandas & Plotly: Veri manipülasyonu ve interaktif grafik çizimi.📸 Ekran GörüntüleriGrafik Tanıma ModülüOtomatik Çizim & Analiz(Buraya Vision sekmesinin ekran görüntüsünü ekleyebilirsin)(Buraya Wizard sekmesinin ekran görüntüsünü ekleyebilirsin)🙏 TeşekkürBu projenin geliştirilmesindeki katkıları ve vizyonları için değerli hocalarım:Prof. Dr. Nurettin ŞenyerArş. Gör. Ömer DURMUŞhocalarıma teşekkür ederim.
```
