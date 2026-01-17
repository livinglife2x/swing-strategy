def backtest_strategy(df):
    """Run backtest on the data"""
    position = 0  # 0: no position, 1: long, -1: short
    entry_price = None
    entry_time = None
    entry_reason = None
    trade_count = 0
    wins = 0
    losses = 0
    total_pnl = 0
    support = None
    resistance = None
    last_resistance_time = None
    last_support_time = None
    last_long_resistance_time = None
    last_short_support_time = None
    trades_list = []
    
    # Add signal columns
    df['Signal'] = 0
    df['Position'] = 0
    df['PnL'] = 0.0
    
    # Extract time from datetime for intraday close check
    df['Time'] = pd.to_datetime(df['Datetime']).dt.time
    df['Date'] = pd.to_datetime(df['Datetime']).dt.date
    
    # Strategy loop
    for i in range(2, len(df)):
        current_price = df.loc[i, 'Close']
        current_open = df.loc[i, 'Open']
        current_high = df.loc[i, 'High']
        current_low = df.loc[i, 'Low']
        current_time = df.loc[i, 'Time']
        current_date = df.loc[i, 'Date']
        prev_low = df.loc[i-1, 'Low']
        prev_high = df.loc[i-1, 'High']
        prev_close = df.loc[i-1, 'Close']
        
        # Detect RESISTANCE
        if (df.loc[i-1, 'High'] > df.loc[i-2, 'High'] and 
            df.loc[i-1, 'High'] > current_high and
            df.loc[i-1, 'Low'] > df.loc[i-2, 'Low'] and
            df.loc[i-1, 'Low'] > current_low):
            resistance = df.loc[i-1, 'High']
            last_resistance_time = df.loc[i-1, 'Datetime']
        
        # Detect SUPPORT
        if (df.loc[i-1, 'Low'] < df.loc[i-2, 'Low'] and 
            df.loc[i-1, 'Low'] < current_low and
            df.loc[i-1, 'High'] < df.loc[i-2, 'High'] and
            df.loc[i-1, 'High'] < current_high):
            support = df.loc[i-1, 'Low']
            last_support_time = df.loc[i-1, 'Datetime']
        
        # INTRADAY CLOSE at 3:15 PM
        if position != 0:
            entry_date = pd.to_datetime(entry_time).date()
            entry_time_only = pd.to_datetime(entry_time).time()
            
            # Check if we're at or past 3:15 PM on same day as entry
            if current_date == entry_date and current_time >= pd.to_datetime('15:15:00').time():
                # Determine exit price
                if entry_time_only == pd.to_datetime('15:15:00').time():
                    # Trade opened at 3:15, close at 3:15 close
                    exit_price = current_price
                else:
                    # Trade opened before 3:15, close at 3:15 open
                    exit_price = current_open
                
                exit_time = df.loc[i, 'Datetime']
                
                # Calculate PnL
                if position == 1:
                    pnl = (exit_price - entry_price) / entry_price
                    absolute_profit = exit_price - entry_price
                else:
                    pnl = (entry_price - exit_price) / entry_price
                    absolute_profit = entry_price - exit_price
                
                total_pnl += pnl
                
                # Store trade
                trades_list.append({
                    'Entry Time': entry_time,
                    'Entry Price': entry_price,
                    'Exit Time': exit_time,
                    'Exit Price': exit_price,
                    'Position': 'Long' if position == 1 else 'Short',
                    'Entry Reason': entry_reason,
                    'Exit Reason': 'Intraday close at 3:15 PM',
                    'Absolute Profit': absolute_profit,
                    'PnL %': pnl * 100
                })
                
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1
                
                df.loc[i, 'Signal'] = -position
                df.loc[i, 'PnL'] = pnl
                position = 0
                entry_price = None
                continue
        
        # LONG ENTRY
        if position == 0 and resistance is not None and last_resistance_time is not None:
            if prev_close > resistance and (last_long_resistance_time is None or last_resistance_time > last_long_resistance_time):
                position = 1
                entry_price = current_open
                entry_time = df.loc[i, 'Datetime']
                entry_reason = f"Closed above resistance ({resistance:.2f})"
                last_long_resistance_time = last_resistance_time
                trade_count += 1
                df.loc[i, 'Signal'] = 1
                df.loc[i, 'Position'] = 1
                continue
        
        # SHORT ENTRY
        if position == 0 and support is not None and last_support_time is not None:
            if prev_close < support and (last_short_support_time is None or last_support_time > last_short_support_time):
                position = -1
                entry_price = current_open
                entry_time = df.loc[i, 'Datetime']
                entry_reason = f"Closed below support ({support:.2f})"
                last_short_support_time = last_support_time
                trade_count += 1
                df.loc[i, 'Signal'] = -1
                df.loc[i, 'Position'] = -1
                continue
        
        # STOPLOSS EXITS
        if position != 0:
            exit_signal = False
            exit_price = None
            exit_reason = None
            
            if position == 1:
                if current_open < prev_low:
                    exit_signal = True
                    exit_price = current_open
                    exit_reason = 'Opened below previous low'
                elif current_low < prev_low:
                    exit_signal = True
                    exit_price = prev_low
                    exit_reason = 'Crossed below previous low'
            
            if position == -1:
                if current_open > prev_high:
                    exit_signal = True
                    exit_price = current_open
                    exit_reason = 'Opened above previous high'
                elif current_high > prev_high:
                    exit_signal = True
                    exit_price = prev_high
                    exit_reason = 'Crossed above previous high'
            
            if exit_signal:
                exit_time = df.loc[i, 'Datetime']
                
                if position == 1:
                    pnl = (exit_price - entry_price) / entry_price
                    absolute_profit = exit_price - entry_price
                else:
                    pnl = (entry_price - exit_price) / entry_price
                    absolute_profit = entry_price - exit_price
                
                total_pnl += pnl
                
                trades_list.append({
                    'Entry Time': entry_time,
                    'Entry Price': entry_price,
                    'Exit Time': exit_time,
                    'Exit Price': exit_price,
                    'Position': 'Long' if position == 1 else 'Short',
                    'Entry Reason': entry_reason,
                    'Exit Reason': exit_reason,
                    'Absolute Profit': absolute_profit,
                    'PnL %': pnl * 100
                })
                
                if pnl > 0:
                    wins += 1
                else:
                    losses += 1
                
                df.loc[i, 'Signal'] = -position
                df.loc[i, 'PnL'] = pnl
                position = 0
                entry_price = None
                continue
        
        # Track position
        if position == 1:
            df.loc[i, 'Position'] = 1
        elif position == -1:
            df.loc[i, 'Position'] = -1
    
    # Calculate metrics
    win_rate = (wins / trade_count * 100) if trade_count > 0 else 0
    avg_pnl = (total_pnl / trade_count * 100) if trade_count > 0 else 0
    
    trades_df = pd.DataFrame(trades_list) if trades_list else pd.DataFrame()
    
    return trades_df
