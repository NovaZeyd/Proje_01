# 🚀 Kurulum Rehberi

## Gereksinimler

- Python 3.10+
- SQLite3

## Hızlı Kurulum

```bash
# 1. Depoyu klonla
git clone https://github.com/zeyd/muhasebe.git
cd muhasebe

# 2. Virtual env oluştur
python -m venv venv

# 3. Aktive et (Linux/Mac)
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. Veritabanını hazırla
python -c "from src.db import Database; db = Database()"

# 6. Test et
python main.py
```

## Proje Yapısı

```
muhasebe/
├── src/           # Kaynak kodlar
├── tests/         # Test dosyaları
├── docs/          # Dokümantasyon
├── data/          # Veri dosyaları
└── raporlar/      # Çıktı klasörü
```

## CLI Kullanımı

```bash
# Bakiye raporu
python main.py --rapor bakiye

# Cari raporu
python main.py --rapor cari

# Yeni fiş
python main.py --yeni --aciklama "Açıklama"

# Fiş detayı
python main.py --fis --no FIS-2026-00001
```

## Sorun Giderme

**Import hatası alıyorsanız:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**Veritabanı hatası:**
```bash
rm muhasebe.db  # Yeniden oluşturulacak
```
