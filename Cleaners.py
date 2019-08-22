# Import packages.
import pandas as pd
from datetime import datetime


# A function to clean and reformat the raw data from Roastlog and return a dataframe.
def clean_roast_detail_data(roast_details_df):
    
    # Create a new dataframe for cleaned data.
    clean_roast_details_df = pd.DataFrame(index = roast_details_df.index)
    
    # Add roastable names and eliminate any blends or alternates.
    clean_roast_details_df['roastable'] = roast_details_df['roastable'].apply(lambda x: x.replace("Alt","").replace("Blend","").strip())
    
    # Add starting mass, drop text, and convert to float.
    clean_roast_details_df['start_mass_(lb)'] = roast_details_df['starting_mass'].apply(lambda x: float(x.replace("lb","").strip()))
    
    # Separate components, get their weights in lbs, and add them.
    for i in range(3):
        clean_roast_details_df[f'component_{i+1}'] = roast_details_df['components'].apply(lambda x: x.split(';')[i].split(':')[1].strip() if len(x.split(';')) > i else "None")
        clean_roast_details_df[f'component_{i+1}_percent'] = roast_details_df['components'].apply(lambda x: float(x.split(';')[i].split(':')[0].replace('%','').strip()) / 100 if len(x.split(';')) > i else 0.0)
        clean_roast_details_df[f'component_{i+1}_weight'] = clean_roast_details_df['start_mass_(lb)'] * clean_roast_details_df[f'component_{i+1}_percent']
    
    # Add starting mass.
    clean_roast_details_df['ending_mass_(lb)'] = roast_details_df['ending_mass'].apply(lambda x: float(x.replace("lb","").strip()))
    
    # Add skrinkage.
    clean_roast_details_df['shrinkage'] = 1 - clean_roast_details_df['ending_mass_(lb)'] / clean_roast_details_df['start_mass_(lb)']
    
    # Add date.
    clean_roast_details_df['date'] = roast_details_df['roasted_on'].apply(lambda x: datetime.strptime(x.replace('st','').replace('nd','').replace('rd','').replace('th',''), '%a, %b %d, %Y %H:%M %p').date())
    
    # Add time.
    clean_roast_details_df['time'] = roast_details_df['roasted_on'].apply(lambda x: datetime.strptime(x.replace('st','').replace('nd','').replace('rd','').replace('th',''), '%a, %b %d, %Y %H:%M %p').time())
    
    # Add start temperature.
    clean_roast_details_df['start_temp'] = roast_details_df['intro_time/temp'].apply(lambda x: round(float(x[0:x.find(" ")]),0))
    
    # Add turn time.
    clean_roast_details_df['turn_time'] = roast_details_df['turn_time/temp'].apply(lambda x: datetime.strptime(x[x.find("at ")+3:], '%M:%S').time())
    
    # Add turn temperature.
    clean_roast_details_df['turn_temp'] = roast_details_df['turn_time/temp'].apply(lambda x: round(float(x[0:x.find(" ")]),0))
    
    # Add finish time.
    clean_roast_details_df['finish_time'] = roast_details_df['drop_time/temp'].apply(lambda x: datetime.strptime(x[x.find("at ")+3:], '%M:%S').time())
    
    # Add finish temp.
    clean_roast_details_df['finish_temp'] = roast_details_df['drop_time/temp'].apply(lambda x: round(float(x[0:x.find(" ")]),0))
    
    # Add energy.
    clean_roast_details_df['energy'] = roast_details_df['roast_energy'].apply(lambda x: int(x[0:x.find(" ")]))
    
    # Add development ratio.
    clean_roast_details_df['development_ratio'] = roast_details_df['roast_development_ratio'].apply(lambda x: float(x.replace('%','')) / 100)
    
    # Add development time.
    clean_roast_details_df['development_time'] = clean_roast_details_df['finish_time'].apply(lambda x: x.minute * 60 + x.second) * clean_roast_details_df['development_ratio'].apply(lambda x: x)
    clean_roast_details_df['development_time'] = clean_roast_details_df['development_time'].apply(lambda x: str(int(int(x) / 60)) + ':' + str(int(x) % 60))
    clean_roast_details_df['development_time'] = clean_roast_details_df['development_time'].apply(lambda x: datetime.strptime(x,'%M:%S').time())
    
    # Add roast level.
    clean_roast_details_df['roast_level'] = roast_details_df['roast_level'].apply(lambda x: float(x))
    
    # Add adjusted roast level.
    clean_roast_details_df['adjusted_roast_level'] = roast_details_df['roast_level'].apply(lambda x: (float(x) - 10) / 12)
    
    # Add green cost per pound.
    clean_roast_details_df['green_cost_per_lb'] = roast_details_df['green_cost'].apply(lambda x: float(x.replace('$','').replace(' / lb','')))
    
    # Add roasted cost per pound.
    clean_roast_details_df['roasted_cost_per_lb'] = roast_details_df['roasted_cost'].apply(lambda x: float(x.replace('$','').replace(' / lb','')))
    
    # Add total cost.
    clean_roast_details_df['total_cost'] = roast_details_df['total_cost'].apply(lambda x: float(x.replace('$','')))
    
    # Add flame out count.
    clean_roast_details_df['flame_out_count'] = roast_details_df['roast_notes'].apply(lambda x: len(x[x.lower().find('flame Out: ') + 11:x.lower().find('.', x.find('flame Out: '))].split(',')) if x.lower().find('flame out: ') > -1 else 0)
    
    # Add low gas count.
    clean_roast_details_df['low_gas_count'] = roast_details_df['roast_notes'].apply(lambda x: x.lower().count('low gas'))
    
    # Add roast notes.
    clean_roast_details_df['roast_notes'] = roast_details_df['roast_notes']
    
    # Return the cleaned dataframe.
    return clean_roast_details_df


# A function for extracting an inventory-by-roastable report from a cleaned dataframe.
def make_inventory_by_roastable_report(clean_roast_details_df):
    
    # Isolate the roastable names, components, and weights.
    inventory_components_df = pd.concat([clean_roast_details_df[['roastable','component_1','component_1_weight']].rename(columns={'component_1':'component','component_1_weight':'weight'}),
                                         clean_roast_details_df[['roastable','component_2','component_2_weight']].rename(columns={'component_2':'component','component_2_weight':'weight'}),
                                         clean_roast_details_df[['roastable','component_3','component_3_weight']].rename(columns={'component_3':'component','component_3_weight':'weight'})],
                                         axis = 0, ignore_index = True)
    
    # Drop the stuff without any information.
    inventory_components_df = inventory_components_df[inventory_components_df['component'] != 'None']
    
    # Group by roastable and component and sum up the weights.
    inventory_by_roastable_df = inventory_components_df.groupby(['roastable', 'component']).sum()
    
    # Return the dataframe.
    return inventory_by_roastable_df


# A function for isolating relevant output columns and formatting them.
def make_output_data_report(clean_roast_details_df):
    
    # Drop off the unneeded columns.
    output_roast_details_df = clean_roast_details_df.drop(
            ['component_1',
             'component_1_percent',
             'component_1_weight',
             'component_2',
             'component_2_percent',
             'component_2_weight',
             'component_3',
             'component_3_percent',
             'component_3_weight',
             'roast_level'], axis = 1)
        
    return output_roast_details_df


# A function for isolating relevant columns and calculating averages for each roastable.
def make_roastable_averages_report(output_roast_details_df):
    
    # Drop off the unneeded columns.
    pre_calc_details_df = output_roast_details_df.drop(
            ['date',
             'time',
             'roast_notes'], axis = 1)
        
    # Convert any time columns to seconds.
    time_columns = ['turn_time', 'finish_time', 'development_time']
    for col in time_columns:
        pre_calc_details_df[col] = pre_calc_details_df[col].apply(lambda x: x.minute * 60 + x.second)
    
    # Group by roastable and calculate averages.
    roastable_averages_df = pre_calc_details_df.groupby('roastable').mean()
    
    # Convert the second columns back to time.
    for col in time_columns:
        roastable_averages_df[col] = roastable_averages_df[col].apply(lambda x: str(int(int(x) / 60)) + ':' + str(int(x) % 60))
        roastable_averages_df[col] = roastable_averages_df[col].apply(lambda x: datetime.strptime(x,'%M:%S').time())
    
    return roastable_averages_df