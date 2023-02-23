from get_data import all_restaurant_data
from extract_restaurant_csv import retrieve_user_rating
import pandas as pd
# restaurant_data = retrieve_data(restaurant_data_url)

def retrieve_all_restaurants_data(restaurant_data_all,relevant_fields):
    rating_data = []
    for restaurant in restaurant_data_all:
        user_rating_data = restaurant['restaurant']['user_rating']
        relevant_user_rating_data = {key:value for (key,value) in user_rating_data.items() if key in relevant_fields}
        rating_data.append(relevant_user_rating_data)
    return rating_data

def translate_ratings(rating_data_raw):
    pass

def find_min_max_rating(relevant_rating_data):
    #ratings
    ratings = ['Excellent','Very Good','Good','Average','Poor']
    #convert to df
    df = pd.DataFrame(relevant_rating_data) 
    print(df.groupby(['rating_text']).min())
    print(df.groupby(['rating_text']).max())
    # translate to the same language 
    #Bardzo dobrze 
    #Bueno  
    #Eccellente
    #Excelente  
    #Muito Bom
    #Muy Bueno 
    #Skvělá volba
    #Skvělé
    #Terbaik
    #Velmi dobré 



relevant_fields = ['aggregate_rating','rating_text']
rating_data_raw = retrieve_all_restaurants_data(all_restaurant_data,relevant_fields)

print(find_min_max_rating(rating_data_raw))