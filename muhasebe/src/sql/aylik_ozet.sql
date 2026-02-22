-- ═════════════════════════════════════════════════════════════
-- AYLIK ÖZET RAPORU
-- Amaç: Belirli bir ay için tüm işlemlerin özetini gösterme
-- Parametreler: @yil, @ay
-- ═════════════════════════════════════════════════════════════

SELECT 
    k.yil,
    k.ay,
    COUNT(*) AS toplam_kayit,
    SUM(CASE WHEN k.tip = 'satis' THEN k.tutar ELSE 0 END) AS satis_toplam,
    SUM(CASE WHEN k.tip = 'alis' THEN k.tutar ELSE 0 END) AS alis_toplam,
    SUM(k.edv_tutari) AS toplam_edv,
    SUM(k.yekun_tutar) AS genel_toplam
FROM kayitlar k
WHERE k.yil = :yil AND k.ay = :ay
GROUP BY k.yil, k.ay;