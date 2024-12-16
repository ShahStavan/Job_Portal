from typing import Dict, Any, List
import json
from pathlib import Path

class JobDataProcessor:
    def __init__(self, data_path: str = 'data.json'):
        self.data_path = data_path
        self.all_jobs = []
        self.current_company_data = None
        self._load_data()
    
    def _load_data(self) -> None:
        try:
            if not Path(self.data_path).exists():
                print(f"Data file {self.data_path} not found!")
                self.all_jobs = []
                return

            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.all_jobs = json.load(f)
                if not isinstance(self.all_jobs, list):
                    self.all_jobs = [self.all_jobs]
        except Exception as e:
            print(f"Error loading data: {e}")
            self.all_jobs = []

    def set_company(self, company_name: str) -> bool:
        """Find and set the current company data"""
        for job in self.all_jobs:
            if job.get('company_name', '').lower() == company_name.lower():
                self.current_company_data = job
                return True
        return False

    def _safe_get(self, key: str, default: Any = "Not available") -> Any:
        """Safely get a value from current company data with a default fallback"""
        if self.current_company_data is None:
            return default
        return self.current_company_data.get(key, default)
    
    def get_job_summary(self) -> Dict[str, Any]:
        return {
            'job_title': self._safe_get('job_title'),
            'company_name': self._safe_get('company_name'),
            'location': self._safe_get('job_location'),
            'overview': self._safe_get('job_overview', "No overview available")
        }
    
    def get_company_info(self) -> Dict[str, Any]:
        return {
            'name': self._safe_get('company_name'),
            'rating': self._safe_get('company_rating', 0.0),
            'culture_rating': self._safe_get('company_culture_and_values_rating', 0.0),
            'balance_rating': self._safe_get('company_work/life_balance_rating', 0.0),
            'career_rating': self._safe_get('company_career_opportunities_rating', 0.0)
        }
    
    def get_benefits_info(self) -> Dict[str, Any]:
        return {
            'rating': self._safe_get('company_benefits_rating', 0.0),
            'summary': self._safe_get('company_benefits_employer_summary', "No benefits summary available"),
            'reviews': self._safe_get('employee_benefit_reviews', []),
            'pay_range': self._safe_get('pay_range_glassdoor_est', "Salary range not available")
        }

    def get_company_name(self) -> str:
        return self._safe_get('company_name', 'Unknown Company')
