import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px

import seaborn as sns
from scipy.stats import ttest_ind, f_oneway

# Read CSV files
both_df = pd.read_csv('data/raw/UNdata_Export_20250106_135531463.csv')
male_df = pd.read_csv('data/raw/UNdata_Export_20250106_135951253.csv')
female_df = pd.read_csv('data/raw/UNdata_Export_20250106_140234264.csv')

# Output file path
file_path = 'data/output'

# WHO area coordinates (latitude, longitude) for a bubble map
who_areas_coordinates = {
    'WHO: African region (AFRO)': {'lat': 1.0, 'lon': 20.0},
    'WHO: Americas (AMRO)': {'lat': 15.0, 'lon': -60.0},
    'WHO: Eastern Mediterranean Region (EMRO)': {'lat': 24.0, 'lon': 45.0},
    'WHO: European Region (EURO)': {'lat': 50.0, 'lon': 10.0},
    'WHO: South-East Asia region (SEARO)': {'lat': 10.0, 'lon': 90.0},
    'WHO: Western Pacific region (WPRO)': {'lat': 25.0, 'lon': 130.0},
    'World': {'lat': 20.0, 'lon': 0.0},
}

# Generate abbreviations from who_areas_coordinates
area_abbreviations = {area: area.split('(')[-1].strip(')') for area in who_areas_coordinates.keys()}

# List of Area
areas = list(area_abbreviations.values())

# Color list
colours =  ['#F4D0A2', '#A6C9F2', '#D3AED6']

def extract_life_expectancy(df, area):
    # Extract life expectancy for each year from 2019 to 2024 (Pre-COVID, COVID, Post-COVID).
    return {year: df[(df['Country or Area'] == area) & (df['Year(s)'] == year)]['Value'].values[0]
            for year in range(2019, 2025) if not df[(df['Country or Area'] == area) & (df['Year(s)'] == year)].empty}

def calculate_mean_life_expectancy():
    # Calculate mean life expectancy by area and gender - dictionary
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
    global_data_dict = {'year': range(2019, 2025), 'both': [], 'male': [], 'female': []}
    
    for year in global_data_dict['year']:
        global_data_dict['both'].append(np.mean([v['both'].get(year, np.nan) for v in mean_life_expectancy_by_area.values()]))
        global_data_dict['male'].append(np.mean([v['male'].get(year, np.nan) for v in mean_life_expectancy_by_area.values()]))
        global_data_dict['female'].append(np.mean([v['female'].get(year, np.nan) for v in mean_life_expectancy_by_area.values()]))
    
    return pd.DataFrame(global_data_dict)

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


"""
1. Global life expectancy line plot with genders
"""
plt.figure(figsize=(10, 6)) # plot size

for gender, color in zip(['both', 'male', 'female'], colours): # Three coloured lines
    plt.plot(
            global_life_expectancy['year'],
            global_life_expectancy[gender],
            marker='o',
            color=color,
            label=gender.capitalize()
        )
    
plt.title('Global Average Life Expectancy (2019-2024)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Life Expectancy (years)', fontsize=12)
plt.grid(True)
plt.legend()

# Save the plot to the specified path, overwriting the file if it exists
plt.savefig(f'{file_path}/global_average_life_expectancy.png')


"""
2. Area life expectancy bar plots with genders
"""
fig, axes = plt.subplots(2, 3, figsize=(16, 10), sharey=True) # Plot bar charts 2 x 3

width = 0.25  # Bar width for each gender
years = range(2019, 2025) # 2024 + 1

for i, year in enumerate(years): # number and list
    ax = axes[i // 3, i % 3]
    year_data = area_life_expectancy[area_life_expectancy['year'] == year]
    
    for j, (gender, color) in enumerate(zip(['both', 'male', 'female'], colours)):
        subset = year_data[year_data['gender'] == gender]
        x = np.arange(len(subset['area']))
        ax.bar(
                x + (j - 1) * width, subset['life_expectancy'],
                width,
                label=gender.capitalize(),
                color=color,
                alpha=0.7 # transparency
               )
    
    ax.set_title(f'Life Expectancy by Area ({year})', fontsize=13)
    ax.set_xlabel('Area', fontsize=12)
    ax.set_ylabel('Life Expectancy (years)', fontsize=12)

    ax.set_xticks(np.arange(len(areas))) # x-axis: areas
    ax.set_xticklabels([area for area in areas], rotation=45, ha='right')

    ax.grid(axis='y', linestyle='--', alpha=0.7)

fig.tight_layout()

# Save the plot to the specified path, overwriting the file if it exists
plt.savefig(f'{file_path}/area_average_life_expectancy.png')


"""
3. Map plot using both data - both gender
"""
both_data = area_life_expectancy[(area_life_expectancy['gender'] == 'both') & (area_life_expectancy['area'] != 'World')]

both_data['lat'] = both_data['area'].map(lambda x: who_areas_coordinates[x]['lat'])
both_data['lon'] = both_data['area'].map(lambda x: who_areas_coordinates[x]['lon'])

# Scaling for bubble size
both_data['scaled_size'] = (area_life_expectancy['life_expectancy'] - area_life_expectancy['life_expectancy'].min()) / \
                                   (area_life_expectancy['life_expectancy'].max() - area_life_expectancy['life_expectancy'].min()) * 100

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

# Save the animated figure as an HTML file
fig.write_html(f'{file_path}/life_expectancy_animation.html')


"""
4. Statistics - Life Expectancy before, during, and after COVID-19
"""

def filter_data_by_period(area_life_expectancy, start_year, end_year):
    # Filter data for pre-COVID, COVID period, and post-COVID period
    # input: area_life_expectancy, start_year, end_year
    # output: area_life_expectancy list

    return area_life_expectancy[(area_life_expectancy['year'] >= start_year) &
                                (area_life_expectancy['year'] <= end_year)]

# Filter data for each period
pre_covid_data = filter_data_by_period(area_life_expectancy, 2019, 2019)
post_covid_data = filter_data_by_period(area_life_expectancy, 2024, 2024)
# covid_period_data = filter_data_by_period(area_life_expectancy, 2020, 2023)

def perform_ttest_for_period(data, gender1, gender2):
    # Perform t-tests for pre-COVID and post-COVID periods
    # input:  data, gender1, gender2
    # output: t_stat, p_val

    gender1_data = data[data['gender'] == gender1]['life_expectancy']
    gender2_data = data[data['gender'] == gender2]['life_expectancy']
    
    if gender1_data.empty or gender2_data.empty:
        return np.nan, np.nan  # Handle empty data case
    
    t_stat, p_val = ttest_ind(gender1_data, gender2_data, equal_var=False)
    return t_stat, p_val


# T-tests for pre-COVID and post-COVID periods
print("T-Test Results for Pre-COVID:")

t_stat_pre, p_val_pre = perform_ttest_for_period(pre_covid_data, 'male', 'female')

print(f"T-Statistic (Pre-COVID): {t_stat_pre:.2f}, P-Value: {p_val_pre:.4f}")

# p-value checker - threshold is 0.05
if p_val_pre < 0.05:
    print("The result is statistically significant: there is a difference in life expectancy between genders (Pre-COVID).")
else:
    print("The result is not statistically significant: no difference in life expectancy between genders (Pre-COVID).")

print("\nT-Test Results for Post-COVID:")

t_stat_post, p_val_post = perform_ttest_for_period(post_covid_data, 'male', 'female')

print(f"T-Statistic (Post-COVID): {t_stat_post:.2f}, P-Value: {p_val_post:.4f}")

if p_val_post < 0.05:
    print("The result is statistically significant: there is a difference in life expectancy between genders (Post-COVID).")
else:
    print("The result is not statistically significant: no difference in life expectancy between genders (Post-COVID).")


# ANOVA by Area
anova_result_area = f_oneway(
    *[area_life_expectancy[area_life_expectancy['area'] == area]['life_expectancy'].dropna()
      for area in area_life_expectancy['area'].unique()]
)

# ANOVA by Year
anova_result_year = f_oneway(
    *[area_life_expectancy[area_life_expectancy['year'] == year]['life_expectancy'].dropna()
      for year in area_life_expectancy['year'].unique()]
)

print("\nANOVA by Area: F-statistic =", anova_result_area.statistic, ", p-value =", anova_result_area.pvalue)
print("ANOVA by Year: F-statistic =", anova_result_year.statistic, ", p-value =", anova_result_year.pvalue)

# Convert area column to abbreviations
area_life_expectancy['area'] = area_life_expectancy['area'].map(area_abbreviations) 

# Pivot data for heatmap
anova_heatmap_data = area_life_expectancy.pivot_table(
    values='life_expectancy', index='area', columns='year', aggfunc='mean'
)

# Plot heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(anova_heatmap_data, cmap='YlGnBu', annot=True, fmt='.1f', linewidths=.5)
plt.title(f'Life Expectancy by Area and Year\n'
          f'(ANOVA by Area: p = {anova_result_area.pvalue:.3f}, '
          f'ANOVA by Year: p = {anova_result_year.pvalue:.3f})', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Area', fontsize=12)

# Save the plot to the specified path, overwriting the file if it exists
plt.savefig(f'{file_path}/heatmap.png')

plt.show()


# TODO1: To reduce hardcoding
# TODO2: To devide into files by process