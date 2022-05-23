# sqlalchemy-challenge
In this challenge, we are going to have a long holiday vacation in Honolulu, Hawaii.To help with our trip planning, we need to do some climate analysis on the area. The following sections outline the steps we must take to accomplish this task.

### Part 1: Climate Analysis and Exploration
In this section, Python and SQLAlchemy were used to perform basic climate analysis and data exploration of the climate database. The following tasks were completed by using SQLAlchemy ORM queries, Pandas, and Matplotlib.

Use the provided starter notebook and hawaii.sqlite files to complete your climate analysis and data exploration.

Use SQLAlchemy’s create_engine to connect to your SQLite database.

Use SQLAlchemy’s automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

Link Python to the database by creating a SQLAlchemy session.
#### Precipitation Analysis
To perform an analysis of precipitation in the area, do the following:

Find the most recent date in the dataset.

Using this date, retrieve the previous 12 months of precipitation data by querying the 12 previous months of data. Note: Do not pass in the date as a variable to your query.

Select only the date and prcp values.

Load the query results into a Pandas DataFrame, and set the index to the date column.

Sort the DataFrame values by date.

Plot the results by using the DataFrame plot method, as shown in the following image:
![prcp_12m](https://user-images.githubusercontent.com/100816322/169881759-23ddfbdc-0772-49cc-a5b2-ca593b2a20d7.png)

Use Pandas to print the summary statistics for the precipitation data.

#### Station Analysis
To perform an analysis of stations in the area, do the following:

Design a query to calculate the total number of stations in the dataset.

Design a query to find the most active stations (the stations with the most rows).

List the stations and observation counts in descending order.

Which station id has the highest number of observations?

Using the most active station id, calculate the lowest, highest, and average temperatures.

Hint: You will need to use functions such as func.min, func.max, func.avg, and func.count in your queries.

Design a query to retrieve the previous 12 months of temperature observation data (TOBS).

Filter by the station with the highest number of observations.

Query the previous 12 months of temperature observation data for this station.

Plot the results as a histogram with bins=12, as shown in the following image:
![tobs_plot](https://user-images.githubusercontent.com/100816322/169881961-f4290baa-3e04-46e8-a8a2-5bbe97dedae3.png)

### Part 2: Design Your Climate App
In this section, a Flask API was designed based on the queries that you have just developed.
Use Flask to create your routes, as follows:

Homepage: List all available routes.

<img width="285" alt="homepage" src="https://user-images.githubusercontent.com/100816322/169882312-1219d266-818e-4a6f-81fd-a0386d8e5ba5.PNG">

/api/v1.0/precipitation

Convert the query results to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.

/api/v1.0/stations
Return a JSON list of stations from the dataset.

/api/v1.0/tobs
Query the dates and temperature observations of the most active station for the previous year of data.
Return a JSON list of temperature observations (TOBS) for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).

### Bonus: Other Recommended Analyses

  Use the provided temp_analysis_bonus_1_starter.ipynb and temp_analysis_bonus_2_starter.ipynb starter notebooks for their respective bonus challenge.


#### Temperature Analysis 1

  Conduct an analysis to answer the following question: Hawaii is reputed to enjoy mild weather all year round. Is there a meaningful difference between the temperatures in, for example, June and December?

  Use Pandas to perform the following steps:

 Convert the date column format from string to datetime.

 Set the date column as the DataFrame index.

  Drop the date column.

  Identify the average temperature in June at all stations across all available years in the dataset. Do the same for the temperature in December.
Use the t-test to determine whether the difference in means, if any, is statistically significant. Will you use a paired t-test or an unpaired t-test? Why?

##### The t test tells you how significant the differences between group means are. It lets you know if those differences in means could have happened by chance. A paired t-test is designed to compare the means of the same group or item under two separate scenarios. An unpaired t-test compares the means of two independent or unrelated groups.
  
##### In this analysis, unpaired t-test is used because the means of two independent groups are compared. The temprature in June and December are the data of two independent groups. The pvalue of 3.90 is higher than 0.05, and indicated the result is non-significant.

#### Temperature Analysis 2

Using historical data in the dataset, find out what the temperature has previously been from August 1 to August 7.
Note: The starter notebook contains a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d. The function will return the minimum, average, and maximum temperatures for that range of dates.

Complete the following steps:

Use the calc_temps function to calculate the minimum, average, and maximum temperatures for your trip using the matching dates from a previous year (for example, use "2017-08-01").

Plot the minimum, average, and maximum temperature from your previous query as a bar chart, as captured in the following steps and image:
Use "Trip Avg Temp" as the title.
Use the average temperature as the bar height (y value).
Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

  ![tripavgplot](https://user-images.githubusercontent.com/100816322/169883113-99a32733-47b4-4c2c-95c5-f1300d576341.png)

#### Daily Rainfall Average
We also need to know what the rainfal has been. The following steps were completed:

Calculate the rainfall per weather station using the previous year's matching dates.

Sort this in descending order by precipitation amount, and list the station, name, latitude, longitude, and elevation.

### Daily Temperature Normals
Calculate the daily normals for the duration of the trip. Normals are the averages for the minimum, average, and maximum temperatures.
You are provided with a function called daily_normals that will calculate the daily normals for a specific date. This date string will be in the format %m-%d. Make sure to use all historic TOBS that match that date string.

Use Pandas to plot an area plot (stacked=False) for the daily normals, as shown in the following image:

  ![trip_plot](https://user-images.githubusercontent.com/100816322/169883370-978a7961-c76b-47f6-a38c-198d33fef51e.png)

References
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://doi.org/10.1175/JTECH-D-11-00103.1

© 2022 Trilogy Education Services, a 2U, Inc. brand. All Rights Reserved.
