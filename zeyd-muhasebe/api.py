#!/usr/bin/env python3
"""
🇦🇿 Zeyd Muhasebe REST API - Flask ile
n8n yerine - Çalışan ve stabil çözüm
PORT: 3000
"""

from flask import Flask, request, jsonify, render_template_string
import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

WORKSPACE = Path('/root/.openclaw/workspace/zeyd-muhasebe')
DATA_DIR = WORKSPACE / 'data'
OUTPUT_DIR = WORKSPACE / 'output'

def calculate_payroll(isciler):
    """Azerbaycan maaş hesaplama (inline)"""
    results = []
    
    for i in isciler:
        maas = float(i.get('maas', i.get('Maaş', 0)))
        baslama = i.get('baslama_tarihi', i.get('İşə_Başlama_Tarixi', '2020-01-01'))
        
        # Vergi hesaplamaları (Azerbaycan 2026)
        dsmf = maas * 0.03
        issizlik = maas * 0.005
        
        # Gelir vergisi progression
        if maas * 12 > 12000:
            yillik_brut = maas * 12
            gelir_vergi = (yillik_brut - 12000) * 0.25 / 12 + (12000 - 8000) * 0.14 / 12
        elif maas * 12 > 8000:
            gelir_vergi = (maas * 12 - 8000) * 0.14 / 12
        else:
            gelir_vergi = 0
            
        toplam_kesinti = dsmf + issizlik + gelir_vergi
        net = maas - toplam_kesinti
        isveren_maliyet = maas + (maas * 0.22) + (maas * 0.005) + (maas * 0.02)
        
        # Mezuniyyət
        try:
            baslama_date = datetime.strptime(str(baslama)[:10], '%Y-%m-%d')
            staj_gun = (datetime.now() - baslama_date).days
            staj_yil = staj_gun / 365.25
        except:
            staj_yil = 0
            
        mezuniyet = 30 + (int(staj_yil / 5) * 2)
        if staj_yil > 15:
            mezuniyet += 2
            
        results.append({
            'id': i.get('id', i.get('ID')),
            'ad': i.get('ad', i.get('Ad', '')),
            'soyad': i.get('soyad', i.get('Soyad', '')),
            'maas_brut': round(maas, 2),
            'maas_net': round(net, 2),
            'dsmf': round(dsmf, 2),
            'issizlik': round(issizlik, 2),
            'gelir_vergi': round(gelir_vergi, 2),
            'kesinti_toplam': round(toplam_kesinti, 2),
            'isveren_maliyet': round(isveren_maliyet, 2),
            'staj_yil': round(staj_yil, 2),
            'mezuniyet_gun': mezuniyet,
            'gunluk_ucret': round(maas / 30, 2)
        })
    
    return {
        'isciler': results,
        'ozet': {
            'toplam_isci': len(results),
            'toplam_brut': round(sum(r['maas_brut'] for r in results), 2),
            'toplam_net': round(sum(r['maas_net'] for r in results), 2),
            'toplam_kesinti': round(sum(r['kesinti_toplam'] for r in results), 2),
            'toplam_isveren_maliyet': round(sum(r['isveren_maliyet'] for r in results), 2)
        }
    }

@app.route('/')
def index():
    """Ana sayfa - Web arayüzü"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🇦🇿 Zeyd Muhasebe Sistemi</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .endpoint { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }
            code { background: #34495e; color: white; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🇦🇿 Zeyd Muhasebe API</h1>
        <p>2026 Azerbaycan muhasebe hesaplamaları</p>
        
        <h2>Endpointler</h2>
        <div class="endpoint">
            <strong>POST /api/hesapla</strong><br>
            JSON ile işçi gönder, hesaplama yap<br>
            <code>curl -X POST http://localhost:3000/api/hesapla -H "Content-Type: application/json" -d '{"isciler":[...]}'</code>
        </div>
        
        <div class="endpoint">
            <strong>POST /api/upload</strong><br>
            Excel dosya yükle ve hesaplat<br>
            <code>curl -F "file=@isciler.xlsx" http://localhost:3000/api/upload</code>
        </div>
        
        <div class="endpoint">
            <strong>GET /api/health</strong><br>
            Sağlık kontrolü
        </div>
        
        <h2>Örnek Veri</h2>
        <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
{
  "isciler": [
    { "id": 1, "ad": "Əli", "soyad": "Məmmədov", "maas": 2500, "baslama_tarihi": "2019-03-15" },
    { "id": 2, "ad": "Səməd", "soyad": "Həsənli", "maas": 3500, "baslama_tarihi": "2020-01-10" }
  ]
}
        </pre>
    </body>
    </html>
    ''')

@app.route('/api/health')
def health():
    """Sağlık kontrolü"""
    return jsonify({
        'status': 'ok',
        'service': 'zeyd-muhasebe',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/hesapla', methods=['POST'])
def hesapla():
    """Maaş hesaplama - JSON input"""
    try:
        data = request.get_json()
        if not data or 'isciler' not in data:
            return jsonify({'error': 'isciler alanı gerekli'}), 400
        
        result = calculate_payroll(data['isciler'])
        result['timestamp'] = datetime.now().isoformat()
        
        # Sonucu kaydet
        output_file = OUTPUT_DIR / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'data': result, 'saved_to': str(output_file)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    """Excel dosya yükleme"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Dosya gönderilmedi'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Dosya seçilmedi'}), 400
        
        # Geçici kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"upload_{timestamp}_{file.filename}"
        filepath = DATA_DIR / filename
        file.save(filepath)
        
        # Python ile hesaplat
        result = subprocess.run(
            [sys.executable, str(WORKSPACE / 'src' / 'payroll_calculator.py'), str(filepath)],
            capture_output=True, text=True, timeout=30
        )
        
        # Geçici dosyayı sil
        filepath.unlink(missing_ok=True)
        
        if result.returncode != 0:
            return jsonify({'error': 'Hesaplama hatası', 'details': result.stderr}), 500
        
        # Sonuçları oku
        output_file = WORKSPACE / 'output' / 'payroll_output.json'
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': True, 'output': result.stdout})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('🇦🇿 Zeyd Muhasebe API başlatılıyor...')
    print('📍 http://localhost:3000')
    print('')
    print('Kullanım:')
    print('  curl http://localhost:3000/api/health')
    print('  curl -X POST http://localhost:3000/api/hesapla -H "Content-Type: application/json" -d @veri.json')
    app.run(host='0.0.0.0', port=3000, debug=False)
