-- ═════════════════════════════════════════════════════════════
-- CARİ HESAP Ekstre Sorgusu
-- Amaç: Müşteri/Tedarikçi hesap hareketleri
-- ═════════════════════════════════════════════════════════════

SELECT 
    ch.tarih,
    ch.belge_no,
    ch.aciklama,
    CASE 
        WHEN ch.tip = 'borc' THEN ch.tutar 
        ELSE 0 
    END AS borc,
    CASE 
        WHEN ch.tip = 'alacak' THEN ch.tutar 
        ELSE 0 
    END AS alacak,
    SUM(CASE 
        WHEN ch.tip = 'borc' THEN ch.tutar 
        ELSE -ch.tutar 
    END) OVER (ORDER BY ch.tarih, ch.id) AS bakiye
FROM cari_hareketler ch
WHERE ch.cari_kodu = :cari_kodu
ORDER BY ch.tarih, ch.id;