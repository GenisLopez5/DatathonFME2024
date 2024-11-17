# %% [markdown]
# **Creació dels arrays de test i fit**

# %%
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

Train = pd.read_csv("train_final.csv", low_memory=False)
y_train = Train['Listing.Price.ClosePrice'] # preu dels train
x_train = Train.drop('Listing.Price.ClosePrice', axis=1) # valors excepte el train 

x_test = pd.read_csv("test_final.csv", low_memory=False)
x_test = x_test.reindex(columns=x_train.columns, fill_value=0) #align columns with the train

# %%
modelRF = RandomForestRegressor(n_estimators=100)
modelRF.fit(x_train, y_train)
y_pred = modelRF.predict(x_test)

result = x_test['Listing.ListingId']
result = pd.concat([result, y_pred])

result




# %%
y_pred


