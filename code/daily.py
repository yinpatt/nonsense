def get_table(ytd, td):
    df1 = pd.read_csv('main_df_{}.csv'.format(ytd))
    df2 = pd.read_csv('main_df_{}.csv'.format(td))
    df1['pid'] = df1.ccass_id+'_'+df1.taker.astype(str)
    df2['pid'] = df2.ccass_id+'_'+df2.taker.astype(str)
    df = pd.merge(df1, df2, on = 'pid', how = 'right')

    df['stake_changes'] = df.stake_y - df.stake_x
    df['holding_changes'] = df.holding_y - df.holding_x
    df.stake_changes.sort_values()
    col = ['taker_x','ccass_id_x','name_x','holding_y','holding_changes','stake_y','stake_changes']
    df = df.sort_values('stake_changes', ascending = False).dropna()[col]
    df.columns = ['Ticker','Participant ID','CCASS Participant','Shareholding','Shareholding Change','Stake%','Stake% Change']
    return df
