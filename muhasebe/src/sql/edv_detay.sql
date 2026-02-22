-- ═════════════════════════════════════════════════════════════
-- EDV DETAY RAPORU
-- Amaç: EDV hesaplamalarının detaylı listesi
-- ═════════════════════════════════════════════════════════════

SELECT 
    k.seri || '-' || k.no AS fatura_no,
    k.tarih,
    k.tip,
    k.voen,
    k.unvan,
    k.edv_siz_tutar AS matrah,
    k.edv_tutari AS edv,
    k.yekun_tutar AS toplam,
    CASE 
        WHEN k.tip = 'satis' THEN 'Çıkış'
        WHEN k.tip = 'alis' THEN 'Giriş'
        ELSE 'Diğer'
    END AS islem_turu
FROM kayitlar k
WHERE k.yil = :yil AND k.ay = :ay
ORDER BY k.tarih, k.tip;