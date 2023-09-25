import math
import re
refreshRate = 20 #Refresh rate in seconds
emailRecipieints = ['jgilmartin@b2uco.com']

dpsFaultTypes = {}
dpsRateLimit = {}

dpsRateLimit['1-1'] = 0
dpsRateLimit['1-2'] = 0
dpsRateLimit['1-3'] = 0
dpsRateLimit['1-4'] = 0
dpsRateLimit['1-5'] = 0
dpsRateLimit['1-6'] = 0
dpsRateLimit['2-1'] = 0
dpsRateLimit['2-2'] = 0
dpsRateLimit['2-3'] = 0
dpsRateLimit['2-4'] = 0
dpsRateLimit['2-5'] = 0
dpsRateLimit['2-6'] = 0
dpsRateLimit['3-1'] = 0
dpsRateLimit['3-2'] = 0
dpsRateLimit['3-3'] = 0
dpsRateLimit['3-4'] = 0
dpsRateLimit['3-5'] = 0
dpsRateLimit['3-6'] = 0


enabledBIUs = [ 
    '1-3-1',
    '1-3-2',
    '1-3-3',
    '1-3-4',

    '1-4-1',
    '1-4-2',
    '1-4-3',
    '1-4-4',

    '1-5-1',
    '1-5-2',
    '1-5-3',
    '1-5-4',

    '1-6-1',
    '1-6-2',
    '1-6-3',
    '1-6-4',

    '2-1-1',
    '2-1-2',
    '2-1-3',
    '2-1-4',

    '2-2-1',
    '2-2-2',
    '2-2-3',
    '2-2-4',

    '2-3-1',
    '2-3-2',
    '2-3-3',
    '2-3-4', 

    '2-4-1',
    '2-4-2',
    '2-4-3',
    '2-4-4',

    '2-5-1',
    '2-5-2',
    '2-5-3',
    '2-5-4', 

    '2-6-1',
    '2-6-2',
    '2-6-3',
    '2-6-4', 

    '3-1-1',
    '3-1-2',
    '3-1-3',
    '3-1-4',

    '3-2-1',
    '3-2-2',
    '3-2-3',
    '3-2-4', 

    '3-3-1', 
    '3-3-2',
    '3-3-3',
    '3-3-4',

    '3-4-1',
    '3-4-2',
    '3-4-3',
    '3-4-4', 

    '3-5-1',
    '3-5-2',
    '3-5-3',
    '3-5-4', 

    '3-6-1',
    '3-6-2',
    '3-6-3',
    '3-6-4'
    ]

masterBius = [
    '1-3-1', 
    '1-4-1',
    '1-5-1',
    '1-6-1',
    '2-1-1',
    '2-2-1',
    '2-3-1',
    '2-4-1',
    '2-5-1',
    '2-6-1',
    '3-1-1',
    '3-2-1',
    '3-3-1',
    '3-4-1',
    '3-5-1',
    '3-6-1'
    
]

dpsFaultTypes[1] =[
    'Reserved',
    'Reserved',
    'Reserved',
    'Choke High Temp',
    'IGBT1 Gate driver Board',
    'IGBT2 Gate driver Board',
    'IGBT3 Gate driver Board',
    'IGBT4 Gate driver Board',
    'Port 1 Over Voltage Analog',
    'Port 2 Over Voltage Analog',
    'Fan Fail',
    'Emergency Power Off',
    'SPD Fault',
    'Customer EPO',
    'Input Source Fault',
    'Thermal Switch Trip'
]

dpsFaultTypes[2] = [
    'Fault Active',
    'Settings Files Fault',
    'Auto Pre-charge Sequence Fault',
    'Battery Overtemperature Fault',
    'Ambient Overtemperature Fault',
    'IGBT Overtemperature Fault',
    'Contactor Fault',
    'Port 1 Pre-charge Circuit Fault',
    'Port 2 Pre-charge Circuit Fault',
    'RESERVED',
    'CPU Over Temp'
    'Port 2 Thermal Switch Trip',
    'Port 1 Thermal Switch Trip',
    'Firmware Key Fault',
    'Reserved',
    'Watchdog Fault'
]

dpsFaultTypes[3] = [
    'Reserved',
    'Fault Status 1 Active',
    'Port 1 Under Voltage Instantaneous',
    'Port 1 Timed Under Voltage',
    'Port 1 Over Voltage Instantaneous',
    'Port 1 Time Over Voltage',
    'Port 1 Over Current Instantaneous',
    'Reserved',
    'Port 2 Under Voltage Instantaneous',
    'Port 2 Timed Under Voltage',
    'Port 2 Over Voltage Instantaneous',
    'Port 2 Time Over Voltage',
    'Port 2 Over Current Instantaneous',
    'Reserved',
    'Port 2 Cap voltage Difference Fault',
    'Port 1 Cap Voltage Difference Fault'
]

dpsFaultTypes[4] = [
    'Inductor 1 Over Current Instantaneous',
    'Reserved',
    'Inductor 2 Over Current Instantaneous',
    'Reserved',
    'Port 1 Top Cap Over Voltage Instantaneous',
    'Port 1 Bottom Cap Over Voltage Instantaneous',
    'Port 2 Top Cap Over Voltage Instantaneous',
    'Port 2 Bottom Cap Over Voltage Instantaneous',
    'Port 1 Charge Overcurrent Trip',
    'Port 1 Discharge Overcurrent Trip',
    'Port 2 Charge Overcurrent Trip',
    'Port 2 Discharge Overcurrent Trip',
    'RESERVED'
]

dpsFaultTypes[5] = [
    'Inductor Current Unbalance Fault',
    'Power Level Unbalanced Fault',
    'Port 1 CMV Fault',
    'Port 2 CMV Fault',
    'Reserved'
]

dpsList = [
    '1-1',
    '1-2',
    '1-3',
    '1-4',
    '1-5',
    '1-6',

    '2-1',
    '2-2',
    '2-3',
    '2-4',
    '2-5',
    '2-6',

    '3-1',
    '3-2',
    '3-3',
    '3-4',
    '3-5',
    '3-6'
]

invFaults = {}
invFaults[1393] = 'WaitDC'
invFaults[21936] = 'BatOnly'


clarityPacks = {}
clarityPacksConversion = {}
leafPacks = {}

clarityPacks[0] = '1-1'
clarityPacks[1] = '1-2'
clarityPacks[2] = '1-3'
clarityPacks[3] = '2-1'
clarityPacks[4] = '2-2'
clarityPacks[5] = '2-3'
clarityPacks[6] = '3-1'
clarityPacks[7] = '3-2'
clarityPacks[8] = '3-3'
clarityPacks[9] = '4-1'
clarityPacks[10] = '4-2'
clarityPacks[11] = '4-3'
clarityPacks[12] = '5-1'
clarityPacks[13] = '5-2'
clarityPacks[14] = '5-3'
clarityPacks[15] = '6-1'
clarityPacks[16] = '6-2'
clarityPacks[17] = '6-3'
clarityPacks[18] = '7-1'
clarityPacks[19] = '7-2'
clarityPacks[20] = '7-3'
clarityPacks[21] = '8-1'
clarityPacks[22] = '8-2'
clarityPacks[23] = '8-3'

clarityPacksConversion['1-1'] = 0
clarityPacksConversion['1-2'] = 1
clarityPacksConversion['1-3'] = 2
clarityPacksConversion['2-1'] = 3
clarityPacksConversion['2-2'] = 4
clarityPacksConversion['2-3'] = 5
clarityPacksConversion['3-1'] = 6
clarityPacksConversion['3-2'] = 7
clarityPacksConversion['3-3'] = 8
clarityPacksConversion['4-1'] = 9
clarityPacksConversion['4-2'] = 10
clarityPacksConversion['4-3'] = 11
clarityPacksConversion['5-1'] = 12
clarityPacksConversion['5-2'] = 13
clarityPacksConversion['5-3'] = 14
clarityPacksConversion['6-1'] = 15
clarityPacksConversion['6-2'] = 16
clarityPacksConversion['6-3'] = 17
clarityPacksConversion['7-1'] = 18
clarityPacksConversion['7-2'] = 19
clarityPacksConversion['7-3'] = 20
clarityPacksConversion['8-1'] = 21
clarityPacksConversion['8-2'] = 22
clarityPacksConversion['8-3'] = 23


leafPacks[0] = '1-1'
leafPacks[1] = '1-2'
leafPacks[2] = '2-1'
leafPacks[3] = '2-2'
leafPacks[4] = '3-1'
leafPacks[5] = '3-2'
leafPacks[6] = '4-1'
leafPacks[7] = '4-2'
leafPacks[8] = '5-1'
leafPacks[9] = '5-2'
leafPacks[10] = '6-1'
leafPacks[11] = '6-2'
leafPacks[12] = '7-1'
leafPacks[13] = '7-2'
leafPacks[14] = '8-1'
leafPacks[15] = '8-2'
leafPacks[16] = '9-1'
leafPacks[17] = '9-2'
leafPacks[18] = '10-1'
leafPacks[19] = '10-2'

tags = {}

tags['poa'] = 'Advantech2-HIST.LANCASTER.MET.POA_IRR'

tags['dot'] = 'ADVANTECH2-HIST.LANCASTER.RTAC.ADS_DOT_MW_SP'
tags['site_soc'] = 'ADVANTECH2-HIST.LANCASTER.RTAC.SOC_Plant'
tags['pod'] = 'ADVANTECH2-HIST.LANCASTER.RTAC.RIG_POD_MW'
tags['poa'] = 'ADVANTECH2-HIST.LANCASTER.MET.POA_IRR'

tags['invTotWat'] = ['ADVANTECH2-HIST.LANCASTER.INV_1.DCTOTWAT', 'ADVANTECH2-HIST.LANCASTER.INV_2.DCTOTWAT', 'ADVANTECH2-HIST.LANCASTER.INV_3.DCTOTWAT']

tags['dps_Power'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.DCWATT'
tags['invBatPower'] = ['ADVANTECH2-HIST.LANCASTER.INV_1.DCS_DCW','ADVANTECH2-HIST.LANCASTER.INV_2.DCS_DCW', 'ADVANTECH2-HIST.LANCASTER.INV_3.DCS_DCW']

tags['biu_SOC'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.DPS_SOC'
tags['biu_Fault'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.BIU_FaultEvntReg'
tags['biu_State'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.BIU_State'
tags['biu_Current'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.BIU_TotStringCur'
tags['biu_stringCount'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.BIU_ConStringCt'
tags['biu_heartbeat'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.BIU_Heartbeat'

tags['pack_max_cell_temp'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Cell_Max_T'
tags['pack_max_cell_v'] = 'ADVANTECH2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Cell_Max_V'
tags['pack_min_cell_v'] = 'ADVANTECH2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Cell_Min_V'

tags['pack_Current'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Current'
tags['pack_Voltage'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Voltage'

tags['pack_Fault'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Diagn_Fault'
tags['pack_Warning'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.Diagn_Warning'

tags['pack_SOC'] = 'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.Pack_1-1.SOC'
tags['plant_SOC'] = 'ADVANTECH2-HIST.LANCASTER.RTAC.SOC_Plant'

tags['BCP1_Current'] = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.DPS_Current'
tags['BCP1_Voltage'] = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.DPS_String_voltage'
tags['BCP1_SOC'] = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.DPS_SOC'

tags['DPS_MaxACharge'] = 'ADVANTECH2-HIST.LANCASTER.INV_2.DPS_1.DPS_MaxBatACha'
tags['DPS_MaxADischarge'] = 'ADVANTECH2-HIST.LANCASTER.INV_2.DPS_1.DPS_MaxBatADischa'

tags['allStringCounts'] = [
    'Advantech2-HIST.LANCASTER.INV_1.DPS_3.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_1.DPS_3.BIU_2.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_1.DPS_4.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_1.DPS_4.BIU_2.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_1.DPS_5.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_1.DPS_5.BIU_2.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_1.DPS_6.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_1.DPS_6.BIU_2.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_1.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_2.DPS_2.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_2.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_2.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_2.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_2.DPS_3.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_3.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_3.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_3.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_2.DPS_4.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_4.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_4.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_4.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_2.DPS_5.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_5.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_5.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_2.DPS_6.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_6.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_6.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_2.DPS_6.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_3.DPS_1.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_1.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_1.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_1.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_3.DPS_2.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_2.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_2.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_2.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_3.DPS_3.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_3.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_3.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_3.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_3.DPS_4.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_4.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_4.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_4.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_3.DPS_5.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_5.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_5.BIU_4.BIU_ConStringCt',

    'Advantech2-HIST.LANCASTER.INV_3.DPS_6.BIU_1.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_6.BIU_2.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_6.BIU_3.BIU_ConStringCt',
    'Advantech2-HIST.LANCASTER.INV_3.DPS_6.BIU_4.BIU_ConStringCt'
]

def getBIUTags(BIUs, type):
    sampleTag = tags[type]
    biuTags = []
    for BIU in BIUs:
        inv = BIU[0]
        dps = BIU[2]
        biu = BIU[4]

        newTag = sampleTag.replace('INV_2.DPS_1.BIU_1', 'INV_{inv}.DPS_{dps}.BIU_{biu}'.format(inv = inv, dps = dps, biu = biu))
        biuTags.append(newTag)
    return biuTags



def getSiteTags():
    return [tags['poa'], tags['pod'], tags['dot'], tags['site_soc']] + tags['invBatPower'] + tags['invTotWat']

def getDCTOTWAT():
    return tags['invTotWat']

def getBatPower():
    return tags['invBatPower']

def getBCPTags():
    bcp1Vol = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.BATVOL'
    bcp1Cur = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.BATAMP'
    bcp1SOC = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.DPS_SOC'
    bcp2Vol = 'Advantech2-HIST.LANCASTER.INV_1.DPS_2.BATVOL'
    bcp2Cur = 'Advantech2-HIST.LANCASTER.INV_1.DPS_2.BATAMP'
    bcp2SOC = 'Advantech2-HIST.LANCASTER.INV_1.DPS_2.DPS_SOC'
    return [bcp1Vol, bcp1Cur, bcp1SOC, bcp2Vol, bcp2Cur, bcp2SOC]

def getDPSPowerTags():
    baseTag = 'Advantech2-HIST.LANCASTER.INV_1.DPS_1.DCWATT'
    tags = []
    for dps in dpsRateLimit.keys():
        inv = dps[0]
        dps = dps[2]
        tags.append(baseTag.replace('INV_1.DPS_1', 'INV_{inv}.DPS_{dps}'.format(inv = inv, dps = dps)))
    return tags

def createFullCabinet(cabinet, type):
    sampleTag = tags[type]
    inv = cabinet[0]
    dps = cabinet[2]
    biu = cabinet[4]
    tagList = []

    if int(inv) > 1 or (int(inv) == 1 and (int(dps) == 5 or int(dps) == 6)):
        sampleTag = sampleTag.replace('INV_2.DPS_1.BIU_1', 'INV_{inv}.DPS_{dps}.BIU_{biu}'.format(inv = inv, dps = dps, biu = biu))
        for i in clarityPacks:
            newTag = str(sampleTag.replace('Pack_1-1', 'Pack_{pack}'.format(pack = clarityPacks[i])))
            tagList.append(newTag)
    elif int(inv) == 1:
        sampleTag = sampleTag.replace('INV_2.DPS_1.BIU_1', 'INV_{inv}.DPS_{dps}.BIU_{biu}'.format(inv = inv, dps = dps, biu = biu))
        for i in leafPacks:
            newTag = str(sampleTag.replace('Pack_1-1', 'Pack_{pack}'.format(pack = leafPacks[i])))
            tagList.append(newTag)
    return tagList

def getDPSTag(cabinet, type):
    sampleTag = tags[type]
    inv = cabinet[0]
    dps = cabinet[2]
    sampleTag = str(sampleTag.replace('INV_2.DPS_1', 'INV_{inv}.DPS_{dps}'.format(inv = inv, dps = dps)))
    return sampleTag

def getOneBiuTag(cabinet, type):
    sampleTag = tags[type]
    inv = cabinet[0]
    dps = cabinet[2]
    biu = cabinet[4]
    sampleTag = str(sampleTag.replace('INV_2.DPS_1.BIU_1', 'INV_{inv}.DPS_{dps}.BIU_{biu}'.format(inv = inv, dps = dps, biu = biu)))
    return sampleTag

def getOneSocTag(cabinet):
    sampleTag = tags['biu_SOC']
    inv = cabinet[0]
    dps = cabinet[2]
    sampleTag = sampleTag.replace('INV_2.DPS_1', 'INV_{inv}.DPS_{dps}'.format(inv = inv, dps = dps))
    return sampleTag

def tagToPack(tag):
    index = tag.find('Pack')
    return(tag[index:][5:8])

def tagToCabinet(tag):
    index = tag.find('INV_')
    inv = tag[index:][4]
    dps = tag[index:][10]
    biu = tag[index:][16]
    return '{inv}-{dps}-{biu}'.format(inv = inv, dps = dps, biu = biu)

def tagToDPS(tag: str):
    inverterIndex = tag.find('INV_')
    dpsIndex = tag.find('DPS_')
    char1 = tag[inverterIndex+4]
    char2 = tag[dpsIndex+4]
    return char1+'-'+char2

def dpsToMaster(tag: str):
    return tag+'-1'

def convertDpsFaults(values):
    faultList = []
    for i in range(0, len(values)):
        if values[i] != 0:
            slot = i+1
            value = values[i]
            faultList.append(dpsFaultTypes[slot][int(math.log2(value)-1)])
    return faultList

def cabinetStringToDPS(faultList):
    r = re.compile('.*-.*-.*')
    registered = []
    if r.match(faultList) is not None:
        registered.append(faultList[0:3])
    return registered[0]

def dpsToCabinetStrings(dps):
    list = []
    for i in enabledBIUs:
        if i.__contains__(dps+'-'):
            list.append(i)
    return list

def compareDPSBits(current, newSelection):
    easyBits = 0
    binVal1 = bin(current)[2:].zfill(6)
    binVal2 = bin(newSelection)[2:].zfill(6)
    for i in range(-1, len(binVal1)):
        print(binVal1[i] + '-'+ binVal2[i])
        if binVal1[i] == '0' and binVal2[i] == '1':
            print('Easy reset bit ', abs(i - 6))
            easyReset = easyReset + pow(2, abs(i-6)-1)
    return easyReset

def checkBitPresence(comparee, value):
    check = 0
    binVal1 = bin(comparee)[2:].zfill(6)
    binVal2 = bin(value)[2:].zfill(6)
    
    for i in range(0, len(binVal1)):
        if binVal1[i] == '1' and binVal2[i] == '1':
            check = check+1
    if check == 1:
        return True
    elif check == 0:
        return False
    else:
        raise Exception('More than one DPS value received for a single check')
    
def reduceToDPS(lst):
    dpsList = list(map(lambda x: x[:3], lst))
    return list(set(dpsList))