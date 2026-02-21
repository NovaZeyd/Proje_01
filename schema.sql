-- Generic Multi-Tenant Vergi Sistemi - PostgreSQL Schema
-- Company: Generic mapping ile her şirket için özelleştirilebilir

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core: Şirket/Mükellef tablosu
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    voen VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    activity_code VARCHAR(20),  -- faaliyetNo (örn: 4771107)
    activity_name VARCHAR(255),   -- faaliyet adı
    tax_type VARCHAR(20) DEFAULT 'SVS', -- 'SVS', 'Ümumi', 'Sadələşdirilmiş'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Excel/XML Import Mapping (Her şirket kendi formatını tanımlar)
CREATE TABLE import_mappings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    -- Kaynak tipi
    source_type VARCHAR(20) NOT NULL, -- 'excel_bank', 'excel_invoice', 'xml_tax'
    
    -- Kolon eşləmeleri (JSON: {kaynak_kolon: hedef_alan})
    column_mapping JSONB NOT NULL,
    -- Örnek: {"0": "tarix", "1": "mebleg", "2": "aciqlama", "5": "voen"}
    
    -- Format ayarları
    date_format VARCHAR(20) DEFAULT 'DD.MM.YYYY',
    decimal_separator VARCHAR(5) DEFAULT ',',
    skip_rows INTEGER DEFAULT 0,  -- Başlık satırı atla
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Qaimələr (Gelen + Giden)
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    -- Qaimə tipi
    direction VARCHAR(10) NOT NULL CHECK (direction IN ('IN', 'OUT')), -- Gelen/Gönderilen
    status VARCHAR(50) DEFAULT 'Təsdiqləndi', -- Təsdiqləndi, Gözləyir, Ləğv
    
    -- Vergi bilgileri
    voen_counterparty VARCHAR(20) NOT NULL, -- Karşı taraf VÖEN
    counterparty_name VARCHAR(255),
    
    -- Qaimə detayları
    invoice_date DATE,
    series VARCHAR(10),      -- MT2501, MT2512 vs.
    number VARCHAR(50),      -- Qaimə nömrəsi
    
    -- Məbləğler
    amount_without_vat DECIMAL(15,2),
    vat_amount DECIMAL(15,2),
    total_amount DECIMAL(15,2),
    
    -- Metadata
    description TEXT,
    contract_info VARCHAR(500), -- Müqavilə məlumatı
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Hızlı sorgular için indexler
    INDEX idx_company_date (company_id, invoice_date),
    INDEX idx_voen (voen_counterparty),
    INDEX idx_direction (company_id, direction)
);

-- Bank Əməliyyatları
CREATE TABLE bank_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    transaction_date DATE NOT NULL,
    document_no VARCHAR(100), -- Əməliyyat nömrəsi
    
    -- Məbləğler (birisi NULL olur)
    amount_in DECIMAL(15,2) DEFAULT 0,   -- Mədaxil
    amount_out DECIMAL(15,2) DEFAULT 0,  -- Məxaric
    currency VARCHAR(3) DEFAULT 'AZN',
    
    -- Karşı taraf
    voen_counterparty VARCHAR(20),
    counterparty_name VARCHAR(255),
    bank_name VARCHAR(100), -- Kapital, PASHA vs.
    
    -- Əməliyyat tipi (otomatik/elle seçilebilir)
    transaction_type VARCHAR(50), -- 'POS', 'Transfer', 'Vergi', 'Əmək haqqı'
    description TEXT,
    
    -- Qaimə ile ilişkilendirme (opsiyonel)
    matched_invoice_id UUID REFERENCES invoices(id),
    match_status VARCHAR(20) DEFAULT 'unmatched', -- matched, unmatched, partial
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_company_date (company_id, transaction_date),
    INDEX idx_match_status (company_id, match_status)
);

-- ƏDV Bəyannamələri (XML'den import)
CREATE TABLE vat_declarations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    -- Dönem
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    period_type INTEGER DEFAULT 0, -- 0: aylıq, 1: rüblük
    
    -- Vergi hesaplama (XML'den)
    vat_accrued DECIMAL(15,2) DEFAULT 0,      -- Dərc olunmuş (gösterici 1001)
    vat_deductible DECIMAL(15,2) DEFAULT 0,   -- Əvəz olunmuş (gösterici 1008)
    vat_payable DECIMAL(15,2) DEFAULT 0,      -- Ödənilməli (1023)
    vat_receivable DECIMAL(15,2) DEFAULT 0,   -- Qaytarılmalı (varsa)
    
    -- Asıl vergi
    base_tax_amount DECIMAL(15,2),
    
    -- Raw XML (kaynak saklama)
    raw_xml TEXT,
    
    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, submitted, confirmed
    submitted_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, year, month),
    INDEX idx_period (year, month)
);

-- Sadələşdirilmiş Vergi Sistemi (SVS) Kayıtları
CREATE TABLE svs_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    
    -- Gelir
    total_income DECIMAL(15,2) DEFAULT 0,      -- Ümumi gəlir
    pos_income DECIMAL(15,2) DEFAULT 0,       -- POS satışları
    invoice_income DECIMAL(15,2) DEFAULT 0,   -- Fakturalı satışlar
    
    -- Xərc
    total_expenses DECIMAL(15,2) DEFAULT 0,   -- Ümumi xərclər
    rent_expense DECIMAL(15,2) DEFAULT 0,     -- İcarə xərci
    utility_expense DECIMAL(15,2) DEFAULT 0,  -- Kommunal
    salary_expense DECIMAL(15,2) DEFAULT 0,     -- Əmək haqqı
    other_expense DECIMAL(15,2) DEFAULT 0,
    
    -- SVS Hesaplama
    taxable_base DECIMAL(15,2), -- Vergi əsası (Gəlir - Xərc)
    svs_rate DECIMAL(5,2) DEFAULT 2.0, -- %1 veya %2 (Bakı/region)
    svs_tax DECIMAL(15,2),      -- Hesaplanan vergi
    
    -- Durum
    is_submitted BOOLEAN DEFAULT FALSE,
    submitted_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, year, month)
);

-- Debitor/Kreditor Hesapları (Anlık bakiye)
CREATE TABLE receivables_payables (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    voen_counterparty VARCHAR(20) NOT NULL,
    counterparty_name VARCHAR(255),
    type VARCHAR(20) CHECK (type IN ('DEBITOR', 'KREDITOR')), -- Alacaklı/Borçlu
    
    -- Bakiyeler
    opening_balance DECIMAL(15,2) DEFAULT 0, -- Açılış
    total_debit DECIMAL(15,2) DEFAULT 0,     -- Borç artışı
    total_credit DECIMAL(15,2) DEFAULT 0,    -- Ödeme/tahsilat
    current_balance DECIMAL(15,2) DEFAULT 0, -- Güncel bakiye
    
    -- Son güncelleme
    last_transaction_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, voen_counterparty, type),
    INDEX idx_balance (company_id, type, current_balance)
);

-- Sistem Ayarları (Logging/Audit)
CREATE TABLE import_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id),
    source_type VARCHAR(20), -- 'excel', 'xml', 'manual'
    file_name VARCHAR(255),
    records_processed INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    errors JSONB, -- Hatalı satırlar
    imported_by VARCHAR(100),
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Views (Yardımcı sorgular)
CREATE VIEW company_monthly_summary AS
SELECT 
    c.id as company_id,
    c.name,
    DATE_TRUNC('month', b.transaction_date) as month,
    SUM(b.amount_in) as total_in,
    SUM(b.amount_out) as total_out,
    COUNT(*) as transaction_count
FROM companies c
LEFT JOIN bank_transactions b ON c.id = b.company_id
GROUP BY c.id, c.name, DATE_TRUNC('month', b.transaction_date);

-- Trigger: Bakiye güncelleme (Debitor/Kreditor)
-- Invoice eklendiğinde/ güncellendiğinde bakiyeyi otomatik güncelleyen function

COMMIT;
