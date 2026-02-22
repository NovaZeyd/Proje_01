#!/usr/bin/env python3
"""
Bakiye Raporu Modülü
Hesap bakiyelerini ve hareket özetlerini raporlar
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from decimal import Decimal
import json

@dataclass
class BakiyeKaydi:
    hesap_kodu: str
    hesap_adi: str
    toplam_borc: Decimal
    toplam_alacak: Decimal
    net_bakiye: Decimal

class BakiyeRaporu:
    """Bakiye raporlama motoru"""
    
    def __init__(self, data_kaynak: Optional[str] = None):
        self.kayitlar: List[BakiyeKaydi] = []
        self.data_kaynak = data_kaynak
    
    def kayit_ekle(self, kayit: BakiyeKaydi):
        """Yeni bakiye kaydı ekle"""
        self.kayitlar.append(kayit)
    
    def json_yukle(self, dosya_yolu: str) -> int:
        """JSON dosyasından veri yükle"""
        import json
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            veri = json.load(f)
        
        for item in veri:
            kayit = BakiyeKaydi(
                hesap_kodu=item['hesap_kodu'],
                hesap_adi=item['hesap_adi'],
                toplam_borc=Decimal(str(item['toplam_borc'])),
                toplam_alacak=Decimal(str(item['toplam_alacak'])),
                net_bakiye=Decimal(str(item['net_bakiye']))
            )
            self.kayitlar.append(kayit)
        
        return len(self.kayitlar)
    
    def ozet(self) -> Dict:
        """Genel bakiye özeti"""
        if not self.kayitlar:
            return {'durum': 'Veri yok'}
        
        toplam_borc = sum(k.toplam_borc for k in self.kayitlar)
        toplam_alacak = sum(k.toplam_alacak for k in self.kayitlar)
        net = sum(k.net_bakiye for k in self.kayitlar)
        
        return {
            'toplam_hesap': len(self.kayitlar),
            'toplam_borc': toplam_borc,
            'toplam_alacak': toplam_alacak,
            'net_bakiye': net,
            'durum': 'Borçlu' if net > 0 else 'Alacaklı' if net < 0 else 'Dengeli'
        }
    
    def excel_rapor(self, cikis_dosya: str):
        """Excel formatında rapor oluştur"""
        try:
            import pandas as pd
            
            data = []
            for k in self.kayitlar:
                data.append({
                    'Hesap Kodu': k.hesap_kodu,
                    'Hesap Adı': k.hesap_adi,
                    'Borç': float(k.toplam_borc),
                    'Alacak': float(k.toplam_alacak),
                    'Net Bakiye': float(k.net_bakiye)
                })
            
            df = pd.DataFrame(data)
            df.to_excel(cikis_dosya, index=False, sheet_name='Bakiye')
            return True
        except ImportError:
            print("⚠️ pandas kurulu değil: pip install pandas openpyxl")
            return False
    
    def metin_rapor(self) -> str:
        """Metin formatında rapor"""
        o = self.ozet()
        
        rapor = f"""
╔════════════════════════════════════════════════════════════╗
║                    BAKIYE RAPORU                           ║
╠════════════════════════════════════════════════════════════╣
Tarih: {datetime.now().strftime('%d-%m-%Y %H:%M')}
╠════════════════════════════════════════════════════════════╣
Toplam Hesap:    {o.get('toplam_hesap', 0):>15} adet
Toplam Borç:     {o.get('toplam_borc', 0):>15,.2f} AZN
Toplam Alacak:   {o.get('toplam_alacak', 0):>15,.2f} AZN
╠════════════════════════════════════════════════════════════╣
NET BAKIYE:      {o.get('net_bakiye', 0):>15,.2f} AZN
Durum:           {o.get('durum', 'Bilinmiyor'):>15}
╚════════════════════════════════════════════════════════════╝

Hesap Detayları:
{'─' * 60}
{'Hesap Kodu':<15} {'Hesap Adı':<25} {'Net Bakiye':>15}
{'─' * 60}"""
        
        for k in self.kayitlar[:20]:  # İlk 20 kayıt
            rapor += f"\n{k.hesap_kodu:<15} {k.hesap_adi:<25} {k.net_bakiye:>15,.2f}"
        
        if len(self.kayitlar) > 20:
            rapor += f"\n... ve {len(self.kayitlar) - 20} kayıt daha"
        
        return rapor
    
    def ara(self, anahtar: str) -> List[BakiyeKaydi]:
        """Hesap kodu veya adında arama yap"""
        anahtar = anahtar.lower()
        return [
            k for k in self.kayitlar 
            if anahtar in k.hesap_kodu.lower() 
            or anahtar in k.hesap_adi.lower()
        ]

if __name__ == "__main__":
    # Test
    rapor = BakiyeRaporu()
    
    # Örnek veri
    rapor.kayitlar = [
        BakiyeKaydi('100', 'Kasa', Decimal('5000'), Decimal('2000'), Decimal('3000')),
        BakiyeKaydi('120', 'Alıcılar', Decimal('15000'), Decimal('5000'), Decimal('10000')),
        BakiyeKaydi('320', 'Satıcılar', Decimal('8000'), Decimal('12000'), Decimal('-4000')),
    ]
    
    print(rapor.metin_rapor())