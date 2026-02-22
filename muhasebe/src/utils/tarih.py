"""
Tarih işlemleri yardımcı fonksiyonları
"""

from datetime import datetime, date, timedelta
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class TarihAraligi:
    baslangic: datetime
    bitis: datetime
    
    def gun_sayisi(self) -> int:
        return (self.bitis - self.baslangic).days + 1
    
    def aylara_bol(self) -> list:
        """Tarih aralığını aylara böl"""
        aylar = []
        current = self.baslangic
        while current <= self.bitis:
            ay_baslangic = current
            ay_sonu = ayin_sonu(current.year, current.month)
            ay_bitis = min(ay_sonu, self.bitis)
            aylar.append(TarihAraligi(ay_baslangic, ay_bitis))
            current = ay_sonu + timedelta(days=1)
        return aylar

def ayin_sonu(yil: int, ay: int) -> datetime:
    """Verilen yıl ve ayın son gününü döndür"""
    if ay == 12:
        return datetime(yil + 1, 1, 1) - timedelta(seconds=1)
    return datetime(yil, ay + 1, 1) - timedelta(seconds=1)

def yilin_sonu(yil: int) -> datetime:
    """Verilen yılın son gününü döndür"""
    return datetime(yil, 12, 31, 23, 59, 59)

def yilin_basi(yil: int) -> datetime:
    """Verilen yılın ilk gününü döndür"""
    return datetime(yil, 1, 1, 0, 0, 0)

def bu_ay() -> TarihAraligi:
    """Bulunduğumuz ayın tarih aralığı"""
    bugun = datetime.now()
    baslangic = datetime(bugun.year, bugun.month, 1)
    bitis = ayin_sonu(bugun.year, bugun.month)
    return TarihAraligi(baslangic, bitis)

def bu_yil() -> TarihAraligi:
    """Bulunduğumuz yılın tarih aralığı"""
    bugun = datetime.now()
    return TarihAraligi(yilin_basi(bugun.year), yilin_sonu(bugun.year))

def onceki_ay(ay_sayisi: int = 1) -> TarihAraligi:
    """N ay öncesinin tarih aralığı"""
    bugun = datetime.now()
    ay = bugun.month - ay_sayisi
    yil = bugun.year
    while ay <= 0:
        ay += 12
        yil -= 1
    baslangic = datetime(yil, ay, 1)
    bitis = ayin_sonu(yil, ay)
    return TarihAraligi(baslangic, bitis)

def ozel_donem(baslangic_str: str, bitis_str: str, format: str = "%Y-%m-%d") -> TarihAraligi:
    """String tarihlerden dönem oluştur"""
    baslangic = datetime.strptime(baslangic_str, format)
    bitis = datetime.strptime(bitis_str, format).replace(hour=23, minute=59, second=59)
    return TarihAraligi(baslangic, bitis)

def vade_kontrolu(vade_tarihi: datetime, bugun: Optional[datetime] = None) -> str:
    """Vade durumunu kontrol et"""
    if bugun is None:
        bugun = datetime.now()
    
    if vade_tarihi < bugun:
        gun = (bugun - vade_tarihi).days
        return f"Geçmiş ({gun} gün)"
    elif vade_tarihi.date() == bugun.date():
        return "Bugün"
    else:
        gun = (vade_tarihi - bugun).days
        return f"{gun} gün kaldı"

def cvp_tarih_formati(tarih: datetime) -> str:
    """Cari vade planı formatı"""
    return tarih.strftime("%Y%m%d")
