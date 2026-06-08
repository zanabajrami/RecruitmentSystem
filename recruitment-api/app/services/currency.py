import httpx
from typing import Optional, Dict
import re

class CurrencyService:
    # Third-party API URL to fetch real-time exchange rates based on EUR
    API_URL = "https://open.er-api.com/v6/latest/EUR"

    @staticmethod
    async def get_exchange_rates() -> Optional[Dict[str, float]]:
        """
        Asynchronously fetches live exchange rates from the external API.
        Returns a dictionary of rates or None if the request fails.
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(CurrencyService.API_URL)
                if response.status_code == 200:
                    return response.json().get("rates", {})
                return None
        except Exception:
            return None

    @staticmethod
    def clean_and_convert_salary(salary_str: Optional[str], rates: Optional[Dict[str, float]]) -> Dict[str, str]:
        """
        Parses, cleans, and converts a salary string (single value or range) 
        into multiple dynamically converted currencies (USD, ALL) based on EUR.
        """
        # Initialize default responses
        result = {
            "EUR": salary_str if salary_str else "N/A", 
            "USD": "N/A", 
            "ALL": "N/A"
        }
        
        # Guard clause if no input or rates are provided
        if not salary_str or not rates:
            return result

        # Remove alphabetic characters and whitespace using regex, keeping numbers and dashes
        clean_str = re.sub(r'[a-zA-Z\s]+', '', salary_str).strip()
        if not clean_str:
            return result

        try:
            # Handle salary ranges (e.g., "2500-3000")
            if "-" in clean_str:
                parts = clean_str.split("-")
                min_salary = float(parts[0].strip())
                max_salary = float(parts[1].strip())

                if "USD" in rates:
                    usd_min = min_salary * rates['USD']
                    usd_max = max_salary * rates['USD']
                    result["USD"] = f"{usd_min:.2f}-{usd_max:.2f}"
                    
                if "ALL" in rates:
                    all_min = min_salary * rates['ALL']
                    all_max = max_salary * rates['ALL']
                    result["ALL"] = f"{all_min:.2f}-{all_max:.2f}"

            # Handle single salary values (e.g., "2500")
            else:
                base_salary = float(clean_str)
                if "USD" in rates:
                    result["USD"] = f"{base_salary * rates['USD']:.2f}"
                if "ALL" in rates:
                    result["ALL"] = f"{base_salary * rates['ALL']:.2f}"
                    
        except ValueError:
            # Fallback gracefully if float conversion fails
            pass

        return result