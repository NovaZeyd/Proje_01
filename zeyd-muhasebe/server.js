#!/usr/bin/env node
/**
 * Zeyd Muhasebe REST API
 * n8n yerine - Node.js + Python subprocess
 * /hesapla endpoint'i - POST ile Excel dosya veya JSON veri
 */

const http = require('http');
const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const querystring = require('querystring');

const PORT = 5679; // n8n'den farklı port
const WORKSPACE = '/root/.openclaw/workspace/zeyd-muhasebe';

// HTTP Server
const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // /hesapla endpoint - JSON işçi listesi gönder
  if (req.url === '/hesapla' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        calculatePayroll(data, res);
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Geçersiz JSON', message: e.message }));
      }
    });
    return;
  }

  // /api/calculate endpoint - Excel dosya al
  if (req.url === '/api/calculate' && req.method === 'POST') {
    handleFileUpload(req, res);
    return;
  }

  // /health - sunucu durumu
  if (req.url === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({ status: 'ok', service: 'zeyd-muhasebe', timestamp: new Date().toISOString() }));
    return;
  }

  // / - ana sayfa
  if (req.url === '/') {
    res.writeHead(200);
    res.end(JSON.stringify({
      name: 'Zeyd Muhasebe API',
      version: '1.0',
      endpoints: {
        'POST /hesapla': 'İşçi listesi gönder, hesaplama yap',
        'POST /api/calculate': 'Excel dosya yükle',
        'GET /health': 'Sağlık kontrolü'
      },
      example: {
        method: 'POST',
        url: '/hesapla',
        body: {
          isciler: [
            { id: 1, ad: 'Əli', soyad: 'Məmmədov', maas: 2500, baslama_tarihi: '2019-03-15' }
          ]
        }
      }
    }));
    return;
  }

  // 404
  res.writeHead(404);
  res.end(JSON.stringify({ error: 'Sayfa bulunamadı' }));
});

// Dosya yükleme işleme
function handleFileUpload(req, res) {
  const boundary = req.headers['content-type']?.split('boundary=')[1];
  if (!boundary) {
    res.writeHead(400);
    res.end(JSON.stringify({ error: 'Content-Type: multipart/form-data gerekli' }));
    return;
  }

  let data = Buffer.from([]);
  req.on('data', chunk => data = Buffer.concat([data, chunk]));
  req.on('end', () => {
    const content = data.toString();
    const filePart = content.split(`--${boundary}`).find(p => p.includes('filename='));
    if (!filePart) {
      res.writeHead(400);
      res.end(JSON.stringify({ error: 'Dosya bulunamadı' }));
      return;
    }

    // Dosyayı kaydet
    const filename = `upload_${Date.now()}.xlsx`;
    const filepath = path.join(WORKSPACE, 'data', filename);
    
    // Binary veriyi çıkar ve kaydet
    const fileData = filePart.split('\r\n\r\n').slice(1).join('\r\n\r\n').replace(/\r\n--.*--$/, '');
    fs.writeFileSync(filepath, Buffer.from(fileData, 'binary'));

    // Python ile hesaplat
    exec(`cd ${WORKSPACE} && python3 src/payroll_calculator.py "data/${filename}"`, 
      { encoding: 'utf-8', timeout: 30000 },
      (error, stdout, stderr) => {
        // Geçici dosyayı sil
        try { fs.unlinkSync(filepath); } catch(e) {}

        if (error) {
          res.writeHead(500);
          res.end(JSON.stringify({ error: 'Hesaplama hatası', details: stderr }));
          return;
        }

        // Sonuçları oku
        const resultPath = path.join(WORKSPACE, 'output', 'hesabat.json');
        if (fs.existsSync(resultPath)) {
          const result = JSON.parse(fs.readFileSync(resultPath, 'utf8'));
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, data: result }));
        } else {
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, message: stdout }));
        }
      }
    );
  });
}

// Maaş hesaplama - direkt Node.js'te
function calculatePayroll(data, res) {
  const isciler = data.isciler || [];
  if (isciler.length === 0) {
    res.writeHead(400);
    res.end(JSON.stringify({ error: 'İşçi listesi boş' }));
    return;
  }

  // Python script oluştur ve çalıştır
  const pythonScript = `
import sys
import json
from datetime import datetime

isciler = ${JSON.stringify(isciler)}

results = []
for i in isciler:
    maas = i.get('maas', 0) or i.get('Maaş', 0) or 0
    baslama = i.get('baslama_tarihi', i.get('İşə_Başlama_Tarixi', '2020-01-01'))
    
    # Vergi hesaplama (Azerbaycan 2026)
    dsmf = maas * 0.03
    issizlik = maas * 0.005
    gelir_vergi = maas * 0.14 if maas > 8000 else maas * 0.14 if maas > 200 else maas * 0
    toplam_kesinti = dsmf + issizlik + gelir_vergi
    net = maas - toplam_kesinti
    isveren_maliyet = maas * 1.245
    
    # Mezuniyyet hesaplama
    try:
        staj_yil = (datetime.now() - datetime.strptime(str(baslama), '%Y-%m-%d')).days / 365.25
    except:
        staj_yil = 0
    mezuniyet = 30 + (int(staj_yil / 5) * 2) + (2 if staj_yil > 15 else 0)
    
    results.append({
        'id': i.get('id') or i.get('ID'),
        'ad': i.get('ad') or i.get('Ad'),
        'soyad': i.get('soyad') or i.get('Soyad'),
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

ozet = {
    'toplam_isci': len(results),
    'toplam_brut': round(sum(r['maas_brut'] for r in results), 2),
    'toplam_net': round(sum(r['maas_net'] for r in results), 2),
    'toplam_kesinti': round(sum(r['kesinti_toplam'] for r in results), 2),
    'toplam_isveren_maliyet': round(sum(r['isveren_maliyet'] for r in results), 2)
}

print(json.dumps({'isciler': results, 'ozet': ozet}, ensure_ascii=False))
`;

  const proc = exec(`python3 -c '${pythonScript}'`, { encoding: 'utf-8', timeout: 10000 }, (error, stdout, stderr) => {
    if (error) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: 'Hesaplama hatası', details: stderr }));
      return;
    }
    try {
      const result = JSON.parse(stdout);
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, ...result }));
    } catch (e) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: 'Sonuç ayrıştırma hatası', output: stdout }));
    }
  });
}

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🇦🇿 Zeyd Muhasebe API çalışıyor`);
  console.log(`📍 http://localhost:${PORT}`);
  console.log(`➜ GET  /health - Sağlık kontrolü`);
  console.log(`➜ POST /hesapla - Hesaplama yap`);
  console.log(`➜ POST /api/calculate - Excel dosya`);
  console.log('');
  console.log('Örnek kullanım:');
  console.log(`curl -X POST http://localhost:${PORT}/hesapla \\\n  -H "Content-Type: application/json" \\\n  -d '${JSON.stringify({isciler: [{id:1, ad:'Əli', soyad:'Məmmədov', maas:2500, baslama_tarihi:'2019-03-15'}]})}'`);
});
