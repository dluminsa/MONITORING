import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import time
import datetime as dt

#st.title("PMTCT DASHBOARD DATA ENTRY FORM")
st.markdown("<h4><b>MONITORING ENTRIES DONE SO FAR</b></h4>", unsafe_allow_html=True)


CHOICE = st.radio('**WHICH DATABASE DO YOU WANT TO MONITOR**', options= ['ANC', 'PCR', 'DELIVERY'], horizontal=True, index = None)
if not CHOICE:
     st.stop()
elif CHOICE == 'ANC':
    #try:
     st.write('**SEARCHING ANC DATABASE**')
     conn = st.connection('gsheets', type=GSheetsConnection)
     exist = conn.read(worksheet= 'PMTCT', usecols=list(range(34)),ttl=5)
     df = exist.dropna(how='all')
     df = df.rename(columns={'ANC DATE': 'DATEY', 'FACILITY DISTRICT':'DISTRICT', 'HEALTH FACILITY':'FACILITY'})
    #except:
         #"POOR NETWORK, COUDN'T CONNECT TO DATABASE"
elif CHOICE == 'DELIVERY':
    try:
        st.write('**SEARCHING DELIVERY DATABASE**')
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'DELIVERY', usecols=list(range(34)),ttl=5)
        df = exist.dropna(how='all')
        df = df.rename(columns={'DATE OF DELIVERY': 'DATEY'})
    except:
         "POOR NETWORK, COUDN'T CONNECT TO DELIVERY DATABASE"
elif CHOICE == 'PCR':
    try:
        st.write('**SEARCHING PCR DATABASE**')
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'PCR', usecols=list(range(34)),ttl=5)
        df = exist.dropna(how='all')
        df = df.rename(columns={'DATE OF PCR': 'DATEY'})
    except:
         "POOR NETWORK, COUDN'T CONNECT TO PCR DATABASE"

#file = r"C:\Users\Desire Lumisa\Desktop\APP\PMTCT.xlsx"         

#df = pd.read_excel(file)
#df = df.rename(columns={'ANC DATE': 'DATEY', 'FACILITY DISTRICT':'DISTRICT', 'HEALTH FACILITY':'FACILITY'})

df = df[['DISTRICT', 'FACILITY', 'DATEY']].copy()
df['DATEY'] = pd.to_datetime(df['DATEY'], errors='coerce')
df['MONTH'] = df['DATEY'].dt.strftime('%B')
df['YEAR'] = df['DATEY'].dt.year


st.sidebar.subheader('Filter from here ')
district = st.sidebar.multiselect('Pick a DISTRICT', df['DISTRICT'].unique())

if not district:
    df2 = df.copy()
else:
    df2 = df[df['DISTRICT'].isin(district)]

#create for facility
facility = st.sidebar.multiselect('**Select a facility**', df2['FACILITY'].unique())
if not facility:
    df3 = df2.copy()
else:
    df3 = df2[df2['FACILITY'].isin(facility)]
 
#for year
year = st.sidebar.multiselect('**Select a year**', df3['YEAR'].unique())

if not year:
    df4 = df3.copy()
else:
    df4 = df3[df3['YEAR'].isin(year)]

#for month
month = st.sidebar.multiselect('**Select a month**', df4['MONTH'].unique())

if not month:
    df5 = df4.copy()
else:
    df5 = df4[df4['MONTH'].isin(month)]

###############################################################################################
                
# if not year and not facility:
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['MONTH'].isin(month)]

# elif not month and not facility:
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['YEAR'].isin(year)]

# elif not month and not year: 
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['FACILITY'].isin(facility)]

# elif not district and not facility:
#     fdf = df5[df5['MONTH'].isin(month) & df5['YEAR'].isin(year)]

# elif not year and not facility:
#     fdf = df5[df5['MONTH'].isin(month) & df5['YEAR'].isin(year)]

# elif not month and not district:
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['YEAR'].isin(year)]

# elif not month and not facility and not year:
#     fdf = df5[df5['DISTRICT'].isin(district)]

# elif not district and not year and not facility:
#     fdf = df5[df5['MONTH'].isin(month)]  

# elif not facility and not district and not month:
#     fdf = df5[df5['YEAR'].isin(year)]

# elif not district and not year and not month:
#     fdf5 = df5[df5['FACILITY'].isin(facility)]  

# elif not facility:
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['MONTH'].isin(month) & df5['YEAR'].isin(year)]

# elif not year:
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['MONTH'].isin(month) & df5['FACILITY'].isin(facility)]

# elif not month:
#     fdf = df5[df5['DISTRICT'].isin(district) & df5['FACILITY'].isin(facility) & df5['YEAR'].isin(year)]

# elif not district:
#     fdf = df5[df5['FACILITY'].isin(facility) & df5['MONTH'].isin(month) & df5['YEAR'].isin(year)]

# else:
#     fdf = df5


##################################################################################################
# Base DataFrame to filter
fdf = df5.copy()

# Apply filters based on selected criteria
if district:
    fdf = fdf[fdf['DISTRICT'].isin(district)]

if facility:
    fdf = fdf[fdf['FACILITY'].isin(facility)]

if year:
    fdf = fdf[fdf['YEAR'].isin(year)]

if month:
    fdf = fdf[fdf['MONTH'].isin(month)]

##################################################################################
dis = fdf['DISTRICT'].unique()
mon = fdf['MONTH'].unique()
yea = fdf['YEAR'].unique()
fac = fdf['FACILITY'].unique()

fdf['DISTRICT'] = fdf['DISTRICT'].astype(str)
disa = ', '.join(fdf['DISTRICT'].unique())

fdf['MONTH'] = fdf['MONTH'].astype(str)
mona = ', '.join(fdf['MONTH'].unique())

fdf['YEAR'] = fdf['YEAR'].astype(str)
yeaa = ', '.join(fdf['YEAR'].unique())

faca = ', '.join(fdf['FACILITY'].unique())

total = fdf.shape[0]

cola,colb,colc = st.columns(3)

colb.write('**SUMMARIES**')

if len(dis)==1:
    st.markdown(f'**DISTRICT : {disa}**')

if len(fac)==1:
    st.markdown(f'**FACILITY: {faca}**')

if len(yea)==1:  
    st.markdown(f'**YEAR : {yeaa}**')
if len(mon)==1:
    st.markdown(f'**MONTH : {mona}**')
st.markdown(f'**TOTAL ENTERED : {total}**')
