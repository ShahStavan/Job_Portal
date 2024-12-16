from typing import Dict, Any

class DataTransformer:
    @staticmethod
    def format_job_summary(data: Dict[str, Any]) -> str:
        return (
            f"Job Title: {data.get('job_title', 'N/A')}\n"
            f"Company: {data.get('company_name', 'N/A')}\n"
            f"Location: {data.get('location', 'N/A')}\n\n"
            f"Overview:\n{data.get('overview', 'No overview available')}"
        )

    @staticmethod
    def format_company_analysis(data: Dict[str, Any]) -> str:
        return (
            f"Company: {data.get('name', 'N/A')}\n"
            f"Overall Rating: {data.get('rating', 'N/A')}\n"
            f"Culture Rating: {data.get('culture_rating', 'N/A')}\n"
            f"Work/Life Balance: {data.get('balance_rating', 'N/A')}\n"
            f"Career Opportunities: {data.get('career_rating', 'N/A')}"
        )

    @staticmethod
    def format_benefits_info(data: Dict[str, Any]) -> str:
        reviews = data.get('reviews', [])
        if not reviews:
            reviews_text = "No reviews available"
        else:
            reviews_text = '\n- '.join(reviews)
        
        return (
            f"Benefits Rating: {data.get('rating', 'N/A')}\n"
            f"Pay Range: {data.get('pay_range', 'Not available')}\n\n"
            f"Benefits Summary:\n{data.get('summary', 'No summary available')}\n\n"
            f"Employee Reviews:\n- {reviews_text}"
        )
