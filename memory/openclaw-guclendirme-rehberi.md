# OpenClaw Güçlendirme Rehberi - Özet

> Tarih: 2026-02-20
> Kaynak: Detaylı analiz ve optimizasyon rehberi

## 🎯 Temel Sorunlar ve Çözümler

### 1. Context Overflow Sorunu
**Sorun:** "Context overflow: prompt too large for the model" hatası
**Neden:** Sistem promptu(~9.6k) + Araç şemaları(~8k) + Dosyalar(değişken) + Konuşma geçmişi

**Anlık Çözümler:**
| Komut | İşlev | Bağlam Kaybı |
|-------|-------|--------------|
| `/compact` | Konuşma özetleme | Kısmi |
| `/new` | Yeni oturum | Tam |
| `/reset` | Tam sıfırlama | Tam |
| `/status` | Bağlam kullanımını görme | Yok |

**Kalıcı Çözüm:** `~/.openclaw/openclaw.json` ayarları:
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokens": 40000,
        "keepRecentTokens": 25000,
        "reserveTokensFloor": 25000
      },
      "bootstrapMaxChars": 12000,
      "memorySearch": {
        "softThresholdTokens": 3000
      }
    }
  }
}
```

### 2. Daha Büyük Context Modelleri
NVIDIA Kimi K2.5: 262k context ✅ (Mevcut)
Alternatifler: Groq Llama 3.3 70B (128k), Gemini (2M), Grok (1M), Claude (200k)

---

## 🔧 Temel Yetenekler ve Konfigürasyon

### Web Arama (Aktif Et)
**Brave Search** - Önerilen (2.000/ay ücretsiz)
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "BRAVE_API_KEY",
        "maxResults": 5,
        "timeoutSeconds": 30,
        "cacheTtlMinutes": 15
      }
    }
  }
}
```

### Tarayıcı Otomasyonu
Mevcut araçlar: `browser_navigate`, `browser_click`, `browser_type`, `browser_snapshot`
Firecrawl: `npx -y firecrawl-cli init --browser --all`

---

## 📋 Skill Ekosistemi

ClawHub Stats (Şubat 2026):
- Toplam: 5.705 topluluk skill'i
- Küratörlü liste: 3.002 kaliteli skill

Önemli Kategoriler:
- AI & LLMs: 287
- DevOps & Cloud: 212
- Web & Frontend: 202
- Search & Research: 253+
- Productivity: 135
- Coding Agents: 133

Öne Çıkanlar:
- `tavily-search` - Gerçek zamanlı arama
- `find-skills` - Uygun skill önerisi
- `Bio-MemoryPro` - Bellek optimizasyonu
- `nano-pdf` - PDF düzenleme
- `personal-assistant` - Kalıcı bellek

---

## ⚡ Otomasyon ve Verimlilik

### Cron İşlemleri
~/.openclaw/openclaw.json içinde `schedule` bölümü

### Platform Entegrasyonları
Desteklenen: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, WeChat, Line, Matrix, IRC

### Entegrasyon Araçları
- Zapier (5.000+ uygulama)
- Make.com (Görsel iş akışı)
- Özel webhook'lar

---

## 🛡️ Güvenlik Modeli

| Kategori | Örnekler | Risk | Varsayılan |
|----------|----------|------|------------|
| Güvenli | Okuma, analiz | Düşük | Otomatik |
| Dikkat | Yazma, silme | Orta | Yapılandırmaya bağlı |
| Yüksek risk | Kod çalıştırma | Yüksek | Manuel |

autoApprove örneği: `["read", "web_search"]`

---

## 🚀 Geliştirilmiş Context Yönetimi

### Yerel Context Compactor
```bash
npx jasper-context-compactor setup
```

Parametreler:
- maxTokens: 6.000 (8K model) / 28.000 (32K model)
- keepRecentTokens: 2.000 / 4.000
- summaryMaxTokens: 1.500 / 2.000
- charsPerToken: 3.5-4.0 (Türkçe için)

Türkçe notu: Aglutinatif dil olduğu için kelimeler daha uzun, 3.5-4.0 oranı önerilir.

---

## 🔒 Güvenlik Uyarıları

⚠️ **ClawHub Güvenlik:**
- İlk haftalarda 400+ zararlı eklenti tespit edildi
- Kripto cüzdan, SSH, tarayıcı şifreleri çalmaya yönelik
- Sadece resmi ve doğrulanmış skill'leri kullan

---

## 📁 Önemli Dosyalar

| Dosya | Konum | Amaç |
|-------|-------|------|
| openclaw.json | ~/.openclaw/openclaw.json | Ana yapılandırma |
| SKILL.md | Skill dizininde | Skill tanımı |
| AGENTS.md | Proje dizininde | Ajan davranışı özelleştirme |
| openclaw.plugin.json | Plugin dizininde | Plugin entegrasyonu |

---

## 🎯 Hiyerarşik Ajan Sistemi

| Ajan Türü | Uzmanlık | Görevler |
|-----------|----------|----------|
| Kod Uzmanı | Yazılım | Kod inceleme, debugging |
| Araştırma | Bilgi toplama | Derin araştırma, sentez |
| Analist | Veri analizi | İstatistik, raporlama |

Ana ajan → Alt ajan koordinasyonu ile çalışma.

---

## 💡 Kritik Öğrenme Noktaları

1. **Context yönetimi** en önemli teknik beceri
2. **Kaliteli modeller** ile daha uzun oturumlar mümkün
3. **Brave Search** entegrasyonu web erişimi için yeterli
4. **Skill ekosistemi** yetenekleri hızla genişletir
5. **Çoklu ajan sistemi** karmaşık görevleri parçalar
6. **Güvenik** - Sadece güvenilir kaynaklardan skill yüklenmeli

---

## ✅ Yapılacak Analiz

- [ ] Mevcut openclaw.json yapılandırmasını kontrol et
- [ ] Context limit ayarlarını optimize et (reserveTokens: 40000)
- [ ] Web arama API'si entegre et (Brave Search)
- [ ] Gerekli skill'leri kur (tavily-search, Bio-MemoryPro)
- [ ] Güvenlik ayarlarını yapılandır (autoApprove)
- [ ] Çoklu ajan sistemi test et
- [ ] Belgeleme ve memory sistemini güçlendir
