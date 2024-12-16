DESCRIPTION_PROMPTS = {
    "job_summary": """Summarize the job posting for {job_title} at {company_name}. Include key responsibilities and requirements.""",
    "company_analysis": """Analyze {company_name} based on the following metrics:
    - Company Rating: {company_rating}
    - Culture and Values: {culture_rating}
    - Work/Life Balance: {balance_rating}
    - Career Opportunities: {career_rating}""",
    
    "benefits_analysis": """Analyze the benefits package at {company_name} including:
    - Benefits Rating: {benefits_rating}
    - Employee Reviews
    - Compensation Range""",
    
    "culture_insights": """Provide insights about the company culture at {company_name} based on:
    - Pros mentioned by employees
    - Cons mentioned by employees
    - Overall recommendations""",
    
    "job_stats_analysis": """Analyze the job market statistics for keyword '{keyword}':
    Total Jobs: {total_jobs}
    Average Salary: ${avg_salary:,.2f}
    Salary Range: ${min_salary:,.2f} - ${max_salary:,.2f}
    
    Top Locations:
    {locations}
    
    Top Companies Hiring:
    {companies}
    """,
    
    "benefits_trends": """Analyze the most common benefits offered for {keyword} positions:
    
    {benefits}
    
    What makes these benefits stand out and how do they compare to industry standards?
    """,
    
    "title_trends": """Analyze the trending job titles related to {keyword}:
    
    {titles}
    
    What do these titles indicate about current industry trends and skill requirements?
    """,
    
    "location_analysis": """Analyze job opportunities in {location}:

    Total Jobs Available: {total_jobs}
    Average Salary: ${avg_salary:,.2f}
    Salary Range: ${min_salary:,.2f} - ${max_salary:,.2f}

    Top Companies Hiring:
    {companies}

    Most Common Job Titles:
    {titles}

    What insights can be drawn about the job market in {location}?
    """
}

SYSTEM_PROMPT = """You are a job portal assistant helping users understand job opportunities.
Be concise and factual in your responses."""