import pandas as pd
from data.get_data import all_restaurant_data

# functions

def retrieve_photos(event_data_photos_list):
    ret_dict = {}
    ret_dict['photo_url'] = []
    for photo in event_data_photos_list:
        ret_dict['photo_url'].append(photo['photo']['url'])
    return ret_dict


def retrieve_events_details(events, fields_from_events):
    formatted_event_data = []
    # no data
    if len(events) == 0:
        return formatted_event_data
    else:
        events_list = events['zomato_events']
        # events_list =
        for event in events_list:
            photos_url = retrieve_photos(event['event']['photos'])
            event_data_formatted = {key: value for (
                key, value) in event['event'].items() if key in fields_from_events}
            event_data_final = event_data_formatted | photos_url
            formatted_event_data.append(event_data_final)
        return formatted_event_data


def retrieve_all_restaurant_events_data(restaurants_list, restaurant_data_events_fields, fields_from_events):
    # store only restaurant objs
    ret_data = []
    # loop through array of results
    for res in restaurants_list:
        restaurant_data_no_events = {key: value for (
            key, value) in res['restaurant'].items() if key in restaurant_data_events_fields}
        restaurant_data_events = {key: value for (
            key, value) in res['restaurant'].items() if key == 'zomato_events'}
        restaurant_data_events_formatted = retrieve_events_details(
            restaurant_data_events, fields_from_events)
        restaurant_data_no_events['events'] = restaurant_data_events_formatted
        ret_data.append(restaurant_data_no_events)

    return ret_data


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
        df_combined = pd.concat([df, events_df], axis=1)
        df_combined.drop(columns=['events'], inplace=True)
        df_apr2019 = df_combined.loc[df_combined['start_date']
                                     == '2019-04-01'].copy(deep=True)
        df_apr2019.fillna('NA', inplace=True)
        df_apr2019.to_csv("./csv_output/restaurant_events.csv", index=False)
    except:
        print("cannot write to file!")


restaurant_data_events_fields = ['id', 'name']
fields_from_events = ['event_id', 'title', 'start_date', 'end_date']
all_restaurants_events_data = retrieve_all_restaurant_events_data(
    all_restaurant_data, restaurant_data_events_fields, fields_from_events)
extract_to_csv(all_restaurants_events_data)

# To include main function and boiler plate
if __name__ == "__main__":
    pass
