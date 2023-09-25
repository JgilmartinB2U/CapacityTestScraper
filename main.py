import pandas as pd
from canary_api import getDetailed, dfTranspose
import config
from config import enabledBIUs, masterBius
from config import createFullCabinet, getDPSTag, getOneBiuTag
import time

checked_dates = pd.read_csv('checked_dates.csv')
start_date = checked_dates['date'].iloc[-1]
start_date = pd.to_datetime(start_date)

date_range = pd.date_range(start_date, pd.datetime.now().date())

def check_FullCharge(cabinet, date): 
    try:
        value = None
        'Look for DPS charge less than 5A during the evening and DPS soc > 90'
        dps_charge = getDPSTag(cabinet, 'DPS_MaxACharge') 
        dps_soc = getDPSTag(cabinet, 'DPS_SOC')
        tags = [dps_charge, dps_soc]
        
        data = getDetailed(tags, date, date, '00:01:00', maxSize=1000000)
        data = dfTranspose(data)

        data = data[data[dps_charge] < 5]
        data = data[data.index.hour > 15]
        data = data[data.index.hour < 20]
        data = data[data[dps_soc] > 95]
        if not data.empty:
            return data.tail(1)
        else:
            return None
    except:
        return None

def check_start_time(cabinet, dateTime):
    pass

def check_faulted_packs(cabinet, start_dt, end_dt):
    start_time = start_dt.strftime('%H:%M:%S')
    end_time = end_dt.strftime('%H:%M:%S')
    date = start_dt.strftime('%Y-%m-%d')
    tags = createFullCabinet(cabinet, 'pack_Fault')
    data = getDetailed(tags, date, date, '00:01:00', maxSize=1000000, start_time=start_time, end_time=end_time)
    data = dfTranspose(data)
    return (data != 0).any().any()

def check_fully_connceted(cabinet, date, start_time, end_time):
    tags = createFullCabinet(cabinet, 'biu_stringCount')

def check_end_time(cabinet, date, start_time):
    dps_soc = getDPSTag(cabinet, 'DPS_SOC')
    dps_discharge = getDPSTag(cabinet, 'DPS_MaxADischarge')
    date = date.strftime('%Y-%m-%d')
    start_time = start_time.strftime('%H:%M:%S')
    data = getDetailed([dps_discharge, dps_soc], date, date, '00:01:00', maxSize=1000000, start_time=start_time)
    if len(data) != 0:
        data = dfTranspose(data)
    data = data[data[dps_soc] < 5]
    data = data[data[dps_discharge] < 15]

    if not data.empty:
        return data.head(1)

for date in date_range:
    #Iterate through date ranges for capacity tests
    start_date = date.strftime('%Y-%m-%d')
    for cabinet in masterBius[0:1]:
        start_ready = False
        end_ready = False

        # try:
            # Check if cabinet is fully charged and get full charge time
        data = check_FullCharge(cabinet, start_date)
        if data is not None:
            full_charge_time = data.index[0]
            starting_soc = data.iloc[:, 1].values
            full_charge_time = pd.to_datetime(full_charge_time)

            # Expand the time range for high frequency pull
            extended_start_dt = full_charge_time - pd.Timedelta(minutes=30)
            extended_end_dt = full_charge_time + pd.Timedelta(minutes=10)

            if cabinet[0] == '1':
                start_ready = check_faulted_packs(cabinet, extended_start_dt ,extended_end_dt)
            
            else:
                start_ready = check_fully_connceted(cabinet, extended_start_dt ,extended_end_dt)
        
        # Get end time after discharge and run capacity test
        if start_ready: 
            # print(f'{cabinet} is ready for capacity test')
            end_time = check_end_time(cabinet, date, full_charge_time)
            if end_time is not None:
                end_ready = True
                end_soc = end_time.iloc[:, 1].values
                end_time = end_time.index[0]
                print(f'{cabinet} is ready on {full_charge_time.date()} {full_charge_time.time()} to {end_time.time()}, soc range {starting_soc - end_soc}')
        if end_ready:
            pass