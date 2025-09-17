# 📄 OCR Destekli Sınav Kağıdı Okuma Sistemi

Bu proje, sınav kağıtlarındaki **öğrenci isim, numara ve puan bilgilerini otomatik olarak okuyup** Excel/CSV dosyalarına aktaran bir sistemdir.  
Google Cloud Vision API ve OpenCV kullanılarak geliştirilmiştir. Ayrıca **Streamlit arayüzü** ile kullanıcı dostu bir şekilde PDF veya resim dosyaları yüklenebilir.

---

## 🚀 Özellikler
- 📂 **PDF → PNG dönüştürme** (sayfa bazlı)
- 🖼️ **PNG/JPG yükleme desteği**
- 🤖 **Google Vision API ile OCR (Türkçe + İngilizce)**
- 🧹 **Veri temizleme**
  - Puanlar **0-100 aralığında değilse** “Bilinmiyor” olarak işaretlenir
  - Okunamayan alanlar **“Bilinmiyor”** şeklinde kaydedilir
  - İsim ve numara alanlarındaki gereksiz metinler temizlenir
- 📊 **Sonuçları Excel & CSV olarak kaydetme**
- 📈 **İstatistikler (ortalama, en yüksek puan, okunamayan kayıt sayısı)**
- 🌐 **Streamlit arayüzü ile kolay kullanım**

![WhatsApp Görsel 2025-08-27 saat 14 27 14_09e31afb](https://github.com/user-attachments/assets/30ae0807-8dc2-47dc-99c1-1a00367eb02a)
![WhatsApp Görsel 2025-08-27 saat 14 28 20_ec18f0d1](https://github.com/user-attachments/assets/0031bcca-b2f7-4e80-826f-3f1fd85f6f9c)

