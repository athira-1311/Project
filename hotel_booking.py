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
reserved_room_type_map = {k: i for i, k in enumerate(['A', 'B','C', 'D', 'E', 'F','G','H'])}
assigned_room_type_map = {k: i for i, k in enumerate(['A', 'B','C', 'D', 'E', 'F','G' , 'I','H', 'K'])}
deposit_type_map = {'No Deposit': 0, 'Refundable': 1, 'Non Refund': 2}
customer_type_map = {'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3}

# Streamlit UI
st.title("Hotel Booking Cancellation Predictor")

# Collect inputs
hotel = st.selectbox("Hotel", list(hotel_map.keys()))
lead_time = st.number_input("Lead Time (0-650)", min_value=0,max_value=650,step=1)
adults = st.number_input("Adults (limit=25)",min_value=0,max_value=25,step=1)
meal = st.selectbox("Meal", list(meal_map.keys()))
market_segment = st.selectbox("Market Segment", list(market_segment_map.keys()))
distribution_channel = st.selectbox("Distribution Channel", list(distribution_channel_map.keys()))
previous_cancellations = st.number_input("Previous Cancellations (0-25)",min_value=0,max_value=25,step=1)
reserved_room_type = st.selectbox("Reserved Room Type", list(reserved_room_type_map.keys()))
assigned_room_type = st.selectbox("Assigned Room Type", list(assigned_room_type_map.keys()))
deposit_type = st.selectbox("Deposit Type", list(deposit_type_map.keys()))
days_in_waiting_list = st.number_input("Days in Waiting List (0-390)",min_value=0,max_value=390,step=1)
customer_type = st.selectbox("Customer Type", list(customer_type_map.keys()))
adr = st.number_input("Average Daily Rate (max rate=5400)",min_value=0.0,max_value=5400.0,step=0.1)
total_of_special_requests = st.number_input("Total Special Requests (0-5)",min_value=0,max_value=5,step=1)

# Predict
if st.button("Predict"):
    # Map categorical inputs
    data = [
        hotel_map[hotel],
        lead_time,
        adults,
        meal_map[meal],
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
    result = "Cancelled" if prediction == 1 else "Not Cancelled"
    st.subheader(f"Prediction: {result}")