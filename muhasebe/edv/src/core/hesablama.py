#!/usr/bin/env python3
"""
EDV (Əlavə Dəyər Vergisi) Hesablama Motoru
Azerbaycan Respublikasi qanunvericiliyinə uyğun
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from decimal import Decimal, ROUND_HALF_UP

# EDV Dərəcələri (Zeyd təsdiqləyəcək)
EDV_RATES = {
    "standart": Decimal("0.18"),    # 18% - Əsas dərəcə
    "sadələşdirilmiş": Decimal("0"),  # 0% - Ərzaq, dərman və s.
    "güzəştli": Decimal("0.10"),     # 10% - Bəzi kateqoriyalar
}

@dataclass
class Emeliyat:
    """Əməliyyat məlumatları"""
    id: str
    nov: str  # "satis" və ya "alis"
    mebleg: Decimal        # ƏDV-siz məbləğ
    edv_rate: Decimal      # Məsrəf faizi (0.18, 0.10, 0)
    tarix: datetime
    counterparty: str      # Tərəf-müqabil
    sened: str            # Sənəd nömrəsi (faktura)
    xidmet_mehsul: str    # Xidmət/Məhsul təsviri
    
    @property
    def edv_mebleg(self) -> Decimal:
        """Hesablanmış EDV məbləği"""
        return (self.mebleg * self.edv_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    
    @property
    def umumi_mebleg(self) -> Decimal:
        """ƏDV daxil ümumi məbləğ"""
        return self.mebleg + self.edv_mebleg


class EDVHesablama:
    """EDV hesablama və əvəzləşdirmə sistemi"""
    
    def __init__(self, shirket_id: str, il: int):
        self.shirket_id = shirket_id
        self.il = il
        self.emeliyatlar: List[Emeliyat] = []
    
    def emeliyat_elave(self, emeliyat: Emeliyat):
        """Əməliyyat əlavə et"""
        self.emeliyatlar.append(emeliyat)
    
    def aylig_hesabla(self, ay: int) -> dict:
        """
        Aylıq EDV hesablama
        
        Returns:
            {
                'satis_edv': Decimal,      # Satışdan əldə olunan
                'alis_edv': Decimal,       # Alışda ödədiyimiz
                'net_edv': Decimal,        # Fərq (ödəniləcək/geri alınacaq)
                'emri': str               # 'ode' və ya 'geri_al'
            }
        """
        o_ay_emeliyatlar = [
            e for e in self.emeliyatlar 
            if e.tarix.month == ay and e.tarix.year == self.il
        ]
        
        satis_edv = sum(
            e.edv_mebleg for e in o_ay_emeliyatlar if e.nov == "satis"
        )
        
        alis_edv = sum(
            e.edv_mebleg for e in o_ay_emeliyatlar if e.nov == "alis"
        )
        
        net_edv = satis_edv - alis_edv
        
        return {
            'satis_edv': satis_edv.quantize(Decimal("0.01")),
            'alis_edv': alis_edv.quantize(Decimal("0.01")),
            'net_edv': net_edv.quantize(Decimal("0.01")),
            'emri': 'ode' if net_edv >= 0 else 'geri_al',
            'ay': ay,
            'il': self.il
        }
    
    def evvellesdirme_hesabla(self, ay: int) -> dict:
        """
        Əvəzləşdirmə (Offset) hesablama
        Əgər alış edv > satış edv → geri alınır
        """
        result = self.aylig_hesabla(ay)
        
        if result['emri'] == 'geri_al':
            result['geri_alinacaq'] = abs(result['net_edv'])
            result['status'] = 'govde_geri_alma'
        else:
            result['odenilecek'] = result['net_edv']
            result['status'] = 'ode'
            
        return result
    
    def illik_umumi(self) -> dict:
        """İllik ümumi hesabat"""
        illik_net = Decimal('0')
        aylig_detallar = []
        
        for ay in range(1, 13):
            aylig = self.aylig_hesabla(ay)
            aylig_detallar.append(aylig)
            illik_net += aylig['net_edv']
        
        return {
            'illik_net_edv': illik_net.quantize(Decimal("0.01")),
            'aylig_detallar': aylig_detallar,
            'emri': 'ode' if illik_net >= 0 else 'geri_al'
        }


# Test nümunələri
if __name__ == "__main__":
    # Sadə test
    sistem = EDVHesablama("SHRK-001", 2026)
    
    # Satış əməliyyatı
    satis1 = Emeliyat(
        id="SAT-001",
        nov="satis",
        mebleg=Decimal("1000"),
        edv_rate=EDV_RATES["standart"],
        tarix=datetime(2026, 2, 20),
        counterparty="Müştəri A",
        sened="F-2026-001",
        xidmet_mehsul="Məhsul satışı"
    )
    sistem.emeliyat_elave(satis1)
    
    # Alış əməliyyatı  
    alis1 = Emeliyat(
        id="ALIS-001",
        nov="alis",
        mebleg=Decimal("500"),
        edv_rate=EDV_RATES["standart"],
        tarix=datetime(2026, 2, 20),
        counterparty="Təchizatçı B",
        sened="QF-2026-001",
        xidmet_mehsul="Xammal alışı"
    )
    sistem.emeliyat_elave(alis1)
    
    # Fevral hesablama
    result = sistem.aylig_hesabla(2)
    print(f"Fevral 2026 EDV Hesablama:")
    print(f"  Satış ƏDV: {result['satis_edv']} AZN")
    print(f"  Alış ƏDV: {result['alis_edv']} AZN")
    print(f"  Net ƏDV: {result['net_edv']} AZN")
    print(f"  Əmri: {result['emri']}")