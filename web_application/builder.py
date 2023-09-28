import streamlit as st
from views import main_sidebar
import importlib
import pandas as pd

class App:


    def __init__(self, name) -> None:
        self.app_name = name

    def apply_styles(self, style_file:str) -> None:
        with open(style_file) as style:
            st.markdown(f'<style>{style.read()}</style>', unsafe_allow_html=True)

    def start_app(self, app_session_state) -> None:
            
            choosed_module = importlib.import_module(self.choosed_app)
            module_name = choosed_module.__name__
            function_name = main_sidebar.module_mapping[module_name]
            choosed_function = getattr(choosed_module, function_name)
            choosed_function(results=app_session_state)
    
    def build_app(self):
        self.choosed_app = main_sidebar.main_sidebar()
        st.session_state.ALL_RESULTS['deveui_data'] = pd.read_excel('/home/china/everynet_project/tagvis_all.xlsx')
        return st.session_state.ALL_RESULTS