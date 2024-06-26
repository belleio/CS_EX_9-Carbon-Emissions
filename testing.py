import streamlit as st
import pandas as pd
import requests
import base64
import random
import matplotlib.pyplot as plt
# Emoji shower
from streamlit_extras.let_it_rain import rain
# Offset button
from offsetbutton import carbon_offset_button
# Cap's distance calculation
from distancecalculate import haversine_distance
# Tree image
from treecode import display_tree_images

# Load the airport codes CSV file
airport_data = pd.read_csv("airport-codes.csv")

# Import APIs
from apigetting import(
    get_carbon_emissions_flight,
    get_carbon_emissions_vehicles,
    get_train_carbon_emissions,
    get_vehicle_makes,
    get_vehicle_models
)

# Display flight details page
def flight_calculate_page():
    st.title('Flight Results')

    # Shows flight emojis raining down on page
    def flightemoji():
        rain(
            emoji="✈️",
            font_size=54,
            falling_speed=3,
            animation_length="5s",
        )
    flightemoji()

    results = st.session_state.results

    if results:
        # Display flight results
        st.write('Departure Airport:', results.get('departure_airport'))
        st.write('Destination Airport:', results.get('destination_airport'))
        st.write('Carbon Emitted (kg):', results['carbon_emissions'])

        # Calculate number of trees needed to offset CO2 emissions
        co2_emissions = results['carbon_emissions']
        trees_needed = round(co2_emissions / 21.77)
        st.write(f'{trees_needed} trees to offset {co2_emissions} kilograms of CO2.')

        # Calculate and display distance
        st.write('Distance (km):', round(results['distance_km'], 2))

        display_tree_images(trees_needed)

        distance_km = results.get('distance_km')

        trees_needed_vehicle1 = (trees_needed * 1.5)
        trees_needed_train1 = (trees_needed / 70)

        # Plotting the comparison chart
        fig, ax = plt.subplots()
        modes_of_transport = ['Flight', 'Vehicle', 'Train']
        trees_needed = [trees_needed, trees_needed_vehicle1, trees_needed_train1]

        ax.bar(modes_of_transport, trees_needed, color=['blue', 'red', 'green'])
        ax.set_xlabel('Transport Type')
        ax.set_ylabel('Number of Trees')
        ax.set_title('Comparison of Trees Needed to Offset CO2 Emissions')

        st.pyplot(fig)

                # Get train and car carbon emissions for the same distance
        carbon_emissions_t = get_train_carbon_emissions(distance_km)
        carbon_emissions_c = get_carbon_emissions_vehicles('km', distance_km, 'f46c68e5-4b0d-4136-a8cd-ed103cc202d1')
        # print(carbon_emissions)
        # print(carbon_emissions_t)
        # print(carbon_emissions_c[0])

        colors = ['blue', 'green', 'red']
        transport_types = ['Flight', 'Train', 'Vehicle']
        carbon_emission = [co2_emissions,carbon_emissions_t,carbon_emissions_c[0]]
        print(carbon_emission)
        # Plotting the bar chart
        plt.bar(transport_types, carbon_emission, color=colors)
        plt.xlabel('Transport Type')
        plt.ylabel('Carbon Emissions (kg)')
        plt.title('Comparison of Carbon Emissions by Transport Type')
        st.pyplot(plt)

        st.write("Vehicle in question used for bar chart is: Alfa Romeo - Spider Veloce 2000")

    else:
        st.error("No results available. Please calculate CO2 emissions first.")

    # Display the custom HTML button for offsetting carbon footprint
    button_html = carbon_offset_button()
    st.markdown(button_html, unsafe_allow_html=True)

    # Add return to homepage button
    if st.button('Return to Homepage'):
        st.session_state.page = "Home"

# Display vehicle details page
def vehicle_calculate_page():
    st.title('Vehicle Results')
    def caremoji():
        rain(
            emoji="🚗",
            font_size=54,
            falling_speed=3,
            animation_length="5s",
        )
    caremoji()
    # Retrieve results from session state
    results = st.session_state.results

    if results:
        # Display vehicle results
        st.write('Distance:', results.get('distance_value', 'Unknown'), results.get('distance_unit', 'Unknown'))
        st.write('Estimated CO2 Emission (kg):', results.get('carbon_emissions', 'Unknown'))

        # Calculate number of trees needed to offset CO2 emissions
        co2_emissions = results['carbon_emissions']
        trees_needed = round(co2_emissions / 21.77)
        st.write(f'{trees_needed} trees to offset {co2_emissions} kilograms of CO2.')

        # Display tree image corresponding to the number of trees
        display_tree_images(trees_needed)


        trees_needed_flight1 = (trees_needed / 1.5)
        trees_needed_train2 = (trees_needed / 105)

        # Plotting the comparison chart
        fig, ax = plt.subplots()
        modes_of_transport = ['Flight', 'Vehicle', 'Train']
        trees_needed = [trees_needed_flight1, trees_needed, trees_needed_train2]

        ax.bar(modes_of_transport, trees_needed, color=['blue', 'red', 'green'])
        ax.set_xlabel('Transport Type')
        ax.set_ylabel('Number of Trees')
        ax.set_title('Comparison of Trees Needed to Offset CO2 Emissions')

        st.pyplot(fig)

                    # Calculate CO2 emissions for train to compare

        carbon_emissions_t = get_train_carbon_emissions(results.get('distance_value', 0.0))
        carbon_emissions_p = (co2_emissions / 2)
                
        colors = ['blue','red','green']
        transport_types = ['Flight', 'Vehicle', 'Train']
        carbon_emission = [carbon_emissions_p,co2_emissions,carbon_emissions_t]

        print(carbon_emission)
        # Plotting the bar chart of comparison
        plt.bar(transport_types, carbon_emission, color=colors)
        plt.xlabel('Transport Type')
        plt.ylabel('Carbon Emissions (kg)')
        plt.title('Comparison of Carbon Emissions by Transport Type')
        st.pyplot(plt)

    else:
        st.error("No results available. Please calculate CO2 emissions first.")

    # Display the custom HTML button for offsetting carbon footprint
    button_html = carbon_offset_button()
    st.markdown(button_html, unsafe_allow_html=True)

    # Add return to homepage button
    if st.button('Return to Homepage'):
        st.session_state.page = "Home"

# Display train details page
def train_calculate_page():
    st.title('Train Results')
    def trainemoji():
        rain(
            emoji="🚂",
            font_size=54,
            falling_speed=3,
            animation_length="5s",
        )
    trainemoji()

    distance_km = st.session_state.train_distance_km

    if distance_km:
        # Call the estimates API for train emissions
        carbon_emissions = get_train_carbon_emissions(distance_km)

        # Calculate number of trees needed to offset CO2 emissions
        trees_needed = round(carbon_emissions / 21.77)

        # Display train results
        st.write("Distance:", distance_km, "km")
        st.write('Estimated CO2 Emission (kg):', carbon_emissions)
        st.write(f'{trees_needed} trees to offset {carbon_emissions} kilograms of CO2.')

        display_tree_images(trees_needed)

        if trees_needed == 0:
            trees_needed_vehicle2 = 52.5
            trees_needed_flight2 = 35
        else:
            trees_needed_vehicle2 = trees_needed * 105
            trees_needed_flight2 = trees_needed * 70

        # Plotting the comparison chart
        fig, ax = plt.subplots()
        modes_of_transport = ['Flight', 'Vehicle', 'Train']
        trees_needed = [trees_needed_flight2, trees_needed_vehicle2, trees_needed]

        ax.bar(modes_of_transport, trees_needed, color=['blue', 'red', 'green'])
        ax.set_xlabel('Transport Type')
        ax.set_ylabel('Number of Trees')
        ax.set_title('Comparison of Trees Needed to Offset CO2 Emissions')

        st.pyplot(fig)

                    # Get the carbon emission of the car for the same distance
        carbon_emissions_c = get_carbon_emissions_vehicles('km', distance_km, 'f46c68e5-4b0d-4136-a8cd-ed103cc202d1')

        carbon_emissions_p = (carbon_emissions * 70)

        colors = ['blue','green','red']
        transport_types = ['Flight', 'Train', 'Vehicle']
        carbon_emission = [carbon_emissions_p,carbon_emissions,carbon_emissions_c[0]]
        print(carbon_emission)
            # Plotting the bar chart
        plt.bar(transport_types, carbon_emission, color=colors)
        plt.xlabel('Transport Type')
        plt.ylabel('Carbon Emissions (kg)')
        plt.title('Comparison of Carbon Emissions by Transport Type')
        st.pyplot(plt)

        st.write("Vehicle in question used for bar chart is: Alfa Romeo - Spider Veloce 2000")

    else:
        st.error("No results available. Please calculate CO2 emissions first.")

    # Display the custom HTML button for offsetting carbon footprint
    button_html = carbon_offset_button()
    st.markdown(button_html, unsafe_allow_html=True)

    # Add return to homepage button
    if st.button('Return to Homepage'):
        st.session_state.page = "Home"

# Displays the home page
def home_page():
    st.title("Wie nachhaltig sind Ihre Reisen?")
    st.text("Sind Sie neugierig auf die Umweltauswirkungen der von Ihnen gewählten Verkehrsmittel?\nUnsere Website veranschaulicht die Kohlendioxidemissionen der verschiedenen Verkehrsmittel, \nund hilft Ihnen, fundierte und umweltfreundliche Entscheidungen zu treffen.\nErforschen Sie mit uns nachhaltige Transportmöglichkeiten für eine grünere Zukunft!")

    st.subheader("Which method of transport will you be taking?")
    selected_page = st.selectbox("Select Transport Mode", ("Plane", "Train", "Vehicle"))

    if selected_page == 'Plane':
        # Flight GIF: https://giphy.com/stickers/plane-airplane-flight-RiHa3e54ievRdyT77O
        file_path = "flightgif.gif"
        file_ = open(file_path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        width = 200

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="flight gif" width="{width}">',
            unsafe_allow_html=True,
        )
        st.subheader("Where are you going on this trip?")
        # Dropdown for selecting departure airport
        departure_airport = st.selectbox('Select Departure Airport', airport_data['iata_code'])

        # Dropdown for selecting destination airport
        destination_airport = st.selectbox('Select Destination Airport', airport_data['iata_code'])

        # add with vehicle/train?

        if st.button('Calculate your CO2 Emission'):
            # Calculate carbon emissions
            carbon_emissions = get_carbon_emissions_flight(departure_airport, destination_airport)

            # Get departure and destination coordinates
            departure_coords = airport_data.loc[airport_data['iata_code'] == departure_airport, 'coordinates'].iloc[0].split(',')
            destination_coords = airport_data.loc[airport_data['iata_code'] == destination_airport, 'coordinates'].iloc[0].split(',')

            departure_lat, departure_lon = map(float, departure_coords)
            destination_lat, destination_lon = map(float, destination_coords)

            # Calculate distance in kilometers
            distance_km = haversine_distance(departure_lat, departure_lon, destination_lat, destination_lon)

            # Store results in session state
            st.session_state.results = {
                'departure_airport': departure_airport,
                'destination_airport': destination_airport,
                'carbon_emissions': carbon_emissions,
                'distance_km': distance_km
            }
            # Redirect to the results page
            st.session_state.page = "Flight Results"

    elif selected_page == 'Train':
        # Train GIF: https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BqjwHPRsik3v7iaMZDfCIg.gif
        file_path = "traingif.gif"
        file_ = open(file_path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        width = 200

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="train gif" width="{width}">',
            unsafe_allow_html=True,
        )

        # Retrieve distance input from the user
        distance_km = st.number_input('Distance (in kilometers)', value=500.0)
        st.session_state.train_distance_km = distance_km  # Store distance in session state

        if st.button('Calculate CO2 Emission'):
            # Call the function to calculate train emissions
            carbon_emissions = get_train_carbon_emissions(distance_km)

            # Store the calculated emissions and distance in session state
            st.session_state.results = {
                'distance_km': distance_km,
                'carbon_emissions': carbon_emissions
            }
            # Navigate to the train results page
            st.session_state.page = "Train Results"


    elif selected_page == 'Vehicle':
        #Car GIF: https://giphy.com/gifs/car-2d-jonasbodtker-ikQbF4upEQRhkRV0kQ    
        file_path = "cargif.gif"
        file_ = open(file_path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        width = 200

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="car gif" width="{width}">',
            unsafe_allow_html=True,
        )
        st.subheader("Enter vehicle details:")
        # Always show distance unit as kilometers
        distance_unit = 'km'  # or 'km', depending on your preference
        distance_value = st.number_input('Distance Value (in km)', value=100.0)

        # Fetch the vehicle makes
        vehicle_makes = get_vehicle_makes()
        selected_make = st.selectbox('Select Vehicle Make', list(vehicle_makes.keys()))

        vehicle_models = get_vehicle_models(vehicle_makes, selected_make)
        selected_model = st.selectbox('Select Vehicle Model', list(vehicle_models.keys()))

        if st.button('Calculate your CO2 Emission'):
            # Get the vehicle model ID
            vehicle_model_id = vehicle_models[selected_model]

            # Calculate CO2 emissions for vehicle and get car type
            carbon_emissions, car_type = get_carbon_emissions_vehicles(distance_unit, distance_value, vehicle_model_id)

            # Store results in session state
            st.session_state.results = {
                'distance_value': distance_value,
                'distance_unit': distance_unit,
                'carbon_emissions': carbon_emissions,
                'car_type': car_type
            }
            st.session_state.page = "Vehicle Results"

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Flight Results":
        flight_calculate_page()
    elif st.session_state.page == "Vehicle Results":
        vehicle_calculate_page()
    elif st.session_state.page == "Train Results":
        train_calculate_page()

if __name__ == "__main__":
    main()
