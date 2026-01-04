from dep import *
import time
from datetime import datetime, timedelta
import pytz
import pandas as pd

config = load_dict_json("config.json")

access_token = config['access_token']
print (f"Access Token: {access_token}")

last_frequent_execution = None
last_scheduled_execution = None
india = pytz.timezone('Asia/Calcutta')

instrument = "NSE_EQ|INE160A01022"



while True:
    now = datetime.now(india)
    if now.time()>=datetime.strptime("9:15:00", '%H:%M:%S').time():
    
        """
        # Check for 9:15-15:30 frequent execution window (every 2 seconds)
        if (now.hour == 9 and now.minute >= 15) or \
        (9 < now.hour < 15) or \
        (now.hour == 15 and now.minute <= 30):
            if last_frequent_execution is None or (now - last_frequent_execution).total_seconds() >= 2:
                my_task()
                last_frequent_execution = now
        """
        
        # Check for 15-minute scheduled executions (9:00 to 15:30)
        if (9 <= now.hour < 15 or (now.hour == 15 and now.minute <= 30)):
            if now.minute in [0, 15, 30, 45] and now.second == 2 :
                if last_scheduled_execution is None or (now - last_scheduled_execution).total_seconds() > 5:
                    #my_task()
                    if now.hour==9 and now.minute==15:
                        start_date=str(now.date()+timedelta(days = -10))
                        end_date = str(now.date())
                        data = get_historical_data(instrument,start_date,end_date)
                        if data:
                            data = pd.DataFrame(data['data']['candles'])
                            if data[2].iloc[1]>data[2].iloc[2] and data[2].iloc[1]>data[2].iloc[0]:
                                if data[3].iloc[1]>data[3].iloc[2] and data[3].iloc[1]>data[3].iloc[0]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Resistance detected previous day at {data[2].iloc[1]} \n')

                            if data[2].iloc[1]<data[2].iloc[2] and data[2].iloc[1]<data[2].iloc[0]:
                                if data[3].iloc[1]<data[3].iloc[2] and data[3].iloc[1]<data[3].iloc[0]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {data[3].iloc[1]} \n')
                    
                    elif now.hour==9 and now.minute==30:
                        start_date=str(now.date()+timedelta(days = -10))
                        end_date = str(now.date())
                        intraday_data = get_intraday_data(instrument)
                        hist_data = get_historical_data(instrument,start_date,end_date)
                        if intraday_data and hist_data:
                            if hist_data[2].iloc[0]>intraday_data[2].iloc[0] and hist_data[2].iloc[0]>hist_data[2].iloc[1]:
                                if hist_data[3].iloc[0]>intraday_data[3].iloc[0] and hist_data[3].iloc[0]>hist_data[3].iloc[1]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Resistance detected previous day at {hist_data[2].iloc[0]} \n')

                            if hist_data[3].iloc[0]<intraday_data[3].iloc[0] and hist_data[3].iloc[0]<hist_data[3].iloc[1]:
                                if hist_data[2].iloc[0]<intraday_data[2].iloc[0] and hist_data[2].iloc[0]<hist_data[2].iloc[1]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {hist_data[3].iloc[0]} \n')
                    
                    #build for 9:45 logic also
                    elif now.hour==9 and now.minute==45:
                        start_date=str(now.date()+timedelta(days = -10))
                        end_date = str(now.date())
                        intraday_data = get_intraday_data(instrument)
                        hist_data = get_historical_data(instrument,start_date,end_date)
                        if intraday_data and hist_data:
                            if intraday_data[2].iloc[1]>hist_data[2].iloc[0] and intraday_data[2].iloc[1]>intraday_data[2].iloc[0]:
                                if intraday_data[3].iloc[1]>hist_data[3].iloc[0] and intraday_data[3].iloc[1]>intraday_data[3].iloc[0]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Resistance detected previous day at {intraday_data[2].iloc[1]} \n')
                            
                            if intraday_data[2].iloc[1]<hist_data[2].iloc[0] and intraday_data[2].iloc[1]<intraday_data[2].iloc[0]:
                                if intraday_data[3].iloc[1]<hist_data[3].iloc[0] and intraday_data[3].iloc[1]<intraday_data[3].iloc[0]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {intraday_data[3].iloc[1]} \n')

                    else:
                        intraday_data = get_intraday_data(instrument)
                        if intraday_data:
                            if intraday_data[2].iloc[1]>intraday_data[2].iloc[0] and intraday_data[2].iloc[1]>intraday_data[2].iloc[2]:
                                if intraday_data[3].iloc[1]>intraday_data[3].iloc[0] and intraday_data[3].iloc[1]>intraday_data[3].iloc[2]:
                                    with open('trading_log.txt', 'a') as f:
                                            f.write(str(now)+f' - Resistance detected previous day at {intraday_data[2].iloc[1]} \n')

                            if intraday_data[2].iloc[1]<intraday_data[2].iloc[0] and intraday_data[2].iloc[1]<intraday_data[2].iloc[2]:
                                if intraday_data[3].iloc[1]<intraday_data[3].iloc[0] and intraday_data[3].iloc[1]<intraday_data[3].iloc[2]:
                                    with open('trading_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {intraday_data[3].iloc[1]} \n')


                            


                            #look at old code to see how high low close open are defined
                            #select last three candles and define support/resistanhce
                            #see cluade code to how to define last resistance/support
                            #last resistance/support time and variables to be stored in config file


                    last_scheduled_execution = now
        
        time.sleep(0.01)







