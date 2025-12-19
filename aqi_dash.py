import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Air Quality Intelligence Platform", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main{background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 50%,#0f172a 100%)}
.stMetric{background:linear-gradient(135deg,rgba(30,41,59,.8),rgba(15,23,42,.8));padding:20px;border-radius:15px;border:1px solid rgba(100,116,139,.3)}
h1{background:linear-gradient(90deg,#60a5fa 0%,#a78bfa 50%,#f472b6 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:3rem!important;font-weight:700}
.city-search{background:rgba(30,41,59,.8);padding:15px;border-radius:10px;border:1px solid rgba(100,116,139,.3)}
</style>
""", unsafe_allow_html=True)

GLOBAL_CITIES={
'Delhi':{'country':'India','flag':'🇮🇳','base_aqi':312,'lat':28.6139,'lon':77.209},
'Mumbai':{'country':'India','flag':'🇮🇳','base_aqi':158,'lat':19.076,'lon':72.8777},
'Bangalore':{'country':'India','flag':'🇮🇳','base_aqi':89,'lat':12.9716,'lon':77.5946},
'Kolkata':{'country':'India','flag':'🇮🇳','base_aqi':184,'lat':22.5726,'lon':88.3639},
'Chennai':{'country':'India','flag':'🇮🇳','base_aqi':97,'lat':13.0827,'lon':80.2707},
'Hyderabad':{'country':'India','flag':'🇮🇳','base_aqi':126,'lat':17.385,'lon':78.4867},
'Beijing':{'country':'China','flag':'🇨🇳','base_aqi':156,'lat':39.9042,'lon':116.4074},
'Shanghai':{'country':'China','flag':'🇨🇳','base_aqi':132,'lat':31.2304,'lon':121.4737},
'Tokyo':{'country':'Japan','flag':'🇯🇵','base_aqi':45,'lat':35.6762,'lon':139.6503},
'Seoul':{'country':'South Korea','flag':'🇰🇷','base_aqi':78,'lat':37.5665,'lon':126.978},
'Bangkok':{'country':'Thailand','flag':'🇹🇭','base_aqi':142,'lat':13.7563,'lon':100.5018},
'Singapore':{'country':'Singapore','flag':'🇸🇬','base_aqi':52,'lat':1.3521,'lon':103.8198},
'Dubai':{'country':'UAE','flag':'🇦🇪','base_aqi':95,'lat':25.2048,'lon':55.2708},
'London':{'country':'United Kingdom','flag':'🇬🇧','base_aqi':58,'lat':51.5074,'lon':-0.1278},
'Paris':{'country':'France','flag':'🇫🇷','base_aqi':62,'lat':48.8566,'lon':2.3522},
'Berlin':{'country':'Germany','flag':'🇩🇪','base_aqi':48,'lat':52.52,'lon':13.405},
'Rome':{'country':'Italy','flag':'🇮🇹','base_aqi':71,'lat':41.9028,'lon':12.4964},
'Madrid':{'country':'Spain','flag':'🇪🇸','base_aqi':65,'lat':40.4168,'lon':-3.7038},
'Amsterdam':{'country':'Netherlands','flag':'🇳🇱','base_aqi':42,'lat':52.3676,'lon':4.9041},
'Moscow':{'country':'Russia','flag':'🇷🇺','base_aqi':89,'lat':55.7558,'lon':37.6173},
'New York':{'country':'United States','flag':'🇺🇸','base_aqi':54,'lat':40.7128,'lon':-74.006},
'Los Angeles':{'country':'United States','flag':'🇺🇸','base_aqi':87,'lat':34.0522,'lon':-118.2437},
'Chicago':{'country':'United States','flag':'🇺🇸','base_aqi':51,'lat':41.8781,'lon':-87.6298},
'Toronto':{'country':'Canada','flag':'🇨🇦','base_aqi':38,'lat':43.6532,'lon':-79.3832},
'Mexico City':{'country':'Mexico','flag':'🇲🇽','base_aqi':118,'lat':19.4326,'lon':-99.1332},
'São Paulo':{'country':'Brazil','flag':'🇧🇷','base_aqi':76,'lat':-23.5505,'lon':-46.6333},
'Buenos Aires':{'country':'Argentina','flag':'🇦🇷','base_aqi':63,'lat':-34.6037,'lon':-58.3816},
'Cairo':{'country':'Egypt','flag':'🇪🇬','base_aqi':168,'lat':30.0444,'lon':31.2357},
'Lagos':{'country':'Nigeria','flag':'🇳🇬','base_aqi':145,'lat':6.5244,'lon':3.3792},
'Sydney':{'country':'Australia','flag':'🇦🇺','base_aqi':35,'lat':-33.8688,'lon':151.2093},
'Melbourne':{'country':'Australia','flag':'🇦🇺','base_aqi':32,'lat':-37.8136,'lon':144.9631}
}

def get_aqi_status(aqi):
    if aqi<=50:return"Good","#10b981","Air quality is satisfactory"
    if aqi<=100:return"Moderate","#fbbf24","Acceptable for most people"
    if aqi<=200:return"Unhealthy","#f97316","Sensitive groups affected"
    if aqi<=300:return"Very Unhealthy","#ef4444","Health alert for everyone"
    return"Hazardous","#991b1b","Emergency conditions"

def generate_24h_data(city):
    base=GLOBAL_CITIES[city]["base_aqi"]
    rows=[]
    for h in range(24):
        m=1.0
        if 7<=h<=10:m=1.3
        elif 18<=h<=21:m=1.15
        elif h>=23 or h<=5:m=0.7
        elif 13<=h<=16:m=0.85
        v=random.uniform(.92,1.08)
        a=int(base*m*v)
        rows.append([f"{h:02d}:00",a,int(a*.65*random.uniform(.95,1.05)),int(a*.85*random.uniform(.95,1.05)),int(a*.28*random.uniform(.95,1.05)),int(a*.15*random.uniform(.95,1.05)),int(a*.12*random.uniform(.95,1.05)),int(a*.22*random.uniform(.95,1.05))])
    return pd.DataFrame(rows,columns=["Hour","AQI","PM2.5","PM10","NO2","SO2","CO","O3"])

def generate_monthly_data(cities):
    dates=[(datetime.now()-timedelta(days=29-i)).strftime('%d/%m') for i in range(30)]
    data={"Date":dates}
    for c in cities:
        base=GLOBAL_CITIES[c]["base_aqi"]
        data[c]=[int(base*random.uniform(.85,1.15)) for _ in range(30)]
    return pd.DataFrame(data)

st.markdown("# 🌍 Air Quality Intelligence Platform")
st.markdown("### Real-time AQI Monitoring & Predictive Analytics for Global Cities")

selected=st.sidebar.selectbox("Select City",list(GLOBAL_CITIES.keys()))

df24=generate_24h_data(selected)
hour=datetime.now().hour
aqi=int(df24.iloc[hour]["AQI"])
status,color,desc=get_aqi_status(aqi)

k1,k2,k3,k4=st.columns(4)
k1.metric("Current AQI",aqi,status)
k2.metric("24-Hour Average",int(df24["AQI"].mean()))
k3.metric("Peak AQI Hour",df24.loc[df24["AQI"].idxmax()]["Hour"])
k4.metric("City",selected)

fig=go.Figure(go.Scatter(x=df24["Hour"],y=df24["AQI"],mode="lines",fill="tozeroy"))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig,use_container_width=True)

st.markdown("---")
st.markdown(f"<p style='text-align:center;color:#64748b'>© 2024 Air Quality Intelligence Platform | Last Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",unsafe_allow_html=True)
