# Import packages.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
from math import sqrt


# A funtion for creating a pie chart of the roastables.
def make_roastable_dist_pie_chart(clean_roast_details_df, output_file_path):
    
    # Isolate the roastable names and counts from the clean dataframe.
    roastable_names_and_counts_df = clean_roast_details_df['roastable'].value_counts()
    
    # Set the axes variables.
    a = roastable_names_and_counts_df.axes[0].tolist()
    b = roastable_names_and_counts_df.tolist()
    
    # Make and save the figure.
    plt.figure(figsize=(12,6))
    plt.pie(x = np.array(b), labels = ["{}, {}".format(a, b) for a, b in zip(a,b)])
    plt.title('Roastable Distribution')
    plt.savefig(output_file_path + '\\Roastable Distribution.png')
    
    
# A function for generating a series of visualization for each unique roastable.
def visualize_roastables(unique_roastables_df, roastables_df, aggregated_profiles_df, event_temps_df, event_times_df, output_file_path):
    
    # Loop through each unique roastable.
    for index, value in unique_roastables_df.items():
        
        # Create dataframes for the given roastable.
        subset_profiles_df = aggregated_profiles_df[roastables_df == value]
        subset_event_times_df = event_times_df[roastables_df == value]
        subset_event_temps_df = event_temps_df[roastables_df == value]
        
        # Calculate the average profile and events.
        average_profile = np.array(subset_profiles_df.mean(axis=0))
        average_event_times = np.array(subset_event_times_df.mean(axis=0))
        average_event_temps = np.array(subset_event_temps_df.mean(axis=0))
        
        # Isolate the drop times and temps, calculate the development time, and do some rounding.
        drop_temps = np.around(np.array(subset_event_temps_df['Drop temperature']),decimals=0)
        drop_times = np.array(subset_event_times_df['Drop temperature'])
        dev_times = drop_times - np.array(subset_event_times_df['Start 1st crack'])
        
        # Set the figure size.
        plt.figure(figsize=(24,12))
        
        # Create a sequence for the profile time dimension.
        t = np.arange(0,len(average_profile))
        
        # Create a plot for the average profile and include a scatter plot of the average event times and temps.
        plt.subplot(2, 2, 1)
        plt.plot(t, average_profile, '-')
        plt.scatter(average_event_times, average_event_temps)
        plt.xticks(np.arange(0, len(average_profile), step=60),[time.strftime('%M:%S', time.gmtime(x)) for x in np.arange(0, len(average_profile), step=60)])
        plt.title('Average Profile')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('Temperature (F)')
        
        # Create a histogram of the finishing temperatures.
        plt.subplot(2, 2, 2)
        plt.hist(drop_temps, bins = np.arange(np.amin(drop_temps),np.amax(drop_temps)+2), edgecolor='black', linewidth=1)
        plt.xticks(np.arange(np.amin(drop_temps),np.amax(drop_temps)+2))
        plt.title('Finish Temperature')
        plt.xlabel('Temperature (F)')
        plt.ylabel('Frequency')
        
        # Creat a histogram of the total times.
        plt.subplot(2, 2, 3)
        plt.hist(drop_times, bins = np.arange(np.amin(drop_times)-5,np.amax(drop_times)+5, step = 5), edgecolor='black', linewidth=1)
        plt.xticks(np.arange(np.amin(drop_times)-5, np.amax(drop_times)+5, step = 5),[time.strftime('%M:%S', time.gmtime(x)) for x in np.arange(np.amin(drop_times)-5, np.amax(drop_times) + 5, step=5)])
        plt.title('Total Time')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('Frequency')
        
        #Create a histogram of the development times.
        plt.subplot(2, 2, 4)
        plt.hist(dev_times, bins = np.arange(np.amin(dev_times)-5,np.amax(dev_times)+5, step = 5), edgecolor='black', linewidth=1)
        plt.xticks(np.arange(np.amin(dev_times)-5, np.amax(dev_times)+5, step = 5),[time.strftime('%M:%S', time.gmtime(x)) for x in np.arange(np.amin(dev_times)-5, np.amax(dev_times) + 5, step=5)])
        plt.title('Development Time')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('Frequency')
        
        # Name the graphic.
        plt.suptitle(value, fontsize=16)
        
        # Save the graphic as a png file.
        plt.savefig(output_file_path + '\\' + value + '.png')
        
        
# A function for visualizing all profile, time, and temperature roast metrics.
def visualize_all_metrics_1(roastables_df, profiles_df, event_temps_df, event_times_df, output_file_path):
    
    # Calculate the average profile and events.
    average_profile = np.array(profiles_df.mean(axis=0))
    average_event_times = np.array(event_times_df.mean(axis=0))
    average_event_temps = np.array(event_temps_df.mean(axis=0))
    
    # Isolate the drop times and temps, calculate the development time, and do some rounding.
    drop_temps = np.around(np.array(event_temps_df['Drop temperature']),decimals=0)
    drop_times = np.array(event_times_df['Drop temperature'])
    dev_times = drop_times - np.array(event_times_df['Start 1st crack'])
    
    # Set the figure size.
    plt.figure(figsize=(24,12))
        
    # Create a sequence for the profile time dimension.
    t = np.arange(0,len(average_profile))
    
    # Create a plot for the average profile and include a scatter plot of the average event times and temps.
    plt.subplot(2, 2, 1)
    plt.plot(t, average_profile, '-')
    plt.scatter(average_event_times, average_event_temps)
    plt.xticks(np.arange(0, len(average_profile), step=60),[time.strftime('%M:%S', time.gmtime(x)) for x in np.arange(0, len(average_profile), step=60)])
    plt.title('Average Profile')
    plt.xlabel('Time (MM:SS)')
    plt.ylabel('Temperature (F)')
    
    # Create a histogram of the finishing temperatures.
    plt.subplot(2, 2, 2)
    plt.hist(drop_temps, bins = np.arange(np.amin(drop_temps)-2,np.amax(drop_temps)+2, step = 2), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(drop_temps),np.amax(drop_temps)+2, step = 2))
    plt.title('Finish Temperature')
    plt.xlabel('Temperature (F)')
    plt.ylabel('Frequency')
    
    # Creat a histogram of the total times.
    plt.subplot(2, 2, 3)
    plt.hist(drop_times, bins = np.arange(np.amin(drop_times)-10,np.amax(drop_times)+10, step = 10), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(drop_times)-10, np.amax(drop_times)+10, step = 10),[time.strftime('%M:%S', time.gmtime(x)) for x in np.arange(np.amin(drop_times)-5, np.amax(drop_times) + 5, step=5)])
    plt.title('Total Time')
    plt.xlabel('Time (MM:SS)')
    plt.ylabel('Frequency')
    
    #Create a histogram of the development times.
    plt.subplot(2, 2, 4)
    plt.hist(dev_times, bins = np.arange(np.amin(dev_times)-5,np.amax(dev_times)+5, step = 5), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(dev_times)-5, np.amax(dev_times)+5, step = 5),[time.strftime('%M:%S', time.gmtime(x)) for x in np.arange(np.amin(dev_times)-5, np.amax(dev_times) + 5, step=5)])
    plt.title('Development Time')
    plt.xlabel('Time (MM:SS)')
    plt.ylabel('Frequency')
    
    # Name the graphic.
    plt.suptitle("All Roast Metrics 1", fontsize=16)
    
    # Save the graphic as a png file.
    plt.savefig(output_file_path + "\\All Roasts Metrics 1" + '.png')
    
    
# A function for visualizing all profile, time, and temperature roast metrics.
def visualize_all_metrics_2(cleaned_roast_details_df, output_file_path):
    
    # Isolate finish temperatures, development ratio, roast energy, and roast level from the cleaned roast details.
    finish_temps = np.array(cleaned_roast_details_df.finish_temp)
    development_ratios = np.around(np.array(cleaned_roast_details_df.development_ratio) * 100, 1)
    energy = np.array(cleaned_roast_details_df.energy)
    roast_level = np.array(cleaned_roast_details_df.adjusted_roast_level)
    
    # Set the figure size.
    plt.figure(figsize=(24,12))
    
    # Create a histrogram for finish temperatures.
    plt.subplot(2, 2, 1)
    plt.hist(finish_temps, bins = np.arange(np.amin(finish_temps)-2, np.amax(finish_temps)+2, step = 2), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(finish_temps)-2, np.amax(finish_temps)+2, step = 2))
    plt.title('Finish Temperatures')
    plt.xlabel('Temperature (F)')
    plt.ylabel('Frequency')
    
    # Create a histogram for development ratios.
    plt.subplot(2, 2, 2)
    plt.hist(development_ratios, bins = np.arange(np.amin(development_ratios)-1,np.amax(development_ratios)+1,step = 1), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(development_ratios)-1, np.amax(development_ratios)+1, step = 1))
    plt.title('Development Ratio')
    plt.xlabel('Development Raio (%)')
    plt.ylabel('Frequency')
    
    # Creat a histogram for roast energy.
    plt.subplot(2, 2, 3)
    plt.hist(energy, bins = np.arange(np.amin(energy)-25,np.amax(energy)+25, step = 25), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(energy)-25, np.amax(energy)+25, step = 25))
    plt.title('Roast Energy')
    plt.xlabel('Degree Minutes')
    plt.ylabel('Frequency')
    
    #Create a histogram for roast level.
    plt.subplot(2, 2, 4)
    plt.hist(roast_level, bins = np.arange(np.amin(roast_level)-.5,np.amax(roast_level)+.5, step = .5), edgecolor='black', linewidth=1)
    plt.xticks(np.arange(np.amin(roast_level)-.5, np.amax(roast_level)+.5, step = .5))
    plt.title('Roast Level')
    plt.xlabel('1-10 Scale')
    plt.ylabel('Frequency')
    
    # Name the graphic.
    plt.suptitle("All Roast Metrics 2", fontsize=16)
    
    # Save the graphic as a png file.
    plt.savefig(output_file_path + '\\All Roasts Metrics 2.png')
    
    
# A function to print out the summary statistics to a txt file.
def print_summary_page(clean_roast_details_df, output_file_path):
    
    
    # A helper function to calculate average time.
    def average_time(time_series):
        
        # Convert pandas series to list.
        time_list = time_series.tolist()
        
        # Loop over the list and get the total number of seconds.
        total_seconds = 0
        for item in time_list:
            total_seconds += item.minute * 60 + item.second
            
        # Calculate average seconds.
        average_seconds =  total_seconds / len(time_list)    
        
        # Return a string.
        return str(int(average_seconds / 60)) + ':' + str(int(average_seconds % 60))
    
    
    # A helper function to calculate standard deviation of time.
    def sd_time(time_series):
        
        # Convert pandas series to list.
        time_list = time_series.tolist()
        
        # Loop over the list and get the total number of seconds.
        total_seconds = 0
        for item in time_list:
            total_seconds += item.minute * 60 + item.second
            
        # Calculate average seconds.
        average_seconds =  total_seconds / len(time_list)    
        
        # Calculate the sum of square differences.
        ssd = 0
        for item in time_list:   
            ssd += ((item.minute * 60 + item.second) - average_seconds) ** 2 
        
        # Divide by n-1 and take square root.
        sd_seconds = ssd / (len(time_list) - 1)
        sd_seconds = sqrt(sd_seconds)
        
        # Return a string.
        return str(int(sd_seconds / 60)) + ':' + str(int(sd_seconds % 60))

    
    df = clean_roast_details_df
    
    with open(output_file_path + '\\Summary.txt', 'w') as f:
        
        print('OVERVIEW'.ljust(50), file = f)
        print('-' * 8, file = f)
        print('Total Roasts:'.ljust(50) + str(len(df)).rjust(15), file = f)
        print('Roast Numbers:'.ljust(50) + (str(df.index[0]) + ' - ' + str(df.index[-1])).rjust(15), file = f)
        print('Total Cost:'.ljust(50) + ('$' + str(int(df.total_cost.sum()))).rjust(15), file = f)
        print('-' * 65, file = f)
        print('\n', file = f)
        print('WEIGHT'.ljust(50), file = f)
        print('-' * 6, file = f)
        print('Total Weight (lb):'.ljust(50) + (str(int(df['start_mass_(lb)'].sum()))).rjust(15), file = f)
        print('Total Yield (lb):'.ljust(50) + (str(int(df['ending_mass_(lb)'].sum()))).rjust(15), file = f)
        print('Total Shrinkage (lb):'.ljust(50) + (str(int(df['start_mass_(lb)'].sum() - df['ending_mass_(lb)'].sum()))).rjust(15), file = f)
        print('Total Shrinkage (%):'.ljust(50) + (str(round(((df['ending_mass_(lb)'].sum() / df['start_mass_(lb)'].sum() - 1) * 100),1)) + '%').rjust(15), file = f)    
        print('-' * 65, file = f)
        print('\n', file = f)
        print('ROAST'.ljust(50), file = f)
        print('-' * 5, file = f)
        print('AVG Roast Energy:'.ljust(50) + (str(int(df.energy.mean()))).rjust(15), file = f)
        print('SD Roast Energy:'.ljust(50) + (str(int(df.energy.std()))).rjust(15), file = f)
        print('AVG Development Ratio:'.ljust(50) + (str(round(df.development_ratio.mean() * 100, 1)) + '%').rjust(15), file = f)
        print('SD Development Ratio:'.ljust(50) + (str(round(df.development_ratio.std() * 100, 1)) + '%').rjust(15), file = f)
        print('AVG Development Time:'.ljust(50) + (average_time(df.development_time)).rjust(15), file = f)
        print('SD Development Time:'.ljust(50) + (sd_time(df.development_time)).rjust(15), file = f)
        print('AVG Total Time:'.ljust(50) + (average_time(df.finish_time)).rjust(15), file = f)
        print('SD Total Time:'.ljust(50) + (sd_time(df.finish_time)).rjust(15), file = f)
        print('AVG Roast Level:'.ljust(50) + (str(round(df.adjusted_roast_level.mean(),1))).rjust(15), file = f)
        print('SD Roast Level:'.ljust(50) + (str(round(df.adjusted_roast_level.std(),1))).rjust(15), file = f)
        print('-' * 65, file = f)
        print('\n', file = f)
        print('COSTS'.ljust(50), file = f)
        print('-' * 5, file = f)
        print('AVG Green Cost per Pound:'.ljust(50) + ('$' + str(round(df.green_cost_per_lb.mean(),2))).rjust(15), file = f)
        print('SD Green Cost per Pound:'.ljust(50) + ('$' + str(round(df.green_cost_per_lb.std(),2))).rjust(15), file = f)
        print('AVG Roasted Cost per Pound:'.ljust(50) + ('$' + str(round(df.roasted_cost_per_lb.mean(),2))).rjust(15), file = f)
        print('SD Roasted Cost per Pound:'.ljust(50) + ('$' + str(round(df.roasted_cost_per_lb.std(),2))).rjust(15), file = f)
        print('AVG Cost per Roast:'.ljust(50) + ('$' + str(round(df.total_cost.mean(),2))).rjust(15), file = f)
        print('SD Cost per Roast:'.ljust(50) + ('$' + str(round(df.total_cost.std(),2))).rjust(15), file = f)       
        print('-' * 65, file = f)
        print('\n', file = f)
        print('MACHINE ERRORS'.ljust(50), file = f)
        print('-' * 14, file = f)
        print('Flame Outs:'.ljust(50) + (str(df.flame_out_count.sum())).rjust(15), file = f)
        print('Low Gas:'.ljust(50) + (str(df.low_gas_count.sum())).rjust(15), file = f)
        
    
    
    