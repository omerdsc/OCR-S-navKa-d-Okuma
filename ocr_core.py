# ocr_core.py
import os
import cv2
import fitz
import pandas as pd
import re
from google.cloud import vision

# --- Google Vision kimlik dosyası (gerekirse yolunu değiştir)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r""
client = vision.ImageAnnotatorClient()

# ---------- Yardımcılar ----------
def pdf_to_png(pdf_path, out_dir="pages", zoom=3.0):
    """PDF dosyasını PNG sayfalarına çevirir."""
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        out_path = os.path.join(out_dir, f"page_{i}.png")
        pix.save(out_path)
        paths.append(out_path)
    doc.close()
    return paths

def netlestir(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thr = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 15
    )
    thr = cv2.medianBlur(thr, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    thr = cv2.dilate(thr, kernel, iterations=1)
    return thr

def vision_ocr(img_bgr):
    ok, buf = cv2.imencode(".png", img_bgr)
    image = vision.Image(content=buf.tobytes())
    ctx = vision.ImageContext(language_hints=["tr","en"])
    resp = client.document_text_detection(image=image, image_context=ctx)
    return resp.full_text_annotation.text.strip() if resp.full_text_annotation else ""

# ---------- Temizleme ----------
def temizle_isim(text):
    if not text: return "Bilinmiyor"
    text = re.sub(r"(?i)(name surname|isim soyisim|numarası.*)", "", text)
    text = re.sub(r"[:;,.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip() if text.strip() else "Bilinmiyor"

def temizle_numara(text):
    if not text: return "Bilinmiyor"
    nums = re.sub(r"\D", "", text)
    return nums if nums else "Bilinmiyor"

def temizle_puan(text):
    if not text: return "Bilinmiyor"
    nums = re.sub(r"\D", "", text)
    if not nums: return "Bilinmiyor"
    try:
        puan = int(nums)
        return str(puan) if 0 <= puan <= 100 else "Bilinmiyor"
    except:
        return "Bilinmiyor"

# ---------- ROI Fonksiyonları ----------
def ROI_1(path, df):
    img = cv2.imread(path)
    thr = netlestir(img)
    puan_alani = thr[385:470, 980:1550]
    ad_soyad   = thr[460:525, 180:1012]
    ogrenci_no = thr[515:580, 180:1012]

    metin_puan = temizle_puan(vision_ocr(cv2.cvtColor(puan_alani, cv2.COLOR_GRAY2BGR)))
    metin_ad   = temizle_isim(vision_ocr(cv2.cvtColor(ad_soyad,   cv2.COLOR_GRAY2BGR)))
    metin_no   = temizle_numara(vision_ocr(cv2.cvtColor(ogrenci_no, cv2.COLOR_GRAY2BGR)))

    df.loc[len(df)] = [path, metin_ad, metin_no, metin_puan]

def ROI_2(path, df):
    img = cv2.imread(path)
    thr = netlestir(img)
    puan_alani = thr[470:525, 850:1044]
    ad_soyad   = thr[590:670, 230:650]
    ogrenci_no = thr[590:670, 650:1035]

    metin_puan = temizle_puan(vision_ocr(cv2.cvtColor(puan_alani, cv2.COLOR_GRAY2BGR)))
    metin_ad   = temizle_isim(vision_ocr(cv2.cvtColor(ad_soyad,   cv2.COLOR_GRAY2BGR)))
    metin_no   = temizle_numara(vision_ocr(cv2.cvtColor(ogrenci_no, cv2.COLOR_GRAY2BGR)))

    df.loc[len(df)] = [path, metin_ad, metin_no, metin_puan]

# ---------- Sayfa Seçimi ----------
def sayfa_bulma(path, df):
    img_roi_2 = cv2.imread(path)
    img_roi_2 = img_roi_2[:430,300:1450]
    roi_2_metni = vision_ocr(cv2.cvtColor(img_roi_2, cv2.COLOR_BGR2RGB))
    if "BMU103" in roi_2_metni:
        ROI_2(path, df)
    else:
        ROI_1(path, df)

# ---------- Ana Çalıştırıcı ----------
def process_images(image_paths):
    df = pd.DataFrame(columns=["Path", "Name_Surname", "Numara", "Puan"])
    for path in image_paths:
        sayfa_bulma(path, df)
    return df
