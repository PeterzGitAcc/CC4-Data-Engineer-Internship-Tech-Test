import requests

def retrieve_data(data_url):
    response = requests.get(data_url)
    if response.ok:
        response_data = response.json()
    else:
        return "An error has occured"

    return response_data


def retrieve_all_restaurants_data(restaurant_data):
    ret_data = []
    # loop through array of results
    for res in restaurant_data:
        for restaurant in res['restaurants']:
            ret_data.append(restaurant)
    return ret_data


restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
restaurant_data = retrieve_data(restaurant_data_url)
all_restaurant_data = retrieve_all_restaurants_data(restaurant_data)

if __name__ == "__main__":
    pass
