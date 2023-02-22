import requests
import pandas as pd
#initialize global values 
restaurant_data_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
restaurant_data_events_fields = ["id",'name']
fields_from_events = ['event_id','title','start_date','end_date']


#functions
def retrieve_data(data_url):
    response = requests.get(data_url)
    if response.ok:
        response_data = response.json()
    else:
        return "An error has occured"
    
    return response_data


restaurant_data = retrieve_data(restaurant_data_url)

def retrieve_photos(event_data_photos_list):
    ret_dict ={}
    ret_dict['photo_url']= []
    for photo in event_data_photos_list:
        ret_dict['photo_url'].append(photo['photo']['url'])
    return ret_dict


def retrieve_events_details(events): 
    formatted_event_data = {}
    #no data
    if len(events) == 0:
        return formatted_event_data
    else:
        events_list =events['zomato_events']
        # events_list = 
        for event in events_list:             
            photos_url = retrieve_photos(event['event']['photos'])
            event_data_formatted = {key:value for (key,value) in event['event'].items() if key in fields_from_events}
            event_data_final = event_data_formatted | photos_url
            formatted_event_data.update(event_data_final)
        return formatted_event_data


def format_data_for_csv(single_restaurant_event_data):
    # need to pull event data from events 
    pass


#Test case: if data dict or list (retrieve specific dictionary)
def retrieve_all_restaurant_events_data(list_data_object):
    #store only restaurant objs
    ret_data = []
    #loop through array of results 
    for res in list_data_object:
        for restaurants in res['restaurants']:
            restaurant_data_no_events ={ key:value for (key,value) in restaurants['restaurant'].items() if key in restaurant_data_events_fields}
            restaurant_data_events ={ key:value for (key,value) in restaurants['restaurant'].items() if key == 'zomato_events'}
            restaurant_data_events_formatted = retrieve_events_details(restaurant_data_events)
            restaurant_data = restaurant_data_no_events | restaurant_data_events_formatted
            ret_data.append(restaurant_data)

    return ret_data


all_restaurants_events_data = retrieve_all_restaurant_events_data(restaurant_data)

def extract_to_csv(events_data):
    try:
        df = pd.DataFrame(events_data)
        df.fillna('NA',inplace=True)
        df.to_csv("restaurant_events.csv")
    except:
        print("cannot write to file!")

extract_to_csv(all_restaurants_events_data)


# Extract list of restaurants that have past event in month of april 2019 

#1. pull data 

#2. extract fields and fill na

#3. save as restaurant_events.csv

# From the dataset restaurant_data.json 

#1. Deternmine treshold for diff. rating txt based on aggregate ratings

# ◦ Excellent
# ◦ Very Good
# ◦ Good
# ◦ Average
# ◦ Poor