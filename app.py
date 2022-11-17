import streamlit as st
import pandas as pd
import numpy as np
from urllib import request
from bs4 import BeautifulSoup as bs
from plotly import graph_objects as go

st.set_page_config(page_title='Weather', page_icon='❄')
st.title('5-Day Weather Forecast ⛅')

@st.cache
def get_data():
    url = 'http://www.tsag-agaar.gov.mn/export'
    response = request.urlretrieve(url, 'tsag_agaar.xls')
    return response

def convert_to_xlsx():
        with open('tsag_agaar.xls', encoding='utf-8') as xml_file:
            soup = bs(xml_file.read(), 'xml')
            writer = pd.ExcelWriter('tsag_agaar.xlsx')
            for sheet in soup.findAll('Worksheet'):
                sheet_as_list = []
                for row in sheet.findAll('Row'):
                    sheet_as_list.append([cell.Data.text if cell.Data else '' for cell in row.findAll('Cell')])
                pd.DataFrame(sheet_as_list).to_excel(writer, sheet_name=sheet.attrs['ss:Name'], index=False,
                                                     header=False)

            writer.save()
            
convert_to_xlsx()

df = pd.read_excel('tsag_agaar.xlsx', skiprows=1)
df['Огноо'] = pd.to_datetime(df['Огноо']).dt.date

city = st.selectbox('Select City ', df['Хотын нэр'].unique())
selected = df.loc[df['Хотын нэр'] == city].drop('Хотын нэр', axis=1).reset_index(drop=True)
selected['Өдрийн салхи'] = selected['Өдрийн салхи'].str.replace('м/с', '').astype(np.int64)
selected['Шөнийн салхи'] = selected['Шөнийн салхи'].str.replace('м/с', '').astype(np.int64)
selected = selected.rename(columns={'Өдрийн салхи' : 'Өдрийн салхи (м/с)', 
                                    'Шөнийн салхи' : 'Шөнийн салхи (м/с)'})
selected['delta_wind_day'] = selected['Өдрийн салхи (м/с)'].diff()
selected['delta_wind_night'] = selected['Шөнийн салхи (м/с)'].diff()
selected['delta_temp_day'] = selected['Өдрийн температур'].diff()
selected['delta_temp_night'] = selected['Шөнийн температур'].diff()
col1, col2, col3, col4, col5= st.columns(5)
cloudy = ('https://cdn-icons-png.flaticon.com/512/414/414927.png')
partly_cloudy = ('https://cdn-icons-png.flaticon.com/512/3208/3208676.png')
snowy = ('https://cdn-icons-png.flaticon.com/512/2315/2315309.png')
partly_snowy = ('https://cdn-icons-png.flaticon.com/512/1163/1163629.png')
less_cloudy = ('https://cdn-icons-png.flaticon.com/512/1163/1163661.png')
partly_precipitation = ('https://cdn-icons-png.flaticon.com/512/1163/1163657.png')
col1.text(selected['Огноо'].iloc[0])
col1.write(selected['Өдрийн үзэгдэл'].iloc[0])
if 'Үүлшинэ' in selected['Өдрийн үзэгдэл'].iloc[0]:
    col1.image(cloudy)
elif 'Цас' in selected['Өдрийн үзэгдэл'].iloc[0]:
    col1.image(snowy)
elif 'Багавтар үүлтэй' in selected['Өдрийн үзэгдэл'].iloc[0]:
    col1.image(partly_cloudy)
elif 'Үүл багаснa' in selected['Өдрийн үзэгдэл'].iloc[0]:
    col1.image(less_cloudy)
elif 'Ялимгүй цас' in selected['Өдрийн үзэгдэл'].iloc[0]:
    col1.image(partly_snowy)
elif 'Ялимгүй хур тунадас' in selected['Өдрийн үзэгдэл'].iloc[0]:
    col1.image(partly_precipitation)
col1.metric(label='Өдрийн температур', value='{} °C'.format(selected['Өдрийн температур'].iloc[0]), delta='{} °C'.format(selected['delta_temp_day'].iloc[0]))
col1.metric(label='Шөнийн температур', value='{} °C'.format(selected['Шөнийн температур'].iloc[0]), delta='{} °C'.format(selected['delta_temp_night'].iloc[0]))
col1.metric(label='Өдрийн салхи (м/с)', value='{} м/с'.format(selected['Өдрийн салхи (м/с)'].iloc[0]), delta='{} м/с'.format(selected['delta_wind_day'].iloc[0]))
col1.metric(label='Шөнийн салхи (м/с)', value='{} м/с'.format(selected['Шөнийн салхи (м/с)'].iloc[0]), delta='{} м/с'.format(selected['delta_wind_night'].iloc[0]))
col2.text(selected['Огноо'].iloc[1])
col2.write(selected['Өдрийн үзэгдэл'].iloc[1])
if 'Үүлшинэ' in selected['Өдрийн үзэгдэл'].iloc[1]:
    col2.image(cloudy)
elif 'Цас' in selected['Өдрийн үзэгдэл'].iloc[1]:
    col2.image(snowy)
elif 'Багавтар үүлтэй' in selected['Өдрийн үзэгдэл'].iloc[1]:
    col2.image(partly_cloudy)
elif 'Үүл багаснa' in selected['Өдрийн үзэгдэл'].iloc[1]:
    col2.image(less_cloudy)
elif 'Ялимгүй цас' in selected['Өдрийн үзэгдэл'].iloc[1]:
    col2.image(partly_snowy)
elif 'Ялимгүй хур тунадас' in selected['Өдрийн үзэгдэл'].iloc[1]:
    col2.image(partly_precipitation)
col2.metric(label='Өдрийн температур', value='{} °C'.format(selected['Өдрийн температур'].iloc[1]), delta='{} °C'.format(selected['delta_temp_day'].iloc[1]))
col2.metric(label='Шөнийн температур', value='{} °C'.format(selected['Шөнийн температур'].iloc[1]), delta='{} °C'.format(selected['delta_temp_night'].iloc[1]))
col2.metric(label='Өдрийн салхи (м/с)', value='{} м/с'.format(selected['Өдрийн салхи (м/с)'].iloc[1]), delta='{} м/с'.format(selected['delta_wind_day'].iloc[1]))
col2.metric(label='Шөнийн салхи (м/с)', value='{} м/с'.format(selected['Шөнийн салхи (м/с)'].iloc[1]), delta='{} м/с'.format(selected['delta_wind_night'].iloc[1]))
col3.text(selected['Огноо'].iloc[2])
col3.write(selected['Өдрийн үзэгдэл'].iloc[2])
if 'Үүлшинэ' in selected['Өдрийн үзэгдэл'].iloc[2]:
    col3.image(cloudy)
elif 'Цас' in selected['Өдрийн үзэгдэл'].iloc[2]:
    col3.image(snowy)
elif 'Багавтар үүлтэй' in selected['Өдрийн үзэгдэл'].iloc[2]:
    col3.image(partly_cloudy)
elif 'Үүл багаснa' in selected['Өдрийн үзэгдэл'].iloc[2]:
    col3.image(less_cloudy)
elif 'Ялимгүй цас' in selected['Өдрийн үзэгдэл'].iloc[2]:
    col3.image(partly_snowy)
elif 'Ялимгүй хур тунадас' in selected['Өдрийн үзэгдэл'].iloc[2]:
    col3.image(partly_precipitation)
col3.metric(label='Өдрийн температур', value='{} °C'.format(selected['Өдрийн температур'].iloc[2]), delta='{} °C'.format(selected['delta_temp_day'].iloc[2]))
col3.metric(label='Шөнийн температур', value='{} °C'.format(selected['Шөнийн температур'].iloc[2]), delta='{} °C'.format(selected['delta_temp_night'].iloc[2]))
col3.metric(label='Өдрийн салхи (м/с)', value='{} м/с'.format(selected['Өдрийн салхи (м/с)'].iloc[2]), delta='{} м/с'.format(selected['delta_wind_day'].iloc[2]))
col3.metric(label='Шөнийн салхи (м/с)', value='{} м/с'.format(selected['Шөнийн салхи (м/с)'].iloc[2]), delta='{} м/с'.format(selected['delta_wind_night'].iloc[2]))
col4.text(selected['Огноо'].iloc[3])
col4.write(selected['Өдрийн үзэгдэл'].iloc[3])
if 'Үүлшинэ' in selected['Өдрийн үзэгдэл'].iloc[3]:
    col4.image(cloudy)
elif 'Цас' in selected['Өдрийн үзэгдэл'].iloc[3]:
    col4.image(snowy)
elif 'Багавтар үүлтэй' in selected['Өдрийн үзэгдэл'].iloc[3]:
    col4.image(partly_cloudy)
elif 'Үүл багаснa' in selected['Өдрийн үзэгдэл'].iloc[3]:
    col4.image(less_cloudy)
elif 'Ялимгүй цас' in selected['Өдрийн үзэгдэл'].iloc[3]:
    col4.image(partly_snowy)
elif 'Ялимгүй хур тунадас' in selected['Өдрийн үзэгдэл'].iloc[3]:
    col4.image(partly_precipitation)
col4.metric(label='Өдрийн температур', value='{} °C'.format(selected['Өдрийн температур'].iloc[3]), delta='{} °C'.format(selected['delta_temp_day'].iloc[3]))
col4.metric(label='Шөнийн температур', value='{} °C'.format(selected['Шөнийн температур'].iloc[3]), delta='{} °C'.format(selected['delta_temp_night'].iloc[3]))
col4.metric(label='Өдрийн салхи (м/с)', value='{} м/с'.format(selected['Өдрийн салхи (м/с)'].iloc[3]), delta='{} м/с'.format(selected['delta_wind_day'].iloc[3]))
col4.metric(label='Шөнийн салхи (м/с)', value='{} м/с'.format(selected['Шөнийн салхи (м/с)'].iloc[3]), delta='{} м/с'.format(selected['delta_wind_night'].iloc[3]))
col5.text(selected['Огноо'].iloc[4])
col5.write(selected['Өдрийн үзэгдэл'].iloc[4])
if 'Үүлшинэ' in selected['Өдрийн үзэгдэл'].iloc[4]:
    col5.image(cloudy)
elif 'Цас' in selected['Өдрийн үзэгдэл'].iloc[4]:
    col5.image(snowy)
elif 'Багавтар үүлтэй' in selected['Өдрийн үзэгдэл'].iloc[4]:
    col5.image(partly_cloudy)
elif 'Үүл багаснa' in selected['Өдрийн үзэгдэл'].iloc[4]:
    col5.image(less_cloudy)
elif 'Ялимгүй цас' in selected['Өдрийн үзэгдэл'].iloc[4]:
    col5.image(partly_snowy)
elif 'Ялимгүй хур тунадас' in selected['Өдрийн үзэгдэл'].iloc[4]:
    col5.image(partly_precipitation)
col5.metric(label='Өдрийн температур', value='{} °C'.format(selected['Өдрийн температур'].iloc[4]), delta='{} °C'.format(selected['delta_temp_day'].iloc[4]))
col5.metric(label='Шөнийн температур', value='{} °C'.format(selected['Шөнийн температур'].iloc[4]), delta='{} °C'.format(selected['delta_temp_night'].iloc[4]))
col5.metric(label='Өдрийн салхи (м/с)', value='{} м/с'.format(selected['Өдрийн салхи (м/с)'].iloc[4]), delta='{} м/с'.format(selected['delta_wind_day'].iloc[4]))
col5.metric(label='Шөнийн салхи (м/с)', value='{} м/с'.format(selected['Шөнийн салхи (м/с)'].iloc[4]), delta='{} м/с'.format(selected['delta_wind_night'].iloc[4]))

st.dataframe(selected[['Огноо', 'Өдрийн температур', 'Өдрийн салхи (м/с)', 'Өдрийн үзэгдэл', 
                       'Шөнийн температур', 'Шөнийн салхи (м/с)', 'Шөнийн үзэгдэл']])
def bargraph():
    fig=go.Figure(data=
        [
        go.Bar(name='Өдрийн температур', x=selected['Огноо'], y=selected['Өдрийн температур'], marker_color='crimson'),
        go.Bar(name='Шөнийн температур', x=selected['Огноо'], y=selected['Шөнийн температур'], marker_color='navy')
        ])
    fig.update_layout(xaxis_title='Dates', yaxis_title='Temperature', barmode='group', margin=dict(l=70, r=10, t=80, b=80), font=dict(color='black'))
    st.plotly_chart(fig)
bargraph()
