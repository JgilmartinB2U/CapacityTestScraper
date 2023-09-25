import pandas as pd
from canary_api import getDetailed, dfTranspose
import config
from config import enabledBIUs, masterBius
from config import createFullCabinet, getDPSTag, getOneBiuTag

checked_dates = pd.read_csv('checked_dates.csv')
start_date = checked_dates['date'].iloc[-1]
start_date = pd.to_datetime(start_date)

date_range = pd.date_range(start_date, pd.datetime.now().date())


def check_FullCharge(cabinet, date): 
    'Look for DPS charge less than 3A in the afternoon'
    dps_charge = getDPSTag(cabinet, 'DPS_MaxACharge') 
    connected_strings = getOneBiuTag(cabinet, 'biu_stringCount')
    tags = [dps_charge, connected_strings]
    
    data = getDetailed(tags, date, date, '00:05:00', maxSize=1000000)
    data = dfTranspose(data)
    # data.reset_index(inplace=True)
    data = data[data[dps_charge] < 3]
    data = data[data.index.hour > 15]
    return(data.tail(1))

def check_start_time(cabinet, dateTime):
    pass

def check_faulted_packs(cabinet, start_dt, end_dt):
    start_time = start_dt.strftime('%H:%M:%S')
    end_time = end_dt.strftime('%H:%M:%S')
    date = start_dt.strftime('%Y-%m-%d')
    tags = createFullCabinet(cabinet, 'pack_Fault')
    data = getDetailed(tags, date, date, '00:01:00', maxSize=1000000, start_time=start_time, end_time=end_time)
    data = dfTranspose(data)
    if len(data) > 0:
        print(f'Faulted packs found on {cabinet} on {date}')
        print(data)

def check_fully_connceted(cabinet, date, start_time, end_time):
    tags = createFullCabinet(cabinet, 'biu_stringCount')

def check_end_time(cabinet, start_time):
    dps_soc = getDPSTag(cabinet, 'biu_SOC')
    tags = createFullCabinet(cabinet, 'DPS_MaxADischarge')


for date in date_range:
    #Iterate through date ranges for capacity tests
    start_date = date.strftime('%Y-%m-%d')
    for cabinet in masterBius[0:1]:
        try:
            # Check if cabinet is fully charged and get full charge time
            data = check_FullCharge(cabinet, start_date)
            if not data.empty:
                full_charge_time = data.index[0]
                full_charge_time = pd.to_datetime(full_charge_time)

                # Expand the time range for high frequency pull
                extended_start_dt = full_charge_time - pd.Timedelta(minutes=30)
                extended_end_dt = full_charge_time + pd.Timedelta(minutes=10)
                if cabinet[0] == '1':
                    ready = check_faulted_packs(cabinet, extended_start_dt ,extended_end_dt)
                else:
                    ready = check_fully_connceted(cabinet, extended_start_dt ,extended_end_dt)
            
            # Get end time after discharge and run capacity test
            if ready: 
                end_time = check_end_time(cabinet, full_charge_time)

        except:
            print(f'Failed to check full charge on {cabinet} on {start_date}')