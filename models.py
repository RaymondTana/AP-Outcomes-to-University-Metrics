import pandas as pd
from geopy.geocoders import Nominatim
from sklearn.ensemble import RandomForestRegressor
import joblib

N_CORES = joblib.cpu_count(only_physical_cores=True)

def wisconsin_pred_2023_24(lat, long):
    inc_pop = pd.read_csv('data/County_Income_Population_2023.csv')
    training = pd.read_csv('data/Wisconsin/train_test_split/training.csv')
    wisconsin_data = pd.read_csv('data/Wisconsin/train_test_split/Wisconsin_closest_five_method.csv')
    variables = training.columns[9:]
    X_train = training[variables]
    y_train = training['PERCENT_3_OR_ABOVE']
    random_forest = RandomForestRegressor(min_samples_leaf=5, random_state=0, n_jobs=N_CORES)
    random_forest.fit(X_train,y_train)
    location = geolocator.reverse(str(lat)+','+str(long))
    if location.raw.get('address').get('country') == 'United States' and location.raw.get('address').get('state') == 'Wisconsin':
        county = location.raw.get('address').get('county').rsplit(' ', 1)[0]
        state = location.raw.get('address').get('ISO3166-2-lvl4')[-2:]
        pci = inc_pop[(inc_pop.County == county) & (inc_pop.State_Abbreviation == state)]
        inc = int(pci.Income.values[0])
        pop = int(pci.Population.values[0])
        row = wisconsin_data[wisconsin_data.COUNTY == county][wisconsin_data.columns[9:]].iloc[0]
        row = pd.DataFrame(row).T
        row['population'] = pop
        row['per_capita_income'] = inc
        return random_forest.predict(row)#pd.DataFrame(row).T #inc_pop[(inc_pop.County == county) & (inc_pop.State_Abbreviation == state)]
    else:
        return "Invalid coordinates"