#%%
## Imports
import streamlit as st
import pandas as pd

import plotly.express as px
import math
import altair as alt


#%%
#cool colour gradients
#https://coolors.co/e9d985-b2bd7e-749c75-6a5d7b-5d4a66
color_list = ['#E9D985','#B2BD7E','#749C75','#6A5D7B','#C62E65']

#%%
planes = pd.read_csv(r"qantas_streamlit\data\qantas_cluster_analysis.csv")

#%%
col_to_view = ['TAIL_ID', 'AVERAGE DELAY', 'AVERAGE TURNAROUND', 'DISTANCE', 'FLIGHTS',
       'FLIGHTS DELAYED', 'PER FLIGHT', 'TOP AIRPORT', 'CLUSTERS', 'Aircraft Type', 
       'Aircraft Name', 'Age_clean']

planes_filtered = planes[col_to_view]

#tidy columns
planes_filtered.columns = planes_filtered.columns.str.upper().str.replace(' ','_')
planes_filtered = planes_filtered.rename(columns={'AGE_CLEAN':'AGE_YEARS',
                                                  'AVERAGE_DELAY': 'AVG_DELAY_MINS',
                                                  'AVERAGE_TURNAROUND': 'AVG_TURNAROUNG_MINS',
                                                  'DISTANCE':'DISTANCE_KM',
                                                  'FLIGHTS_DELAYED':'FLIGHTS_DELAYED_COUNT',
                                                  'PER_FLIGHT':'DISTANCE_PER_FLIGHT_KM'})
#%%
#Add radio buttons
# plane_models = planes_filtered['AIRCRAFT_TYPE'].unique().tolist()
# plane_models.sort()
# choice = st.multiselect("Select one or more plane models", plane_models)

# st.dataframe(planes_filtered[planes_filtered['AIRCRAFT_TYPE'].isin(choice)])
# %%
plane_models = planes_filtered['AIRCRAFT_TYPE'].unique().tolist()
plane_models.sort()

#%%
add_sidebar = st.sidebar.selectbox('Select analysis type',
                                   ('Fleet overview', 'Individual aircraft','Individual scatter plot'))

#%%
if add_sidebar == 'Fleet overview':
    # Title block
    st.title("Qantas Fleet Overview ✈️")
    choices = st.multiselect("Select aircraft", plane_models, 
                         default=['Airbus A330-200', 'Airbus A330-300', 'Airbus A380-800', 
                                  'Boeing 737-800', 'Boeing 787-9 Dreamliner'])
    presented_df = planes_filtered[planes_filtered['AIRCRAFT_TYPE'].isin(choices)]

    st.write(f"{len(presented_df)} of {len(planes)} aircraft in Qantas fleet are shown")
    st.dataframe(planes_filtered[planes_filtered['AIRCRAFT_TYPE'].isin(choices)])

    fig = px.histogram(data_frame=presented_df, x=['DISTANCE_KM'], color_discrete_sequence =['green'],
                   title='Distance per year')
    fig.update_traces(marker_line_width=3, marker_line_color='black')
    st.plotly_chart(fig, use_container_width=True)
#%%
if add_sidebar == 'Individual aircraft':
    # Title block
    st.title("Qantas Individual Aircraft Investigation 🔍")
    st.write('test 123')

    # Display the dataframe as an interactive table
    st.dataframe(planes_filtered)

    # Create a drop down to select an aircraft
    selected_aircraft = st.selectbox("Select an aircraft", planes_filtered["TAIL_ID"])

    # Get the distance value for the selected aircraft
    selected_distance = planes_filtered[planes_filtered["TAIL_ID"] == selected_aircraft]["DISTANCE_KM"].iloc[0]


    # Create a histogram with Plotly Express
    bin_width= 500000
    # here you can choose your rounding method, I've chosen math.ceil
    nbins = math.ceil((planes_filtered["DISTANCE_KM"].max() - planes_filtered["DISTANCE_KM"].min()) / bin_width)
    fig = px.histogram(planes_filtered, x="DISTANCE_KM", color_discrete_sequence =['green'], nbins=10, title="Histogram of distance")
    fig.update_traces(marker_line_width=3, marker_line_color='black')
    # Add a vertical line for the selected distance
    fig.add_vline(x=selected_distance, line_color="red", line_width=3)

    # Display the histogram as a Plotly chart
    st.plotly_chart(fig)

# %%
#%%
if add_sidebar == 'Individual scatter plot':
    # Title block
    st.title("Qantas Individual Scatter Plot 📈")
    st.write('test 123')

    pca_df = pd.read_csv(r"qantas_streamlit\data\qantas_pca_results.csv", index_col=0)

    #combine with planes_filtered
    pca_df = pca_df.merge(planes_filtered)

    #make nice scatter chart
    alt_scatter = alt.Chart(pca_df).mark_point().encode(
        x='PC1', y='PC2', 
        color=alt.Color('CLUSTERS', scale=alt.Scale(range=color_list)))

    st.altair_chart(alt_scatter, use_container_width=True)
# %%
