
from datetime import timedelta, datetime

def parse_duration(duration_str):
    # remove PT and replace it with nothing

    duration_str = duration_str.replace("P", " ").replace("T"," ") # PT18M24S -> 18M24S

    components = ['D','H','M','S']
    values = {'D':0,'H':0,'M':0,'S':0}

    for component in components:
        if component in duration_str: # 18M24S
            value, duration_str = duration_str.split(component) # '18'
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"],
        hours=values["H"],
        minutes=values["M"],
        seconds=values["S"]
    )

    return total_duration

# 
def transform_data(row):

    duration_td =parse_duration(row["Duration"])

    row["Duration"] = (datetime.min + duration_td).time()

    row["Video_Type"] = "Shorts" if duration_td.total_seconds() < 60 else "Normal"

    return row


        