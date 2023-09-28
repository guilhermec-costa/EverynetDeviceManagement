import streamlit as st
import builder
import session_states
import plotly.graph_objects as go

st.set_page_config('Everynet - Maps', layout='wide')

if __name__ == '__main__':
    session_states.initialize_session_states([('ALL_RESULTS', {}), ('location_map', go.Figure())])
    app = builder.App("everynet_project")
    required_data = app.build_app()
    #app.apply_styles()
    app.start_app(app_session_state=required_data)