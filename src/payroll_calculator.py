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
        if 'İşçi Məlumatları' not in self.data:
            return []
        df = self.data['İşçi Məlumatları']
        employees = []
        for _, row in df.iloc[2:].iterrows():
            try:
                if pd.isna(row[1]):
                    continue
                emp = Employee(
                    id=int(row[1]),
                    first_name=str(row[2]) if pd.notna(row[2]) else "",
                    last_name=str(row[3]) if pd.notna(row[3]) else "",
                    fin=str(row[4]) if pd.notna(row[4]) else "",
                    position=str(row[5]) if pd.notna(row[5]) else "",
                    start_date=pd.to_datetime(row[6]) if pd.notna(row[6]) else datetime.now(),
                    gross_salary=float(row[7]) if pd.notna(row[7]) else 0,
                    employment_type=str(row[8]) if pd.notna(row[8]) else "müqaviləli",
                    is_active=str(row[10]).lower() == 'aktiv' if pd.notna(row[10]) else True
                )
                employees.append(emp)
            except Exception as e:
                logger.error(f"Satır parse xeta: {e}")
        return employees

class PayrollSystem:
    def __init__(self, excel_path):
        self.excel = ExcelProcessor(excel_path)
        self.tax_calc = AzerbaijanTaxCalculator()
        self.vac_calc = VacationCalculator()
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
