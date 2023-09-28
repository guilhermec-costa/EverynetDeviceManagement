import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def get_mapbox_token() -> str:
    return st.secrets.mapbox.mapbox_token

def check_bubble_size(type_of_group: str) -> dict.values:
    dinamic_sizes = {'Pontos instalados': 35, 'IEF': 25}
    return dinamic_sizes.get(type_of_group)

@st.cache_data
def add_traces_on_map(fig, another_data, name=None, fillcolor: str = 'rgba(255, 205, 0, 0)') -> None:
    fig.add_trace(go.Scattermapbox(lat=another_data['Latitude'], lon=another_data['Longitude'],
                                   mode='lines', line=dict(color=fillcolor), fill='toself', name=name))

@st.cache_data
def last_location_chart(data, lat, long):
    # fig = px.scatter_mapbox(data, lat=lat, lon=long, height=750, center=dict(lat=-23.5607, lon=-46.8171), zoom=11, opacity=0.95, size_max=45)
    
    fig = go.Figure(go.Scattermapbox(lat=data[lat], lon=data[long], hovertext=data['dev_eui'],
                                   mode='markers', marker=go.scattermapbox.Marker(size=16, color='blue', opacity=1)))
    
    fig.update_layout(mapbox=dict(accesstoken=st.secrets.mapbox.mapbox_token, style='satellite-streets'), showlegend=False, height=750)
    return fig