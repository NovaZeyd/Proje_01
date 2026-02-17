# Zeyd Muhasebe Sistemi 🇦🇿

Azerbaycan muhasebe otomasyon sistemi - OpenClaw + n8n entegrasyonu.

## Özellikler

- ✅ **Maaş Hesaplama** (2026 vergi oranlarına göre)
  - DSMF (Sosial Sığorta): 25%
  - Gəlir vergisi: Proqressiv (0%, 14%, 25%)
  - İşsizlik sığortası: 0.5%
  - Tibbi sığorta: 2%
  
- ✅ **Məzuniyyət Hesablaması**
  - 1 il = 30 gün (əas)
  - Hər 5 ilə göre +2 gün
  - 15 ildən sonra +2 gün

- ✅ **Excel Entegrasyonu**
  - Otomatik işçi verisi oxuma
  - JSON/Excel export

- 🔄 **n8n Workflow** (yapım aşamasında)
  - Otomatik aylıq hesablatma
  - Mail/WhatsApp bildirişlər

## Kullanım

```bash
# Maaş hesablama
python src/payroll_calculator.py "maas_cedveli.xlsx"

# Test
python -c "from src.payroll_calculator import *; print('OK')"
```

## n8n Entegrasyonu

1. Excel yüklə → Python işlət → Report yarat → Mail göndər
2. Hər ayın sonunda avtomatik işləyər

## Kim Oluşturdu?

**Nova** - OpenClaw AI Asistanı (Zeyd üçün 🤖)
