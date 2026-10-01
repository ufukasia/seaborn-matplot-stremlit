# Matplotlib vs Seaborn — Veri Görselleştirme Dersi (Streamlit)

Veri görselleştirme dersi için hazırlanmış, Matplotlib ve Seaborn ile aynı grafiklerin nasıl çizildiğini yan yana karşılaştıran tek dosyalık bir Streamlit uygulaması. Örneklerde Seaborn'un `tips`, `iris` ve `penguins` veri setleri kullanılır.

## Bölümler

Kenar çubuğundaki **Ders Menüsü**nden seçilir:

1. Giriş & Genel Bakış
2. Grafik Türleri Karşılaştırması
3. Stil & Estetik
4. İstatistiksel Grafikler
5. İlişki Grafikleri (pair plot, korelasyon ısı haritası)
6. Çoklu Grafik (FacetGrid)
7. Seaborn'un Süper Güçleri (kod uzunluğu karşılaştırması)
8. Canlı Deney Alanı — veri seti, grafik türü (violin, box, swarm, strip, bar, point), renk paleti ve tema seçerek grafiği anında değiştirme

## Kurulum ve çalıştırma

```bash
pip install -r requirements.txt
streamlit run app.py
```

Veri setleri `seaborn.load_dataset()` ile yüklendiğinden ilk çalıştırmada internet bağlantısı gerekir.

## Bağımlılıklar

`streamlit`, `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy` (sürüm aralıkları `requirements.txt` dosyasındadır).

## İletişim

Dr. Öğr. Üyesi Ufuk Asil, Ostim Teknik Üniversitesi.
