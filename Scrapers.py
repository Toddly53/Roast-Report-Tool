# Import packages.
from bs4 import BeautifulSoup
import re
import pandas as pd


# A function to scrape Roastlog.com and return a pandas dataframe of the data.
def scrape_web(roast_list, session):
    
    # Set list of variables to get from Roastlog.
    parameters = ['Roastable:', 'Components:', 'Starting mass:', 'Roasted on:', 'Ending mass:', 'Shrinkage:', 'Intro time/temp:', 'Turn time/temp:', 'Drop time/temp:', 'Roast Energy:', 'Roast development ratio:', 'Roast level:', 'Green cost:', 'Roasted cost:', 'Total cost:', 'Roast Notes:']
    
    
    # Loop through roasts and scrape data to be stored in lists.
    roast_data_list = []
    for roast in roast_list:
        
        # Set url and scrape.
        url = f'https://roastlog.com/roasts/{roast}/'    
        result = session.get(url, headers = dict(referer = url))
        
        # Convert to BeautifulSoup object.
        soup = BeautifulSoup(result.text,'lxml')
        
        # Find the first table and collect data values.
        roast_detail_table = soup.find('table')
        if roast_detail_table == None:
            continue
        roast_detail_table_data = roast_detail_table.find_all('td')
        
        # Isolate the text, clean it up, and consolidate the components.
        for i in range(len(roast_detail_table_data)):
            roast_detail_table_data[i] = roast_detail_table_data[i].get_text()
            roast_detail_table_data[i] = roast_detail_table_data[i].replace('\n','')
            roast_detail_table_data[i] = roast_detail_table_data[i].strip()
        
        # Create a dictionary for the given roast's table details.
        roast_details = {}
        
        # Label the various parameters in the dictionary and assign each parameter it's value. Leave it blank if unavailable.
        for param in parameters:
            if param not in roast_detail_table_data:
                roast_details[param] = ""
            else:
                roast_details[param] = roast_detail_table_data[roast_detail_table_data.index(param)+1]
            
        # Get rid of the whitespace between each component.    
        roast_details['Components:'] = re.sub('  +',';',roast_details['Components:'])
        
        # Convert the dictionary into a series, name it as roast number, and add it to the list of roasts.
        roast_data_list.append(pd.Series(roast_details, index = parameters, name = roast))
        
    # Make a dataframe of all the roast series and transpose.    
    roast_details_df = pd.concat(roast_data_list, axis=1).T
    
    # Rename the columns.
    roast_details_df.columns = [x.replace(':','').replace(' ','_').lower() for x in parameters]
    
    # Return the dataframe
    return roast_details_df


# A function to go through the csv profiles, isolate the bean temperature, and aggregate them into one dataframe.
def aggregate_profiles(roast_list, file_path):
    
    # Create a list for each roast profile and ppend each as they are read in.
    roast_profile_list = []
    for roast in roast_list:
        profile_df = pd.read_csv(file_path + '\\roast-' + str(roast) + '.csv',
                                 names=['second', 'val1', 'val2', 'val3', 'val4'])
        roast_profile_list.append(profile_df['val1'].rename(roast))
    
    # Concatenate and transpose the profiles.
    aggregated_profiles_df = pd.concat(roast_profile_list, axis=1).T
    
    # Return the aggregate profiles dataframe.
    return aggregated_profiles_df


# A function to get the event data from a csv file, format it, and separate it into two dataframes for times and temps.
def get_events(events_file_name, file_path):

    # read the events data from csv.
    events_df = pd.read_csv(file_path + '\\' + events_file_name)
    
    # Replace the mm:ss of time with seconds.
    events_df['Time'] = events_df['Time'].apply(lambda x: int(x[:2])*60 + int(x[-2:]) if len(x) == 5 else int(x[:1])*60 + int(x[-2:]))
    
    # Reorganize the data into event times and event temps by roast number.
    event_temps_df = events_df.pivot_table(values='Temperature', index='Roast', columns='Event')
    event_times_df = events_df.pivot_table(values='Time', index='Roast', columns = 'Event')
    
    # Return the temps and times.
    return event_temps_df, event_times_df