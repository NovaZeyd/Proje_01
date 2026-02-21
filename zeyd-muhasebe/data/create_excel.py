#!/usr/bin/env python3
"""Doğru formatta örnek Excel oluşturur"""
import pandas as pd
from datetime import datetime, timedelta

data = {
    'ID': [1, 2, 3, 4, 5],
    'Ad': ['Əli', 'Vəli', 'Səməd', 'Əhməd', 'Qasım'],
    'Soyad': ['Məmmədov', 'Əliyev', 'Həsənli', 'Quliyev', 'Səfərov'],
    'FIN': ['5Z2F7KX', '2A9B3CD', '8X4Y2ZT', '1Q2W3ER', '6Y7U8IO'],
    'Vezifə': ['Mühhasib', 'Marketoloq', 'Proqramçı', 'Menecer', 'Satışçı'],
    'İşə Başlama Tarixi': [
        datetime(2019, 3, 15),
        datetime(2021, 6, 1),
        datetime(2020, 1, 10),
        datetime(2018, 9, 20),
        datetime(2022, 4, 5)
    ],
    'Maaş (AZN)': [2500, 1800, 3500, 2200, 1500],
    'İş Tipi': ['müqaviləli', 'müqaviləli', 'müqaviləli', 'müqaviləli', 'müqaviləli'],
    'Məzuniyyət Günü': [30, 30, 30, 34, 30],
    'Status': ['Aktiv', 'Aktiv', 'Aktiv', 'Aktiv', 'Aktiv']
}

df = pd.DataFrame(data)

df.to_excel('/root/.openclaw/workspace/zeyd-muhasebe/data/isciler.xlsx', 
            sheet_name='İşçi Məlumatları', index=False)

print("✅ Excel dosyası oluşturuldu: data/isciler.xlsx")
print(f"   {len(df)} işçi kaydedildi")
