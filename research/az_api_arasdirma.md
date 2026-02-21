# Azərbaycan Bank və Vergi API-ləri - Araşdırma
**Tarix:** 19 Fevral 2026
**Araşdırmaç:** Nova

## 1️⃣ Bank API-ləri (Açıq Bankçılıq)

### ✅ Mövcud vəziyyət:
Zeyd'in təsdiqlədiyi məlumat: **Bütün banklar API xidməti verir**

#### Mərkəzi Bank (Cbar) - Open Banking Framework:
- Azərbaycan Respublikası Mərkəzi Bankı **PSD2/Açıq Bankçılıq** standartlarını tətbiq edir
- 2023-2024-cü illərdə API infrastrukturu quruldu
- Banklar məcburən API təmin etməlidir (qanunvericilik tələbi)

#### Banklar və API-ləri:
| Bank | API | Status | Mühasib Faydası |
|------|-----|--------|----------------|
| **Kapital Bank** | Var ✅ | Açıq (təsisçilər üçün) | Hesab çıxarışları, balans |
| **PASHA Bank** | Var ✅ | Açıq | Kart əməliyyatları, hesablar |
| **Unibank** | Var ✅ | Məhdud | Elektron hesab |
| **ABB** (Azərbaycan Beynəlxalq) | Var ✅ | Açıq | Hesablar, əməliyyatlar |
| **Rabitəbank** | Var ✅ | Məhdud | E-pul, hesablar |
| **Expressbank** | Var ✅ | Məhdud | Kart əməliyyatları |
| **ADB** | Var ✅ | Məhdud | SME üçün |

### ⚠️ Problem:
- Bank API-ləri çoxu **yalnız təsisçilər və ya müqavilə ilə** açıqdır
- Standart **developer portal** yoxdur (bəyənnəmə messuliyyətlidir)
- **Mühasiblər üçün əlçatmazdır** (tech bilik tələb edir)

## 2️⃣ Vergi API-ləri (e-Gov / EDV)

### ✅ E-Gov Portal (e-gov.az):
- **Sahibkar xidmətləri** bölməsi:
  - Məcburi dövlət sosial sığortası hesabatları (3646)
  - Elektron Gömrük Bəyannamələri (3542)
  - Sığortaolunan qeydiyyatı (2750)
  - Əmək müqaviləsi bildirişləri (3187)
  - Müvəqqəti əlillik cədvəli (3144)

### ✅ EDV (ƏDV) Qaimə Sistemi:
Zeyd'in təsdiqi: **Qaimələrdən malları çəkən sistem var**
- ASAN İmza ilə giriş
- QR kod ilə qaimə yoxlama
- API mövcuddur (government internal)

### ⚠️ Problem:
- **Rəsmi API sənədləşdirilmiş deyil** (public docs yoxdur)
- Giriş üçün **ASAN İmza** və ya **Elektron İmza** tələb olunur
- **Automasiya məhduddur** (zəncirvi işləməz)

## 3️⃣ Rəqabət Təhlili

### Mövcud Proqramlar və Zəiflikləri:

| Proqram | Problem | Nə edə bilərik |
|---------|---------|----------------|
| **1C:Azərbaycan** | Çətin, qəliz, bahalı | Sadələşdirilmiş UI |
| **Logix** | Klassik, yavaş | Modern web alternativ |
| **Excel** | Manual, səhvə meylli | Avtomatlaşdırma |
| **SADƏ** | Məhdud funksionallıq | Tam qapsamlı |

## 4️⃣ Fürsətlər (Zeyd üçün biznes potensialı)

### 🎯 Hədəf Problem:
Zeyd'in dediyi: *"Hesabat yığmaq, izləmək, mal qalığı, çox adlı mallar"*

### 💡 Həll yolu:
1. **Bank API + Manual export** → Excel/CSV parsing (interim həll)
2. **E-Gov scraping** → ASAN imza avtomatlaşdırması (riskli)
3. **Manual data entry** → Smart forms, AI categorization
4. **Inventory tracking** → SKU management, QR/Barcode sistemi

## 5️⃣ Texniki Əlaqə İmkanları

### Bank ilə:
- İnternet Bankçılıq → **CSV/Excel export** → Parse
- Swift/Message sistemi (böyük şirkətlər üçün)
- **EBICS** protokolu (avro standart, bəzi banklar)

### Vergi ilə:
- E-gov → **ASAN login** → Data scraping (unstable)
- Bəzi xidmətlər **SOAP/XML API** ilə işləyir (sənədləşmə gizli)

## 6️⃣ Nəticə və Tövsiyələr

### ✅ Edə bilərik:
1. **Mühasib ui/dizayn** - 1C'dən asan, Excel'dən güclü
2. **Bank CSV import** - Bütün banklar dəstəklənir
3. **Hesabat builder** - Drag-drop ilə vergi hesabatları
4. **Inventory tracking** - QR kod ilə mal qalığı izləmə
5. **Mail bildirişləri** - Rəhbərlərə avtomatik raporlar

### ❌ Çətindir (hüquqi texniki):
1. **Real-time bank API** - Banklar açmır (təhlükəsizlik)
2. **Vergi sistemi avtomatlaşdırması** - ASAN imza ilə birləşdirmək riskli

### 🚀 Minimum Canlı Məhsul (MVP):
- **Bank əməliyyat importu** (CSV/Excel)
- **Kategorizasiya** (AI-assisted)
- **Hesabat generator** (Excel/PDF çıxış)
- **Mail scheduler** (aylıq/rüblük raporlar)

---

**Növbəti addım:**
1. CSV nümunəsi göstər (bankdan)
2. Hədəf müşəri profili (web-based)
3. Tech stack seçimi (FastAPI/React?)
