import requests
import pandas as pd

def retrieve_data(data_url):
    response = requests.get(data_url)
    if response.ok:
        response_data = response.json()
    else:
        return "An error has occured"

    return response_data


def retrieve_all_restaurants_data(restaurant_data):
    ret_data = []
    for res in restaurant_data:
        for restaurant in res['restaurants']:
            ret_data.append(restaurant['restaurant'])
    return ret_data

def retrieve_country_data():
        # import country data
    try:
        country_data_df = pd.read_excel('./data/Country-Code.xlsx', engine='openpyxl')
        return country_data_df
    except:
        print("Excel file cannot be read !")

restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
restaurant_data = retrieve_data(restaurant_data_url)
all_restaurant_data = retrieve_all_restaurants_data(restaurant_data)
country_data_df = retrieve_country_data()

if __name__ == "__main__":
    print("Running module directly!")


