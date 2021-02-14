"""
You can download the full data from CMS website for your need
https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/Provider-of-Services/index
Note: I have used a small file for 3 states - CT,MA,RI.
File Name: pos_other_Dec20.csv
"""
import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from pathlib import Path

# Set the process for the state needed
state = 'CT'
data_path = Path('.').absolute().parent / 'data'

def prep_prov_data(state='CT'):
    """
    Takes the state code and creates output file for the state
    :param state:
    :return:
    """
    # Read the POS file
    file = f"{data_path}\pos_other_Dec20.csv"
    df = pd.read_csv(file, encoding='cp1252')
    df = df[['PRVDR_NUM', 'ST_ADR', 'CITY_NAME', 'STATE_CD', 'ZIP_CD','FIPS_CNTY_CD', 'CBSA_URBN_RRL_IND']]
    print(f'Original dataframe has {df.shape[0]} rows')

    # Filter to remove blank values in address
    filter = df['ST_ADR'].isna()
    df = df[~filter]
    print(f'After null filter dataframe has {df.shape[0]} rows')

    # Lets save the data for given state only, STATE_CD = 'CT'
    filter = df['STATE_CD'] == state
    df = df[filter]
    print(f'After State={state} filter dataframe has {df.shape[0]} rows')

    df['ADDRESS'] = df['ST_ADR'].astype(str) + "," + df['CITY_NAME'].astype(str) + "," + \
                    df['STATE_CD'].astype(str)

    print("######## Sample Address ##########")
    print(df.ADDRESS.head())

    # Return dataframe
    return df

df = prep_prov_data(state=state)
df.reset_index(drop=True,inplace=True)

# ##---------------Address Processing ---------------##
geolocator = Nominatim(user_agent="ProviderAddressGenerator")

def get_lat_long(text):

    try:
        location = geolocator.geocode(text)
        return_lat = location.latitude
        return_long = location.longitude
    except Exception as e:
        print(f'Exception: {e}')
        return_lat = 0
        return_long = 0

    return return_lat, return_long

for i in range(df.shape[0]):
    addr = df.loc[i,"ADDRESS"]
    df.loc[i, "LAT"],df.loc[i,"LONG"] = get_lat_long(addr)
    sleep(1) # Sleep for a second before calling API
    print(f'Processed address rec:{i}/{df.shape[0]}')

# Save output file
file_name = f'{data_path}\pos_{state}_address.csv'
print(file_name)
df.to_csv(file_name, header=True, index=None)