from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

module_mapping = {
                'views.maps_visualization':'maps_visualization',
            }

def main_sidebar():
    map_app_tabs = {'Geomaps overview': 'maps_visualization'}
    with st.sidebar:
        st.markdown('---')
        st.title('You are welcome!')
        selected_menu = option_menu(None, options=['Geomaps overview'], default_index=0,
                                    orientation='vertical', menu_icon='menu-button-wide',
            styles={
        "container": {"padding": "0!important", "background-color": "#0C0431", "border-radius":"6px", "height":"300px", "font-weight":"bold", "family":"roboto"},
        "icon": {"color": "#F33309", "font-size": "25px"}, 
                                    "nav-link": {"font-size": "23px", "text-align": "left", "margin":"0px", "--hover-color": "##7FA6EB", "family":"roboto", "padding-top":"20px", "hover":"black"},
        "nav-link-selected": {"background-color": "#15E815"},
    }, icons=['globe-americas'])
    

    return 'views.' + map_app_tabs[selected_menu]