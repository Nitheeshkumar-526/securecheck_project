import pandas as pd

def clean_data(path):
    df = pd.read_csv(path)

    # Drop empty columns
    df.dropna(axis=1, how='all', inplace=True)

    # Fill age if missing
    df['driver_age'] = df['driver_age'].fillna(df['driver_age'].median())

    # Clean critical fields
    df.dropna(subset=['stop_date', 'stop_time', 'country_name'], inplace=True)

    # Format date & time
    df['stop_date'] = pd.to_datetime(df['stop_date'], errors='coerce')
    df['stop_time'] = pd.to_datetime(df['stop_time'], errors='coerce').dt.time

    return df[[
        'stop_date', 'stop_time', 'country_name', 'driver_gender',
        'driver_age', 'driver_race', 'violation', 'search_conducted',
        'search_type', 'stop_outcome', 'is_arrested', 'stop_duration',
        'drugs_related_stop'
    ]]
