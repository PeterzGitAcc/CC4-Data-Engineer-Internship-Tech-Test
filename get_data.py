import requests
restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"

def retrieve_data(data_url):
    response = requests.get(data_url)
    if response.ok:
        response_data = response.json()
    else:
        return "An error has occured"
    
    return response_data

if __name__ == "__main__":
    retrieve_data(restaurant_data_url) 