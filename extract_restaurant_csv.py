import requests
import pandas as pd
#initialize global values 
restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
restaurant_data_fields = ["id",'name','location','user_rating','cuisines']
to_remove = ['location','user_rating']
country_data_df = pd.read_excel('./Country-Code.xlsx')


#functions
def retrieve_data(data_url):
    response = requests.get(data_url)
    if response.ok:
        response_data = response.json()
    else:
        return "An error has occured"
    
    return response_data


restaurant_data = retrieve_data(restaurant_data_url)

def retrieve_country_from_id(*country_id):   
    if len(country_id) != 0:
        country_row = country_data_df.loc[country_data_df['Country Code'] == country_id]
        country = country_row['Country'].to_string(index = False)
        return country
    # country = country_row['Country'].iloc[0]
    # return country
    # except:
    #     print("No excel file / data found !")

def format_data_for_csv(single_restaurant_data):
    single_restaurant_data['city'] = single_restaurant_data['location']['city']
    single_restaurant_data['country'] = retrieve_country_from_id(single_restaurant_data['location']['country_id'])
    single_restaurant_data['votes'] = single_restaurant_data['user_rating']['votes']
    single_restaurant_data['aggregate_rating'] = single_restaurant_data['user_rating']['aggregate_rating']
    single_restaurant_data ={ key:value for (key,value) in single_restaurant_data.items() if key not in to_remove}
    return single_restaurant_data



#Test case: if data dict or list (retrieve specific dictionary)
def retrieve_all_only_restaurant_data(list_data_object):
    #store only restaurant objs
    restaurants_all = []
    ret_data = []
    #loop through array of results 
    for res in list_data_object:
        for restaurants in res['restaurants']:
            restaurant_data ={ key:value for (key,value) in restaurants['restaurant'].items() if key in restaurant_data_fields}
            restaurants_all.append(restaurant_data)
    for res_data in restaurants_all:
        ret_data.append(format_data_for_csv(res_data))

    return ret_data

restaurant_data_final = retrieve_all_only_restaurant_data(restaurant_data)


def extract_to_csv(restautant_data):
    try:
        df = pd.DataFrame(restautant_data)
        df.to_csv("restaurants.csv")

    except:
        print("cannot write to file!")


extract_to_csv(restaurant_data_final)
