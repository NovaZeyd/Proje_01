#!/usr/bin/env python3
"""
EDV (KDV) Hesabat Sistemi - Azerbaycan Vergi Formatı
Alis/Satis ayrımı, avans/sadə faktura desteği
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json

try:
    import pandas as pd
except ImportError:
    raise ImportError("pip install pandas openpyxl")


@dataclass
class EDV_Kaydi:
    tarih: datetime
    seri: str
    no: int
    tip: str
    voen: str
    unvan: str
    edv_siz_tutar: float
    edv_tutari: float
    yekun_tutar: float
    veziyyet: str
    yil: int
    ay: int


class EDV_Motor:
    """EDV hesaplama motoru"""
    
    COLUMNS = {
        'tarix': ['Qaimə tarixi', 'Tarih'],
        'seri': ['Qaimə seriyası', 'Seriya'],
        'no': ['Qaimə nömrəsi', 'Nömrə', 'No'],
        'tip': ['Tipi', 'Növü', 'Təlimat'],
        'voen': ['VÖEN', 'VOEN'],
        'unvan': ['Adı', 'Unvan', 'Name'],
        'edvsiz': ['Malın ƏDV-siz dəyəri', 'ƏDV-siz', 'Net'],
        'edv': ['ƏDV məbləği', 'ƏDV'],
        'yekun': ['Yekun məbləğ', 'Yekun', 'Toplam'],
        'veziyyet': ['Vəziyyəti', 'Status'],
    }

    def __init__(self):
        self.kayitlar: List[EDV_Kaydi] = []

    def excel_yukle(self, dosya: str) -> int:
        df = pd.read_excel(dosya)
        df.columns = [c.strip() for c in df.columns]
        harita = self._kolon_bul(df.columns)
        
        for _, row in df.iterrows():
            k = self._kayit_olustur(row, harita)
            if k:
                self.kayitlar.append(k)
        
        return len(self.kayitlar)

    def _kolon_bul(self, kolonlar) -> Dict:
        bulunan = {}
        for anahtar, isimler in self.COLUMNS.items():
            for isim in isimler:
                if isim in kolonlar:
                    bulunan[anahtar] = isim
                    break
        return bulunan

    def _kayit_olustur(self, row, h: Dict) -> Optional[EDV_Kaydi]:
        try:
            tarih = self._parse_tarih(row.get(h.get('tarix', ''), ''))
            if not tarih:
                return None
            
            tip_val = str(row.get(h.get('tip', ''), '')).lower()
            vez = str(row.get(h.get('veziyyet', ''), ''))
            
            return EDV_Kaydi(
                tarih=tarih,
                seri=str(row.get(h.get('seri', ''), '')),
                no=int(row.get(h.get('no', ''), 0) or 0),
                tip='satis' if ('sww' in tip_val or 'təsdiq' in vez.lower()) else 'alis',
                voen=str(row.get(h.get('voen', ''), '')).strip(),
                unvan=str(row.get(h.get('unvan', ''), '')).strip()[:50],
                edv_siz_tutar=self._para(row.get(h.get('edvsiz', 0), 0)),
                edv_tutari=self._para(row.get(h.get('edv', 0), 0)),
                yekun_tutar=self._para(row.get(h.get('yekun', 0), 0)),
                veziyyet=vez,
                yil=tarih.year,
                ay=tarih.month
            )
        except:
            return None

    def _parse_tarih(self, val) -> Optional[datetime]:
        if isinstance(val, datetime):
            return val
        for fmt in ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d']:
            try:
                return datetime.strptime(str(val).strip()[:10], fmt)
            except:
                pass
        return None

    def _para(self, val) -> float:
        if isinstance(val, (int, float)):
            return float(val)
        try:
            return float(str(val).replace(',', '.').replace(' ', '').replace('AZN', ''))
        except:
            return 0.0

    def aylik_ozet(self, yil: int, ay: int) -> Dict:
        aylik = [k for k in self.kayitlar if k.yil == yil and k.ay == ay]
        satis = [k for k in aylik if k.tip == 'satis']
        alis = [k for k in aylik if k.tip == 'alis']
        
        net = sum(k.edv_tutari for k in satis) - sum(k.edv_tutari for k in alis)
        
        return {
            'alis': {'edv_siz': sum(k.edv_siz_tutar for k in alis),
                     'edv': sum(k.edv_tutari for k in alis),
                     'yekun': sum(k.yekun_tutar for k in alis),
                     'sayi': len(alis)},
            'satis': {'edv_siz': sum(k.edv_siz_tutar for k in satis),
                      'edv': sum(k.edv_tutari for k in satis),
                      'yekun': sum(k.yekun_tutar for k in satis),
                      'sayi': len(satis)},
            'net': round(net, 2),
            'odenecek': max(0, round(net, 2)),
            'iade': abs(min(0, round(net, 2)))
        }

    def rapor(self, yil: int, ay: int, voen: str = "") -> str:
        o = self.aylik_ozet(yil, ay)
        return f"""╔════════════════════════════════════════════════════════════╗
║                   EDV BEYANNAMƏSI v1.0                    ║
╠════════════════════════════════════════════════════════════╣
  Dönem: {ay:02d}/{yil}     VÖEN: {voen or '_________'}
╠════════════════════════════════════════════════════════════╣

SATIŞ (ÇIXIŞ)
  ƏDV-siz:     {o['satis']['edv_siz']:>15,.2f} AZN
  ƏDV (18%):   {o['satis']['edv']:>15,.2f} AZN
  Yekun:       {o['satis']['yekun']:>15,.2f} AZN
  Kayıt:       {o['satis']['sayi']:>15} adet

ALIŞ (GİRİŞ) - Əvəzləşdirilməsi
  ƏDV-siz:     {o['alis']['edv_siz']:>15,.2f} AZN
  ƏDV (18%):   {o['alis']['edv']:>15,.2f} AZN  
  Yekun:       {o['alis']['yekun']:>15,.2f} AZN
  Kayıt:       {o['alis']['sayi']:>15} adet

NET HESAB
  Satış ƏDV:        {o['satis']['edv']:>12,.2f} AZN
  Alış ƏDV:         {o['alis']['edv']:>12,.2f} AZN
  Net Yükümlülük:   {o['net']:>12,.2f} AZN
  ────────────────────────────────────
  ÖDƏNƏCƏK:         {o['odenecek']:>12,.2f} AZN
  İADƏ EDİLƏCƏK:    {o['iade']:>12,.2f} AZN

╚════════════════════════════════════════════════════════════╝"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description='EDV Sistemi')
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-r', '--rapor', nargs=2, metavar=('YIL', 'AY'))
    parser.add_argument('--voen', default='')
    args = parser.parse_args()
    
    print("🇦🇿 EDV Hesabat Sistemi\n" + "=" * 35)
    
    m = EDV_Motor()
    if not Path(args.file).exists():
        print(f"❌ Dosya yok: {args.file}")
        return 1
    
    n = m.excel_yukle(args.file)
    print(f"✅ {n} kayıt yüklendi\n")
    
    if args.rapor:
        print(m.rapor(int(args.rapor[0]), int(args.rapor[1]), args.voen))
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
