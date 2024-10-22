import re
from itertools import permutations
import pandas as pd
from geopy.distance import geodesic
import polyline

# Function for Question 1: Reverse List by N Elements
def reverse_by_n(lst, n):
    result = []
    for i in range(0, len(lst), n):
        group = lst[i:i+n]
        reversed_group = []
        for j in range(len(group) - 1, -1, -1):
            reversed_group.append(group[j])
        result.extend(reversed_group)
    return result

# Function for Question 2: Group strings by length
def group_by_length(strings):
    result = {}
    for s in strings:
        length = len(s)
        if length not in result:
            result[length] = []
        result[length].append(s)
    return dict(sorted(result.items()))

# Function for Question 3: Flatten a Nested Dictionary
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_dict({f"{k}[{i}]": item}, parent_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Function for Question 4: Generate Unique Permutations
def unique_permutations(lst):
    return [list(p) for p in set(permutations(lst))]

# Function for Question 5: Find All Dates in a Text
def find_all_dates(text):
    date_pattern = r"\b(?:\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{4}\.\d{2}\.\d{2})\b"
    return re.findall(date_pattern, text)

# Function for Question 6: Decode Polyline, Convert to DataFrame with Distances
def decode_polyline_to_df(encoded_polyline):
    coordinates = polyline.decode(encoded_polyline)
    df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
    df['distance'] = [0] + [geodesic(df.iloc[i-1], df.iloc[i]).meters for i in range(1, len(df))]
    return df

# Function for Question 7: Matrix Rotation and Transformation
def rotate_and_transform(matrix):
    n = len(matrix)
    rotated_matrix = [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated_matrix[i]) - rotated_matrix[i][j]
            col_sum = sum(row[j] for row in rotated_matrix) - rotated_matrix[i][j]
            rotated_matrix[i][j] = row_sum + col_sum
    return rotated_matrix

# Function for Question 8: Time Check
def check_time_completeness(df):
    def is_complete(group):
        group['start_datetime'] = pd.to_datetime(group['startDay'] + ' ' + group['startTime'])
        group['end_datetime'] = pd.to_datetime(group['endDay'] + ' ' + group['endTime'])
        full_week = pd.date_range(group['start_datetime'].min(), group['end_datetime'].max(), freq='D').nunique() == 7
        return full_week
    return df.groupby(['id', 'id_2']).apply(is_complete)

# Main function to handle user inputs and call respective functions
def main():
    print("Select a question to test (1-8): ")
    print("1: Reverse List by N Elements")
    print("2: Group strings by length")
    print("3: Flatten a Nested Dictionary")
    print("4: Generate Unique Permutations")
    print("5: Find All Dates in a Text")
    print("6: Decode Polyline, Convert to DataFrame with Distances")
    print("7: Matrix Rotation and Transformation")
    print("8: Time Check")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        lst = list(map(int, input("Enter the list elements separated by spaces: ").split()))
        n = int(input("Enter the value of n: "))
        result = reverse_by_n(lst, n)
        print("Output:", result)

    elif choice == 2:
        strings = input("Enter the list of strings separated by spaces: ").split()
        result = group_by_length(strings)
        print("Output:", result)

    elif choice == 3:
        nested_dict = {
            "road": {
                "name": "Highway 1",
                "length": 350,
                "sections": [
                    {
                        "id": 1,
                        "condition": {
                            "pavement": "good",
                            "traffic": "moderate"
                        }
                    }
                ]
            }
        }
        result = flatten_dict(nested_dict)
        print("Output:", result)

    elif choice == 4:
        lst = list(map(int, input("Enter the list elements separated by spaces: ").split()))
        result = unique_permutations(lst)
        print("Output:", result)

    elif choice == 5:
        text = input("Enter the text: ")
        result = find_all_dates(text)
        print("Output:", result)

    elif choice == 6:
        encoded_polyline = input("Enter the polyline string: ")
        df = decode_polyline_to_df(encoded_polyline)
        print("Output:")
        print(df)

    elif choice == 7:
        n = int(input("Enter the size of the matrix (n x n): "))
        matrix = []
        print("Enter the matrix row by row:")
        for _ in range(n):
            row = list(map(int, input().split()))
            matrix.append(row)
        result = rotate_and_transform(matrix)
        print("Output:", result)

    elif choice == 8:
        file_path = input("Enter the path to dataset-1.csv: ")
        df = pd.read_csv(file_path)
        result = check_time_completeness(df)
        print("Output:")
        print(result)

if __name__ == "__main__":
    main()