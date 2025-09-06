# Importar librerias necesarias
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datasets
passengers_df = pd.read_csv('data/monthly_passengers.csv')
holidays_df = pd.read_csv('data/global_holidays.csv')
population_df = pd.read_csv('data/population_by_country.csv')
countries_df = pd.read_csv('data/countries.csv')
happiness2015_df = pd.read_csv('data/happiness/2015.csv')
happiness2016_df = pd.read_csv('data/happiness/2016.csv')
happiness2017_df = pd.read_csv('data/happiness/2017.csv')
happiness2018_df = pd.read_csv('data/happiness/2018.csv')
happiness2019_df = pd.read_csv('data/happiness/2019.csv')

# Lista de los paises del hemisferio sur
SouthHemisphere = [
    # Sudamérica
    "Argentina","Bolivia, Plurinational State of","Brazil","Chile","Colombia",
    "Ecuador","Paraguay","Peru","Uruguay",
    # África
    "Angola","Botswana","Burundi","Comoros","Equatorial Guinea","Eswatini",
    "Gabon","Kenya","Lesotho","Madagascar","Malawi","Mauritius","Mayotte",
    "Mozambique","Namibia","Réunion","Rwanda","Sao Tome and Principe",
    "Seychelles","Somalia","South Africa","Tanzania",
    "Congo, The Democratic Republic of the","Zambia","Zimbabwe",
    # Oceanía y territorios
    "Australia","New Zealand","Papua New Guinea","Fiji","Solomon Islands",
    "Vanuatu","Samoa","Tonga","Tuvalu","Nauru","Kiribati","Niue",
    "Cook Islands","French Polynesia","Tokelau","Wallis and Futuna",
    "New Caledonia","Norfolk Island","Pitcairn","American Samoa",
    "Christmas Island","Cocos (Keeling) Islands","Heard Island and McDonald Islands",
    "Bouvet Island","South Georgia and the South Sandwich Islands",
    "Saint Helena, Ascension and Tristan da Cunha"
]
countries_df.drop(columns=['alpha_2', 'numeric', 'official_name', 'common_name'], inplace=True)


# Añadir el hemisferio del pais
countries_df["Hemisphere"] = countries_df["name"].apply(
    lambda x: "South" if x in SouthHemisphere else "North"
)
# Añadir los meses por temporada
countries_df["Spring_Months"] = countries_df["Hemisphere"].apply(
    lambda x: [9, 10, 11] if x == "South" else [3, 4, 5]
)
countries_df["Summer_Months"] = countries_df["Hemisphere"].apply(
    lambda x: [12, 1, 2] if x == "South" else [6, 7, 8]
)
countries_df["Autumn_Months"] = countries_df["Hemisphere"].apply(
    lambda x: [3, 4, 5] if x == "South" else [9, 10, 11]
)
countries_df["Winter_Months"] = countries_df["Hemisphere"].apply(
    lambda x: [6, 7, 8] if x == "South" else [12, 1, 2]
)

passengers_df.sort_values(by=['Total', 'Total_OS'], ascending=False, inplace=True)
passengers_df.reset_index(drop=True, inplace=True)
passengers_df.isnull().sum(), holidays_df.isnull().sum()
passengers_df.fillna(0, inplace=True)
passengers_df.isnull().sum(), holidays_df.isnull().sum()
holidays_df['Date'] = pd.to_datetime(holidays_df['Date'], errors='coerce')
passengers_df.fillna(0, inplace=True)

# Funcion para analizar patrones por temporada
def analyze_seasonal_patterns(passengers_df, countries_df):
    passengers_seasonal = passengers_df.merge(
        countries_df[['alpha_3', 'name', 'Hemisphere']], 
        left_on='ISO3',
        right_on='alpha_3',
        how='left'
    )

    season_map_north = {12:'Winter',1:'Winter',2:'Winter', 3:'Spring',4:'Spring',5:'Spring',
                        6:'Summer',7:'Summer',8:'Summer', 9:'Autumn',10:'Autumn',11:'Autumn'}
    season_map_south = {12:'Summer',1:'Summer',2:'Summer', 3:'Autumn',4:'Autumn',5:'Autumn',
                        6:'Winter',7:'Winter',8:'Winter', 9:'Spring',10:'Spring',11:'Spring'}

    passengers_seasonal['Month'] = passengers_seasonal['Month'].astype(int)
    passengers_seasonal['Season'] = np.where(
        passengers_seasonal['Hemisphere'].eq('South'),
        passengers_seasonal['Month'].map(season_map_south),
        passengers_seasonal['Month'].map(season_map_north)
    )

    passengers_seasonal['Total_Final'] = passengers_seasonal['Total'].fillna(passengers_seasonal['Total_OS'])
    passengers_seasonal['Total_Domestic'] = passengers_seasonal['Domestic'].fillna(0)
    passengers_seasonal['Total_International'] = passengers_seasonal['International'].fillna(0)

    annual_stats = (
        passengers_seasonal
        .groupby(['ISO3', 'name', 'Hemisphere', 'Year'], as_index=False)
        .agg(
            Annual_Total_Passengers = ('Total_Final', 'sum'),
            Annual_Domestic_Passengers = ('Total_Domestic', 'sum'),
            Annual_International_Passengers = ('Total_International', 'sum')
        )
    )

    return annual_stats, passengers_seasonal

# Funcion para graficar tendencias del tipo de viaje
def plot_traffic_trends(annual_stats, traffic_type='international', n=16):
    if traffic_type == 'international':
        column = 'Annual_International_Passengers'
        title = 'turismo internacional'
        ylabel = 'Pasajeros Internacionales Anuales'
    elif traffic_type == 'domestic':
        column = 'Annual_Domestic_Passengers'
        title = 'turismo doméstico'
        ylabel = 'Pasajeros Domésticos Anuales'
    else:   
        column = 'Annual_Total_Passengers'
        title = 'turismo total'
        ylabel = 'Pasajeros Totales Anuales'

    top_countries = (
        annual_stats.groupby('name', as_index=False)[column]
        .sum()
        .sort_values(by=column, ascending=False)
        .head(n)['name']
        .tolist()
    )
    df_top = annual_stats[annual_stats['name'].isin(top_countries)]

    plt.figure(figsize=(14, 8))
    sns.lineplot(
        data=df_top,
        x='Year',
        y=column,
        hue='name',
        alpha=0.7
    )
    plt.title(f'Top {n} países por {title} a lo largo de los años')
    plt.xlabel('Año')
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Funcion para analizar si hay una correlacion con la felicidad
def analyze_happiness_correlation():
    happiness_dfs = [
        happiness2015_df[['Happiness Score', 'Country', 'Region']].rename(columns={'Happiness Score': 'Score'}),
        happiness2016_df[['Happiness Score', 'Country', 'Region']].rename(columns={'Happiness Score': 'Score'}),
        happiness2017_df[['Happiness.Score', 'Country']].rename(columns={'Happiness.Score': 'Score'}),
        happiness2018_df[['Score', 'Country or region']].rename(columns={'Country or region': 'Country'}),
        happiness2019_df[['Score', 'Country or region']].rename(columns={'Country or region': 'Country'})
    ]

    combined_happiness = pd.concat(happiness_dfs)
    average_happiness = combined_happiness.groupby('Country')['Score'].mean().reset_index()
    average_happiness.rename(columns={'Score': 'Average Happiness Score'}, inplace=True)
    average_happiness.sort_values(by='Average Happiness Score', ascending=False, inplace=True)
    average_happiness.reset_index(drop=True, inplace=True)

    average_happiness = average_happiness.merge(
        countries_df[['name', 'alpha_3']],
        left_on='Country',
        right_on='name',
        how='left'
    )

    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=average_happiness.head(20),
        x='Average Happiness Score',
        y='alpha_3',
        palette='viridis'
    )
    plt.title('Top 20 países por puntaje promedio de felicidad (2015-2019)')
    plt.xlabel('Puntaje Promedio de Felicidad')
    plt.ylabel('País')
    plt.tight_layout()
    plt.show()

    return average_happiness

# Funcion para graficar los top 10 paises con mas volumen de pasajeros
def plot_top_10_countries(df):
    df_until_2018 = df[df['Year'] <= 2018].copy()
    
    country_totals = df_until_2018.groupby('ISO3')['Total'].sum().sort_values(ascending=False)
    top_10_countries = country_totals.head(10).index
    
    top_10_df = df_until_2018[df_until_2018['ISO3'].isin(top_10_countries)]
    
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=top_10_df, x='Year', y='Total', hue='ISO3')
    plt.title('Top 10 Países por Volumen de Pasajeros (Hasta 2018)')
    plt.xlabel('Año')
    plt.ylabel('Total de Pasajeros')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='País')
    plt.tight_layout()
    plt.show()

# Funcion para graficar el ratio entre pasajeros y poblacion por pais
def plot_population_passenger_ratio(passengers_df, population_df, year=2018, show_top=True, n=10):
    passengers_year = passengers_df[passengers_df['Year'] == year].copy()
    population_year = population_df[population_df['year'] == year].copy()
    
    passengers_by_country = passengers_year.groupby('ISO3')['Total'].sum().reset_index()
    
    merged_data = passengers_by_country.merge(
        population_year[['country_code', 'value']], 
        left_on='ISO3', 
        right_on='country_code',
        how='inner'
    )
    
    merged_data['ratio'] = (merged_data['Total'] / merged_data['value']) * 1000000
    
    if show_top:
        selected_ratios = merged_data.nlargest(n, 'ratio')
        title_prefix = 'Mayor'
    else:
        selected_ratios = merged_data.nsmallest(n, 'ratio')
        title_prefix = 'Menor'
    
    plt.figure(figsize=(15, 8))
    bars = plt.bar(selected_ratios['ISO3'], selected_ratios['ratio'])
    plt.title(f'{n} Países con {title_prefix} Número de Pasajeros por Millón de Habitantes ({year})')
    plt.xlabel('Código de País')
    plt.ylabel('Pasajeros por Millón de Habitantes')
    plt.xticks(rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# Funcion para graficar la distribucion de viajes domesticos vs internacionales
def plot_domestic_international_distribution(df, year=2018, country_code=None):
    df_year = df[df['Year'] == year].copy()
    
    if country_code:
        df_year = df_year[df_year['ISO3'] == country_code]
        title_prefix = f'Distribución de Viajes Domésticos vs Internacionales para {country_code}'
    else:
        title_prefix = 'Distribución Global de Viajes Domésticos vs Internacionales'
    
    total_domestic = df_year['Domestic'].sum()
    total_international = df_year['International'].sum()
    
    plt.figure(figsize=(10, 8))
    sizes = [total_domestic, total_international]
    labels = ['Doméstico', 'Internacional']
    colors = ['#ff7777', '#4494ff']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, shadow=False, 
            wedgeprops={'edgecolor': 'white', 'linewidth': 2},
            textprops={'color': 'black', 'weight': 'bold'})
    plt.title(f'{title_prefix} ({year})', pad=20)
    plt.axis('equal')
    plt.show()

# Funcion para encontrar los paises con mas viajes domesticos
def find_extreme_domestic_countries(df, year=2018):
    df_year = df[df['Year'] == year].copy()
    
    country_stats = df_year.groupby('ISO3').agg({
        'Domestic': 'sum',
        'International': 'sum'
    }).reset_index()
    
    country_stats['Total'] = country_stats['Domestic'] + country_stats['International']
    
    min_passengers = 50000  
    min_percentage = 0.05 
    
    valid_countries = country_stats[
        (country_stats['Total'] >= min_passengers) &
        (country_stats['Domestic'] / country_stats['Total'] >= min_percentage) &
        (country_stats['International'] / country_stats['Total'] >= min_percentage)
    ]
    
    valid_countries['Domestic_Percentage'] = (valid_countries['Domestic'] / valid_countries['Total']) * 100
    
    most_domestic = valid_countries.nlargest(1, 'Domestic_Percentage')['ISO3'].iloc[0]
    least_domestic = valid_countries.nsmallest(1, 'Domestic_Percentage')['ISO3'].iloc[0]
    
    return most_domestic, least_domestic

# Analisis de viajes domesticos vs internacionales
def analyze_travel_distributions():
    most_domestic_country, least_domestic_country = find_extreme_domestic_countries(passengers_df)
    
    plt.figure(figsize=(24, 7))
    
    plt.subplot(1, 3, 1)
    plot_domestic_international_distribution(passengers_df)
    plt.subplot(1, 3, 2)
    plot_domestic_international_distribution(passengers_df, country_code=most_domestic_country)
    plt.subplot(1, 3, 3)
    plot_domestic_international_distribution(passengers_df, country_code=least_domestic_country)
    
    plt.tight_layout(pad=3.0, w_pad=4.0)
    plt.show()

# Funcion para graficar los paises con mas dias feriados
def plot_top_holiday_countries(holidays_df, year=2018, n=20):
    holidays_df['Date'] = pd.to_datetime(holidays_df['Date'])
    holidays_year = holidays_df[holidays_df['Date'].dt.year == year]
    
    holidays_count = holidays_year.groupby('ISO3').size().sort_values(ascending=False)
    top_n_countries = holidays_count.head(n)
    
    plt.figure(figsize=(12, 10))
    bars = plt.barh(top_n_countries.index, top_n_countries.values)
    plt.title(f'Top {n} Países por Número de Días Festivos ({year})')
    plt.xlabel('Número de Días Festivos')
    plt.ylabel('Código de País')
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2,
                f'{int(width)}',
                ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
# Analisis de dias festivos
plot_top_holiday_countries(holidays_df)
# Analisis de patrones de viaje
analyze_travel_distributions()
# Paises con mayor numero de pasajeros por millon de habitantes
plot_population_passenger_ratio(passengers_df, population_df, show_top=True)
# Paises con menor numero de pasajeros por millon de habitantes
plot_population_passenger_ratio(passengers_df, population_df, show_top=False)
# 10 paises por mas volumen de pasajeros
plot_top_10_countries(passengers_df)
# Analisis por estaciones
annual_stats, passengers_seasonal = analyze_seasonal_patterns(passengers_df, countries_df)
# Viajes Internacionales
plot_traffic_trends(annual_stats, 'international')
# Viajes domesticos
plot_traffic_trends(annual_stats, 'domestic')
# Viajes totales
plot_traffic_trends(annual_stats, 'total')
# Analisis de felicidad
average_happiness = analyze_happiness_correlation()