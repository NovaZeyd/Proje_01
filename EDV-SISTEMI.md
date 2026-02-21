# EDV (ƏDV) Otomasyon Sistemi

## 1. EDV Temel Qaydaları (Azerbaycan)

### 1.1 EDV Oranları
| Vergi Oranı | Tətbiq Sahəsi |
|-------------|---------------|
| **18%** | Standart əməliyyatlar (əsas oran) |
| **0%** | İxrac əməliyyatları |
| **Azad** | Bəlli qaydada güzəştli əməliyyatlar |

### 1.2 Vergiyə Cəlb Olunma
- **Vergi ödəyicisi** = İllik dövriyyə 200,000 AZN-dən yüksək olanlar
- **Könüllü qeydiyyat** = Dövriyyə limitinə çatmaq istəyənlər

### 1.3 Əsas Vəsaitlərin (Ə.V.) EDV-si
- **1 ilədək faydalı istifadə müddəti olan Ə.V.** = Tam məbləğdə əvəzləşdirilir (satıcı mərhələsində)
- **1 ildən uzun faydalı istifadə müddəti olan Ə.V.** = Üzərinə 36 ay (3 il) bölünərək əvəzləşdirilir

### 1.4 Əvəzləşdirmə (Credit) Mexanizmi
```
Ödəniləcək EDV = Satışdan yığılan EDV - Satınalmadan ödənilən EDV
```
- **Məbləğ > 0** → Dövlətə ödəniş
- **Məbləğ < 0** → Dövlətdən geri alma (3 aya qədər iadə)

## 2. Sistem Arxitekturası

### 2.1 Verilənlər Bazası Strukturu
```
┌─────────────────────────────────────────────────────────┐
│                  EDV AUTOMASIYA SİSTEMİ                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   MƏHSULLAR  │  │  ƏMƏLİYYATLAR │  │   MÜƏSSİSƏ   │ │
│  │              │  │               │  │              │ │
│  │  - id        │  │  - id         │  │  -id         │ │
│  │  - ad        │  │  - tip        │  │  - ad        │ │
│  │  - kod       │  │  - tarixi     │  │  - VÖEN      │ │
│  │  - qiymət    │  │  - məbləğ     │  │  - ünvan     │ │
│  │  - edv_oran  │  │  - edv_məbləğ │  │  - tel       │ │
│  │              │  │  - qarşıtərəf │  │              │ │
│  │              │  │  - sənəd_no   │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │           EDV HESABLAMA MOTORU                  │    │
│  │                                                 │    │
│  │   satis_edv()    → Satışdan alınan EDV        │    │
│  │   alis_edv()     → Alışda ödənilən EDV        │    │
│  │   avto_was()     → Ə.V. üçün aylıq əvəz       │    │
│  │   net_edv()      → Net vəziyyət hesabı        │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │           HESABAT MODULU                         │    │
│  │                                                 │    │
│  │   - Aylıq bəyannamə (vergi.gov.az format)       │    │
│  │   - Bölünmüş əvəzləşdirmə cədvəli               │    │
│  │   - Salamətlik balansı                          │    │
│  │   - Vergi hesabı çıxarışı                       │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 3. Hesablama Alqoritmləri

### 3.1 Məbləğdən EDV Çıxarma (Alış)
```
Məbləğ = 1000 AZN (EDV ilə)
EDV = 1000 × 18/118 = 152.54 AZN (yuxarı yuvarlaqlaşdırılır)
Xalis məbləğ = 1000 - 152.54 = 847.46 AZN
```

### 3.2 Məbləğə EDV Əlavə (Satış)
```
Xalis məbləğ = 1000 AZN
EDV məbləği = 1000 × 18% = 180 AZN
Ümumi məbləğ = 1000 + 180 = 1180 AZN
```

### 3.3 Əsas Vəsait Üzrə Aylıq Əvəzləşdirmə
```
Məsələn: Komputer = 3000 AZN (EDV ilə)
EDV = 3000 × 18/118 = 457.63 AZN
Aylıq əvəz = 457.63 ÷ 36 = 12.71 AZN/ay
```

## 4. Klass Strukturu (OOP)

```python
class Məhsul:
    """Məhsul və ya xidmət məlumatı"""
    def __init__(self, ad, kod, qiymət, edv_oran=18):
        self.ad = ad
        self.kod = kod
        self.qiymət = qiymət
        self.edv_oran = edv_oran

class Əmiləət:
    """Alış və ya satış əməliyyatı"""
    def __init__(self, tip, məhsul, miqdar, tarix):
        self.tip = tip  # "alış" və ya "satış"
        self.məhsul = məhsul
        self.miqdar = miqdar
        self.tarix = tarix
        self.edv_məbləği = self.hesablama_edv()

    def hesablama_edv(self):
        if self.tip == "satış":
            return self.məhsul.qiymət * self.miqdar * self.məhsul.edv_oran / 100
        else:  # alış
            ümumi = self.məhsul.qiymət * self.miqdar
            return ümumi * self.məhsul.edv_oran / (100 + self.məhsul.edv_oran)

class ƏsasVəysait:
    """1 ildən çox istifadə müddəti olan aktivlər"""
    def __init__(self, ad, alış_qiyməti, alış_tarixi):
        self.ad = ad
        self.alış_qiyməti = alış_qiyməti
        self.alış_tarixi = alış_tarixi
        self.ümumi_edv = alış_qiyməti * 18 / 118
        self.qalıq_ay = 36
        self.avto_was = self.ümumi_edv / 36

class EDVMeneceri:
    """Ümumi EDV idarəetmə sinfi"""
    def __init__(self, müəssisə_voen):
        self.voen = müəssisə_voen
        self.əməliyyatlar = []
        self.əsas_vəsaitlər = []

    def əlavə_ət_əməliyyat(self, əməliyyat):
        self.əməliyyatlar.append(əməliyyat)

    def aylıq_xülasə(self, il, ay):
        """Göstərilən ay üçün EDV hesabları"""
        satış_edv = sum(e.edv_məbləği for e in self.əməliyyatlar
                        if e.tip == "satış" and e.tarix.year == il and e.tarix.month == ay)
        alış_edv = sum(e.edv_məbləği for e in self.əməliyyatlar
                       if e.tip == "alış" and e.tarix.year == il and e.tarix.month == ay)

        # Əsas vəsaitlər üzrə aylıq əvəzləşdirmə
        avto_was = 0
        for əv in self.əsas_vəsaitlər:
            if əv.qalıq_ay > 0:
                avto_was += əv.avto_was
                əv.qalıq_ay -= 1

        net_edv = satış_edv - alış_edv - avto_was
        return {
            "satış_edv": satış_edv,
            "alış_edv": alış_edv,
            "vəsayət_was": avto_was,
            "net_edv": net_edv,
            "ödəniləcək": max(0, net_edv),
            "gerialınacaq": max(0, -net_edv)
        }
```

## 5. File Strukturu

```
/edv-sistemi/
├── main.py              # Əsas giriş nöqtəsi
├── models/
│   ├── __init__.py
│   ├── məhsul.py        # Məhsul modeli
│   ├── əməliyyat.py     # Əməliyyat modeli
│   ├── vəsait.py        # Əsas vəsait modeli
│   └── müəssisə.py      # Müəssisə məlumatları
├── engine/
│   ├── __init__.py
│   ├── hesablama.py     # EDV hesablama funksiyaları
│   └── avto_was.py      # Əvəzləşdirmə modulu
├── reports/
│   ├── __init__.py
│   ├── bəyannamə.py     # Aylıq bəyannamə
│   └── çıxarış.py       # Vergi hesabı çıxarışı
├── database/
│   └── db.sqlite        # SQLite verilənlər bazası
└── config.py            # Sistem konfiqurasiyası
```

## 6. Əsas Funksiyonallıqlar

| № | Funksiya | Prioritet |
|---|----------|-----------|
| 1 | Alış/Satış əməliyyatı daxil etmək | 🔴 Yüksək |
| 2 | Aylıq EDV hesablaması | 🔴 Yüksək |
| 3 | Bəyannamə generasiyası | 🔴 Yüksək |
| 4 | Əsas vəsait izləmə | 🟡 Orta |
| 5 | Excel/CSV idxal-ixrac | 🟡 Orta |
| 6 | QB (QuickBooks) integrasiyası | 🟢 Aşağı |
| 7 | vergi.gov.az upload | 🟢 Aşağı |

## 7. Növbəti Addımlar

1. **SQLite veritabanı** yaratmaq
2. **Klass modellərini** Python ilə yazmaq
3. **CLI interfeysi** (komanda satırı) inşa etmək
4. **Test məlumatları** ilə sistemi yoxlamaq
5. **GUI** (qrafik interfeys) əlavə etmək (istəyə bağlı)

---
*Yaratma tarixi: 2026-02-20*
*Tərtibatçı: Nova (AI assistant)*
*Müştəri: Zeyd*
