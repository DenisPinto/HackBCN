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
np.random.seed(42)
n_row = len(flight_data[:,0])
## Weather conditions
flight_data['Weather'] = np.random.choice(['snow','rain','sun',
                                           'fog','storm'], n_row)


## Seasonal factors
flight_data['Season'] = np.random.choice(['Winter', 'Spring', 'Summer', 'Autumn'], n_row)


## Holidays
flight_data['Holiday'] = np.random.choice([0, 1], n_row, p=[0.9, 0.1]) # 10% of holiday probability, 1 holiday every 10 flight days


## Political factors
sanction_levels = ['No sanctions', 'Economic sanctions', 'Flight restrictions']
flight_data['Sanction_Level'] = np.random.choice(sancion_levels, n_row, p=[0.7, 0.2, 0.1]) # 70%, 20%, 10%

flight_data['Security_Alert'] = np.random.choice([0, 1], n_row, p=[0.95, 0.05])



## Airport condition
flight_data['Runway_Condition'] = np.random.choice(['Good', 'Fair', 'Poor'], n_row, p=[0.7, 0.2, 0.1])
flight_data['Operational_Issues'] = np.random.choice([0, 1], n_row, p=[0.95, 0.05])


airlines = flight_data['Airline'].unique()


flight_dummy = pd.get_dummies(flight_data,
                              columns=['Airline','Flight',])


flight_data['AirportFrom'][0]+'-'+flight_data['AirportTo'][0]













