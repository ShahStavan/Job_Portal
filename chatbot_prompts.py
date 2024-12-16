from data_processor import JobDataProcessor
from data_transformer import DataTransformer
from prompts import DESCRIPTION_PROMPTS, SYSTEM_PROMPT
from typing import Dict, Any, List

class ChatbotPromptManager:
    def __init__(self):
        self.data_processor = JobDataProcessor()
        self.transformer = DataTransformer()
        self.current_keyword = None  # Add this line
    
    def get_job_summary_prompt(self, company_name: str) -> str:
        if not self.data_processor.set_company(company_name):
            return f"No data found for company: {company_name}"
            
        job_data = self.data_processor.get_job_summary()
        formatted_data = self.transformer.format_job_summary(job_data)
        
        return f"{SYSTEM_PROMPT}\n\n{formatted_data}"
    
    def get_company_analysis_prompt(self, company_name: str) -> str:
        company_data = self.data_processor.get_company_info()
        return DESCRIPTION_PROMPTS["company_analysis"].format(
            company_name=company_name,
            company_rating=company_data['rating'],
            culture_rating=company_data['culture_rating'],
            balance_rating=company_data['balance_rating'],
            career_rating=company_data['career_rating']
        )
    
    def get_benefits_analysis_prompt(self, company_name: str) -> str:
        benefits_data = self.data_processor.get_benefits_info()
        return DESCRIPTION_PROMPTS["benefits_analysis"].format(
            company_name=company_name,
            benefits_rating=benefits_data['rating']
        )

    def get_stats_analysis_prompt(self, stats: Dict[str, Any], keyword: str) -> str:
        self.current_keyword = keyword  # Set current keyword
        locations = "\n".join([f"- {loc}: {count} jobs" for loc, count in stats['top_locations']])
        companies = "\n".join([f"- {comp}: {count} positions" for comp, count in stats['top_companies']])
        
        return DESCRIPTION_PROMPTS["job_stats_analysis"].format(
            keyword=self.current_keyword,
            total_jobs=stats['total_jobs'],
            avg_salary=stats['avg_salary'],
            min_salary=stats['salary_range'][0],
            max_salary=stats['salary_range'][1],
            locations=locations,
            companies=companies
        )

    def get_benefits_trends_prompt(self, benefits: List[tuple], keyword: str) -> str:
        self.current_keyword = keyword  # Set current keyword
        benefits_text = "\n".join([f"- {benefit}: {count} mentions" for benefit, count in benefits])
        
        return DESCRIPTION_PROMPTS["benefits_trends"].format(
            keyword=self.current_keyword,
            benefits=benefits_text
        )

    def get_titles_analysis_prompt(self, titles: List[tuple], keyword: str) -> str:
        self.current_keyword = keyword  # Set current keyword
        titles_text = "\n".join([f"- {title}: {count} positions" for title, count in titles])
        
        return DESCRIPTION_PROMPTS["title_trends"].format(
            keyword=self.current_keyword,
            titles=titles_text
        )

    def get_location_analysis_prompt(self, stats: Dict[str, Any], location: str) -> str:
        """Generate prompt for location-based analysis"""
        companies = "\n".join([f"- {comp}: {count} positions" for comp, count in stats['top_companies']])
        titles = "\n".join([f"- {title}: {count} openings" for title, count in stats['top_titles']])
        
        return DESCRIPTION_PROMPTS["location_analysis"].format(
            location=location,
            total_jobs=stats['total_jobs'],
            avg_salary=stats['avg_salary'],
            min_salary=stats['salary_range'][0],
            max_salary=stats['salary_range'][1],
            companies=companies,
            titles=titles
        )
