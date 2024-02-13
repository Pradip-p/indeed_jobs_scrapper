import requests

def get_logo_url(company_name):
    
    api_url = f'https://autocomplete.clearbit.com/v1/companies/suggest?query={company_name}'
    
    try:
        response = requests.get(api_url)
        if response.ok:
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list) and 'logo' in data[0]:
                return data[0]['logo']
            else:
                return None
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching logo URL: {e}")
        return None

