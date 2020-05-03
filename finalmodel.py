import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split # for validation 
import lightgbm as lgb
import gc # memory 
import argparse
import sys
from datetime import datetime # train time checking



parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', dest="input", type=argparse.FileType('r'),
        help='Input file.',
        default=sys.stdin)
args = parser.parse_args()
inputcsv = args.input


most_freq_hours_in_test_data    = [4, 5, 9, 10, 13, 14]
middle1_freq_hours_in_test_data = [16, 17, 22]
least_freq_hours_in_test_data   = [6, 11, 15]
def prep_data( df ):
    
    df['hour'] = pd.to_datetime(df.click_time).dt.hour.astype('uint8')
    df['day'] = pd.to_datetime(df.click_time).dt.day.astype('uint8')
    df.drop(['click_time'], axis=1, inplace=True)
    gc.collect()
    
    df['in_test_hh'] = (   4 
                         - 3*df['hour'].isin(  most_freq_hours_in_test_data ) 
                         - 2*df['hour'].isin(  middle1_freq_hours_in_test_data ) 
                         - 1*df['hour'].isin( least_freq_hours_in_test_data ) ).astype('uint8')
    gp = df[['ip', 'day', 'in_test_hh', 'channel']].groupby(by=['ip', 'day', 'in_test_hh'])[['channel']].count().reset_index().rename(index=str, columns={'channel': 'nip_day_test_hh'})
    df = df.merge(gp, on=['ip','day','in_test_hh'], how='left')
    df.drop(['in_test_hh'], axis=1, inplace=True)
    df['nip_day_test_hh'] = df['nip_day_test_hh'].astype('uint32')
   
    del gp
    gc.collect()

    gp = df[['ip', 'day', 'hour', 'channel']].groupby(by=['ip', 'day', 'hour'])[['channel']].count().reset_index().rename(index=str, columns={'channel': 'nip_day_hh'})
    df = df.merge(gp, on=['ip','day','hour'], how='left')
    df['nip_day_hh'] = df['nip_day_hh'].astype('uint16')
    del gp
    gc.collect()
    
    gp = df[['ip', 'os', 'hour', 'channel']].groupby(by=['ip', 'os', 'hour'])[['channel']].count().reset_index().rename(index=str, columns={'channel': 'nip_hh_os'})
    df = df.merge(gp, on=['ip','os','hour'], how='left')
    df['nip_hh_os'] = df['nip_hh_os'].astype('uint16')
    del gp
    gc.collect()

    gp = df[['ip', 'app', 'hour', 'channel']].groupby(by=['ip', 'app',  'hour'])[['channel']].count().reset_index().rename(index=str, columns={'channel': 'nip_hh_app'})
    df = df.merge(gp, on=['ip','app','hour'], how='left')
    df['nip_hh_app'] = df['nip_hh_app'].astype('uint16')
    del gp
    gc.collect()

    gp = df[['ip', 'device', 'hour', 'channel']].groupby(by=['ip', 'device', 'hour'])[['channel']].count().reset_index().rename(index=str, columns={'channel': 'nip_hh_dev'})
    df = df.merge(gp, on=['ip','device','hour'], how='left')
    df['nip_hh_dev'] = df['nip_hh_dev'].astype('uint32')
    del gp
    gc.collect()

    df.drop( ['day'], axis=1, inplace=True )
    gc.collect()
    return df
model=lgb.Booster(model_file='model.txt')
target = 'is_attributed'
predictors = ['app','device','os', 'channel', 'hour', 'nip_day_test_hh', 'nip_day_hh', 'nip_hh_os', 'nip_hh_app', 'nip_hh_dev']
categorical = ['app', 'device', 'os', 'channel', 'hour']

    
from ipaddress import IPv4Address
import random

def ipecg(seed):
    random.seed(seed)
    return str(IPv4Address(random.getrandbits(32)))
def ipgen(ip):

    
    
    j=random.randint(2,999)
    rev=ipecg(ip+j)
    return rev
    

dtypes = {
        'ip'            : 'uint32',
        'app'           : 'uint16',
        'device'        : 'uint16',
        'os'            : 'uint16',
        'channel'       : 'uint16',
        'is_attributed' : 'uint8',
        'click_id'      : 'uint32'
        }


test_cols = ['ip','app','device','os', 'channel', 'click_time', 'click_id']
test_df = pd.read_csv(inputcsv, dtype=dtypes, usecols=test_cols)
test_df2 = prep_data(test_df)

sub = pd.DataFrame()
sub['click_id'] = test_df2['click_id']
sub['ip']=test_df2['ip']



sub['is_attributed']=model.predict(test_df2[predictors])
k=sub[sub['is_attributed']==0.0]
sub['address']=k['ip']
fp=open("ipt.txt","w")
print("Starting IP Predictions")
for i in k['ip']:

        fp.write(ipgen(i))
        fp.write('\n')
        print("Predicting Fraudulent Entries")
fp.close()


leg = sub[sub['is_attributed']==1.0]
sub['address']=leg['ip']
fp1=open("legit.txt","w")
#print("Starting IP Predictions")
for i in leg['ip']:

        fp1.write(ipgen(i))
        fp1.write('\n')
        print("Predicting Legitimate Entries")
fp1.close()


print("Completed Predictions")
#sub.to_csv(output_filename, index=False, float_format='%.9f')
