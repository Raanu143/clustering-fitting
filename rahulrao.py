# -*- coding: utf-8 -*-
"""Rahul_assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15ckZNiVjo-s16dG-0-F8hLbs1_7112Aj
"""

# importing all the important libraries. 

# it is python library which is used to work with datasets.
import pandas as PD 
# it is python library which is used to work with arrays.
import numpy as np 
# K-means is a way to group data points without being told what to do. The algorithm divides the data points in to the K clusters by reducing the amount of difference between each cluster.
from sklearn.cluster import KMeans  
import matplotlib.pyplot as plots

# importing warnings.
import warnings 
warnings.filterwarnings('ignore')

"""# K Means Clustering"""

# Creates the function for analyse the dataset.
def read_dataset(new_file):
    electricity_data = PD.read_csv(new_file, skiprows=4) # using pandas read data and skip starting 4 rows from data.
    electricity_data1 = electricity_data.drop(['Unnamed: 66', 'Indicator Code',  'Country Code'],axis=1) # dropping the columns.
    electricity_data2 = electricity_data1.set_index("Country Name")  
    electricity_data2=electricity_data2.T 
    electricity_data2.reset_index(inplace=True) 
    electricity_data2.rename(columns = {'index':'Year'}, inplace = True) 
    return electricity_data1, electricity_data2 

# define the path of electricity data.
new_file = '/content/drive/MyDrive/Rahul Assignment/API_EG.ELC.ACCS.ZS_DS2_en_csv_v2_4771419.csv'  
Final_Dataset, Transpose_data = read_dataset(new_file)   
Final_Dataset.head() # showing starting rows.

Transpose_data.head()

# Extracting 20 years of data with the help of function.
def Final_Dataset2(Final_Dataset): 
    Final_Dataset1 = Final_Dataset[['Country Name', 'Indicator Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                                    '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']] 
    Final_Dataset2 = Final_Dataset1.dropna() # drop null values from data.
    return Final_Dataset2

# calling the function to extract the data. 
Final_Dataset3 = Final_Dataset2(Final_Dataset) 
Final_Dataset3.head(10) # shows starting rows from data.

# check shape of data.
Final_Dataset3.shape

# check null values from data.
Final_Dataset3.isnull().sum()

# importing label encoder from scikit learn. 
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()# define classifier for encoder.
Final_Dataset3['Country Name'] = encoder.fit_transform(Final_Dataset3['Country Name']) 
Final_Dataset3.head(10) # showing 5 rows from data.

X = Final_Dataset3.drop(['Country Name','Indicator Name'], axis=1)
y = Final_Dataset3['Country Name']  

# importing minmax scaler for normalize the data.
from sklearn.preprocessing import MinMaxScaler
Min_max_scaler = MinMaxScaler()# define classifier.
Min_max_scaled = Min_max_scaler.fit_transform(X)# fit classifier with data.

"""# Elbow Method """

# using the elbow method to find out the clusters.
from scipy.spatial.distance import cdist 
Cluster = range(10) 
Meandist = list()

for k in Cluster:
    model = KMeans(n_clusters=k+1) 
    model.fit(Min_max_scaled) 
    Meandist.append(sum(np.min(cdist(Min_max_scaled, model.cluster_centers_, 'euclidean'), axis=1)) / Min_max_scaled.shape[0]) 

# setting all the parameter and ploting the graph.

# define font size.
plots.rcParams.update({'font.size': 20})
# define figure size.
plots.figure(figsize=(10,7))
# set parameter for graph.
plots.plot(Cluster, Meandist, marker="o") 
# define xlabel.
plots.xlabel('Numbers of Clusters')
# define ylabel.
plots.ylabel('Average distance') 
# define title for graph.
plots.title('Choosing k with the Elbow Method');

# define classifier for clustering.
k_means_model = KMeans(n_clusters=3, max_iter=100, n_init=10,random_state=10)
# fit classifier with data.  
k_means_model.fit(Min_max_scaled) 
# predict model to getting the label.
predictions = k_means_model.predict(Min_max_scaled)

predictions

# define color for all clusters.
color_map = {0 : 'r', 1 : 'b', 2 : 'g'} 
def color(x):  
    return color_map[x]  
colors = list(map(color, k_means_model.labels_))   

# plotting the graph.

# define font size.
plots.rcParams.update({'font.size': 20})
# define figure size.
plots.figure(figsize=(10,7))
# set parameter for scatter plot.
plots.scatter(x=X.iloc[:,0], y=X.iloc[:,2], c=colors)  
# define xlabel.
plots.xlabel('2000')
# define ylabel.  
plots.ylabel('2002') 
# define title for graph. 
plots.title('Scatter plot for 3 Clusters');

# Getting the Centroids and label.
centroids = k_means_model.cluster_centers_
u_labels = np.unique(predictions) 
centroids

# plotting the results.
plots.figure(figsize=(10,7))
for i in u_labels:
    plots.scatter(Min_max_scaled[predictions == i , 0] , Min_max_scaled[predictions == i , 1] , label = i)  

# define parameter for graph like color, data etc.
plots.scatter(centroids[:,0] , centroids[:,1] , s = 40, color = 'r') 
# define xlabel.
plots.xlabel('2000')
# define ylabel.
plots.ylabel('2002')
# define title for graphs.
plots.title('Scatter plot for 3 Clusters with Centroids') 
# define legend for graph.
plots.legend()  
plots.show()

# creating the lists to extract all the cluster.
first_cluster=[]
second_cluster=[] 
third_cluster=[] 

# with the help of loop find out the data availabel in each cluster.
for i in range(len(predictions)):
    if predictions[i]==0:
        first_cluster.append(Final_Dataset.loc[i]['Country Name']) 
    elif predictions[i]==1:
        second_cluster.append(Final_Dataset.loc[i]['Country Name'])
    else:
        third_cluster.append(Final_Dataset.loc[i]['Country Name'])

# showing the data present in first cluster.
First_cluster = np.array(first_cluster)
print(First_cluster)

# showing the data present in second cluster.
Second_cluster = np.array(second_cluster)
print(Second_cluster)

# showing the data present in third cluster.
Third_cluster = np.array(third_cluster)
print(Third_cluster)

first_cluster = First_cluster[3] 
print('Country name :', first_cluster)
arab_country = Final_Dataset3[Final_Dataset3['Country Name']==8]  
arab_country = np.array(arab_country)  
arab_country = np.delete(arab_country,1) 
arab_country

second_cluster = Second_cluster[0] 
print('Country name :', second_cluster) 
afganistan_country = Final_Dataset3[Final_Dataset3['Country Name']==0] 
afganistan_country = np.array(afganistan_country)  
afganistan_country = np.delete(afganistan_country,1) 
afganistan_country

third_cluster = Third_cluster[0] 
print('Country name :', third_cluster) 
africa_country = Final_Dataset3[Final_Dataset3['Country Name']==1] 
africa_country= np.array(africa_country)  
africa_country = np.delete(africa_country,1) 
africa_country

# plotting the line graph for different clusters.
year=list(range(2000,2022))
# define figure size for graph.
plots.figure(figsize=(22,8))

plots.subplot(131)
plots.xlabel('Years')
plots.ylabel('Electricity Consumption') 
plots.title('Arab World Country') 
plots.plot(year,arab_country, color='g');

plots.subplot(132)
plots.xlabel('Years')
plots.ylabel('Electricity Consumption') 
plots.title('Afghanistan Country') 
plots.plot(year,afganistan_country);

plots.subplot(133) 
plots.xlabel('Years') 
plots.ylabel('Electricity Consumption')
plots.title('Africa Eastern and Southern Country') 
plots.plot(year,africa_country, color='r');

"""# Curve Fitting"""

# Creating the function for analyse the dataset.
def read_dataset(File): 
    co2_data = PD.read_csv(File, skiprows=4) #dataset reading with pandas. 
    co2_data1 = co2_data.drop(['Unnamed: 66', 'Indicator Code',  'Country Code'],axis=1) # dropping some column from dataset.
    co2_data2 = co2_data1.fillna(co2_data1.mean()) # fill the mean of data in column.
    co2_data3 = co2_data2.set_index("Country Name")  
    co2_data3 = co2_data3.T 
    co2_data3.reset_index(inplace=True) 
    co2_data3.rename(columns = {'index':'Year'}, inplace = True)
    return co2_data2, co2_data3  

# define the path of co2 emission data.
File = '/content/drive/MyDrive/Rahul Assignment/API_19_DS2_en_csv_v2_4773766.csv'  
co2_Dataset, transpose_data = read_dataset(File)  
co2_Dataset.head() # print starting 5 rows of data.

transpose_data

# check shape of data.
co2_Dataset.shape

# check null values in data.
co2_Dataset.isnull().sum()

# selecting all columns and convert into array.
x = np.array(co2_Dataset.columns) 
# dropping some columns.
x = np.delete(x,0) 
x = np.delete(x,0) 
# convert data type as int.
x = x.astype(np.int)

# selecting all the data for urban population and india.
curve_fit = co2_Dataset[(co2_Dataset['Indicator Name']=='Urban population') & (co2_Dataset['Country Name']=='India')]   

# convert into array.
y = curve_fit.to_numpy() 
# dropping some columns.
y = np.delete(y,0) 
y = np.delete(y,0)
# convert data type as int.
y = y.astype(np.int)

# import scipy.
import scipy
# it is python library which is used to work with arrays.
import numpy as np 
# importing curve fit from scipy.
from scipy.optimize import curve_fit
# Matplotlib is a Python library that lets you make rigid, animated, and interactive visualisations. Matplotlib makes things that are easy and things that are hard possible.
import matplotlib.pyplot as plots
from scipy import stats 

# Define the function to be fitted (linear function y = mx + c)
def linear_func(x, m, c):
    return m*x + c

def create_curve_fit(x,y): 

    # Perform curve fitting
    popt, pcov = curve_fit(linear_func, x, y) 

    # Extract the fitted parameters and their standard errors
    m, c = popt
    m_err, c_err = np.sqrt(np.diag(pcov)) 

    # Calculate the lower and upper limits of the confidence range
    conf_int = 0.95  # set the confidence interval as 95%
    alpha = 1.0 - conf_int 
    m_low, m_high = scipy.stats.t.interval(alpha, len(x)-2, loc=m, scale=m_err)
    c_low, c_high = scipy.stats.t.interval(alpha, len(x)-2, loc=c, scale=c_err)

    # Plot the best-fitting function and the confidence range.
    plots.figure(figsize=(12,6)) #define figure size.
    plots.rcParams.update({'font.size': 20}) #define fontsize.
    plots.plot(x, y, 'bo', label='Data') #set data for graph.
    plots.plot(x, linear_func(x, m, c), 'g', label='Fitted function')
    plots.fill_between(x, linear_func(x, m_low, c_low), linear_func(x, m_high, c_high), color='gray', alpha=0.5, label='Confidence range') # set all the parameter.
    plots.title('Curve Fitting') # define title for graph.
    plots.xlabel('Years') # define xlabel.
    plots.ylabel('Population') # define ylabel. 
    plots.legend() # set legend in graph.
    plots.show()

create_curve_fit(x,y)

