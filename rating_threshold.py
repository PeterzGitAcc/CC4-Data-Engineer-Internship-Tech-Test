def rating_threshold(all_restaurant_data):

    def retrieve_all_restaurants_data(restaurant_data_all, relevant_fields):
        rating_data = []
        for restaurant in restaurant_data_all:
            user_rating_data = restaurant['user_rating']
            relevant_user_rating_data = {key: value for (
                key, value) in user_rating_data.items() if key in relevant_fields}
            rating_data.append(relevant_user_rating_data)
        return rating_data

    def group_ratings(rating_data_raw):
        # aka bucket the rating keys
        # Terbaik (assume to be excellent - since best)
        # Eccellente == Excellent
        # Excelente == Excellent
        # Muito Bom == Very Good
        # Muy Bueno == Very good
        # Bardzo dobrze == Very Good
        # Skvělá volba (assume to be Very Good)
        # Velmi dobré == Very Good
        # Skvělé (assume to be
        # Good)
        # Bueno == Good
        ratings_bucket_dict = {
            'Excellent': ['Excellent', 'Excelente', 'Eccellente', 'Terbaik'],
            'Very Good': ['Very Good', 'Bardzo dobrze',
                          'Muito Bom', 'Muy Bueno', 'Skvělá volba', 'Velmi dobré'],
            'Good': ['Good', 'Bueno', 'Skvělé'],
            'Average': ['Average'],
            'Poor': ['Poor'],

        }
        bucket_list = list(ratings_bucket_dict.keys())
        consolidated_ratings = {bucket_list[i]: []
                                for i in range(0, len(bucket_list))}
        for r_data in rating_data_raw:
            rating_txt = r_data['rating_text']
            rating_score = float(r_data['aggregate_rating'])
            if rating_txt in ratings_bucket_dict['Excellent']:
                consolidated_ratings['Excellent'].append(rating_score)
            elif rating_txt in ratings_bucket_dict['Very Good']:
                consolidated_ratings['Very Good'].append(rating_score)
            elif rating_txt in ratings_bucket_dict['Good']:
                consolidated_ratings['Good'].append(rating_score)
            elif rating_txt in ratings_bucket_dict['Average']:
                consolidated_ratings['Average'].append(rating_score)
            elif rating_txt in ratings_bucket_dict['Poor']:
                consolidated_ratings['Poor'].append(rating_score)

        return consolidated_ratings

    def find_treshold_rating(consolidated_ratings):
        return_str = ''
        try:
            treshold_rating_2dp = {k: min(v)
                                for k, v in consolidated_ratings.items()}
            for k, v in treshold_rating_2dp.items():
                return_str += "Threshold score for {0}: {1}\n".format(k, v)

            return return_str
        except:
            return_str = "No values found in one or more rating categories"

    relevant_fields = ['aggregate_rating', 'rating_text']
    rating_data_raw = retrieve_all_restaurants_data(
        all_restaurant_data, relevant_fields)
    consolidated_ratings = group_ratings(rating_data_raw)
    # print(consolidated_ratings)
    print(find_treshold_rating(consolidated_ratings)) 


if __name__ == "__main__":
    print('Running module directly without data !')

