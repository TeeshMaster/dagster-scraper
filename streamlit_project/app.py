from typing import List
import streamlit as st
import pandas as pd
import pydeck as pdk

conn = st.connection("snowflake")

@st.cache_data
def load_data() -> pd.DataFrame:
    df = conn.query("SELECT * from CORE.ANALYTICS.DATA_ENGINEER_JOBS", ttl=600)
    return df

@st.cache_data
def calculate_kpis(data: pd.DataFrame) -> List[float]:
    total_listings = data['JOB_URL'].nunique()
    total_companies = data['COMPANY_NAME'].nunique()
    return [total_listings, total_companies]

def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(4), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value)

def main():

    data = load_data()

    st.title("Data Engineering Jobs in Melbourne")

    filtered_data = data.copy()
    kpis = calculate_kpis(filtered_data)
    kpi_names = ["Total Listings", "Total Companies"]
    display_kpi_metrics(kpis, kpi_names)

    layer = pdk.Layer(
                    'ScatterplotLayer',
                    data,
                    get_position='[LONGITUDE, LATITUDE]',
                    opacity=0.8,
                    stroked=True,
                    filled=True,
                    pickable=True,
                    radius_scale=6,
                    radius_min_pixels=10,
                    radius_max_pixels=100,
                    line_width_min_pixels=1,
                    get_fill_color=[255, 140, 0],
                    get_line_color=[0, 0, 0],
                )
    view_state = pdk.ViewState(
        longitude=data['LONGITUDE'].mean(),
        latitude=data['LATITUDE'].mean(),
        zoom=4
    )

    tooltip = {
                "html": "<b>Job Title: </b>{JOB_TITLE}</br> <b>Company: </b>{COMPANY_NAME}</br> <b>Listed: </b>{PUBLISHED_DATE}",
                "style": {
                    "font-size": "75%"
                }
            }

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))
    st.write(data)

if __name__ == '__main__':
    main()