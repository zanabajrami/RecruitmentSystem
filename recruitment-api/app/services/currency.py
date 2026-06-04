import httpx
from typing import Optional, Dict

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
        result = {"EUR": salary_str if salary_str else "N/A", "USD": "N/A", "ALL": "N/A"}
        if not salary_str or not rates:
            return result

        digits = "".join([c for c in salary_str if c.isdigit() or c == '.'])
        if not digits:
            return result
            
        try:
            base_salary = float(digits)
            if "USD" in rates:
                result["USD"] = f"{round(base_salary * rates['USD'], 2)} USD"
            if "ALL" in rates:
                result["ALL"] = f"{round(base_salary * rates['ALL'], 2)} ALL"
        except ValueError:
            pass

        return result