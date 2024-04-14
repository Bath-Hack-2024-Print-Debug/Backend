import pandas as pd


def preprocess_features(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    def convert_to_list(x):
        if isinstance(x, str):
            return eval(x)
        elif isinstance(x, list):
            return x
        else:
            return []

    # Convert the string representation of the list into an actual list
    df['features'] = df['features'].apply(convert_to_list)

    # Explode the list into separate rows
    df_exploded = df.explode('features')

    # Count the occurrences of each feature
    feature_counts = df_exploded['features'].value_counts()

    # Filter features that appear more than 4 times
    frequent_features = feature_counts[feature_counts > 4].index

    # Create dummy variables (one-hot encoding) only for frequent features
    df_encoded = pd.get_dummies(df_exploded, columns=['features'], prefix='', prefix_sep='')

    # Filter columns to keep only frequent features
    frequent_columns = [col for col in df_encoded.columns if col in frequent_features]
    df_encoded = df_encoded[frequent_columns]

    # Group by the original index and aggregate the dummy variables
    df_encoded = df_encoded.groupby(level=0).max()

    # Combine the encoded features with the original dataframe
    df_final = pd.concat([df, df_encoded], axis=1)

    # Drop the original 'features' column
    df_final = df_final.drop('features', axis=1)

    return df_final

# Combine bath and bristol property details into a single CSV file
bath = pd.read_csv('bath_ml.csv')
bristol = pd.read_csv('bristol_ml.csv')
df_combined = pd.concat([bath, bristol], ignore_index=True)
df_combined.to_csv('bath_bristol_ml.csv')

# Preprocess the features and save the result to a new CSV file
df_final = preprocess_features('bath_bristol_ml.csv')
df_final.to_csv('bath_bristol_ml_encoded.csv')
print("oh yeah")