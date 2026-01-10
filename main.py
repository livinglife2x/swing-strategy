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
position=0
support = config.get('support')
resistance = config.get('resistance')
last_resistance_time = config.get('last_resistance_time')
last_support_time = config.get('last_support_time')
last_long_resistance_time = config.get('last_long_resistance_time')
last_short_support_time = config.get('last_short_support_time')



while True:
    now = datetime.now(india)
    if now.time()>=datetime.strptime("9:15:00", '%H:%M:%S').time() and now.time()<datetime.strptime("15:29:00", '%H:%M:%S').time():
    
        
        
        # Check for 30-minute scheduled executions (9:00 to 15:30)
        if (9 <= now.hour < 15 or (now.hour == 15 and now.minute <= 30)):
            if now.minute in [15, 45] and now.second == 2 :
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
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Resistance detected previous day at {data[2].iloc[1]} \n')
                                    resistance=data[2].iloc[1]
                                    last_resistance_time=now
                            if data[2].iloc[1]<data[2].iloc[2] and data[2].iloc[1]<data[2].iloc[0]:
                                if data[3].iloc[1]<data[3].iloc[2] and data[3].iloc[1]<data[3].iloc[0]:
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {data[3].iloc[1]} \n')
                                    support = data[3].iloc[1]
                                    last_support_time = now
                    
                    
                    
                    #build for 9:45 logic also
                    elif now.hour==9 and now.minute==45:

                        start_date=str(now.date()+timedelta(days = -10))
                        end_date = str(now.date())
                        intraday_data = get_intraday_data(instrument)
                        hist_data = get_historical_data(instrument,start_date,end_date)
                        if intraday_data and hist_data:
                            if hist_data[2].iloc[0]>intraday_data[2].iloc[0] and hist_data[2].iloc[0]>hist_data[2].iloc[1]:
                                if hist_data[3].iloc[0]>intraday_data[3].iloc[0] and hist_data[3].iloc[0]>hist_data[3].iloc[1]:
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Resistance detected previous day at {hist_data[2].iloc[0]} \n')
                                    resistance = hist_data[2].iloc[0]
                                    last_resistance_time=now
                            if hist_data[3].iloc[0]<intraday_data[3].iloc[0] and hist_data[3].iloc[0]<hist_data[3].iloc[1]:
                                if hist_data[2].iloc[0]<intraday_data[2].iloc[0] and hist_data[2].iloc[0]<hist_data[2].iloc[1]:
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {hist_data[3].iloc[0]} \n')
                                    support = hist_data[3].iloc[0]
                                    last_support_time = now

                        

                    elif now.hour==10 and now.minute==15:
                        start_date=str(now.date()+timedelta(days = -10))
                        end_date = str(now.date())
                        intraday_data = get_intraday_data(instrument)
                        hist_data = get_historical_data(instrument,start_date,end_date)
                        if intraday_data and hist_data:
                            if intraday_data[2].iloc[1]>hist_data[2].iloc[0] and intraday_data[2].iloc[1]>intraday_data[2].iloc[0]:
                                if intraday_data[3].iloc[1]>hist_data[3].iloc[0] and intraday_data[3].iloc[1]>intraday_data[3].iloc[0]:
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Resistance detected previous day at {intraday_data[2].iloc[1]} \n')
                                    resistance = intraday_data[2].iloc[1]
                                    last_resistance_time=now
                            if intraday_data[2].iloc[1]<hist_data[2].iloc[0] and intraday_data[2].iloc[1]<intraday_data[2].iloc[0]:
                                if intraday_data[3].iloc[1]<hist_data[3].iloc[0] and intraday_data[3].iloc[1]<intraday_data[3].iloc[0]:
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {intraday_data[3].iloc[1]} \n')
                                    support = intraday_data[3].iloc[1]
                                    last_support_time = now
            


                    else:
                        intraday_data = get_intraday_data(instrument)
                        if intraday_data:
                            if intraday_data[2].iloc[1]>intraday_data[2].iloc[0] and intraday_data[2].iloc[1]>intraday_data[2].iloc[2]:
                                if intraday_data[3].iloc[1]>intraday_data[3].iloc[0] and intraday_data[3].iloc[1]>intraday_data[3].iloc[2]:
                                    with open('sr_log.txt', 'a') as f:
                                            f.write(str(now)+f' - Resistance detected previous day at {intraday_data[2].iloc[1]} \n')
                                    resistance = intraday_data[2].iloc[1]
                                    last_resistance_time=now
                            if intraday_data[2].iloc[1]<intraday_data[2].iloc[0] and intraday_data[2].iloc[1]<intraday_data[2].iloc[2]:
                                if intraday_data[3].iloc[1]<intraday_data[3].iloc[0] and intraday_data[3].iloc[1]<intraday_data[3].iloc[2]:
                                    with open('sr_log.txt', 'a') as f:
                                        f.write(str(now)+f' - Support detected previous day at {intraday_data[3].iloc[1]} \n')
                                    support = intraday_data[3].iloc[1]
                                    last_support_time = now

                            


                            #look at old code to see how high low close open are defined
                            #select last three candles and define support/resistanhce
                            #see cluade code to how to define last resistance/support
                            #last resistance/support time and variables to be stored in config file
                    
                    

                    if position==0 and resistance is not None and last_resistance_time is not None:
                        intraday_data = get_intraday_data(instrument)
                        if intraday_data:
                            if intraday_data[4].iloc[0]>resistance and (last_long_resistance_time is None or last_resistance_time>last_long_resistance_time):
                                position=1
                                ltp = get_ltp(instrument,access_token)
                                entry_price = ltp
                                entry_time=now
                                entry_reason = f"Closed above resistance {resistance}"
                                last_long_resistance_time = last_resistance_time
                    if position==0 and support is not None and last_support_time is not None:
                        intraday_data = get_intraday_data(instrument)
                        if intraday_data:
                            if intraday_data[4].iloc[0]<support and (last_short_support_time is None or last_support_time>last_short_support_time):
                                position=-1
                                ltp = get_ltp(instrument,access_token)
                                entry_price = ltp
                                entry_time=now
                                entry_reason = f"Closed below support {support}"
                    
                

                    last_scheduled_execution = now
        
        if position==1 and now.time()>=datetime.strptime("15:18:00", '%H:%M:%S').time():
            
            exit_price=get_ltp(instrument,access_token)
            exit_time = now
            exit_reason = "eod"
            profit = exit_price-entry_price
            profit_perc = (100*(exit_price-entry_price))/entry_price
            with open('trade_log.txt', 'a') as f:
                f.write(f'{entry_time},{entry_price},{entry_reason},{exit_time},{exit_price},{exit_reason},{profit},{profit_perc},{position} \n')
            position=0
        if position==-1 and now.time()>=datetime.strptime("15:18:00", '%H:%M:%S').time():
            position=0
            exit_price=get_ltp(instrument,access_token)
            exit_time = now
            exit_reason = "eod"
            profit = entry_price-exit_price
            profit_perc = (100*(entry_price-exit_price))/entry_price
            with open('trade_log.txt', 'a') as f:
                f.write(f'{entry_time},{entry_price},{entry_reason},{exit_time},{exit_price},{exit_reason},{profit},{profit_perc},{position} \n')

        
        # Check for 9:15-15:30 frequent execution window (every 2 seconds)
        if (now.hour == 9 and now.minute >= 15) or \
        (9 < now.hour < 15) or \
        (now.hour == 15 and now.minute <= 30):
            if last_frequent_execution is None or (now - last_frequent_execution).total_seconds() >= 2:
                #my_task()
                if position==1:
                    intraday_data = get_intraday_data(instrument)
                    ltp = get_ltp(instrument,access_token)
                    if ltp and ltp<=intraday_data[3].iloc[0]:
                        
                        exit_price = ltp
                        exit_time=now
                        exit_reason = "less than prv low"
                        profit = exit_price-entry_price
                        profit_perc = (100*(exit_price-entry_price))/entry_price
                        with open('trade_log.txt', 'a') as f:
                            f.write(f'{entry_time},{entry_price},{entry_reason},{exit_time},{exit_price},{exit_reason},{profit},{profit_perc},{position} \n')
                        position=0
                if position==-1:
                    intraday_data = get_intraday_data(instrument)
                    ltp = get_ltp(instrument,access_token)
                    if ltp and  ltp>=intraday_data[2].iloc[0]:
                        exit_price=ltp
                        exit_time=now
                        exit_reason = "greater then prv high"
                        profit = entry_price-exit_price
                        profit_perc = (100*(entry_price-exit_price))/entry_price
                        with open('trade_log.txt', 'a') as f:
                            f.write(f'{entry_time},{entry_price},{entry_reason},{exit_time},{exit_price},{exit_reason},{profit},{profit_perc},{position} \n')
                        position=0


                last_frequent_execution = now
        

        time.sleep(0.01)







