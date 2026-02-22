-- ═════════════════════════════════════════════════════════════
-- VÖEN SORGUSU
-- Amaç: Belirli VÖEN'e ait tüm işlemleri listeleme
-- ═════════════════════════════════════════════════════════════

SELECT 
    voen,
    unvan,
    COUNT(*) AS islem_sayisi,
    SUM(CASE WHEN tip = 'satis' THEN yekun_tutar ELSE 0 END) AS satis_toplam,
    SUM(CASE WHEN tip = 'alis' THEN yekun_tutar ELSE 0 END) AS alis_toplam,
    MIN(tarih) AS ilk_islem,
    MAX(tarih) AS son_islem
FROM kayitlar
WHERE voen = :voen
GROUP BY voen, unvan;