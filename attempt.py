import streamlit as st
import pandas as pd
import requests
import os

# Load the airport codes CSV file
airport_data = pd.read_csv("airport-codes.csv")

# Function to get carbon emissions using Carbon Interface API
def get_carbon_emissions(departure, destination):
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer PADZcJLe9LL9xi6CxF1wAQ",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "flight",
        "legs": [{
            "departure_airport": departure,
            "destination_airport": destination
        }],
        "distance_unit": "km"  # Default distance unit to kilometers
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        return data['data']['attributes']['carbon_kg']
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")


def home_page():
    st.title("Wie nachhaltig sind Ihre Reisen?")
    st.subheader("Where are you going on this trip?")

    # Dropdown for selecting departure airport
    departure_airport = st.selectbox('Select Departure Airport', airport_data['iata_code'])

    # Dropdown for selecting destination airport
    destination_airport = st.selectbox('Select Destination Airport', airport_data['iata_code'])

    if st.button('Calculate your CO2 Emission'):
        # Calculate carbon emissions
        carbon_emissions = get_carbon_emissions(departure_airport, destination_airport)

        # Store results in session state
        st.session_state.results = {
            'departure_airport': departure_airport,
            'destination_airport': destination_airport,
            'carbon_emissions': carbon_emissions
        }

        # Redirect to the results page
        st.session_state.page = "Calculate"


def calculate_page():
    st.title('Results')

    # Retrieve results from session state
    results = st.session_state.results

    if results:
        # Display results
        st.write('Departure Airport:', results['departure_airport'])
        st.write('Destination Airport:', results['destination_airport'])
        st.write('Carbon Emitted (kg):', results['carbon_emissions'])
        
        # Calculate number of trees needed to offset CO2 emissions
        co2_emissions = results['carbon_emissions']
        trees_needed = round(co2_emissions / 21.77)
        st.write(f'{trees_needed} trees to offset {co2_emissions} kilograms of CO2.')

        # Display tree image corresponding to the number of trees
        tree_image_path = "tree.png"

        if os.path.exists(tree_image_path):
            for _ in range(trees_needed):
                st.image(tree_image_path, width=100)
        else:
            st.warning("Tree image not found.")

    else:
        st.error("No results available. Please calculate CO2 emissions first.")


    
    button_html = """
        <style>
        .button {
            background-color: #004080; /* Dark blue color */
            color: white; /* Text color */
            padding: 10px 20px; /* Padding */
            text-align: center; /* Center-align text */
            text-decoration: none; /* Remove underline */
            display: inline-block; /* Make it inline */
            border: none; /* Remove border */
            border-radius: 4px; /* Add border radius */
            cursor: pointer; /* Add cursor pointer */
        }
        </style>
        <a href="https://onetreeplanted.org/products/carbon-offset" class="button" style="color: white;">Want to offset your travel’s carbon footprint?</a>
        """

    # Display the custom HTML
    st.markdown(button_html, unsafe_allow_html=True)




def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Calculate":
        calculate_page()


if __name__ == "__main__":
    main()
