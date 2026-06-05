import httpx
from typing import Optional, Dict
import re

class CurrencyService:
    API_URL = "https://open.er-api.com/v6/latest/EUR"

    @staticmethod
    async def get_exchange_rates() -> Optional[Dict[str, float]]:
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
        result = {
            "EUR": salary_str if salary_str else "N/A", 
            "USD": "N/A", 
            "ALL": "N/A"
        }
        
        if not salary_str or not rates:
            return result

        clean_str = re.sub(r'[a-zA-Z\s]+', '', salary_str).strip()
        if not clean_str:
            return result

        try:
            if "-" in clean_str:
                parts = clean_str.split("-")
                min_salary = float(parts[0].strip())
                max_salary = float(parts[1].strip())

                if "USD" in rates:
                    usd_min = round(min_salary * rates['USD'])
                    usd_max = round(max_salary * rates['USD'])
                    result["USD"] = f"{usd_min}-{usd_max} USD"
                    
                if "ALL" in rates:
                    all_min = round(min_salary * rates['ALL'])
                    all_max = round(max_salary * rates['ALL'])
                    result["ALL"] = f"{all_min}-{all_max} ALL"

            else:
                base_salary = float(clean_str)
                if "USD" in rates:
                    result["USD"] = f"{round(base_salary * rates['USD'], 2)} USD"
                if "ALL" in rates:
                    result["ALL"] = f"{round(base_salary * rates['ALL'], 2)} ALL"
                    
        except ValueError:
            pass

        return result