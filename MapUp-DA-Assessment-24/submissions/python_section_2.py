import pandas as pd
from datetime import time

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    toll_ids = df['id_start'].append(df['id_end']).unique()
    dist_matrix = pd.DataFrame(0, index=toll_ids, columns=toll_ids)

    for _, row in df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        dist_matrix.at[id_start, id_end] = distance
        dist_matrix.at[id_end, id_start] = distance

    for k in toll_ids:
        for i in toll_ids:
            for j in toll_ids:
                dist_matrix.at[i, j] = min(dist_matrix.at[i, j], dist_matrix.at[i, k] + dist_matrix.at[k, j])

    return dist_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_data = []

    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end:
                distance = df.at[id_start, id_end]
                unrolled_data.append([id_start, id_end, distance])

    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    lower_threshold = reference_avg_distance * 0.9
    upper_threshold = reference_avg_distance * 1.1
    filtered_df = df.groupby('id_start')['distance'].mean().reset_index()
    filtered_df = filtered_df[(filtered_df['distance'] >= lower_threshold) & (filtered_df['distance'] <= upper_threshold)]

    return filtered_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coeffs = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle, coeff in rate_coeffs.items():
        df[vehicle] = df['distance'] * coeff

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """

    discount_factors = {
        'weekday': {
            (time(0, 0), time(10, 0)): 0.8,
            (time(10, 0), time(18, 0)): 1.2,
            (time(18, 0), time(23, 59, 59)): 0.8
        },
        'weekend': 0.7
    }

    df['start_day'] = ''
    df['start_time'] = None
    df['end_day'] = ''
    df['end_time'] = None

    for index, row in df.iterrows():

        for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
            df.at[index, vehicle] *= discount_factors['weekday'][(time(0, 0), time(10, 0))]

    return df