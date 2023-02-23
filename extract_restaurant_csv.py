import pandas as pd
from get_data import retrieve_data , restaurant_data_url

#initialize global values 
restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
restaurant_data_fields = ["id",'name','location','user_rating','cuisines']
to_remove = ['location','user_rating']

#import country data
try:
    country_data_df = pd.read_excel('./Country-Code.xlsx')
except:
    print("Excel file cannot be read !")

#functions


restaurant_data = retrieve_data(restaurant_data_url)

def retrieve_country_from_id(country_id):   
    try:
        country_row = country_data_df.loc[country_data_df['Country Code'] == country_id]
        country = country_row['Country'].to_string(index = False)
        return country
    except:
        print("No country data found!")
def retrieve_user_rating(single_restaurant_user_rating):
    ret_dic ={}
    ret_dic['votes'] = single_restaurant_user_rating['votes']
    ret_dic['aggregate_rating']  = single_restaurant_user_rating['aggregate_rating']
    return ret_dic
def format_data_for_csv(single_restaurant_data):
    single_restaurant_data['city'] = single_restaurant_data['location']['city']
    single_restaurant_data['country'] = retrieve_country_from_id(single_restaurant_data['location']['country_id'])
    single_restaurant_data = single_restaurant_data | retrieve_user_rating(single_restaurant_data['user_rating'])
    single_restaurant_data ={ key:value for (key,value) in single_restaurant_data.items() if key not in to_remove}
    return single_restaurant_data



#Test case: if data dict or list (retrieve specific dictionary)
def retrieve_all_only_restaurant_data(list_data_object):
    #store only restaurant objs
    restaurants_all = []
    #loop through array of results 
    for res in list_data_object:
        for restaurants in res['restaurants']:
            restaurant_data ={ key:value for (key,value) in restaurants['restaurant'].items() if key in restaurant_data_fields}
            restaurants_all.append(format_data_for_csv(restaurant_data))

    return restaurants_all

restaurant_data_final = retrieve_all_only_restaurant_data(restaurant_data)


def extract_to_csv(restautant_data):
    try:
        df = pd.DataFrame(restautant_data)
        df.to_csv("restaurants.csv")

    except:
        print("cannot write to file!")


extract_to_csv(restaurant_data_final)
