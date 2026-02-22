"""
Muëllif: Zeyd ƏDV Modulu
Əsas model sinifleri - Tamamilə Azerbaycan terminologiyasi ilə
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional
from enum import Enum


class EmeliyyatTipi(Enum):
    """Alish ve satish emeliyyat tipleri"""
    ALISH = "alish"
    SATISH = "satish"


class EdvOrani(Enum):
    """Azerbaycanda tetbiq olunan EDV oranlari"""
    STANDART = 18  # Esas oran (2026)
    SFIFIR = 0     # Ixrac emeliyyatlari
    SOMS = 1       # Azad


@dataclass
class Məhsul:
    """Mehsul ve ya xidmet melumati"""
    id: int
    ad: str
    kod: str
    qiymet: float
    edv_oran: int = 18
    aktiv: bool = True
    yaradilma_tarixi: datetime = field(default_factory=datetime.now)
    
    def net_qiymət(self) -> float:
        """EDV-siz (xalis) qiymet"""
        return round(self.qiymet / (1 + self.edv_oran / 100), 2)
    
    def edv_məbləği(self) -> float:
        """Mehsulun EDV meblegi"""
        return round(self.qiymet - self.net_qiymət(), 2)


@dataclass
class Emeliyyat:
    """Alish ve ya satish emeliyyati"""
    id: int
    tip: EmeliyyatTipi
    mehsul: Məhsul
    miqdar: float
    tarix: date
    sened_nomresi: str
    qarshi_teref: str
    qeyd: str = ""
    
    def ümumi_məbləğ(self) -> float:
        """Mehsul x miqdar"""
        return round(self.mehsul.qiymet * self.miqdar, 2)
    
    def edv_məbləği(self) -> float:
        """Emeliyyatin EDV meblegi"""
        if self.tip == EmeliyyatTipi.SATISH:
            # Satishda - EDV uzerine gelir
            return round(self.mehsul.net_qiymət() * self.miqdar * self.mehsul.edv_oran / 100, 2)
        else:
            # Alishda - EDV-den cixilir
            return round(self.ümumi_məbləğ() * self.mehsul.edv_oran / (100 + self.mehsul.edv_oran), 2)
    
    def xalis_məbləğ(self) -> float:
        """EDV-siz xalis mebleg"""
        return round(self.ümumi_məbləğ() - self.edv_məbləği(), 2)


@dataclass
class ƏsasVəysait:
    """1 ilden cox faydali istifade muddeti olan aktivler"""
    id: int
    ad: str
    alish_qiyməti: float
    alish_tarixi: date
    faydali_ömür_ay: int = 36  # Default 36 ay (3 il)
    
    def umumi_edv(self) -> float:
        """Aktivin umumi EDVsi"""
        return round(self.alish_qiyməti * 18 / 118, 2)
    
    def aylıq_əvəz(self) -> float:
        """Her ay ucun düşen əvəzləşdirmə meblegi"""
        return round(self.umumi_edv() / self.faydali_ömür_ay, 2)


@dataclass
class Müəssisə:
    """Sirket melumati"""
    id: int
    ad: str
    voen: str  # Vergi ödeyicisi eynilesdirme nomresi
    ünvan: str
    telefon: str
    aktiv: bool = True


@dataclass 
class AylıqXülasə:
    """Bir ay ucun EDV hesabat ozeti"""
    il: int
    ay: int
    satish_edv: float = 0.0
    alish_edv: float = 0.0
    vəsait_əvəzi: float = 0.0
    
    def net_edv(self) -> float:
        """Odenilecek ve ya geri alinacaq net mebleg"""
        return round(self.satish_edv - self.alish_edv - self.vəsait_əvəzi, 2)
    
    def ödəniləcək(self) -> float:
        """Dövlete ödenilecek mebleg"""
        return max(0, self.net_edv())
    
    def geri_alınacaq(self) -> float:
        """Dövletden geri alinacaq mebleg"""
        return max(0, -self.net_edv())
    
    def devlet_butcesi(self) -> float:
        """Devlet butcesine ödenilecek (20% mezós)"""
        return round(self.ödəniləcək() * 0.20, 2)
    
    def qaytarilmali_edv(self) -> float:
        """Qaytarilmali EDV meblegi (80% mezós)"""
        return round(self.ödəniləcək() * 0.80, 2)


@dataclass
class HesabatSətiri:
    """Detallı hesabat setri"""
    sira: int
    tarix: str
    sened_nomre: str
    qarshi_teref: str
    mehsul_ad: str
    miqdar: float
    birlik_qiymet: float
    cem_qiymet: float
    edv_oran: int
    edv_mebleg: float
    emeliyyat_tipi: str  # "Gelis" ve ya "Getme"
