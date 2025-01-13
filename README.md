# Life Expectancy Analysis

This project analyzes global life expectancy data from 2019 to 2024 using UN DATA, focusing on trends before, during, and after the COVID-19 pandemic. The aim is to explore how regions and gender differences influence life expectancy. Python libraries like Pandas, Seaborn, Matplotlib, and Plotly will be used for data manipulation and visualization.

## Dataset Breakdown
- **2019 data**: Pre-COVID period
- **2020 to 2023 data**: COVID period
- **2024 data**: Post-COVID period

## Regional Breakdown
- **Africa**
- **Asia**
- **Australia and New Zealand**
- **Europe**
- **Latin America and the Caribbean**
- **North America**
- **Oceania**
- **Polar regions**

## Gender Breakdown
- **Data:**
  - For the overall data, mixed-gender data is used.  
  - For separate gender data, we have:
    - **Both** (mixed-gender): [UNdata_Export_20250106_135531463.csv](data/raw/UNdata_Export_20250106_135531463.csv)
    - **Male**: [UNdata_Export_20250106_135951253.csv](data/raw/UNdata_Export_20250106_135951253.csv)
    - **Female**: [UNdata_Export_20250106_140234264.csv](data/raw/UNdata_Export_20250106_140234264.csv)

- **URL:**
  - **Both** (mixed-gender): [Life expectancy at birth for both sexes combined (years)](https://data.un.org/Data.aspx?q=life+expectancy&d=PopDiv&f=variableID%3a68)
  - **Male**: [Life expectancy at birth, males (years)](https://data.un.org/Data.aspx?q=life+expectancy&d=PopDiv&f=variableID%3a66)
  - **Female**: [Life expectancy at birth, females (years)](https://data.un.org/Data.aspx?q=life+expectancy&d=PopDiv&f=variableID%3a67)

## Data Format

The data is structured as follows:

| "Country or Area" | "Year(s)" | "Variant" | "Value" |
|-------------------|-----------|-----------|---------|
| WHO Regions       | 2024      | Medium    | 73.2995 |

## Analysis

### 1. **Statistical Processing**
The statistical analysis includes **T-test** for comparing life expectancy between genders before and after COVID, and **ANOVA** to analyze differences by area and year. The results help understand if there are significant changes in life expectancy during these periods.

- **T-test**: A statistical test used to determine if there is a significant difference in life expectancy between males and females before and after COVID.
- **ANOVA**: Used to assess if life expectancy differs by region and year.

#### T-Test Formula:
The T-test statistic is calculated as:

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
$$

Where:
- $\bar{x}_1, \bar{x}_2$ are the sample means of the two groups
- $s_1^2, s_2^2$ are the variances of the groups
- $n_1, n_2$ are the sample sizes of the groups

#### ANOVA Formula:
The F-statistic for ANOVA is calculated as:

$$
F = \frac{\text{Variance between groups}}{\text{Variance within groups}}
$$

### 2. **Results**
- **T-Test Results**: 
  - Pre-COVID: If the p-value is less than 0.05, the result indicates a statistically significant difference in life expectancy between genders in the pre-COVID period.
  - Post-COVID: Similarly, if the p-value is less than 0.05, it indicates a statistically significant difference in life expectancy between genders post-COVID.

- **ANOVA Results**:
  - ANOVA tests for differences in life expectancy between different regions and over the years. If the p-value is less than 0.05, which concludes that there are significant differences.

### 3. **Visualization**
- **Heatmap**: A heatmap is generated to visualize life expectancy across different regions and years.
- **Boxplots**: Boxplots is used to visualize the spread of life expectancy data by region and gender.

## Setup Instructions

To run this project locally:
1. Clone the repository.
2. Install the required libraries by running:  
   `pip install -r requirements.txt`
3. Open the Jupyter notebook to view the analysis and visualizations.

## Required Libraries
- pandas==2.2.2
- matplotlib==3.9.1
- seaborn==0.13.2
- plotly==5.24.1
- scipy==1.14.0

## License
This project does not have a license.
