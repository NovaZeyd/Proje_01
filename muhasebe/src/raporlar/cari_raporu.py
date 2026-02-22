#!/usr/bin/env python3
"""
Cari Hesap Raporu Modülü
Müşteri ve tedarikçi hesap ekstreleri
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional
from decimal import Decimal

@dataclass
class CariHareket:
    id: int
    tarih: datetime
    belge_no: str
    aciklama: str
    borc: Decimal
    alacak: Decimal
    bakiye: Decimal

@dataclass
class CariKart:
    kod: str
    unvan: str
    voen: str = ""
    telefon: str = ""
    adres: str = ""
    hareketler: List[CariHareket] = field(default_factory=list)

class CariRaporu:
    """Cari hesap raporlama sistemi"""
    
    def __init__(self):
        self.cari_kartlar: Dict[str, CariKart] = {}
    
    def cari_ekle(self, cari: CariKart):
        """Yeni cari kart ekle"""
        self.cari_kartlar[cari.kod] = cari
    
    def hareket_ekle(self, cari_kodu: str, hareket: CariHareket):
        """Cari hesaba hareket ekle"""
        if cari_kodu in self.cari_kartlar:
            self.cari_kartlar[cari_kodu].hareketler.append(hareket)
            # Bakiyeyi otomatik hesapla
            hareket.bakiye = self._bakiye_hesapla(cari_kodu)
    
    def _bakiye_hesapla(self, cari_kodu: str) -> Decimal:
        """Cari hesabın güncel bakiyesini hesapla"""
        cari = self.cari_kartlar.get(cari_kodu)
        if not cari:
            return Decimal('0')
        
        toplam_borc = sum(h.borc for h in cari.hareketler)
        toplam_alacak = sum(h.alacak for h in cari.hareketler)
        return toplam_borc - toplam_alacak
    
    def ekstre_rapor(self, cari_kodu: str) -> Optional[str]:
        """Cari hesap ekstresi oluştur"""
        cari = self.cari_kartlar.get(cari_kodu)
        if not cari:
            return f"❌ Cari kod bulunamadı: {cari_kodu}"
        
        rapor = f"""
╔════════════════════════════════════════════════════════════╗
║                    CARİ HESAP EKSTRESİ                     ║
╠════════════════════════════════════════════════════════════╣
Cari Kodu: {cari.kod}
Ünvan:     {cari.unvan}
VÖEN:      {cari.voen or '_________'}
Telefon:   {cari.telefon or '-'}
Adres:     {cari.adres[:40] if cari.adres else '-'}
╠════════════════════════════════════════════════════════════╣
{'Tarih':<12} {'Belge':<12} {'Açıklama':<20} {'Borç':>10} {'Alacak':>10} {'Bakiye':>10}
╠════════════════════════════════════════════════════════════╣"""
        
        toplam_borc = Decimal('0')
        toplam_alacak = Decimal('0')
        
        for h in sorted(cari.hareketler, key=lambda x: x.tarih):
            rapor += f"\n{h.tarih.strftime('%d-%m-%Y'):<12} {h.belge_no:<12} {h.aciklama[:20]:<20} "
            rapor += f"{h.borc:>10,.2f} {h.alacak:>10,.2f} {h.bakiye:>10,.2f}"
            toplam_borc += h.borc
            toplam_alacak += h.alacak
        
        net = toplam_borc - toplam_alacak
        
        rapor += f"""
╠════════════════════════════════════════════════════════════╣
{'TOPLAM:':<47} {toplam_borc:>10,.2f} {toplam_alacak:>10,.2f}
╠════════════════════════════════════════════════════════════╣
{'NET BAKİYE:':<47} {abs(net):>21,.2f} ({'Borç' if net > 0 else 'Alacak'})
╚════════════════════════════════════════════════════════════╝"""
        
        return rapor
    
    def tum_cari_ozet(self) -> str:
        """Tüm cari hesapların özet tablosu"""
        if not self.cari_kartlar:
            return "📋 Kayıtlı cari hesap yok."
        
        rapor = """
╔════════════════════════════════════════════════════════════╗
║                 CARİ HESAP ÖZET TABLOSU                    ║
╠════════════════════════════════════════════════════════════╣
{'Kod':<12} {'Ünvan':<30} {'VÖEN':<12} {'Bakiye':>12}
╠════════════════════════════════════════════════════════════╣"""
        
        for kod in sorted(self.cari_kartlar.keys()):
            cari = self.cari_kartlar[kod]
            bakiye = self._bakiye_hesapla(kod)
            rapor += f"\n{cari.kod:<12} {cari.unvan[:30]:<30} {cari.voen[:12]:<12} {bakiye:>12,.2f}"
        
        rapor += "\n╚════════════════════════════════════════════════════════════╝"
        return rapor
    
    def borc_tl_cari_listesi(self) -> List[CariKart]:
        """Borçlu cari hesapları listele"""
        borclular = []
        for kod, cari in self.cari_kartlar.items():
            if self._bakiye_hesapla(kod) > 0:
                borclular.append(cari)
        return sorted(borclular, key=lambda x: self._bakiye_hesapla(x.kod), reverse=True)
    
    def alacak_tl_cari_listesi(self) -> List[CariKart]:
        """Alacaklı cari hesapları listele"""
        alacaklilar = []
        for kod, cari in self.cari_kartlar.items():
            if self._bakiye_hesapla(kod) < 0:
                alacaklilar.append(cari)
        return sorted(alacaklilar, key=lambda x: abs(self._bakiye_hesapla(x.kod)), reverse=True)
    
    def ara(self, anahtar: str) -> List[CariKart]:
        """Cari hesapta arama yap"""
        anahtar = anahtar.lower()
        return [
            cari for cari in self.cari_kartlar.values()
            if anahtar in cari.kod.lower() 
            or anahtar in cari.unvan.lower()
            or anahtar in cari.voen.lower()
        ]
    
    def export_json(self, dosya_yolu: str):
        """JSON formatına dışa aktar"""
        import json
        veri = []
        for kod, cari in self.cari_kartlar.items():
            veri.append({
                'kod': cari.kod,
                'unvan': cari.unvan,
                'voen': cari.voen,
                'telefon': cari.telefon,
                'adres': cari.adres,
                'bakiye': float(self._bakiye_hesapla(kod)),
                'hareket_sayisi': len(cari.hareketler)
            })
        
        with open(dosya_yolu, 'w', encoding='utf-8') as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Test
    rapor = CariRaporu()
    
    # Örnek cari hesap
    musteri = CariKart(
        kod='C-001',
        unvan='ABC Ticaret Ltd.',
        voen='1234567890',
        telefon='012-345-67-89',
        adres='Baku, Azerbaijan'
    )
    rapor.cari_ekle(musteri)
    
    # Örnek hareketler
    rapor.hareket_ekle('C-001', CariHareket(1, datetime(2026, 2, 1), 'F-001', 'Satış', Decimal('5000'), Decimal('0'), Decimal('0')))
    rapor.hareket_ekle('C-001', CariHareket(2, datetime(2026, 2, 10), 'T-001', 'Tahsilat', Decimal('0'), Decimal('3000'), Decimal('0')))
    
    print(rapor.ekstre_rapor('C-001'))
    print("\n" + rapor.tum_cari_ozet())