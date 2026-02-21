# OpenClaw Long-term Memory - Sıkıştırıldı (19 Şubat 2026)

Önemli not: Eski konuşmalar özetlendi. Context temizlendi.

---

## 🏢 Zeyd'in Profili (Güncel)

### Kimlik
- **İsim:** Zeyd
- **Meslek:** Muhasebeci
- **Lokasyon:** Baku, Azerbaycan (GMT+4)
- **Cihaz:** ASUS TUF Gaming F15, RTX 4050

### Teknik Altyapı
- **Modeller:** NVIDIA Kimi K2.5 (PRIMARY - 262K context - ÜCRETSİZ)
- **Fallback:** Groq Llama 3.3 70B (ÜCRETSİZ)
- **Setup:** OpenClaw + Ollama/NVIDIA modelleri
- **Shell:** Bash, WSL2

### Projeler

#### 📊 Muhasebe Otomasyonu (AKTİF)
**Başlangıç:** 20 Şubat 2026
**Dosya:** `muhasebe.md`
**Durum:** Context sistemi kuruldu, geliştirme başlayacak

### ⚡ Kritik Kısayollar (Nova için)
| Komut | Açıklama |
|-------|----------|

---
## 🚫 SERT KURALLAR (Bunlar Asla Bozulmaz)

> **Kaynak:** `RULES.md` - İlk oturumda oku, her zaman uygula

| # | Kural | Açıklama |
|---|-------|----------|
| **1** | **GÖREV SONU = "bitdi"** | Her görev tamamlanınca SON SATIRDA sadece "bitdi" yaz. Sakın unutma. |
| **2** | **CONTEXT DOLDURMA** | GitHub'a yükle her şeyi. Kod, doküman, rapor → hepsi repo'da. Context'te sadece referans tut. |
| **3** | **NE OLURSA OLSUN BİTİR** | Engel çıkarsa çöz. Çözülmüyorsa bypass yap. Ama görevi bırakma. |

### Uygulama Protokolü
```
1. Yeni görev → Parçalara böl
2. Her parça → GitHub'a commit 
3. Context %60+ → Compact iste (kullanıcı yapar)
4. Bitti → "bitdi" yaz
```

---

### ⚡ Kritik Kısayollar (Nova için)
| Komut | Açıklama |
|-------|----------|
| "CHECKPOINT" | Anında özet al, kaydet |
| "durum" veya "/status" | Context raporu |
| "/compact" | Anlık context sıkıştırma |

### 🔧 Sürekli Kurallar
1. **50+ satır kod** → Hemen dosyaya yaz
2. **Her 30dk/50k token** → Checkpoint al
3. **Context %60+** → Proaktif uyarı ver
4. **Context %80+** → Kritik: Compact + Memory flush

---

*Son güncelleme: 20 Şubat 2026*