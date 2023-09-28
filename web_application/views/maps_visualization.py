import streamlit as st
from .devices import Device
from .session import Session
import pandas as pd
import asyncio
from charts import last_location_map

async def mount_coordinate_for_deveui_last_uplink(device:Device, deveui):
    device_message = await device.get_uplink_message(deveui, '20230916000000', '20230918235959', 1)
    base64_payload, hex_payload = Device.get_payload_from_uplinks(device_message)
    binary_lats, binary_longs = Device.extract_coord_bits_from_payload(hex_payload, 16)
    float_latitudes, float_longitudes = Device.extract_coordinates(binary_lats), Device.extract_coordinates(binary_longs)
    return *float_latitudes, *float_longitudes
    
def maps_visualization(results):
    session = Session()
    session.get_token()
    device = Device()
    deveui_dataframe = pd.DataFrame(results['deveui_data']).dropna(subset=['dev_eui'])
    update_info = st.button("Refresh data")
    if update_info:
        with st.spinner("Loading data..."):
            deveui_dataframe[['Latitude', 'Longitude']] = deveui_dataframe['dev_eui'].apply(lambda x: pd.Series(asyncio.run(mount_coordinate_for_deveui_last_uplink(device, x))))
            deveui_dataframe['Latitude'].fillna(-23, inplace=True, axis=0)
            deveui_dataframe['Longitude'].fillna(-46, inplace=True, axis=0)
            st.session_state['location_map'] = last_location_map.last_location_chart(deveui_dataframe, 'Latitude', 'Longitude')

    # st.write(deveui_dataframe['Latitude'][0].astype(float))
    results['deveui_data'] = deveui_dataframe
    st.write(deveui_dataframe)
    st.plotly_chart(st.session_state['location_map'], use_container_width=True)