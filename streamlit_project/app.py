from typing import List
import streamlit as st
import pandas as pd
import pydeck as pdk
import math

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

    st.map(
        data,
        latitude='LATITUDE',
        longitude='LONGITUDE'
    )

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        layers=[
            pdk.Layer(
            'ScatterplotLayer',
            data,
            get_position='[LATITUDE, LONGITUDE]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position='[LATITUDE, LONGITUDE]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

    st.write(data)

if __name__ == '__main__':
    main()