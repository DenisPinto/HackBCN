import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



flight_data = pd.read_csv('Airlines.csv', nrows=50000)
flight_data.info()


# Check NAs and drop if necessary
flight_data.isna().sum()
''' 
print('Num rows to drop: ', len(flight_data)-len(flight_data.dropna()))
flight_data = flight_data.dropna()
'''
# Total number of registered delayed and non delayed flights
no_delay = (flight_data['Delay'] == 0).sum()
delay = (flight_data['Delay'] == 1).sum()
print('Total flights: ', len(flight_data.iloc[:,0]),
      '\nNumber of non-delayed flights: ', no_delay, 
      '\nNumber of delayed flights: ', delay)

sns.countplot(data=flight_data, x='Delay')
plt.show()


# Number of registered delayed flight per weekday
flight_data.groupby('DayOfWeek')['Delay'].value_counts()
delay_per_day = flight_data.groupby('DayOfWeek')['Delay'].sum().reset_index()
delay_per_day.head()
sns.barplot(data=delay_per_day, x='DayOfWeek', y='Delay')
plt.title('Number of delayed flight per weekday\n')
plt.show()


# Flights per airline
sns.countplot(data=flight_data, x='Airline', hue='Delay')
plt.title('Delayed and non-delayed flights per Airline')
plt.show()


# Drop useless columns
flight_data.drop(columns=['id','Time','Length'], inplace=True)



# Create a route variable from departure and destination airport
flight_data['Route'] = flight_data['AirportFrom'] + '-' + flight_data['AirportTo']



# Check =======================================
flight_data.info()
flight_data.head(20)



# Create new variables

#Set random seed
np.random.seed(42)  

n_row = len(flight_data.iloc[:,0])

## Weather conditions
probs_delay_0 = [0.75, 0.1, 0.05, 0.05, 0.05]
probs_delay_1 = [0.2, 0.5, 0.1, 0.1, 0.1]
weather_0 = np.random.choice(['sun', 'rain', 'snow', 'fog', 'storm'], len(flight_data), p=probs_delay_0)
weather_1 = np.random.choice(['sun', 'rain', 'snow', 'fog', 'storm'], len(flight_data), p=probs_delay_1)
flight_data['Weather'] = np.where(flight_data['Delay'] == 0, weather_0, weather_1)


## Holidays
flight_data['Holiday'] = np.random.choice([0, 1], n_row, p=[0.9, 0.1]) # 10% of holiday probability,
                                                                       # 1 holiday every 10 flight days
flight_data['Holiday'].value_counts()


## Political factors
sanction_levels = ['No sanctions', 'Economic sanctions', 'Flight restrictions']
flight_data['Sanction_Level'] = np.random.choice(sanction_levels, n_row, p=[0.7, 0.2, 0.1]) # 70%, 20%, 10%

# Check =======================================
flight_data.info()
flight_data.head()


# Create dummy variables
## Get the non-numerical columns
columns = flight_data.columns
to_dummies = []
for column in columns:
    if flight_data[column].dtype == 'O':
        to_dummies.append(column)

## Create the dummy variables
for column in to_dummies:
    print(f'Converting {column} column')
    flight_data = pd.get_dummies(flight_data, columns=[column], dtype=int)


flight_data.to_csv('Airlines_with_dummies.csv', index=False)










