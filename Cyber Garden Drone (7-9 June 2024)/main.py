import os
import pandas as pd
import subprocess
import folium
from Unpacker import new_files


subprocess.run(['python', 'Unpacker.py'], capture_output=True, text=True)
files = new_files('.csv', 'Csv', '.html', 'Maps')

for i in range(len(files)):
    
    file = files[i]
    name = file.split('\\')[-1].split('.')[0]

    df = pd.read_csv(file)
    count_rows = len(df['radio_status.rssi'].dropna())
    df.fillna(0)
    anomaly_gps_lon = [ i for i in df['sensor_gps.lon']]
    anomaly_gps_lat = [ i for i in df['sensor_gps.lat']]

    # Конвертация координат
    df = pd.read_csv(file)
    df_copy = df.copy()
    df = df[['vehicle_gps_position.lat', 'vehicle_gps_position.lon']].dropna()
    df['vehicle_gps_position.lat'] = df['vehicle_gps_position.lat'] / 10000000
    df['vehicle_gps_position.lon'] = df['vehicle_gps_position.lon'] / 10000000

    # Создание карты
    map_center = [df['vehicle_gps_position.lat'].iloc[0], df['vehicle_gps_position.lon'].iloc[0]]
    mymap = folium.Map(location=map_center, zoom_start=15, attributionControl = 0)
    # # Добавление точек на карту
    for idx, row in df.iterrows():

        if idx < count_rows and df_copy['radio_status.rxerrors'][idx] != 0:
            
            
            folium.Marker(
                location=[df_copy['sensor_gps.lat'][idx] / 10000000, df_copy['sensor_gps.lon'][idx] / 10000000],
                popup=folium.Popup(f"""<h3>Код ошибки приёма:</h3> <h4>{df_copy['radio_status.rxerrors'][idx]}</h4><br>
                <h3>Сила сигнала:</h3> <h4>{df_copy['radio_status.rssi'][idx]}</h4><br>
                <h3>Уровень удалённых шумов:</h3> <h4>{df_copy['radio_status.remote_noise'][idx]}</h4><br>
                <h3>Координаты:</h3> <h4>{df_copy['sensor_gps.lat'][idx]}, {df_copy['sensor_gps.lon'][idx]}</h4>
                """,max_width=200),
                icon=folium.Icon(color='red')
            ).add_to(mymap)


        if row['vehicle_gps_position.lat'] in anomaly_gps_lat and row['vehicle_gps_position.lon'] in anomaly_gps_lon:
            pass
        else:
            folium.Marker(
                location=[row['vehicle_gps_position.lat'], row['vehicle_gps_position.lon']],
                popup=folium.Popup(f"""<h3>status: </h3><h4>OK</h4><br>
                <h3>Координаты:</h3> <h4>{df_copy['vehicle_gps_position.lat'][idx]}, {df_copy['vehicle_gps_position.lon'][idx]}</h4>""", min_width = 200),
            ).add_to(mymap)
    # Сохранение карты в HTML файл
    mymap.save(f"Maps\\{name}.html")
    print(f'{name} created map ')
else:
    print('New files for maps not found')