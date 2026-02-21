#!/usr/bin/env python3
"""
Azerbaycan Maaş Hesaplama Sistemi - 2026 Kanunlarına Göre
Author: Nova (OpenClaw) for Zeyd
"""

import pandas as pd
import json
import logging
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
    fin: str
    position: str
    start_date: datetime
    gross_salary: float
    employment_type: str = "müqaviləli"
    is_active: bool = True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def tenure_years(self):
        return (datetime.now() - self.start_date).days / 365.25

class AzerbaijanTaxCalculator:
    """2026 Azerbaycan Vergi Hesaplamaları"""

    def __init__(self, year=2026):
        self.year = year
        self.dsmf_rates = {
            "müqaviləli": {"employer": 0.22, "employee": 0.03},
            "xidməti": {"employer": 0.15, "employee": 0.00}
        }
        self.unemployment_rate = 0.005
        self.medical_rate = 0.02
        self.income_tax_brackets = [
            (0, 8000, 0.00),
            (8000, 12000, 0.14),
            (12000, float('inf'), 0.25)
        ]

    def calculate_dsmf(self, gross, emp_type):
        rates = self.dsmf_rates.get(emp_type, self.dsmf_rates["müqaviləli"])
        emp_share = gross * rates["employee"]
        empr_share = gross * rates["employer"]
        return {"employer": empr_share, "employee": emp_share, "total": emp_share + empr_share}

    def calculate_income_tax(self, gross, year_to_date=0):
        annual = gross * 12 + year_to_date
        tax = 0.0
        prev = 0
        for low, high, rate in self.income_tax_brackets:
            if annual > low:
                taxable = min(annual, high) - max(low, prev)
                if taxable > 0:
                    tax += taxable * rate
                prev = high
            else:
                break
        return tax / 12

    def calculate_monthly(self, emp, working_days=27, actual_days=27):
        gross = emp.gross_salary * (actual_days / working_days)
        dsmf = self.calculate_dsmf(gross, emp.employment_type)
        unemployment = {"employee": gross * 0.005, "employer": gross * 0.005}
        medical = {"employer": gross * 0.02, "employee": 0}
        income_tax = self.calculate_income_tax(gross)

        total_deduction = dsmf["employee"] + unemployment["employee"] + income_tax
        net = gross - total_deduction
        employer_cost = gross + dsmf["employer"] + unemployment["employer"] + medical["employer"]

        return {
            "employee_id": emp.id,
            "name": emp.full_name,
            "gross_salary": round(gross, 2),
            "net_salary": round(net, 2),
            "employer_cost": round(employer_cost, 2),
            "deductions": {
                "dsmf": round(dsmf["employee"], 2),
                "unemployment": round(unemployment["employee"], 2),
                "income_tax": round(income_tax, 2),
                "total": round(total_deduction, 2)
            }
        }

class VacationCalculator:
    ANNUAL_DAYS = 30

    def calculate_entitled(self, tenure):
        bonus = int(tenure / 5) * 2
        if tenure > 15:
            bonus += 2
        return self.ANNUAL_DAYS + bonus

    def calculate_vacation_pay(self, emp, days):
        entitled = self.calculate_entitled(emp.tenure_years)
        daily = emp.gross_salary / 30
        pay = daily * days
        return {
            "employee_id": emp.id,
            "entitled_days": entitled,
            "requested_days": days,
            "vacation_pay": round(pay, 2),
            "remaining_days": entitled - days,
            "daily_rate": round(daily, 2)
        }

class CompensasiyaCalculator:
    """Kompensasiya Hesablamaları - Gitməyən işçi və ya istifadə edilməyən məzuniyyət"""
    
    def calculate_unused_vacation_compensation(self, emp, unused_days):
        """İstifadə edilməyən məzuniyyət günləri üçün kompensasiya"""
        daily_rate = emp.gross_salary / 30
        compensation = unused_days * daily_rate
        return {
            "employee_id": emp.id,
            "employee_name": emp.full_name,
            "unused_vacation_days": unused_days,
            "daily_rate": round(daily_rate, 2),
            "compensation_amount": round(compensation, 2),
            "calculation_date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def calculate_severance_compensation(self, emp, reason="layoff"):
        """İşdən çıxma kompensasiyası"""
        tenure = emp.tenure_years
        monthly_salary = emp.gross_salary
        
        if reason == "layoff":
            # İşdən çıxarma: Her il üçün 2 ay maaş
            compensation_months = min(tenure * 2, 24)  # Max 24 ay
        elif reason == "resignation":
            # İstefa: Ortalama məzuniyyət pulu qədər
            compensation_months = tenure * 0.5  # Her il için yarım ay
        elif reason == "mutual":
            # Karşılıklı anlaşma: Her il için 1.5 ay
            compensation_months = min(tenure * 1.5, 18)
        else:
            compensation_months = 0
            
        compensation_amount = monthly_salary * compensation_months
        
        return {
            "employee_id": emp.id,
            "employee_name": emp.full_name,
            "tenure_years": round(tenure, 2),
            "reason": reason,
            "compensation_months": round(compensation_months, 2),
            "monthly_salary": monthly_salary,
            "total_compensation": round(compensation_amount, 2),
            "calculation_date": datetime.now().strftime("%Y-%m-%d")
        }

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = {}

    def read_all_sheets(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Fayl tapılmadı: {self.file_path}")
        xls = pd.ExcelFile(self.file_path)
        for sheet in xls.sheet_names:
            try:
                self.data[sheet] = pd.read_excel(xls, sheet_name=sheet)
                logger.info(f"{sheet}: {len(self.data[sheet])} sətir")
            except Exception as e:
                logger.error(f"{sheet} xeta: {e}")
        return self.data

    def parse_employees(self):
        sheet_name = 'İşçi Məlumatları'
        if sheet_name not in self.data:
            logger.error(f"'{sheet_name}' səhifəsi tapılmadı!")
            return []
        df = self.data[sheet_name]
        logger.info(f"Excel sütunları: {df.columns.tolist()}")
        
        employees = []
        # Başlık satırı atla, veri satırlarından başla
        for idx, row in df.iterrows():
            try:
                # İlk satırda ID yoksa atla
                if pd.isna(row.get('ID')) and pd.isna(row.get('id')) and pd.isna(row.iloc[0] if len(row) > 0 else None):
                    continue
                
                # ID'yi al (ID veya id kolonu veya ilk sütun)
                emp_id = row.get('ID') or row.get('id') or row.iloc[0]
                if pd.isna(emp_id):
                    continue
                    
                # Verileri güvenli şekilde al
                first_name = str(row.get('Ad', row.get('ad', '')))
                last_name = str(row.get('Soyad', row.get('soyad', '')))
                fin = str(row.get('FIN', row.get('fin', '')))
                position = str(row.get('Vezifə', row.get('vezifə', row.get('Pozisiya', ''))))
                
                # Tarih parse
                start_date_raw = row.get('İşə Başlama Tarixi', row.get('Başlama Tarixi', row.get('start_date', None)))
                if pd.notna(start_date_raw):
                    try:
                        start_date = pd.to_datetime(start_date_raw)
                    except:
                        start_date = datetime.now()
                else:
                    start_date = datetime.now()
                
                # Maaş
                salary_raw = row.get('Maaş (AZN)', row.get('Maaş', row.get('maas', row.get('salary', 0))))
                gross_salary = float(salary_raw) if pd.notna(salary_raw) else 0
                
                # İş tipi
                emp_type = str(row.get('İş Tipi', row.get('iş tipi', 'müqaviləli')))
                
                # Status
                status_raw = row.get('Status', row.get('status', 'Aktiv'))
                is_active = str(status_raw).lower() in ['aktiv', 'active', 'true', 'evet', 'yes', '1']
                
                emp = Employee(
                    id=int(emp_id),
                    first_name=first_name,
                    last_name=last_name,
                    fin=fin,
                    position=position,
                    start_date=start_date,
                    gross_salary=gross_salary,
                    employment_type=emp_type,
                    is_active=is_active
                )
                employees.append(emp)
                logger.info(f"İşçi yükləndi: {emp.full_name} (ID: {emp.id})")
            except Exception as e:
                logger.error(f"Satır {idx} parse xeta: {e}")
                continue
        return employees

class PayrollSystem:
    def __init__(self, excel_path):
        self.excel = ExcelProcessor(excel_path)
        self.tax_calc = AzerbaijanTaxCalculator()
        self.vac_calc = VacationCalculator()
        self.comp_calc = CompensasiyaCalculator()
        self.employees = []

    def load_data(self):
        self.excel.read_all_sheets()
        self.employees = self.excel.parse_employees()
        logger.info(f"{len(self.employees)} işçi yükləndi")

    def process_payroll(self, working_days=27, actual_map=None):
        if not self.employees:
            self.load_data()
        results = []
        for emp in self.employees:
            if not emp.is_active:
                continue
            actual = actual_map.get(emp.id, working_days) if actual_map else working_days
            payroll = self.tax_calc.calculate_monthly(emp, working_days, actual)
            results.append(payroll)
        return results

    def export_json(self, data, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"JSON saxlanıldı: {output_path}")
    
    def calculate_all_vacations(self):
        """Bütün işçilər üçün məzuniyyət hesablaması"""
        if not self.employees:
            self.load_data()
        results = []
        for emp in self.employees:
            if not emp.is_active:
                continue
            entitled = self.vac_calc.calculate_entitled(emp.tenure_years)
            vacation_info = {
                "employee_id": emp.id,
                "employee_name": emp.full_name,
                "tenure_years": round(emp.tenure_years, 2),
                "entitled_vacation_days": entitled,
                "gross_salary": emp.gross_salary,
                "daily_rate": round(emp.gross_salary / 30, 2)
            }
            results.append(vacation_info)
        return results
    
    def calculate_all_compensations(self, unused_days_map=None, reason_map=None):
        """Bütün işçilər üçün kompensasiya hesablaması"""
        if not self.employees:
            self.load_data()
        results = []
        for emp in self.employees:
            if not emp.is_active:
                continue
            # Varsayılan: işdən çıxarma (layoff)
            reason = reason_map.get(emp.id, "layoff") if reason_map else "layoff"
            severance = self.comp_calc.calculate_severance_compensation(emp, reason)
            
            # İstifadə edilməyən məzuniyyət
            unused_days = unused_days_map.get(emp.id, 0) if unused_days_map else 0
            vac_comp = None
            if unused_days > 0:
                vac_comp = self.comp_calc.calculate_unused_vacation_compensation(emp, unused_days)
            
            results.append({
                "severance": severance,
                "unused_vacation": vac_comp,
                "total_compensation": round(severance["total_compensation"] + (vac_comp["compensation_amount"] if vac_comp else 0), 2)
            })
        return results

def main():
    import sys
    if len(sys.argv) < 2:
        print("İstifadə: python payroll_calculator.py <excel_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    system = PayrollSystem(input_file)
    system.load_data()

    # Maaş hesablatması
    payroll = system.process_payroll(working_days=27, actual_map=None)

    # JSON export
    system.export_json(payroll, "payroll_output.json")
    print(f"✅ {len(payroll)} işçi üçün hesablama tamamlandı")

if __name__ == "__main__":
    main()
