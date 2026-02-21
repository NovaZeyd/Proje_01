# EDV (Əlavə Dəyər Vergisi) Avtomatlaşdırma Sistemi

**Status:** Quraşdırma mərhələsində  
**Məqsəd:** EDV hesablama və əvəzləşdirmə prosesinin tam avtomatlaşdırılması  
**Yaradılıb:** 20 Fevral 2026

---

## 📋 Azərbaycan EDV Əsasları

### NVMR (Non-VAT Minus Rate? Əvəzləşdirmə)
ƏDV (VAT) = Əlavə dəyər vergisi - mal və xidmətlərin dəyərinin artımına görə tutulan vergi.

### ƏDV Ümumi Formulu
ƏDV üzrə ödəniləcək məbləğ =  
**Satış ƏDV - Alış ƏDV = Ödəniləcək/Alınacaq**

- Müsbət → Dövlətə ödənilir
- Mənfi → Dövlətdən geri alınır (əvəzləşdirmə)

---

## 🏗️ Sistem Arxitekturası

```
edv-system/
├── src/
│   ├── core/
│   │   ├── hesablama.py          # EDV hesablama motoru
│   │   ├── evvellesdirme.py     # Əvəzləşdirmə loqikasi
│   │   └── validator.py          # Məlumat yoxlama
│   ├── models/
│   │   ├── emeliyat.py           # Əməliyyat modeli
│   │   ├── shirket.py            # Müəssisə məlumatı
│   │   └── beyanname.py          # Bəyannamə strukturu
│   ├── reports/
│   │   ├── aylig_beyanname.py    # Aylıq hesabat
│   │   ├── illik_umumi.py        # İllik ümumi
│   │   └── edv_hesabati.py       # EDV spesifik hesabat
│   └── utils/
│       ├── vergi_tarifleri.py    # EDV dərəcələri (18%基调)
│       ├── tarix_utils.py        # Tarix hesablamaları
│       └── export.py             # XML/Excel export
├── data/
│   ├── emeliyatlar/              # Əməliyyat məlumatları
│   ├── shablonlar/               # Bəyannamə şablonları
│   └── arxiv/                    # Tarixi arxiv
├── docs/
│   ├── az_qanunvericilik.md     # Azərbaycan qaydaları
│   └── istifade_qaydalari.md    # Sistem təlimatı
└── tests/
    └── test_hesablama.py

```

---

## ⚙️ Əsas Funksionallıqlar

### 1. Əməliyyat Daxil Edilməsi
```python
# Satış əməliyyatı
satis = Emeliyat(
    nov="satis",
    mebleg=1000,        # ƏDV-siz məbləğ
    edv_rate=18,        # Faiz (standart 18%)
    tarix="2026-02-20",
    counterparty="ABC Şirkət"
)
# EDV = 1000 * 0.18 = 180 AZN
# Ümumi = 1180 AZN

# Alış əməliyyatı
alis = Emeliyat(
    nov="alis", 
    mebleg=500,
    edv_rate=18,
    tarix="2026-02-20",
    counterparty="XYZ Təchizatçı"
)
# EDV = 500 * 0.18 = 90 AZN (avans edv)
```

### 2. Əvəzləşdirmə Hesablama
```
Aylıq Hesablama:
- Ümumi Satış ƏDV: 5,400 AZN
- Ümumi Alış ƏDV:   3,200 AZN
- Fərq:             2,200 AZN (ödəniləcək)

Əgər Alış > Satış olsaydı:
- Fərq: Mənfi → Dövlətdən geri alınır
```

### 3. Avtomatik Təqvimsiz Bildirişlər
- Bəyannamə son tarixinə 5 gün qalmış: "🚨 EDV bəyannaməsi ödəniş tarixi yaxınlaşır"
- Gecikmə cəriməsi hesablama

---

## 📊 Raporlar

| Rapor | Tezlik | Format |
|-------|--------|--------|
| EDV Beyannamesi | Aylıq | XML (e-gov) |
| Əvəzləşdirmə Cədvəli | Aylıq | Excel/PDF |
| Əməliyyat Qeydı | Real-time | Dashboard |
| İllik Ümumi | İllik | PDF |

---

## 🔧 Texnologiya Stack

- **Backend:** Python (FastAPI/FastAPI)
- **DB:** SQLite (yerli) / PostgreSQL (istehsal)
- **Rapor:** Pandas + OpenPyXL (Excel)
- **Export:** XML (Azərbaycan e-gov formatı)

---

## ⚠️ Gözlənilən Azərbaycan Spesifik Baxışı

**Zeyd'i əlavə etməli olduqları (qanunlardan tövsiyə etdiyi):**

1. **ƏDV dərəcələri:**
   - Standart: 18%
   - Ərzaq/məişət: 0% (sadələşdirilmiş)
   - İdxal: ?

2. **Əvəzləşdirmə şərtləri:**
   - Minimum hansı sənədlər tələb olunur?
   - Nə qədər vaxtda geri alınır?
   - Negativ balans necə aparılır?

3. **Bəyannamə təqdimatı:**
   - Son tarix hər ay neçə?
   - Onlayn sistem (e-gov) formatı
   - Cərimə + faiz dərəcələri

**Əlavə mənbələr lazımdır:**
- [ ] https://www.e-qanun.ai/results/46948 (tam oxu)
- [ ] Vergilər Nazirliyi rəsmi saytı
- [ ] e-tax.gov.az portal formatları

Zeyd, bu əsasları vergin - düzələcəyim və tamamlayacağım. Bir də dediklərimi de, yoxsa başqa bir mənbə verim?
