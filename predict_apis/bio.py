# %%
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression  
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import PolynomialFeatures

# %%
data_0 = pd.read_excel(r"agstar-livestock-ad-database-combined.xlsx")
data_0.head()

# %%
columns_to_drop = ['Project Name', 'Cluster Name', 'Project Type', 'City', 'County', 'State', 'Status', 'Year Operational', 'Electricity Generated (kWh/yr)', 'Biogas End Use(s)', 'LCFS Pathway?', 'System Designer(s)/Developer(s) and Affiliates', 'Receiving Utility', 'Awarded USDA Funding?', 'Sheet', 'Year Shutdown', 'Reason for Closure']
data_0.drop(columns=columns_to_drop, inplace=True)

# %%
data_0.head()

# %%
columns_to_drop = ['Co-Digestion']
data_0.drop(columns=columns_to_drop, inplace=True)
data_0.head()

# %%
data_0['Quantity'] = data_0[['Cattle', 'Dairy', 'Poultry', 'Swine']].sum(axis=1)

# %%
data_0.head()

# %%
data_0.fillna(0, inplace=True)

# %%
data_0.head()

# %%
data_0['Total waste kg/day']= (data_0['Cattle'] *36.9) +\
                                (data_0['Dairy'] *68) +\
                                (data_0['Poultry'] *0.28)+\
                                 (data_0['Swine'] *5.7)
data_0[['Cattle', 'Dairy', 'Poultry', 'Swine', 'Total waste kg/day']].head()

# %%
data_0.head()

# %%
columns_to_drop = ['Total Emission Reductions (MTCO2e/yr)', 'Cattle', 'Dairy', 'Poultry', 'Swine']
data_0.drop(columns=columns_to_drop, inplace=True)
data_0.head()

# %%
data_0.isnull().sum()

# %%
data_1 = data_0.dropna()
data_1.head()

# %%
data_1 = data_1[data_1['Biogas Generation Estimate (cu-ft/day)'] != 0.0]

# %%
data_1.head()

# %%
data_1.shape

# %%
columns_to_drop = ['Animal/Farm Type(s)']
data_1.drop(columns=columns_to_drop, inplace=True)

# %%
data_1['Digester Type'].value_counts().plot(kind='bar')

# %%
# Specify the column name and the list of values to be deleted
column_name = 'Digester Type'
values_to_delete = ['Induced Blanket Reactor', 'Fixed Film/Attached Media', 'Modular Plug Flow', 'Unknown or Unspecified', 'Vertical Plug Flow', 'Plug Flow - Unspecified']

# Filter out the rows
data_1 = data_1[~data_1[column_name].isin(values_to_delete)]

# %%
data_1['Digester Type'].value_counts().plot(kind='bar')

# %%
#data_1['Animal/Farm Type(s)'].value_counts().plot(kind='bar')

# %%
#data_1 = data_1[data_1['Digester Type'] != '4, 2, 6, 8, 9, 7']

# %%
#data_1['Digester Type'].value_counts().plot(kind='bar')

# %% [markdown]
# # Encoding 

# %%
le = preprocessing.LabelEncoder()
Digester_Type = le.fit_transform(data_1['Digester Type'])

# %%
#le = preprocessing.LabelEncoder()
#Animal_Type = le.fit_transform(data_1['Animal/Farm Type(s)'])

# %%
data_1.iloc[:, 0] = Digester_Type

# %%
#data_1.iloc[:, 1] = Animal_Type

# %%
data_1.head()

# %% [markdown]
# # Split Dataset into Training and Test dataset

# %%
features_bio = ['Digester Type', 'Total waste kg/day']
x = data_1[features_bio]
y = data_1['Biogas Generation Estimate (cu-ft/day)']

# %%
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

# %%
# help(train_test_split)

# %%
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense

# Initialize the ANN with an Input layer
model = Sequential()

# Add the Input layer with 3 input features
model.add(Input(shape=(2,)))

# Add the first hidden layer (10 neurons)
model.add(Dense(units=10, activation='relu'))

# Add the second hidden layer (10 neurons)
model.add(Dense(units=10, activation='relu'))

# Add the second hidden layer (10 neurons)
model.add(Dense(units=10, activation='relu'))

# Add the output layer (1 neuron for regression)
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')


# %%
'''
# Transform my x data to include polynomial features
# After splitting
poly = PolynomialFeatures(degree=1)

# Transform the training data
x_train_poly = poly.fit_transform(x_train)

# Transform the testing data
x_test_poly = poly.transform(x_test)'''

# %% [markdown]
# # Model Training

# %%
#model_R = LinearRegression()
#model_R.fit(x_train, y_train)
#model_R.fit(x_train_poly, y_train)
# Train the model
model.fit(x_train, y_train, epochs=100, batch_size=10)


# %%
#y_pred = model_R.predict(x_test_poly)
#print(y_pred)
# Predict on the test set
y_pred = model.predict(x_test)

# Evaluate the model
mse = model.evaluate(x_test, y_test)
print(f"Mean Squared Error: {mse}")


# %%


# %%
from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)
print(f"R-squared: {r2}")

# %%
test_loss = model.evaluate(x_test, y_test, verbose=1)
print(f"Test loss: {test_loss}")

model.save('trained_model.keras')
# %%
'''from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")'''

# %%
'''from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean squared Error: {mse}")'''

# %%
'''rmse = mse ** 0.5
print(f"Root Mean Squared Error: {rmse}")'''

# %%
'''residuals = y_test - y_pred
plt.scatter(y_pred, residuals)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Values')
plt.show()'''

# %%



