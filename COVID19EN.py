# -*- coding: UTF-8 -*-
from tkinter import * 
import os 
# storing and anaysis
import pandas as pd
import wget

# visualization
import plotly.express as px
import plotly.figure_factory as ff
import calmap
#import folium
# converter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()   

# hide warnings
import warnings
warnings.filterwarnings('ignore')
import arabic_reshaper
from bidi.algorithm import get_display

###############################################################################33

def download_csv():
	urls = ['https://raw.githubusercontent.com/mopicala-group/data_up/master/covid_19_pik.csv']
	for url in urls:
		filename = wget.download(url)
		
download_csv()

list_m = ["covid_19_pik.csv"]


#################################################################################################################################3


#-----------------------------------End update---------------------------------------------#
# color pallette
cnf = '#393e46' # confirmed - grey
dth = '#ff2e63' # death - red
rec = '#21bf73' # recovered - cyan
act = '#fe9801' # active case - yellow
#_____________________________________________________________
# importing datasets
full_table = pd.read_csv('covid_19_pik.csv',
                         parse_dates=['Date'])
full_table.head()

for hj in list_m:
     print(hj)
     try:
          os.remove(hj)
          print("delete files :",hj)
     except:
          print("no file? :",hj)
          
#data preprocessing
# cases 
cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']

# Active Case = confirmed - deaths - recovered
full_table['Active'] = full_table['Confirmed'] - full_table['Deaths'] - full_table['Recovered']

# replacing Mainland china with just China
full_table['Country/Region'] = full_table['Country/Region'].replace('Mainland China', 'China')

# filling missing values 
full_table[['Province/State']] = full_table[['Province/State']].fillna('')
full_table[cases] = full_table[cases].fillna(0)
# cases in the ships
ship = full_table[full_table['Province/State'].str.contains('Grand Princess')|full_table['Country/Region'].str.contains('Cruise Ship')]

# china and the row
china = full_table[full_table['Country/Region']=='China']
row = full_table[full_table['Country/Region']!='China']

# latest
full_latest = full_table[full_table['Date'] == max(full_table['Date'])].reset_index()
china_latest = full_latest[full_latest['Country/Region']=='China']
row_latest = full_latest[full_latest['Country/Region']!='China']

# latest condensed
full_latest_grouped = full_table.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
china_latest_grouped = china_latest.groupby('Province/State')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
row_latest_grouped = row_latest.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
temp = full_table.groupby(['Country/Region', 'Province/State'])['Confirmed', 'Deaths', 'Recovered', 'Active'].max()
# temp.style.background_gradient(cmap='Reds')
#______________________________________________________

#2222222
"""
يمكننا اظهار الاحصائىة للدولة معين بأخال اسمها
"""
def latest_your_country():
    
    gdf = full_latest_grouped.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered'].max()
    gdf = gdf.reset_index()

    temp = gdf[gdf['Country/Region']==var.get()].reset_index()
    temp = temp.melt(id_vars='Date', value_vars=['Confirmed', 'Deaths', 'Recovered'],
                var_name='Case', value_name='Count')
    fig = px.bar(temp, x="Date", y="Count", color='Case', facet_col="Case",
                 title= "  "+str(var.get()), color_discrete_sequence=[cnf, dth, rec])
    fig.show()
    
    
    
#________________________________
def latest_complete_data():
    """latest complete data"""
    #b111111111111
    temp = full_latest_grouped.groupby('Date')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
    temp = temp[temp['Date']==max(temp['Date'])].reset_index(drop=True)
    temp.style.background_gradient(cmap='Pastel1')    
    tm = temp.melt(id_vars="Date", value_vars=['Active', 'Deaths', 'Recovered'])
    fig = px.treemap(tm, path=["variable"], values="value", height=400, width=600,
                     color_discrete_sequence=[rec, act, dth])
    fig.show()
#b26
def cases_spread():
    temp = full_table.groupby(['Date', 'Country/Region'])['Confirmed'].sum().reset_index().sort_values('Confirmed', ascending=False)
    fig = px.line(temp, x="Date", y="Confirmed", color='Country/Region', title='Cases Spread', height=600)
    fig.show()

"""all country by confirmed"""
#b2222222222222222222222222222222
def all_country_by_confirmed():
    temp_f = full_table.sort_values(by='Confirmed', ascending=False)
    temp_f = temp_f.reset_index(drop=True)
    temp_f.style.background_gradient(cmap='Reds')
    fig = px.line(temp_f, x="Date", y="Confirmed", color='Country/Region', title='all country by confirmed', height=600)
    fig.show()

"""all country by deaths"""
def all_country_by_deaths():
    #b333333333333333333333333333333333333
    temp_f = full_table.sort_values(by='Deaths', ascending=False)
    temp_f = temp_f.reset_index(drop=True)
    fig = px.line(temp_f, x="Date", y="Deaths", color='Country/Region', title='all country by deaths', height=600)
    fig.show()

#b44444444444444444444444444444444444444
"""All country by recovered"""
def all_country_by_recovered():
    temp_f = full_table.sort_values(by='Recovered', ascending=False)
    temp_f = temp_f.reset_index(drop=True)
    fig = px.line(temp_f, x="Date", y="Recovered", color='Country/Region', title='all_country_by_recovered', height=600)
    fig.show()

#________________________________________________________________#
def CON():
    #b5
    temp_f = full_latest_grouped.sort_values(by='Confirmed', ascending=False)
    temp_f = temp_f.reset_index(drop=True)
    temp_f.style.background_gradient(cmap='Reds')
    temp_flg = temp_f[temp_f['Confirmed']>0][['Country/Region', 'Confirmed']]
    temp_flg.sort_values('Confirmed', ascending=False).reset_index(drop=True).style.background_gradient(cmap='Reds')
    print()
    #CON b5
    fig = px.bar(temp_flg.sort_values('Confirmed', ascending=False).head(30).sort_values('Confirmed', ascending=True), 
                 x="Confirmed", y="Country/Region", title='Confirmed Cases', text='Confirmed', orientation='h', 
                 width=700, height=700, range_x = [0, max(temp_flg['Confirmed'])+50000])
    fig.update_traces(marker_color='#46cdcf', opacity=0.8, textposition='outside')
    fig.show()

def DEA():
    #b6
    temp_f = full_latest_grouped.sort_values(by='Deaths', ascending=False)
    temp_f = temp_f.reset_index(drop=True)
    temp_f.style.background_gradient(cmap='Reds')
    temp_flg = temp_f[temp_f['Deaths']>0][['Country/Region', 'Deaths']]
    temp_flg.sort_values('Deaths', ascending=False).reset_index(drop=True).style.background_gradient(cmap='Reds')
    
    #DEA b6
    fig = px.bar(temp_flg.sort_values('Deaths', ascending=False).head(30).sort_values('Deaths', ascending=True), 
                 x="Deaths", y="Country/Region", title='Deaths Cases', text='Deaths', orientation='h', 
                 width=700, height=700, range_x = [0, max(temp_flg['Deaths'])+50000])
    fig.update_traces(marker_color='#46cdcf', opacity=0.8, textposition='outside')
    fig.show()
    
def REC():
    #b7
    temp_flg = full_latest_grouped
    #REC b7
    fig = px.bar(temp_flg.sort_values('Recovered', ascending=True), 
             x="Recovered", y="Country/Region", title='Recovered', text='Recovered', orientation='h', 
             width=700, height=700, range_x = [0, max(temp_flg['Recovered'])+50000])
    fig.update_traces(marker_color=rec, opacity=0.6, textposition='outside')
    fig.show()
    
#__________________________________________________________________________________
#b88888888888888888888888888
"""Countries with no cases recovered  الدول التي لم يتم شفاء اي شخص فيها """
def no_rec():
    temp_f = full_latest_grouped.sort_values(by='Recovered', ascending=False)
    temp_f = temp_f[temp_f['Recovered']==0][['Country/Region', 'Confirmed', 'Deaths', 'Recovered']]
    temp_f = temp_f[temp_f.Recovered == 0]
    fig = px.bar(temp_f,x='Country/Region',y="Recovered",color='Country/Region', title='all country no Recovered', height=600)
    fig.show() 
   
#b999999999999999999999999999
def no_dea():
    temp_f = full_latest_grouped.sort_values(by='Deaths', ascending=False)
    temp_f = temp_f[temp_f.Deaths == 0]
    fig = px.bar(temp_f,x='Country/Region',y="Deaths",color='Country/Region', title='all country no deaths', height=600)
    fig.show()

"""البلدان التي تعافت من جميع الحالات"""
def all_rec():
    temp_f = full_latest_grouped.sort_values(by='Confirmed', ascending=False)
    #print(temp_f.head())
    temp_f = temp_f[temp_f['Recovered'] != 0][['Country/Region', 'Confirmed', 'Deaths', 'Recovered']]
    temp_f = temp_f[temp_f.Recovered == temp_f.Confirmed]
    fig = px.bar(temp_f,x='Country/Region',y="Recovered",color='Country/Region', title='all country full Recovered', height=600)
    fig.show()
 
#b10000000
"""Countries with all cases died"""
def all_dea():
    temp = full_latest_grouped[full_latest_grouped['Confirmed']==
						      full_latest_grouped['Deaths']]
    temp = temp[['Country/Region', 'Confirmed', 'Deaths']]
    temp = temp.sort_values('Confirmed', ascending=False)
    fig = px.bar(temp,x='Country/Region',y="Deaths",color='Country/Region', title='all country no deaths', height=600)
    fig.show()
     
#b122222222222222222
"""البلدان التي لم تعد فيها حالات إصابة"""
def zero_cases():
    temp = full_latest_grouped[full_latest_grouped['Confirmed']==full_latest_grouped['Deaths']+row_latest_grouped['Recovered']]
    temp = temp[['Country/Region', 'Confirmed', 'Deaths', 'Recovered']]
    temp = temp.sort_values('Confirmed', ascending=False)
    fig = px.bar(temp,x='Country/Region',y="Recovered",color='Country/Region', title='all country no deaths', height=600)
    fig.show()





            #GRAPH WORLD
#b2222222222222222222222222222200000000000
"""**graph** to the world"""

def graph_world():
# World wide
    m = folium.Map(location=[0, 0], tiles='cartodbpositron',min_zoom=1, max_zoom=4, zoom_start=1)
    for i in range(0, len(full_latest)):
        folium.Circle(
                location=[full_latest.iloc[i]['Lat'], full_latest.iloc[i]['Long']],
                color='crimson', 
                tooltip =   '<li><bold>Country : '+str(full_latest.iloc[i]['Country/Region'])+
                    '<li><bold>Province : '+str(full_latest.iloc[i]['Province/State'])+
                    '<li><bold>Confirmed : '+str(full_latest.iloc[i]['Confirmed'])+
                    '<li><bold>Deaths : '+str(full_latest.iloc[i]['Deaths'])+
                    '<li><bold>Recovered : '+str(full_latest.iloc[i]['Recovered']),
                    radius=int(full_latest.iloc[i]['Confirmed'])**1.1).add_to(m)
        m
#___________________________________


"""رسمة التضخم مع التاريخ لانتشار الفايروس"""
def expansion_covid19():
    formated_gdf = full_table.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered'].max()
    formated_gdf = formated_gdf.reset_index()
    formated_gdf['Date'] = pd.to_datetime(formated_gdf['Date'])
    formated_gdf['Date'] = formated_gdf['Date'].dt.strftime('%m/%d/%Y')
    formated_gdf['size'] = formated_gdf['Confirmed'].pow(0.3)

    fig = px.scatter_geo(formated_gdf, locations="Country/Region", locationmode='country names', 
                     color="Confirmed", size='size', hover_name="Country/Region", 
                     range_color= [0, max(formated_gdf['Confirmed'])+2], 
                     projection="natural earth", animation_frame="Date", 
                     title='Spread over time')
    fig.update(layout_coloraxis_showscale=False)
    fig.show()

#b2222222222222222222222222222222222222222222
"""منسوب ارتفاع الحالات مع الوقت """
def con_time():
    temp = full_table.groupby('Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()
    temp = temp.melt(id_vars="Date", value_vars=['Recovered', 'Deaths', 'Active'],var_name='Case', value_name='Count')
    temp.head()
    fig = px.area(temp, x="Date", y="Count", color='Case',title='Cases over time', color_discrete_sequence = [rec, dth, act])
    fig.show()


#b2222222222222222222222223333333333
"""Recovery and mortality rate over time
منسوب ارتفاع حالات الشفاء و الموت معا 
"""

def rec_and_dea():
    temp = full_table.groupby('Date').sum().reset_index()

    # adding two more columns
    temp['No. of Deaths to 100 Confirmed Cases'] = round(temp['Deaths']/temp['Confirmed'], 3)*100
    temp['No. of Recovered to 100 Confirmed Cases'] = round(temp['Recovered']/temp['Confirmed'], 3)*100
    # temp['No. of Recovered to 1 Death Case'] = round(temp['Recovered']/temp['Deaths'], 3)
    
    temp = temp.melt(id_vars='Date', value_vars=['No. of Deaths to 100 Confirmed Cases', 'No. of Recovered to 100 Confirmed Cases'], 
                 var_name='Ratio', value_name='Value')

    fig = px.line(temp, x="Date", y="Value", color='Ratio', log_y=True, 
                  title='Recovery and Mortality Rate Over The Time', color_discrete_sequence=[dth, rec])
    fig.show()


#1111111111177777777

"""No. of places to which COVID-19 spread
عدد الأماكن التي انتشر فيها COVID-19
"""
def count_con():
    c_spread = china[china['Confirmed']!=0].groupby('Date')['Province/State'].unique().apply(len)
    c_spread = pd.DataFrame(c_spread).reset_index()

    fig = px.line(c_spread, x='Date', y='Province/State', text='Province/State',
                  title='Number of Provinces/States/Regions of China to which COVID-19 spread over the time',
                  color_discrete_sequence=[cnf,dth, rec])
    fig.update_traces(textposition='top center')

    spread = full_table[full_table['Confirmed']!=0].groupby('Date')['Country/Region'].unique().apply(len)
    spread = pd.DataFrame(spread).reset_index()
    
    fig = px.line(spread, x='Date', y='Country/Region', text='Country/Region',
                  title='Number of Countries/Regions to which COVID-19 spread over the time',
                  color_discrete_sequence=[cnf,dth, rec])
    fig.update_traces(textposition='top center')
    fig.show()






#1111111111111888888888
"""مخطط زمني  لعدد الحالات مع الدول تصاعدي و تنازلي"""
def html():
    HTML('''<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/1571387"><script src="https://public.flourish.studio/resources/embed.js"></script></div>''')


#1111111111999999999
"""ذروة الأيام لأصابة"""
def core_con():
    temp = full_table.groupby('Date')['Confirmed'].sum()
    tempp = temp.diff()
    
    plt.figure(figsize=(20, 5))
    ax = calmap.yearplot(tempp, fillcolor='white', cmap='Reds', linewidth=0.5)
    print(ax)



flg = full_latest_grouped
flg.head()






def tx(name):
    name = arabic_reshaper.reshape(name)
    return get_display(name)



x = Tk()   
var = StringVar()
x.geometry('700x600')
x.title("COVID19EN")

x.configure(background='#30000d')#30000d
ll={"font":"-size 16 -weight bold","fg":"#071c00","bg":"#02cb97"}
bb={"font":"-size 9 -weight bold"}

#9bcb02/029bcb/#3302cb/#02cb97/#6a011c/#30000d
#purple,plum,gray
#,fg='red',bg='plum',font=('times',,'bold')
w = Entry(x,textvariable=var,width=15).place(x=250,y=8)
l1 = Label(text =tx( 'لمعرفة احصائية بلدك '),**ll).place(x= 450, y=5)
b27 = Button(text = tx('اسم بلدك'),**bb, command = latest_your_country,bd=5).place(x=100,y=5)
l2  = Label(text  =tx('إحصائيات عا لمية '),**ll).place(x=490,y=45)
b17= Button(text =tx( 'عدد الدول المنتشر فيها'),**bb,bd=5,fg='purple',command = count_con).place(x=520,y=88)
#b13 = Button(text =tx('الكرة الأرضية'),**bb,fg='purple',bd=5, command = graph_world).place(x=550,y=88)
b1  = Button(text =tx('إحصائية العالم' ),**bb,fg='green',command = latest_complete_data,bd=5).place(x=370,y=88)
b26 = Button(text =tx('حالات الأنتشار '),**bb,fg='blue',command =cases_spread,bd=5).place(x=220 ,y=88)
b14 = Button(text =tx( 'سرعة أنتشار المرض'),**bb,fg='red',bd=5, command = expansion_covid19).place(x=20,y=88)


#All data
l3 = Label(text=tx('إحصائيات العالم لأكثر حالات  '),**ll).place(x=370 , y=130 )
b2 = Button(text =tx('إصابة'),fg='blue',bd=5,**bb, command = all_country_by_confirmed).place(x=500,y=175)
b3 = Button(text =tx('وفاة'),fg='red', bd=5,**bb,command =all_country_by_deaths ).place(x=330,y=175)
b4 = Button(text =tx('شفاء'),fg='green',bd=5,**bb,command = all_country_by_recovered).place(x=150,y=175)

#only col rank_by 
l4 = Label(text = tx('الدول الأكثر'),**ll).place(x=550 ,y=220)
b5 = Button(text =tx('اصابة'),fg='blue',bd=5,**bb,command = CON ).place(x=500,y=265)
b6 = Button(text =tx('وفاة'),fg='red',bd=5,**bb,command = DEA).place(x=330,y=265)
b7 = Button(text =tx('شفاء'),fg='green',bd=5,**bb,command = REC).place(x=150,y=265)
l5 = Label(text = tx('حالات خاصة لبعض الدول'),**ll).place(x=420,y=310)
b8 = Button(text =tx('لم يتم شفاء أي حالة'),**bb,bd=5,fg='red',command=no_rec).place(x=500,y=355)
b10= Button(text =tx('لم يتم وفاة أي حالة '),**bb,bd=5,fg='green',command =  no_dea).place(x=500,y=400)
b11= Button(text = tx( 'تم شفاء جميع الحالات'),**bb,bd=5,fg='green',command = all_rec).place(x=50,y=355)
b9= Button(text = tx('تم وفاة جميع الحالات ') ,**bb,bd=5, fg='red',command = all_dea).place(x=50,y=400)
b12= Button(text =tx('البلدان التي أصبح خالية من المرض'),**bb,fg='purple',bd=5,command = zero_cases).place(x=240,y=375)
l6 = Label(text =tx('منسوب أرتفاع '),**ll).place(x=520, y=450 )
b15= Button(text =tx('حالات التي تم أكتشافها'), fg='green',**bb,bd=5,command = con_time).place(x=425,y=490)
b16= Button(text =tx('حالات الشفاء والموتى '),fg='red',bd=5,**bb, command = rec_and_dea).place(x=150,y=490)

#l7 = Label(text = 'Other',**ll).place(x=20, y=550 )
#b18= Button(text =tx( 'مخطط زمني '),bd=5,fg='purple',**bb,command = html).place(x=300,y=590)#
#b19= Button(text =tx( 'ذروة ايام لأصابة'),bd=5,fg='purple',**bb,command = core_con).place(x=100,y=590)
x.mainloop()
