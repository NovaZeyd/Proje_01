# NOVA'NIN SERT KURALLARI
# Bu dosya HER OTURUMDA ilk okunur, asla değiştirilmez.

## ASLA BOZULMAYACAK 3 KURAL

### KURAL #1: "bitdi" = Görev Sonu
- Her görev tamamlanınca SON SATIRDA sadece ve sadece "bitdi" yaz
- Bu bir onay işaretidir. Kullanıcı bunu bekler
- Asla unutma, asla atla

### KURAL #2: Context Doldurma → GitHub'a At
- 50+ satır kod = HEMEN dosyaya yaz, GitHub'a commit
- Rapor, analiz, not = GitHub'a veya memory'ye
- Context'te sadece referans linki tut
- "context dolduruyorum" deme, davranışınla göster

### KURAL #3: Ne Olursa Olsun Bitir
- Hata çıktı → 3 farklı çözüm dene
- GitHub erişim yok → local hazırla, token güncelle
- API limit → yedek modele geç
- Engel = görev değil, bulunacak çözüm

---

## PROJE PARÇALAMA PROTOKOLÜ

Her büyük görevi adım adım yap:

```
[GÖREV AL]
    ↓
[PARÇALARA BÖL] ← Max 3-4 parça
    ↓
[PARÇA 1] → Kod yaz → Test → Commit → Rapor
[PARÇA 2] → Kod yaz → Test → Commit → Rapor  
[PARÇA 3] → Kod yaz → Test → Commit → Rapor
    ↓
[HEPSİ BİTTİ]
    ↓
"bitdi"
```

### Compact Sinyali
Kullanıcı "compact" derse veya context %60+ olursa:
1. Anlık durumu özetle (1 paragraf)
2. MEMORY.md'ye kaydet
3. Context'i temizle
4. Devam et

---

## GİTHUB PROTOKOLÜ

```bash
# Her an hazır olmalı
cd /root/.openclaw/workspace/zeyd-muhasebe

# Token ayarla (eğer değişmişse)
git remote set-url origin https://TOKEN@github.com/NovaZeyd/zeyd-muhasebe.git

# Her değişiklik sonrası
git add .
git commit -m "açıklama"
git push origin main
```

### Token Erişim Sorunu Olursa:
1. `.github_token` dosyasını kontrol et
2. Yeni token al: GitHub → Settings → Developer → Personal Access Token
3. Dosyayı güncelle
4. Remote URL'yi güncelle
5. Push dene

---

## KONTROL LİSTESİ (Her cevaptan önce)

- [ ] Görev bitti mi? → "bitdi" yazılacak mı?
- [ ] Kod 50+ satır mı? → GitHub'a commit yapıldı mı?
- [ ] Context %60+ mı? → Compact istenecek mi?
- [ ] Bir sonraki adım var mı? → kısa özet yazıldı mı?

---

*Bu kurallar 21 Şubat 2026'da Zeyd tarafından belirlendi.*
*Asla değiştirilmez, sadece eklenebilir.*
