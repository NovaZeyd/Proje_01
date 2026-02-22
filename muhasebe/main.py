#!/usr/bin/env python3
"""
Muhasebe CLI - Ana giriş noktası

Kullanım:
    python main.py [--modul MODUL] [--islem ISLEM]
    
Örnekler:
    python main.py --import excel --file cariler.xlsx
    python main.py --rapor bakiye --tarih 2026-02
"""

import sys
import argparse
from pathlib import Path

# Modül yolunu ekle
sys.path.insert(0, str(Path(__file__).parent / "src"))

from db import Database
from raporlar import BakiyeRaporu, CariRaporu
from hareketler import TekHareketİslem, CiftHareketİslem
from utils import para_formatla, bu_yil

def cmd_bakiye_raporu(db: Database, args):
    """Bakiye raporunu göster"""
    rapor = BakiyeRaporu(db)
    from utils import bu_ay
    
    if args.tarih:
        # Özel dönem
        from utils.tarih import ozel_donem
        yil, ay = args.tarih.split('-') if '-' in args.tarih else (args.tarih, '12')
        aralik = ozel_donem(f"{yil}-{ay}-01", f"{yil}-{ay}-01")
    else:
        aralik = bu_ay()
    
    veri = rapor.ozet_getir(aralik.baslangic, aralik.bitis)
    
    print(f"\n{'='*60}")
    print(f"BAKİYE RAPORU")
    print(f"Dönem: {aralik.baslangic.strftime('%d.%m.%Y')} - {aralik.bitis.strftime('%d.%m.%Y')}")
    print(f"{'='*60}\n")
    
    for kayit in veri:
        print(f"{kayit.hesap_kodu:<10} {kayit.hesap_adi:<30} {para_formatla(kayit.bakiye):>15}")
    
    print(f"\n{'-'*60}")
    toplam_borc = sum(k.bakiye for k in veri if k.bakiye > 0)
    toplam_alacak = sum(abs(k.bakiye) for k in veri if k.bakiye < 0)
    print(f"{'TOPLAM BORÇ BAKİYE:':<41} {para_formatla(toplam_borc):>15}")
    print(f"{'TOPLAM ALACAK BAKİYE:':<41} {para_formatla(toplam_alacak):>15}")
    print(f"{'='*60}\n")

def cmd_cari_raporu(db: Database, args):
    """Cari raporunu göster"""
    rapor = CariRaporu(db)
    kartlar = rapor.tum_kartlar()
    
    print(f"\n{'='*80}")
    print(f"CARİ RAPORU")
    print(f"{'='*80}\n")
    print(f"{'Unvan':<30} {'VÖEN':<12} {'Bakiye':>15}")
    print(f"{'-'*80}")
    
    for kart in kartlar:
        bakiye = rapor.bakiye(kart.cari_id)
        print(f"{kart.unvan[:30]:<30} {kart.voen or '-':<12} {para_formatla(bakiye):>15}")
    
    print(f"{'='*80}\n")

def cmd_fis_al(db: Database, args):
    """Fiş al"""
    islem = CiftHareketİslem(db)
    fis = islem.fis_getir(args.no)
    
    if not fis:
        print(f"Fiş bulunamadı: {args.no}")
        return
    
    print(f"\n{'='*60}")
    print(f"FİŞ DETAYI: {fis.fis_no}")
    print(f"{'='*60}")
    print(f"Tarih: {fis.tarih.strftime('%d.%m.%Y')}")
    print(f"Tür: {fis.tur}")
    print(f"Belge: {fis.belge_no or '-'}")
    print(f"Açıklama: {fis.aciklama or '-'}\n")
    
    print(f"{'Hesap':<15} {'Açıklama':<25} {'Borç':>12} {'Alacak':>12}")
    print(f"{'-'*60}")
    for h in fis.hareketler:
        borc_st = para_formatla(h.borc) if h.borc else "-"
        alc_st = para_formatla(h.alacak) if h.alacak else "-"
        print(f"{h.hesap_kodu:<15} {h.aciklama[:25]:<25} {borc_st:>12} {alc_st:>12}")
    
    print(f"{'='*60}\n")

def cmd_yeni_fis(db: Database, args):
    """Yeni fiş oluştur"""
    islem = CiftHareketİslem(db)
    
    from datetime import datetime
    from decimal import Decimal
    
    # Demo veri
    fis_no = db.fis_no_uret()
    
    with db.transaction():
        fis = islem.fis_olustur(
            fis_no=fis_no,
            tarih=datetime.now(),
            tur="MAHSUP",
            aciklama=args.aciklama or "Test fişi"
        )
        
        # Demo hareketler
        islem.hareket_ekle(
            fis_id=fis.fis_id,
            hesap_kodu="120",
            borc=Decimal("1000.00"),
            aciklama="Cari borç"
        )
        islem.hareket_ekle(
            fis_id=fis.fis_id,
            hesap_kodu="600",
            alacak=Decimal("1000.00"),
            aciklama="Satış geliri"
        )
        
        fis.kapat()
    
    print(f"\n✓ Fiş oluşturuldu: {fis_no}")
    print(f"  Toplam: {para_formatla(1000.00)}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Muhasebe Sistemi CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
    python main.py --rapor bakiye              # Aylık bakiye
    python main.py --rapor cari                # Cari listesi
    python main.py --fis --no FIS-2026-00001   # Fiş görüntüle
    python main.py --yeni --aciklama "..."     # Yeni fiş
        """
    )
    
    parser.add_argument('--rapor', choices=['bakiye', 'cari'], help='Rapor türü')
    parser.add_argument('--tarih', help='Rapor dönemi (YYYY-MM formatı)')
    parser.add_argument('--fis', action='store_true', help='Fiş detayı')
    parser.add_argument('--no', help='Fiş numarası')
    parser.add_argument('--yeni', action='store_true', help='Yeni fiş oluştur')
    parser.add_argument('--aciklama', help='Fiş açıklaması')
    parser.add_argument('--db', default='muhasebe.db', help='Veritabanı dosyası')
    
    args = parser.parse_args()
    
    # Veritabanı bağlantısı
    db = Database(args.db)
    
    if args.rapor == 'bakiye':
        cmd_bakiye_raporu(db, args)
    elif args.rapor == 'cari':
        cmd_cari_raporu(db, args)
    elif args.fis:
        if not args.no:
            print("--no parametresi gereklidir")
            sys.exit(1)
        cmd_fis_al(db, args)
    elif args.yeni:
        cmd_yeni_fis(db, args)
    else:
        parser.print_help()
        print("\n📊 Muhasebe Sistemi hazır!")
        print("   --rapor bakiye  -> Bakiye raporu")
        print("   --rapor cari    -> Cari raporu")
        print("   --yeni          -> Demo fiş oluştur\n")

if __name__ == '__main__':
    main()
