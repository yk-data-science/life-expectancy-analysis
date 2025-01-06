import pandas as pd
import numpy as np

# Read CSV files
both_df = pd.read_csv('data/raw/UNdata_Export_20250106_140234264.csv')
male_df = pd.read_csv('data/raw/UNdata_Export_20250106_135531463.csv')
female_df = pd.read_csv('data/raw/UNdata_Export_20250106_135951253.csv')

# List of Area
areas = ['WHO: African region (AFRO)', 'WHO: Americas (AMRO)', 'WHO: Eastern Mediterranean Region (EMRO)', 
         'WHO: European Region (EURO)', 'WHO: South-East Asia region (SEARO)', 'WHO: Western Pacific region (WPRO)', 'World']

def calculate_covid_period_mean(df, area):
    # Filter for the covid period (2020-2023)
    covid_data = df[(df['Country or Area'] == area) & (df['Year(s)'].between(2020, 2023))]
    return covid_data['Value'].mean() if not covid_data.empty else np.nan


def extract_life_expectancy(df, area):
    """Extract pre-COVID, during-COVID (mean), and post-COVID life expectancy for a given area."""
    pre_covid = df[(df['Country or Area'] == area) & (df['Year(s)'] == 2019)]['Value'].values
    after_covid = df[(df['Country or Area'] == area) & (df['Year(s)'] == 2024)]['Value'].values
    covid_period_mean = calculate_covid_period_mean(df, area)

    # Return the values as a dictionary
    return {
        'pre_covid': pre_covid[0] if len(pre_covid) > 0 else None,
        'covid_period_mean': covid_period_mean,
        'after_covid': after_covid[0] if len(after_covid) > 0 else None
    }

# Calculate the life expectancy values for each area by gender
mean_life_expectancy_by_area = {}
for area in areas:
    mean_life_expectancy_by_area[area] = {
        'both': extract_life_expectancy(both_df, area),
        'male': extract_life_expectancy(male_df, area),
        'female': extract_life_expectancy(female_df, area),
    }

print(mean_life_expectancy_by_area)


# Show tables

## plot
# Yearly trend
# By region
# By gender

# Statistics Region, gender