import pandas as pd
from get_data import retrieve_data , restaurant_data_url
#initialize global values 
restaurant_data_events_fields = ['id','name']
fields_from_events = ['event_id','title','start_date','end_date']


#functions

restaurant_data = retrieve_data(restaurant_data_url)

def retrieve_photos(event_data_photos_list):
    ret_dict ={}
    ret_dict['photo_url']= []
    for photo in event_data_photos_list:
        ret_dict['photo_url'].append(photo['photo']['url'])
    return ret_dict


def retrieve_events_details(events): 
    formatted_event_data = []
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
            formatted_event_data.append(event_data_final)
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
            restaurant_data_no_events['events'] = restaurant_data_events_formatted
            ret_data.append(restaurant_data_no_events)

    return ret_data

all_restaurants_events_data = retrieve_all_restaurant_events_data(restaurant_data)

def split_to_cols(df_col):
    rows = []
    for index, row in df_col.items():
        for item in row:
            rows.append(item)
    df_1 = pd.DataFrame(rows)
    return df_1

def extract_to_csv(events_data):
    try:
        df = pd.DataFrame(events_data)
        events_df = split_to_cols(df['events'])
        df_combined = pd.concat([df,events_df], axis=1)
        df_combined.drop(columns=['events'], inplace = True)
        df_apr2019 = df_combined.loc[df_combined['start_date'] == '2019-04-01'].copy(deep=True)
        df_apr2019.fillna('NA',inplace=True)
        df_apr2019.to_csv("restaurant_events.csv")
    except:
        print("cannot write to file!")

extract_to_csv(all_restaurants_events_data)
