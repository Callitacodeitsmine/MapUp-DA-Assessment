from typing import Dict, List
import pandas as pd
from itertools import permutations
import re
import polyline
from haversine import haversine

def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    """
    Reverses the input list by groups of n elements.
    """
    result = []
    for i in range(0, len(lst), n):
        group = []
        for j in range(i, min(i + n, len(lst))):
            group.insert(0, lst[j])
        result.extend(group)
    return result


def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    """
    Groups the strings by their length and returns a dictionary.
    """
    length_dict = {}
    for word in lst:
        length = len(word)
        if length not in length_dict:
            length_dict[length] = []
        length_dict[length].append(word)
    return dict(sorted(length_dict.items()))


def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    """
    Flattens a nested dictionary into a single-level dictionary with dot notation for keys.
    """
    def _flatten(current_dict, parent_key=''):
        items = []
        for key, value in current_dict.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(_flatten(value, new_key).items())
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    items.extend(_flatten({f"{new_key}[{index}]": item}).items())
            else:
                items.append((new_key, value))
        return dict(items)

    return _flatten(nested_dict)


def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list that may contain duplicates.
    """
    return list(set(permutations(nums)))


def find_all_dates(text: str) -> List[str]:
    """
    This function takes a string as input and returns a list of valid dates
    in 'dd-mm-yyyy', 'mm/dd/yyyy', or 'yyyy.mm.dd' format found in the string.
    """
    date_patterns = [
        r'\b\d{2}-\d{2}-\d{4}\b',  
        r'\b\d{2}/\d{2}/\d{4}\b',  
        r'\b\d{4}\.\d{2}\.\d{2}\b' 
    ]
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))
    return dates


def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    """
    Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    """

    coords = polyline.decode(polyline_str)
    data = {'latitude': [], 'longitude': [], 'distance': []}
    
    for i, coord in enumerate(coords):
        data['latitude'].append(coord[0])
        data['longitude'].append(coord[1])
        if i == 0:
            data['distance'].append(0)
        else:
            prev_coord = coords[i - 1]
            distance = haversine(prev_coord, coord) * 1000
            data['distance'].append(distance)
    
    return pd.DataFrame(data)


def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Rotate the given matrix by 90 degrees clockwise, then replace each element
    with the sum of its row and column, excluding itself.
    """
    n = len(matrix)
    rotated = [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]

    final_matrix = []
    for i in range(n):
        row_sum = sum(rotated[i])
        final_matrix.append([])
        for j in range(n):
            col_sum = sum(rotated[k][j] for k in range(n))
            final_matrix[i].append(row_sum + col_sum - rotated[i][j])

    return final_matrix


def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Verifies if each unique (id, id_2) pair in the DataFrame has full 24-hour and 7-day coverage.
    """
    def check_completeness(group):
        pass

    return df.groupby(['id', 'id_2']).apply(check_completeness)