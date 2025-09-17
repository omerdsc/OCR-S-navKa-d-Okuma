# app.py
import streamlit as st
import os
import tempfile
import cv2
import pandas as pd
from ocr_core import pdf_to_png, process_images

st.set_page_config(page_title="OCR Sınav Kağıdı Sistemi", layout="centered")

st.title("📄 OCR Destekli Sınav Kağıdı Okuma Sistemi")

uploaded_files = st.file_uploader("PDF veya Resim Dosyalarını Yükleyin", 
                                   type=["pdf","png","jpg","jpeg"], 
                                   accept_multiple_files=True)

if uploaded_files:
    tmp_dir = tempfile.mkdtemp()
    image_paths = []

    for file in uploaded_files:
        file_path = os.path.join(tmp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

        if file.name.lower().endswith(".pdf"):
            st.info(f"PDF {file.name} PNG sayfalarına dönüştürülüyor...")
            pages = pdf_to_png(file_path, out_dir=tmp_dir)
            image_paths.extend(pages)
        else:
            image_paths.append(file_path)

    st.success(f"{len(image_paths)} sayfa/resim yüklendi ✅")

    # Önizleme: ilk 3 resmi göster
    cols = st.columns(3)
    for i, img_path in enumerate(image_paths[:3]):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        with cols[i % 3]:
            st.image(img, caption=os.path.basename(img_path), use_column_width=True)

    if st.button("OCR İşlemini Başlat"):
        df = process_images(image_paths)

        st.subheader("📊 OCR Sonuçları")
        st.dataframe(df)

        # İstatistikler
        st.subheader("📈 Özet İstatistikler")
        numeric_scores = pd.to_numeric(df["Puan"], errors="coerce")
        st.write(f"Ortalama Puan: {numeric_scores.mean(skipna=True):.2f}")
        st.write(f"En Yüksek Puan: {numeric_scores.max(skipna=True)}")
        st.write(f"Okunamayan Kayıtlar: {(df['Puan']=='Bilinmiyor').sum()}")

        # İndirme butonları
        st.subheader("📥 Sonuçları İndir")
        excel_path = os.path.join(tmp_dir, "results_vision.xlsx")
        csv_path = os.path.join(tmp_dir, "results_vision.csv")
        df.to_excel(excel_path, index=False)
        df.to_csv(csv_path, index=False)

        with open(excel_path, "rb") as f:
            st.download_button("Excel İndir (.xlsx)", f, file_name="results_vision.xlsx")
        with open(csv_path, "rb") as f:
            st.download_button("CSV İndir (.csv)", f, file_name="results_vision.csv")
