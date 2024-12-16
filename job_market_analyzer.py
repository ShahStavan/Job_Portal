from typing import Dict, List, Any
from collections import Counter
from statistics import mean
from data_processor import JobDataProcessor

class JobMarketAnalyzer:
    def __init__(self):
        self.data_processor = JobDataProcessor()
        self.jobs = self.data_processor.all_jobs

    def get_job_statistics(self, keyword: str) -> Dict[str, Any]:
        matching_jobs = self._filter_jobs_by_keyword(keyword)
        
        salaries = []
        locations = []
        companies = []
        
        for job in matching_jobs:
            if 'pay_median_glassdoor' in job:
                salaries.append(job['pay_median_glassdoor'])
            if 'job_location' in job:
                locations.append(job['job_location'])
            if 'company_name' in job:
                companies.append(job['company_name'])

        return {
            'total_jobs': len(matching_jobs),
            'avg_salary': mean(salaries) if salaries else 0,
            'salary_range': (min(salaries), max(salaries)) if salaries else (0, 0),
            'top_locations': Counter(locations).most_common(5),
            'top_companies': Counter(companies).most_common(5)
        }

    def get_common_benefits(self, keyword: str) -> List[str]:
        matching_jobs = self._filter_jobs_by_keyword(keyword)
        
        all_benefits = []
        for job in matching_jobs:
            if 'employee_benefit_reviews' in job:
                all_benefits.extend(job['employee_benefit_reviews'])
        
        return Counter(all_benefits).most_common(10)

    def get_trending_titles(self, keyword: str) -> List[str]:
        matching_jobs = self._filter_jobs_by_keyword(keyword)
        
        titles = [job.get('job_title', '') for job in matching_jobs]
        return Counter(titles).most_common(10)

    def get_location_statistics(self, location: str) -> Dict[str, Any]:
        """Get statistics for jobs in a specific location"""
        matching_jobs = self._filter_jobs_by_location(location)
        
        salaries = []
        companies = []
        titles = []
        
        for job in matching_jobs:
            if 'pay_median_glassdoor' in job:
                salaries.append(job['pay_median_glassdoor'])
            if 'company_name' in job:
                companies.append(job['company_name'])
            if 'job_title' in job:
                titles.append(job['job_title'])

        return {
            'total_jobs': len(matching_jobs),
            'avg_salary': mean(salaries) if salaries else 0,
            'salary_range': (min(salaries), max(salaries)) if salaries else (0, 0),
            'top_companies': Counter(companies).most_common(5),
            'top_titles': Counter(titles).most_common(5)
        }

    def _filter_jobs_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Filter jobs based on keyword in title or description"""
        keyword = keyword.lower()
        return [
            job for job in self.jobs
            if keyword in job.get('job_title', '').lower() or 
               keyword in job.get('job_overview', '').lower()
        ]

    def _filter_jobs_by_location(self, location: str) -> List[Dict[str, Any]]:
        """Filter jobs based on location"""
        location = location.lower()
        return [
            job for job in self.jobs
            if location in job.get('job_location', '').lower() or
               location in job.get('discovery_input', {}).get('location', '').lower()
        ]
