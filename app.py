import streamlit as st
import pickle
import numpy as np
import pandas as pd


# Load saved model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Mapping dictionaries
hotel_map = {'Resort Hotel': 0, 'City Hotel': 1}
meal_map = {'BB': 0, 'FB': 1, 'HB': 2, 'SC': 3, 'Undefined': 4}
market_segment_map = {
    'Corporate': 0, 'Online TA': 1, 'Direct': 2, 'Offline TA/TO': 3,
    'Groups': 4, 'Complementary': 5, 'Aviation': 6}
distribution_channel_map = {'Corporate': 0, 'TA/TO': 1, 'Direct': 2, 'GDS': 3}
reserved_room_type_map = {k: i for i, k in enumerate(['A', 'C', 'D', 'E', 'G', 'F', 'H', 'B'])}
assigned_room_type_map = {k: i for i, k in enumerate(['A', 'C', 'D', 'E', 'G', 'F', 'I', 'B', 'H', 'K'])}
deposit_type_map = {'No Deposit': 0, 'Refundable': 1, 'Non Refund': 2}
customer_type_map = {'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3}

# Full list of countries for dropdown
country_list = ['GBR', 'PRT', 'USA', 'ESP', 'IRL', 'ROU', 'NOR', 'OMN', 'ARG',
       'POL', 'DEU', 'FRA', 'BEL', 'CHE', 'CN', 'GRC', 'ITA', 'DNK',
       'RUS', 'SWE', 'AUS', 'EST', 'CZE', 'BRA', 'FIN', 'MOZ', 'BWA',
       'LUX', 'NLD', 'SVN', 'ALB', 'IND', 'CHN', 'MEX', 'MAR', 'UKR',
       'LVA', 'PRI', 'SRB', 'CHL', 'AUT', 'BLR', 'LTU', 'TUR', 'ZAF',
       'CYM', 'ZMB', 'ZWE', 'DZA', 'KOR', 'CRI', 'HUN', 'ARE', 'TUN',
       'JAM', 'HRV', 'HKG', 'ISR', 'IRN', 'GEO', 'AND', 'GIB', 'URY',
       'JEY', 'CAF', 'CYP', 'COL', 'GGY', 'KWT', 'NGA', 'MDV', 'VEN',
       'SVK', 'AGO', 'FJI', 'KAZ', 'PAK', 'IDN', 'LBN', 'PHL', 'SEN',
       'SYC', 'AZE', 'BHR', 'NZL', 'THA', 'DOM', 'MKD', 'MYS', 'ARM',
       'JPN', 'LKA', 'CUB', 'CMR', 'MUS', 'COM', 'SUR', 'UGA', 'BGR',
       'CIV', 'JOR', 'SYR', 'SGP', 'BDI', 'SAU', 'VNM', 'PLW', 'QAT',
       'EGY', 'PER', 'MLT', 'MWI', 'ISL', 'ECU', 'NPL', 'CPV', 'BHS',
       'MAC', 'TGO', 'TWN', 'DJI', 'KNA', 'ETH', 'IRQ', 'HND', 'RWA',
       'KHM', 'MCO', 'BGD', 'UZB', 'IMN', 'TJK', 'NIC', 'BEN', 'VGB',
       'TZA', 'GAB', 'BIH', 'GHA', 'TMP', 'GLP', 'KEN', 'LIE', 'GNB',
       'MNE', 'UMI', 'MYT', 'FRO', 'MMR', 'PAN', 'BFA', 'LBY', 'MLI',
       'NAM', 'BOL', 'PRY', 'BRB', 'ABW', 'AIA', 'SLV', 'DMA', 'PYF',
       'GUY', 'LCA', 'ATA', 'GTM', 'ASM', 'MRT', 'NCL', 'KIR', 'SDN',
       'ATF', 'SLE', 'LAO']
country_map = {country: idx for idx, country in enumerate(country_list)}

# Streamlit UI
st.title("Hotel Booking Cancellation Predictor")

# Collect inputs
hotel = st.selectbox("Hotel", list(hotel_map.keys()))
lead_time = st.number_input("Lead Time", step=1)
adults = st.number_input("Adults", step=1)
meal = st.selectbox("Meal", list(meal_map.keys()))
country = st.selectbox("Country", country_list)
market_segment = st.selectbox("Market Segment", list(market_segment_map.keys()))
distribution_channel = st.selectbox("Distribution Channel", list(distribution_channel_map.keys()))
previous_cancellations = st.number_input("Previous Cancellations", step=1)
reserved_room_type = st.selectbox("Reserved Room Type", list(reserved_room_type_map.keys()))
assigned_room_type = st.selectbox("Assigned Room Type", list(assigned_room_type_map.keys()))
deposit_type = st.selectbox("Deposit Type", list(deposit_type_map.keys()))
days_in_waiting_list = st.number_input("Days in Waiting List", step=1)
customer_type = st.selectbox("Customer Type", list(customer_type_map.keys()))
adr = st.number_input("Average Daily Rate", step=0.1)
total_of_special_requests = st.number_input("Total Special Requests", step=1)

# Predict
if st.button("Predict"):
    # Map categorical inputs
    data = [
        hotel_map[hotel],
        lead_time,
        adults,
        meal_map[meal],
        country_map.get(country, -1),  # default to -1 if not found
        market_segment_map[market_segment],
        distribution_channel_map[distribution_channel],
        previous_cancellations,
        reserved_room_type_map[reserved_room_type],
        assigned_room_type_map[assigned_room_type],
        deposit_type_map[deposit_type],
        days_in_waiting_list,
        customer_type_map[customer_type],
        adr,
        total_of_special_requests]

    input_array = np.array([data])  # 2D array for prediction
    prediction = model.predict(input_array)[0]
    result = "Canceled" if prediction == 1 else "Not Canceled"
    st.subheader(f"Prediction: {result}")