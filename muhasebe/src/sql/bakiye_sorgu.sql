-- ═════════════════════════════════════════════════════════════
-- BAKIYE RAPORU SORGUSU
-- Amaç: Hesap bakiyelerini ve hareketlerini listeleme
-- ═════════════════════════════════════════════════════════════

SELECT 
    h.hesap_kodu,
    h.hesap_adi,
    COALESCE(SUM(CASE WHEN kh.tip = 'borc' THEN kh.tutar ELSE 0 END), 0) AS toplam_borc,
    COALESCE(SUM(CASE WHEN kh.tip = 'alacak' THEN kh.tutar ELSE 0 END), 0) AS toplam_alacak,
    COALESCE(SUM(CASE WHEN kh.tip = 'borc' THEN kh.tutar ELSE -kh.tutar END), 0) AS net_bakiye
FROM hesaplar h
LEFT JOIN kayit_hareketler kh ON h.hesap_kodu = kh.hesap_kodu
WHERE h.status = 'aktif'
GROUP BY h.hesap_kodu, h.hesap_adi
ORDER BY h.hesap_kodu;