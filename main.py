import google.generativeai as genai
from llm_config import Config
from chatbot_prompts import ChatbotPromptManager
from typing import Dict, Any
import sys
from pathlib import Path
from data_collection import collect_data  # Add this import
from data_processor import JobDataProcessor  # Add this import
from job_market_analyzer import JobMarketAnalyzer  # Add this import

class JobPortalChatbot:
    def __init__(self):
        # Check if data exists
        if not Path('data.json').exists():
            print("Data file not found. Collecting data...")
            collect_data()
            
        # Initialize configuration
        try:
            self.config = Config()
            self.config_data = Config.get_config()
        except ValueError as e:
            print(f"Configuration error: {str(e)}")
            raise
        
        try:
            # Initialize LLM
            genai.configure(api_key=self.config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=self.config.MODEL_NAME,
                generation_config=self.config.GEMINI_CONFIG
            )
            
            # Initialize prompt manager
            self.prompt_manager = ChatbotPromptManager()
            self.data_processor = JobDataProcessor()  # Add this line
            self.job_analyzer = JobMarketAnalyzer()  # Add this line
        except Exception as e:
            print(f"Error initializing chatbot: {str(e)}")
            raise

        self.current_company = None

    async def get_llm_response(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def display_menu(self) -> None:
        print("\n=== Job Portal Assistant ===")
        print("1. Analyze Job Market") # Add this option
        print("2. Get Job Summary")
        print("3. Company Analysis")
        print("4. Benefits Information")
        print("5. Exit")
        print("========================")

    async def handle_choice(self, choice: str) -> bool:
        if choice == "1":
            keyword = input("Enter job keyword to analyze (e.g. 'software developer'): ")
            await self.analyze_job_market(keyword)
            return True
        if not self.current_company:
            print("Please select a company first.")
            return True

        if choice == "2":
            prompt = self.prompt_manager.get_job_summary_prompt(self.current_company)
            response = await self.get_llm_response(prompt)
            print("\nJob Summary:")
            print(response)
        
        elif choice == "3":
            prompt = self.prompt_manager.get_company_analysis_prompt(self.current_company)
            response = await self.get_llm_response(prompt)
            print("\nCompany Analysis:")
            print(response)
        
        elif choice == "4":
            prompt = self.prompt_manager.get_benefits_analysis_prompt(self.current_company)
            response = await self.get_llm_response(prompt)
            print("\nBenefits Analysis:")
            print(response)
        
        elif choice == "5":
            print("Thank you for using Job Portal Assistant!")
            return False
        
        else:
            print("Invalid choice. Please try again.")
        
        return True

    async def analyze_job_market(self, keyword: str) -> None:
        stats = self.job_analyzer.get_job_statistics(keyword)
        benefits = self.job_analyzer.get_common_benefits(keyword) 
        titles = self.job_analyzer.get_trending_titles(keyword)

        prompts = [
            self.prompt_manager.get_stats_analysis_prompt(stats, keyword),
            self.prompt_manager.get_benefits_trends_prompt(benefits, keyword),
            self.prompt_manager.get_titles_analysis_prompt(titles, keyword)
        ]

        print("\nAnalyzing job market data...\n")
        
        for prompt in prompts:
            response = await self.get_llm_response(prompt)
            print(response)
            print("-" * 80)

    async def run(self) -> None:
        print("Welcome to Job Portal Assistant!")
        
        while True:
            company_name = input("Enter the company name (or 'exit' to quit): ")
            if company_name.lower() == 'exit':
                break

            if self.data_processor.set_company(company_name):
                self.current_company = company_name
                print(f"\nFound data for {company_name}!")
                await self.show_company_menu()
            else:
                print(f"\nNo data found for company: {company_name}")
                continue

    async def show_company_menu(self) -> None:
        running = True
        while running:
            self.display_menu()
            choice = input("Enter your choice (1-5): ")
            running = await self.handle_choice(choice)

async def main():
    try:
        chatbot = JobPortalChatbot()
        await chatbot.run()
    except KeyboardInterrupt:
        print("\nExiting Job Portal Assistant...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
