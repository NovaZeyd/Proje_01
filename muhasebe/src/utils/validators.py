"""
Doğrulama fonksiyonları
"""

from decimal import Decimal
import re
from datetime import datetime

def dogrula_hesap_kodu(kod: str, seviye: int = 3) -> tuple:
    """
    Hesap kodunu doğrula
    Args:
        kod: Hesap kodu
        seviye: Hesap planı seviyesi (default 3)
    Returns:
        (bool, str) -> (geçerli_mi, hata_mesaji)
    """
    kod = str(kod).strip()
    
    if not kod:
        return False, "Hesap kodu boş olamaz"
    
    if not kod.isdigit():
        return False, "Hesap kodu sadece rakam içermeli"
    
    if seviye == 3:
        # 100, 120, 120.01 gibi
        if len(kod) > 6:
            return False, "3 seviyeli hesap kodu maksimum 6 haneli olmalı"
    
    return True, ""

def dogrula_belge_no(no: str) -> tuple:
    """Belge numarasını doğrula"""
    no = str(no).strip()
    
    if not no:
        return False, "Belge numarası boş olamaz"
    
    if len(no) > 50:
        return False, "Belge numarası çok uzun (max 50 karakter)"
    
    return True, ""

def dogrula_tutar(tutar) -> tuple:
    """Para tutarını doğrula"""
    try:
        if isinstance(tutar, str):
            tutar = tutar.replace(',', '.').replace(' ', '')
        d = Decimal(str(tutar))
        
        if d < 0:
            return False, "Tutar negatif olamaz"
        
        if d > Decimal('999999999999'):
            return False, "Tutar çok büyük"
        
        return True, ""
    except:
        return False, "Geçersiz tutar formatı"

def dogrula_tarih(tarih: str, format: str = "%Y-%m-%d") -> tuple:
    """Tarih formatını doğrula"""
    try:
        datetime.strptime(tarih, format)
        return True, ""
    except ValueError:
        return False, f"Geçersiz tarih formatı. Beklenen: {format}"

def dogrula_email(email: str) -> tuple:
    """E-posta adresini doğrula"""
    email = str(email).strip().lower()
    
    if not email:
        return True, ""  # Boş geçilebilir
    
    pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    
    return False, "Geçersiz e-posta formatı"

def dogrula_voen(voen: str) -> tuple:
    """VÖEN doğrulama (Azerbaycan)"""
    voen = str(voen).strip()
    
    if not voen:
        return True, ""  # Boş geçilebilir
    
    if not voen.isdigit():
        return False, "VÖEN sadece rakam içermeli"
    
    if not (7 <= len(voen) <= 10):
        return False, "VÖEN 7-10 haneli olmalı"
    
    return True, ""

def dogrula_aciklama(metin: str, max_uzunluk: int = 500) -> tuple:
    """Açıklama metnini doğrula"""
    metin = str(metin).strip()
    
    if not metin:
        return False, "Açıklama boş olamaz"
    
    if len(metin) > max_uzunluk:
        return False, f"Açıklama çok uzun (max {max_uzunluk} karakter)"
    
    return True, ""

def dogrula_telefon(tel: str) -> tuple:
    """Telefon numarasını doğrula"""
    tel = re.sub(r'\D', '', str(tel))
    
    if not tel:
        return True, ""  # Boş geçilebilir
    
    # Azerbaycan formatı
    if len(tel) == 9 or (len(tel) == 10 and tel.startswith('0')):
        return True, ""
    
    # Uluslararası format (+994 ile başlayan)
    if len(tel) == 12 and tel.startswith('994'):
        return True, ""
    
    return False, "Geçersiz telefon formatı"

def dogrula_sembol(sembol: str) -> tuple:
    """Para birimi sembolünü doğrula"""
    gecerli = ['AZN', 'USD', 'EUR', 'GBP', 'TRY', 'RUB']
    sembol = str(sembol).upper().strip()
    
    if sembol in gecerli:
        return True, ""
    
    return False, f"Desteklenmeyen para birimi. Geçerli: {', '.join(gecerli)}"
