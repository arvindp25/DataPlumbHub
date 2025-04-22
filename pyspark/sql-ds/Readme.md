1. Most Consistent Commuter Stations

Dataset: bigquery-public-data.new_york_citibike.citibike_trips

    Find the top 3 stations with the lowest standard deviation in daily trip counts (i.e., consistent usage) in 2019.
    Return:

        start_station_name

        std_dev_trips_per_day
        Consider only stations with at least 200 days of usage and a minimum of 50 trips per day on average.
        Solution:- citibike_trips.py

2. Busiest Hour by Borough

Dataset: bigquery-public-data.austin_bikeshare.bikeshare_trips
Join with: bigquery-public-data.austin_bikeshare.bikeshare_stations

    For each Austin borough (if borough exists or approximate via city), determine the hour of the day (0–23) with the most trip starts.
    Return:

        borough

        hour_of_day

        total_trips

3. Revenue Leakage in Open Payments

Dataset: bigquery-public-data.cms_open_payments.general_payment_data

    Find the top 5 doctors (physician name) who received payments in more than 10 different states but never had a payment value over $500.
    Return:

        physician_name

        distinct_states

        total_payment_amount

4. Most Active StackOverflow Tags

Dataset: bigquery-public-data.stackoverflow.posts_questions

    Find the top 10 tags used in questions that had over 5 answers and an average score > 2.
    Use the tags column (semi-colon separated).
    Return:

        tag

        question_count

        avg_score

5. Longest Average Delay by Airline

Dataset: bigquery-public-data.faa.us_delay_causes

    Find the airline (carrier) with the highest average departure delay in minutes (use dep_delay),
    but only consider flights with more than 1000 entries and average weather delay < 5 minutes.
    Return:

        carrier

        avg_dep_delay

        flight_count

Let me know if you'd like hints, solutions, or want me to generate data for testing on your cluster!