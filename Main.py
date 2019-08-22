# Import helper function modules.
import Filing
import Login
import Scrapers
import Cleaners
import Outputs


# A function that runs all the reporting functions.
def run_reporting_tool(start_roast, finish_roast, username, password, events_file_name, file_path, window):
    
    # Conver roast numbers to integers and create the roast list.
    start_roast = int(start_roast)
    finish_roast = int(finish_roast)
    roast_list = list(range(start_roast, finish_roast + 1))
    
    # Create ouput file.
    output_file_path = Filing.make_output_folder(file_path)

    # Perform login to Roastlog.com.
    session = Login.login('https://roastlog.com/login/', username, password)
    
    # Scrape Roastlog.com from roast table data.
    roast_details_df = Scrapers.scrape_web(roast_list, session)
    
    # Clean and reformat the raw data from Roastlog.com.
    clean_roast_details_df = Cleaners.clean_roast_detail_data(roast_details_df)
    
    # Create a dataframe of all roast profiles.
    aggregated_profiles_df = Scrapers.aggregate_profiles(roast_list, file_path)
    
    # Create dataframes for event times and event temps.
    event_temps_df, event_times_df = Scrapers.get_events(events_file_name, file_path)
    
    # Get a series of roastables and unique roastable names.
    roastables_df = clean_roast_details_df.roastable
    unique_roastables_df = roastables_df.drop_duplicates().reset_index(drop=True)
    
    # Create a roast summary page.
    Outputs.print_summary_page(clean_roast_details_df, output_file_path)
    
    # Create the inventory component table by roastable and output it is a csv file.
    inventory_by_roastable_df = Cleaners.make_inventory_by_roastable_report(clean_roast_details_df)
    inventory_by_roastable_df.to_csv(output_file_path + '\\Inventory By Roastable.csv', index=True)
    
    # Generate a pie chart of the roastable distribution.
    Outputs.make_roastable_dist_pie_chart(clean_roast_details_df, output_file_path)
    
    # Create visualizations for each unique roastable.
    Outputs.visualize_roastables(unique_roastables_df, roastables_df, aggregated_profiles_df, event_temps_df, event_times_df, output_file_path)
    
    # Create visualizations for all roastables.
    Outputs.visualize_all_metrics_1(roastables_df, aggregated_profiles_df, event_temps_df, event_times_df, output_file_path)
    Outputs.visualize_all_metrics_2(clean_roast_details_df, output_file_path)
    
    # Create a table for all relevant cleaned data and output it as a csv file.
    output_roast_details_df = Cleaners.make_output_data_report(clean_roast_details_df)
    output_roast_details_df.to_csv(output_file_path + '\\All Roast Data.csv', index = True)
    
    # Calculate the average roast statistics and print them out to a csv file.
    roastable_averages_df = Cleaners.make_roastable_averages_report(output_roast_details_df)
    roastable_averages_df.to_csv(output_file_path + '\\Averages.csv', index = True)

    # Close the GUI.
    window.destroy()




