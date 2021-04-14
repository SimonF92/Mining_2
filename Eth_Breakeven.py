import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.stats import linregress
import seaborn as sns




dates= pd.date_range(start="2021-01-01",end="2021-12-31")

len(dates)

gwei=[125]*len(dates)

df=pd.read_csv('export-BlockDifficulty.csv')
df

extrapolated_values=list(range((2079-97),2347,1))
extrapolated_values












df1=df.tail(98)
df1

x=np.array(df1.index)
y=np.array(df1.Value)

extrapolator = UnivariateSpline( x, y, k=1 )
test=extrapolator(extrapolated_values)
test


#================================================#
#================================================#


x=extrapolator.get_coeffs()
y=list(range(0,len(x)))

equation=linregress(y, x)


#================================================#
#================================================#



maindf=pd.DataFrame(dates, test)
maindf=maindf.reset_index()
maindf.columns=['difficulty','Date']
maindf['difficulty_constant']=6629.625/maindf['difficulty']
maindf['100mhs_Earnings_Per_Month_USD']=8.14*maindf['difficulty_constant']*30
maindf['100mhs_Earnings_Per_Day_USD']=8.14*maindf['difficulty_constant']
maindf

vals=maindf['100mhs_Earnings_Per_Month_USD'].values.tolist()
vals

vals_adjusted=[]
i=0

for item in vals:
    
    if i < 200:
        vals_adjusted.append(item)
        
    else:
        vals_adjusted.append((item/100)*70)
        
    i+=1
        
maindf['Adjusted for EIP1559']=vals_adjusted
maindf['Daily for EIP1559']=maindf['Adjusted for EIP1559']/30

maindf['With Electricity']=maindf['Adjusted for EIP1559']-20
maindf['With Electricity Daily']=maindf['Daily for EIP1559']-(20/30)
maindf['With Electricity and Taxes/ Daily']=((maindf['Daily for EIP1559']-(20/30))/100)*88

maindf['Jan_Revenue']=maindf['Daily for EIP1559'].cumsum()
maindf['Jan_Earnings']=maindf['With Electricity and Taxes/ Daily'].cumsum()

maindf['Feb_Revenue']=maindf['Daily for EIP1559'].tail(-30).cumsum()
maindf['Feb_Earnings']=maindf['With Electricity and Taxes/ Daily'].tail(-30).cumsum()

maindf['March_Revenue']=maindf['Daily for EIP1559'].tail(-60).cumsum()
maindf['March_Earnings']=maindf['With Electricity and Taxes/ Daily'].tail(-60).cumsum()

maindf['April_Revenue']=maindf['Daily for EIP1559'].tail(-90).cumsum()
maindf['April_Earnings']=maindf['With Electricity and Taxes/ Daily'].tail(-90).cumsum()

maindf['May_Revenue']=maindf['Daily for EIP1559'].tail(-120).cumsum()
maindf['May_Earnings']=maindf['With Electricity and Taxes/ Daily'].tail(-120).cumsum()







#==========================================================#
#==========================================================#








y = maindf[maindf.columns[-10:]]
x=maindf[maindf.columns[:2]]
y
x

result = pd.concat([y, x], axis=1)
dfmelt= pd.melt(result, id_vars=['difficulty','Date'], value_vars=['Jan_Revenue', 'Jan_Earnings','Feb_Revenue', 'Feb_Earnings','March_Revenue', 'March_Earnings','April_Revenue', 'April_Earnings','May_Revenue', 'May_Earnings'])

months=dfmelt['variable'].values.tolist()

months_2=[]
type_2=[]

for thing in months:
    month=thing.split('_')[0]
    types=thing.split('_')[1]
    months_2.append(month)
    type_2.append(types)
    
months_2

dfmelt['Miner started in:']=months_2
dfmelt['type']=type_2
dfmelt








#==========================================================#
#==========================================================#









g=sns.relplot(
    data=dfmelt,
    x="Date", y="value",
    hue="type", col='type',row='Miner started in:',
    height=4, aspect=1.1, kind="line"
)


g.set_axis_labels("Timepoint", "Net Value ($)")
g.set_xticklabels(rotation=30)
g.map(plt.axhline, y=1500, color=".7", dashes=(2, 1), zorder=0)
g.map(plt.text, x=pd.datetime(2021,1,1), y=1650, s='Break even on $1500 \non 100Mhs')


g.savefig('mining_facet.png')
