import pandas as pd
from data.get_data import all_restaurant_data

# import country data
try:
    country_data_df = pd.read_excel('./data/Country-Code.xlsx')
except:
    print("Excel file cannot be read !")


def retrieve_country_from_id(country_id):
    try:
        country_row = country_data_df.loc[country_data_df['Country Code'] == country_id]
        country = country_row['Country'].to_string(index=False)
        return country
    except:
        print("No country data found!")


def retrieve_user_rating(single_restaurant_user_rating):
    ret_dic = {}
    ret_dic['votes'] = single_restaurant_user_rating['votes']
    ret_dic['aggregate_rating'] = single_restaurant_user_rating['aggregate_rating']
    return ret_dic


def format_data_for_csv(single_restaurant_data,to_remove):
    single_restaurant_data['city'] = single_restaurant_data['location']['city']
    single_restaurant_data['country'] = retrieve_country_from_id(
        single_restaurant_data['location']['country_id'])
    single_restaurant_data = single_restaurant_data | retrieve_user_rating(
        single_restaurant_data['user_rating'])
    single_restaurant_data = {key: value for (
        key, value) in single_restaurant_data.items() if key not in to_remove}
    return single_restaurant_data


# Test case: if data dict or list (retrieve specific dictionary)

def retrieve_specific_restaurant_data(all_restaurants_data,restaurant_data_fields,to_remove):
    # store only restaurant objs
    restaurants_all = []
    # loop through array of results
    for res in all_restaurants_data:
        restaurant_data = {key: value for (
            key, value) in res['restaurant'].items() if key in restaurant_data_fields}
        restaurants_all.append(format_data_for_csv(restaurant_data,to_remove))

    return restaurants_all


def extract_to_csv(restautant_data):
    try:
        df = pd.DataFrame(restautant_data)
        df.fillna('NA', inplace=True)
        df.to_csv("./csv_output/restaurants.csv",index=False)

    except:
        print("cannot write to file!")

restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
restaurant_data_fields = ["id", 'name', 'location', 'user_rating', 'cuisines']
to_remove = ['location', 'user_rating']
restaurant_data_final = retrieve_specific_restaurant_data(all_restaurant_data,restaurant_data_fields,to_remove)
extract_to_csv(restaurant_data_final)

# To include main function and boiler plate
