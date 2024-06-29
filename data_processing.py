import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



flight_data = pd.read_csv('C:/Users/rapid/Desktop/HackBCN/Airlines.csv')
flight_data.info()


# Check NAs and drop if necessary
flight_data.isna().sum()
''' 
print('Num rows to drop: ', len(flight_data)-len(flight_data.dropna()))
flight_data = flight_data.dropna()
'''
# Total number of registered delayed and no delyed flights
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
flight_data['Route'] = ''
for i in range(len(flight_data['Airline'])):
    flight_data['Route'][i] = flight_data['AirportFrom'][i]+'-'+flight_data['AirportTo'][i]

# Check
flight_data.info()
flight_data.head()

# Create new variables
n_row = len(flight_data[:,0])
## Weather conditions
flight_data['Weather'] = np.random.choice(['snow','rain','sun',
                                           'fog','storm'], n_row)


## Seasonal factors



## Holidays



## Political factors



## Airport condition




airlines = flight_data['Airline'].unique()


flight_dummy = pd.get_dummies(flight_data,
                              columns=['Airline','Flight',])


flight_data['AirportFrom'][0]+'-'+flight_data['AirportTo'][0]













