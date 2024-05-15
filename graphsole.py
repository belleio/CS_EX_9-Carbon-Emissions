            # Create a graphical representation

            import matplotlib.pyplot as plt

            results = st.session_state.results

            if results:

                # Calculate number of trees needed to offset CO2 emissions
                co2_emissions = results['carbon_emissions']
                trees_needed = round(co2_emissions / 21.77)

                # Create a dictionary to store trees needed for each mode
                trees_needed_dict = {'Plane': trees_needed}

                # Generate and display the bar chart
                fig = create_tree_bar_chart(trees_needed_dict)
                st.pyplot(fig)

            else:
                st.error("No results available. Please calculate CO2 emissions first.")

            if results:

                # Calculate number of trees needed to offset CO2 emissions
                co2_emissions = results['carbon_emissions']
                trees_needed = round(co2_emissions / 21.77)

                # Create a dictionary to store trees needed for each mode
                trees_needed_dict = {'Vehicle': trees_needed}

                # Generate and display the bar chart
                fig = create_tree_bar_chart(trees_needed_dict)
                st.pyplot(fig)

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

                # Create a dictionary to store trees needed for each mode
                trees_needed_dict = st.session_state.get('trees_needed_dict', {})
                trees_needed_dict['Train'] = trees_needed
                st.session_state.trees_needed_dict = trees_needed_dict

                # Generate and display the bar chart
                fig = create_tree_bar_chart(trees_needed_dict)
                st.pyplot(fig)

                def create_tree_bar_chart(trees_needed_dict):
                        transport_modes = list(trees_needed_dict.keys())
                        trees_needed = list(trees_needed_dict.values())
                        colors = ['blue', 'green', 'red']

                        fig, ax = plt.subplots()
                        ax.bar(transport_modes, trees_needed, color=colors)
                        ax.set_xlabel('Transport Mode')
                        ax.set_ylabel('Number of Trees')
                        ax.set_title('Number of Trees Needed to Offset CO2 Emissions')

    