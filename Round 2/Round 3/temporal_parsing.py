import pandas as pd

def enforce_iso_timeline(dataframe, date_column='ISO_timestamp'):
    """
    Forces mixed multi-platform datetime strings into standard ISO-8601 format
    and handles invalid temporal tags gracefully.
    """
    # Convert the column to datetime, automatically detecting mixed platform formats
    dataframe[date_column] = pd.to_datetime(dataframe[date_column], errors='coerce', utc=True)
    
    # Drop rows where the timestamp couldn't be parsed (prevents graph plotting loops from breaking)
    dataframe = dataframe.dropna(subset=[date_column])
    
    # Sort the timeline chronologically from past to present
    dataframe = dataframe.sort_values(by=date_column).reset_index(drop=True)
    
    return dataframe

# Example Usage:
# df = enforce_iso_timeline(scraped_raw_df, date_column='ISO_timestamp')
