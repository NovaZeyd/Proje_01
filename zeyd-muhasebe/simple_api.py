#!/usr/bin/env python3
"""Basit HTTP API - Yerleşik Python kutuphaneleriyle"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import subprocess

PORT = 3000

def hesapla_maas(isciler):
    """Azerbaycan maaş hesaplama"""
    results = []
    
    for i in isciler:
        maas = float(i.get('maas', i.get('Maaş', 0)))
        baslama = i.get('baslama_tarihi', i.get('İşə_Başlama_Tarixi', '2020-01-01'))
        
        # Vergiler
        dsmf = maas * 0.03
        issizlik = maas * 0.005
        
        # Gelir vergisi
        if maas <= 250:
            gelir_vergi = 0
        elif maas <= 8000/12:
            gelir_vergi = 0
        else:
            gelir_vergi = maas * 0.14
            
        toplam_kesinti = dsmf + issizlik + gelir_vergi
        net = maas - toplam_kesinti
        isveren_maliyet = maas + (maas * 0.22) + (maas * 0.005) + (maas * 0.02)
        
        from datetime import datetime as dt
        try:
            baslama_date = dt.strptime(str(baslama)[:10], '%Y-%m-%d')
            staj_yil = (dt.now() - baslama_date).days / 365.25
        except:
            staj_yil = 0
            
        mezuniyet = 30 + (int(staj_yil / 5) * 2)
        if staj_yil > 15:
            mezuniyet += 2
            
        results.append({
            'id': i.get('id', i.get('ID', 0)),
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
            'mezuniyet_gun': mezuniyet
        })
    
    return {
        'isciler': results,
        'ozet': {
            'toplam_isci': len(results),
            'toplam_brut': round(sum(r['maas_brut'] for r in results), 2),
            'toplam_net': round(sum(r['maas_net'] for r in results), 2),
            'toplam_kesinti': round(sum(r['kesinti_toplam'] for r in results), 2)
        }
    }

class APIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/health':
            self._send_json({
                'status': 'ok',
                'service': 'zeyd-muhasebe',
                'time': datetime.now().strftime('%H:%M:%S')
            })
        elif self.path == '/':
            self._send_json({
                'name': '🇦🇿 Zeyd Muhasebe API',
                'endpoints': {
                    'GET /health': 'Sağlık kontrolü',
                    'POST /hesapla': 'Maaş hesapla (JSON)'
                },
                'ornek': {
                    'curl': 'curl -X POST http://localhost:3000/hesapla -H "Content-Type: application/json" -d \'{"isciler":[{"id":1,"ad":"Əli","maas":2500}]}\''
                }
            })
        else:
            self._send_json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        if self.path == '/hesapla':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                if 'isciler' not in data:
                    self._send_json({'error': 'isciler gerekli'}, 400)
                    return
                result = hesapla_maas(data['isciler'])
                result['timestamp'] = datetime.now().isoformat()
                self._send_json({'success': True, 'data': result})
            except Exception as e:
                self._send_json({'error': str(e)}, 500)
        else:
            self._send_json({'error': 'Not found'}, 404)
    
    def log_message(self, format, *args):
        pass  # Logları kapat

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), APIHandler)
    print(f"🇦🇿 Zeyd Muhasebe API çalışıyor: http://localhost:{PORT}")
    print(f"Test: curl http://localhost:{PORT}/health")
    print("Örnek:")
    print(f'curl -X POST http://localhost:{PORT}/hesapla -H "Content-Type: application/json" -d \'{{"isciler":[{{"id":1,"ad":"Əli","soyad":"Məmmədov","maas":2500,"baslama_tarihi":"2019-03-15"}}]}}\'')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKapatılıyor...")
