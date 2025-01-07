import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Read CSV files
both_df = pd.read_csv('data/raw/UNdata_Export_20250106_140234264.csv')
male_df = pd.read_csv('data/raw/UNdata_Export_20250106_135531463.csv')
female_df = pd.read_csv('data/raw/UNdata_Export_20250106_135951253.csv')

# WHO area coordinates(latitude, longtitude) for a bubble map
who_areas_coordinates = {
    'WHO: African region (AFRO)': {'lat': 1.0, 'lon': 20.0},
    'WHO: Americas (AMRO)': {'lat': 15.0, 'lon': -60.0},
    'WHO: Eastern Mediterranean Region (EMRO)': {'lat': 24.0, 'lon': 45.0},
    'WHO: European Region (EURO)': {'lat': 50.0, 'lon': 10.0},
    'WHO: South-East Asia region (SEARO)': {'lat': 10.0, 'lon': 90.0},
    'WHO: Western Pacific region (WPRO)': {'lat': 25.0, 'lon': 130.0},
    'World': {'lat': 20.0, 'lon': 0.0},
}

# List of Area
areas = list(who_areas_coordinates.keys())

def extract_life_expectancy(df, area):
    # Extract life expectancy for each year from 2019 to 2024.

    return {year: df[(df['Country or Area'] == area) & (df['Year(s)'] == year)]['Value'].values[0]
            for year in range(2019, 2025) if not df[(df['Country or Area'] == area) & (df['Year(s)'] == year)].empty}

def calculate_mean_life_expectancy():
    # Calculate mean life expectancy by area and gender. - dictionary
    
    return {
        area: {
            'both': extract_life_expectancy(both_df, area),
            'male': extract_life_expectancy(male_df, area),
            'female': extract_life_expectancy(female_df, area),
        }
        for area in who_areas_coordinates
    }

mean_life_expectancy_by_area = calculate_mean_life_expectancy()

def prepare_global_life_expectancy(mean_life_expectancy_by_area):
    # Prepare data for global average life expectancy plot.
    
    global_data = {'year': range(2019, 2025), 'both': [], 'male': [], 'female': []}
    
    for year in global_data['year']:
        global_data['both'].append(np.mean([v['both'].get(year, np.nan) for v in mean_life_expectancy_by_area.values()]))
        global_data['male'].append(np.mean([v['male'].get(year, np.nan) for v in mean_life_expectancy_by_area.values()]))
        global_data['female'].append(np.mean([v['female'].get(year, np.nan) for v in mean_life_expectancy_by_area.values()]))
    
    return pd.DataFrame(global_data)

def prepare_area_life_expectancy(mean_life_expectancy_by_area):
    # Prepare data for life expectancy by area for each year.
    data = []
    
    for area, values in mean_life_expectancy_by_area.items():
        for year in range(2019, 2025):
            for gender in ['both', 'male', 'female']:
                if year in values[gender]:
                    data.append({'area': area, 'year': year, 'gender': gender, 'life_expectancy': values[gender][year]})
    
    return pd.DataFrame(data)

# Prepare data
global_life_expectancy = prepare_global_life_expectancy(mean_life_expectancy_by_area)
area_life_expectancy = prepare_area_life_expectancy(mean_life_expectancy_by_area)

# 1. Global life expectancy line plot with genders
plt.figure(figsize=(10, 6))

for gender, color in zip(['both', 'male', 'female'], ['#D3AED6', '#A6C9F2', '#F4D0A2']):
    plt.plot(
            global_life_expectancy['year'],
            global_life_expectancy[gender],
            marker='o', color=color,
            label=gender.capitalize()
        )
    
plt.title('Global Average Life Expectancy (2019-2024)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Life Expectancy (years)', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()

# 2. Area life expectancy bar plots with genders
fig, axes = plt.subplots(2, 3, figsize=(18, 12), sharey=True) # Show graphs 2 x 3
width = 0.25  # Bar width for each gender
years = range(2019, 2025)
for i, year in enumerate(years):
    ax = axes[i // 3, i % 3] # side by side
    year_data = area_life_expectancy[area_life_expectancy['year'] == year]
    for j, (gender, color) in enumerate(zip(['both', 'male', 'female'], ['#D3AED6', '#A6C9F2', '#F4D0A2'])):
        subset = year_data[year_data['gender'] == gender]
        x = np.arange(len(subset['area']))
        ax.bar(x + (j - 1) * width, subset['life_expectancy'], width, label=gender.capitalize(), color=color, alpha=0.7)
    
    ax.set_title(f'Life Expectancy by Area ({year})', fontsize=13)

    ax.set_xlabel('Area', fontsize=12)
    ax.set_ylabel('Life Expectancy (years)', fontsize=12)

    ax.set_xticks(np.arange(len(areas)))
    ax.set_xticklabels(areas, rotation=45, ha='right')

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend()

fig.tight_layout()
plt.show()

# 3. Map plot using both data
both_data = area_life_expectancy[(area_life_expectancy['gender'] == 'both') & (area_life_expectancy['area'] != 'World')]

both_data['lat'] = both_data['area'].map(lambda x: who_areas_coordinates[x]['lat'])
both_data['lon'] = both_data['area'].map(lambda x: who_areas_coordinates[x]['lon'])

# Scaling for a bubble size (to be obvious)
both_data['scaled_size'] = (area_life_expectancy['life_expectancy'] - area_life_expectancy['life_expectancy'].min()) \
                                   / (area_life_expectancy['life_expectancy'].max() - area_life_expectancy['life_expectancy'].min()) * 100

fig = px.scatter_mapbox(
    both_data,
    lat="lat",
    lon="lon",
    color="life_expectancy",
    hover_name="area",
    animation_frame="year",
    size="scaled_size",
    size_max=40,
    zoom=1, 
    color_continuous_scale="YlOrBr",
    title="Life Expectancy by WHO Region (2019-2024)"
)
fig.update_layout(mapbox_style="open-street-map")
fig.show()
