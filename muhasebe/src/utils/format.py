"""
Formatlama yardımcı fonksiyonları
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import re

def para_formatla(tutar, sembol: str = "AZN", ondalik: int = 2) -> str:
    """
    Para birimini formatla
    Örnek: 1234567.89 -> 1.234.567,89 AZN
    """
    if isinstance(tutar, (int, float)):
        tutar = Decimal(str(tutar))
    elif not isinstance(tutar, Decimal):
        tutar = Decimal('0')
    
    # Yuvarlama
    quantize_str = '0.' + '0' * ondalik
    tutar = tutar.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    
    # Formatla
    tam_kisim = int(tutar)
    ondalik_kisim = abs(tutar - int(tutar)).quantize(Decimal(quantize_str))
    ondalik_str = str(ondalik_kisim)[2:].zfill(ondalik)
    
    # Binlik ayraç
    tam_str = f"{tam_kisim:,}".replace(",", ".")
    
    return f"{tam_str},{ondalik_str} {sem "}

def para_yazili(tutar: Decimal, para_birimi: str = "AZN") -> str:
    """Para tutarını yazı ile göster"""
    birlikler = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
    onlar = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
    yuzler = ["", "yüz", "iki yüz", "üç yüz", "dört yüz", "beş yüz", "altı yüz", "yedi yüz", "sekiz yüz", "dokuz yüz"]
    
    def uc_haneli_yaz(n: int) -> str:
        y = n // 100
        o = (n % 100) // 10
        b = n % 10
        
        sonuc = []
        if y > 0:
            sonuc.append(yuzler[y])
        if o > 0:
            sonuc.append(onlar[o])
        if b > 0:
            sonuc.append(birlikler[b])
        
        return " ".join(sonuc)
    
    tam_kisim = int(abs(tutar))
    kurus = int((abs(tutar) - tam_kisim) * 100)
    
    if tam_kisim == 0:
        sonuc = "sıfır"
    else:
        milyar = tam_kisim // 1_000_000_000
        milyon = (tam_kisim % 1_000_000_000) // 1_000_000
        binler = (tam_kisim % 1_000_000) // 1_000
        yuzluk = tam_kisim % 1_000
        
        parcalar = []
        if milyar > 0:
            parcalar.append(f"{uc_haneli_yaz(milyar)} milyar")
        if milyon > 0:
            parcalar.append(f"{uc_haneli_yaz(milyon)} milyon")
        if binler > 0:
            parcalar.append(f"{uc_haneli_yaz(binler)} bin")
        if yuzluk > 0:
            parcalar.append(uc_haneli_yaz(yuzluk))
        
        sonuc = " ".join(parcalar)
    
    if para_birimi == "AZN":
        birim = "manat"
        kurus_birim = "qəpik"
    elif para_birimi == "USD":
        birim = "dolar"
        kurus_birim = "sent"
    elif para_birimi == "EUR":
        birim = "euro"
        kurus_birim = "sent"
    else:
        birim = para_birimi
        kurus_birim = "kurus"
    
    if kurus == 0:
        return f"{sonuc} {birim}"
    else:
        return f"{sonuc} {birim}, {kurus} {kurus_birim}"

def tarih_formatla(tarih, format: str = "%d.%m.%Y") -> str:
    """Tarihi formatla"""
    if isinstance(tarih, str):
        try:
            tarih = datetime.fromisoformat(tarih.replace('Z', '+00:00'))
        except:
            return tarih
    
    if isinstance(tarih, datetime):
        return tarih.strftime(format)
    
    return str(tarih)

def voen_dogrula(voen: str) -> bool:
    """VÖEN (Vergi Ödəyicisi Ehtiyat Nömrəsi) doğrulama"""
    voen = str(voen).strip()
    
    # TIN (Taxpayer Identification Number): 10 haneli
    # VÖEN: 7-10 haneli olabilir
    if not re.match(r'^\d{7,10}$', voen):
        return False
    
    return True

def hesap_kodu_formatla(kod: str) -> str:
    """Hesap kodunu standard formata getir"""
    kod = str(kod).strip()
    return kod.lstrip('0') or '0'

def belge_no_formatla(no: str, prefix: str = "", yil: bool = True) -> str:
    """Belge numarası formatla"""
    no = str(no).strip()
    if prefix:
        no = f"{prefix}-{no}"
    if yil:
        no = f"{no}/{datetime.now().year}"
    return no

def iban_formatla(iban: str) -> str:
    """IBAN'ı formatla (gruplu)"""
    iban = str(iban).replace(' ', '').upper()
    if len(iban) == 28 and iban.startswith('AZ'):
        return ' '.join([iban[i:i+4] for i in range(0, len(iban), 4)])
    return iban

def tel_formatla(tel: str) -> str:
    """Telefon numarasını formatla"""
    tel = re.sub(r'\D', '', str(tel))
    if len(tel) == 9 and tel.startswith('0'):
        tel = tel[1:]
    if len(tel) == 9:
        return f"+994 ({tel[:2]}) {tel[2:5]}-{tel[5:7]}-{tel[7:9]}"
    return tel
