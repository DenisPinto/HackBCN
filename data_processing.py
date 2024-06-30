import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



flight_data = pd.read_csv('./Airlines.csv')
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

# Check =======================================
flight_data.info()
flight_data.head(20)



# Create new variables
np.random.seed(42)  #Set random seed
n_row = len(flight_data.iloc[:,0])

## Weather conditions
flight_data['Weather'] = 0
np.random.seed(42)  #Set random seed
### Different prob if there's delay or not
for i in range(n_row):
    if flight_data['Delay'][i] == 0:
        weather = np.random.choice(['sun','rain','snow','fog','storm'], 
                                                  1, p=[0.75,0.1,0.05,.05,.05])  # if there's NO delay, lower p for bad conditions 
        flight_data['Weather'][i] = str(weather[0])  # to avoid type error: np.ndarray, we convert the cell data to string
    elif flight_data['Delay'][i] == 1:
        weather = np.random.choice(['sun','rain','snow','fog','storm'], 
                                                  1, p=[0.2,0.5,0.1,.1,.1]) # if there's delay,  higher p for bad conditions
        flight_data['Weather'][i] = str(weather[0])  # to avoid type error: np.ndarray, we convert the cell data to string


## Seasonal factors
flight_data['Season'] = ''
np.random.seed(42)  #Set random seed
for i in range(n_row):
    # Set the season to winter if it snowed
    if flight_data['Weather'][i] == 'snow':
        flight_data['Season'][i] = str('Winter')
    # Else, random select season
    else:
        season = np.random.choice(['Spring', 'Summer', 'Autumn'], 1)
        flight_data['Season'][i] = str(season[0])


## Holidays
flight_data['Holiday'] = np.random.choice([0, 1], n_row, p=[0.9, 0.1]) # 10% of holiday probability,
                                                                       # 1 holiday every 10 flight days
flight_data['Holiday'].value_counts()


## Political factors
sanction_levels = ['No sanctions', 'Economic sanctions', 'Flight restrictions']
flight_data['Sanction_Level'] = np.random.choice(sanction_levels, n_row, p=[0.7, 0.2, 0.1]) # 70%, 20%, 10%

flight_data['Security_Alert'] = np.random.choice([0, 1], n_row, p=[0.95, 0.05])



## Airport condition
flight_data['Runway_Condition'] = np.random.choice(['Good', 'Fair', 'Poor'], n_row, p=[0.7, 0.2, 0.1])
flight_data['Operational_Issues'] = np.random.choice([0, 1], n_row, p=[0.95, 0.05])



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


# Create the Response variable
delay = pd.DataFrame(flight_data['Delay'])
flight_data.drop(columns=['Delay'], inplace=True)


# Final notes ==========================================================================
#  When doing the train_test_split, the column flight_data['Delay'] will be the y.
#  If necessary, extract the column with: delay = pd.DataFrame(flight_data['Delay'])
#  and remove it from the flight_data dataframe.

#  About training the models: if you have enough time, try to train them with the dummy
#  variables dataset but also with the original dataset (without dummy conversion)
# ======================================================================================









