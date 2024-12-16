import streamlit as st
import asyncio
from typing import Dict, Any
import google.generativeai as genai
from llm_config import Config
from chatbot_prompts import ChatbotPromptManager
from data_processor import JobDataProcessor
from job_market_analyzer import JobMarketAnalyzer
from pathlib import Path
from data_collection import collect_data

class StreamlitJobPortal:
    def __init__(self):
        self._initialize_session_state()
        self._initialize_components()
        
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'current_company' not in st.session_state:
            st.session_state.current_company = None
        if 'current_keyword' not in st.session_state:
            st.session_state.current_keyword = None
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None

    def _initialize_components(self):
        """Initialize all required components"""
        # Check if data exists
        if not Path('data.json').exists():
            st.warning("Data file not found. Collecting data...")
            collect_data()

        # Initialize configuration and components
        try:
            self.config = Config()
            genai.configure(api_key=self.config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=self.config.MODEL_NAME,
                generation_config=self.config.GEMINI_CONFIG
            )
            self.prompt_manager = ChatbotPromptManager()
            self.data_processor = JobDataProcessor()
            self.job_analyzer = JobMarketAnalyzer()
        except Exception as e:
            st.error(f"Error initializing components: {str(e)}")
            raise

    async def get_llm_response(self, prompt: str) -> str:
        """Get response from LLM"""
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def show_job_market_analysis(self, keyword: str):
        """Display job market analysis results"""
        stats = self.job_analyzer.get_job_statistics(keyword)
        benefits = self.job_analyzer.get_common_benefits(keyword)
        titles = self.job_analyzer.get_trending_titles(keyword)

        # Display statistics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Market Statistics")
            st.metric("Total Jobs", stats['total_jobs'])
            st.metric("Average Salary", f"${stats['avg_salary']:,.2f}")
            st.metric("Salary Range", f"${stats['salary_range'][0]:,.2f} - ${stats['salary_range'][1]:,.2f}")

        with col2:
            st.subheader("Top Locations")
            for loc, count in stats['top_locations']:
                st.write(f"• {loc}: {count} jobs")

        # Display trending titles
        st.subheader("Trending Job Titles")
        for title, count in titles:
            st.write(f"• {title}: {count} positions")

        # Display benefits
        st.subheader("Common Benefits")
        for benefit, count in benefits:
            st.write(f"• {benefit}: {count} mentions")

    def show_company_analysis(self, company_name: str):
        """Display company analysis results"""
        if self.data_processor.set_company(company_name):
            company_info = self.data_processor.get_company_info()
            benefits_info = self.data_processor.get_benefits_info()
            job_summary = self.data_processor.get_job_summary()

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Company Ratings")
                st.metric("Overall Rating", f"{company_info['rating']:.1f}/5.0")
                st.metric("Culture Rating", f"{company_info['culture_rating']:.1f}/5.0")
                st.metric("Work/Life Balance", f"{company_info['balance_rating']:.1f}/5.0")
                st.metric("Career Opportunities", f"{company_info['career_rating']:.1f}/5.0")

            with col2:
                st.subheader("Benefits & Compensation")
                st.metric("Benefits Rating", f"{benefits_info['rating']:.1f}/5.0")
                st.write("**Pay Range:**", benefits_info['pay_range'])
                st.write("**Benefits Summary:**", benefits_info['summary'])

            # Job details
            st.subheader("Current Job Opening")
            st.write("**Title:**", job_summary['job_title'])
            st.write("**Location:**", job_summary['location'])
            with st.expander("Job Overview"):
                st.write(job_summary['overview'])

        else:
            st.error(f"No data found for company: {company_name}")

    def main(self):
        """Main Streamlit interface"""
        st.title("Job Portal Assistant")
        st.write("Explore job market trends and company insights")

        # Sidebar navigation
        analysis_type = st.sidebar.radio(
            "Choose Analysis Type",
            ["Job Market Analysis", "Company Analysis", "Location Analysis"]  # Add location option
        )

        if analysis_type == "Location Analysis":
            st.header("Location Analysis")
            location = st.text_input("Enter location (e.g. 'India')")
            if location:
                self.show_location_analysis(location)

        elif analysis_type == "Job Market Analysis":
            st.header("Job Market Analysis")
            keyword = st.text_input("Enter job keyword (e.g., 'software developer')")
            if keyword:
                self.show_job_market_analysis(keyword)

        else:  # Company Analysis
            st.header("Company Analysis")
            company_name = st.text_input("Enter company name")
            if company_name:
                self.show_company_analysis(company_name)

        # Additional information
        with st.sidebar:
            st.markdown("---")
            st.markdown("### About")
            st.write("This tool helps analyze job market trends and company insights using real-time data.")

    def show_location_analysis(self, location: str):
        """Display location-based analysis"""
        stats = self.job_analyzer.get_location_statistics(location)
        
        if stats['total_jobs'] == 0:
            st.error(f"No jobs found in {location}")
            return

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Market Statistics")
            st.metric("Total Jobs", stats['total_jobs'])
            st.metric("Average Salary", f"${stats['avg_salary']:,.2f}")
            st.metric("Salary Range", f"${stats['salary_range'][0]:,.2f} - ${stats['salary_range'][1]:,.2f}")

        with col2:
            st.subheader("Top Companies")
            for company, count in stats['top_companies']:
                st.write(f"• {company}: {count} positions")

        st.subheader("Common Job Titles")
        for title, count in stats['top_titles']:
            st.write(f"• {title}: {count} openings")

def run_async_app():
    """Run the Streamlit app with async support"""
    portal = StreamlitJobPortal()
    portal.main()

if __name__ == "__main__":
    run_async_app()
