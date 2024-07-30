import streamlit as st
import mysql.connector as sconn
from mysql.connector import Error
import pandas as pd
import time
import numpy as np

st.set_page_config(page_title="Redbus", page_icon=":oncoming_bus:", layout="wide")

def timedelta_to_hhmm(value):
    #this function will convert the timedelta format into HH:MM
    t_seconds = value.seconds
    hours = t_seconds//3600  # 1hour = 3600 seconds
    minutes = (t_seconds%3600)//60 #1hour = 60minutes and 3600seconds
    return f"{hours:02}:{minutes:02}" #formatiing to display the time in 00:00 format

def configuration():
    try:
        config = {
            "user": "root",
            "password": "6381581291",
            "host": "localhost",
            "database": "REDBUS"
        }
        return config
    except Error as e:
        st.error(f"Error occurred during configuration: {e}")
        return None

def connection():
    try:
        config = configuration()
        if config is None:
            return None
        conn = sconn.connect(**config)
        if conn.is_connected():
            return conn
        else:
            st.error("Failed to connect to the database.")
            return None
    except Error as e:
        st.error(f"Error occurred when opening connection: {e}")
        return None

def fetch_distinct_value(conn, query):
    c = conn.cursor()
    try:
        c.execute(query)
        return [item[0] for item in c.fetchall()]
    except Error as e:
        st.error(f"Error occurred when fetching distinct values: {e}")
        return []

def fetch_filtered_value(conn, query):
    c = conn.cursor()
    try:
        c.execute(query)
        columns = [col[0] for col in c.description]
        data = c.fetchall()
        df = pd.DataFrame(data, columns=columns)
        if "Departure_Time" in df.columns:
            df["Departure_Time"] = df["Departure_Time"].apply(timedelta_to_hhmm)
        if "Reaching_Time" in df.columns:
            df["Reaching_Time"] = df["Reaching_Time"].apply(timedelta_to_hhmm)
        if "star_rating" in df.columns:
            df['star_rating'] = df['star_rating'].replace(0.0, np.nan)
        return df
    except Error as e:
        st.error(f"Error occurred when fetching filtered value: {e}")
        return pd.DataFrame()

conn = connection()

# Load custom CSS from file
with open("Customization_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Title and welcome message
st.title("REDBUS - Bus Ticket Booking 🚍")
st.markdown("**Welcome to Redbus! 👉 Find and book bus tickets easily. Use the filters below to search for buses 🔍.**")

# Sidebar with image and filter options
bus_image_url = "https://media.istockphoto.com/id/1312644983/vector/modern-city-passenger-bus-against-the-background-of-an-abstract-cityscape-vector-illustration.jpg?s=612x612&w=0&k=20&c=QNTyvmklpvs4cT-JzD-DjmdK_EsN8Wh6I5sLZ9UoB_E="
st.sidebar.image(bus_image_url, use_column_width=True)

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #FFFFFF;
        margin-right: 20px;
        border-right: 2px solid #FFFFFF
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.header("Filter Options 🔽")
bus_type_query = "SELECT DISTINCT Bus_Type FROM BusDetails;"
bus_types = fetch_distinct_value(conn, bus_type_query)
bus_type = st.sidebar.selectbox("**Seat Type**", ['--- select bus type ---'] + ['All'] + bus_types)

price_range = st.sidebar.slider("**Price Range**", 0, 3000, (0, 3000),100)
rating_range = st.sidebar.slider("**Star Rating**", 0, 5, (0, 5),1)
departure_range = st.sidebar.slider("**Departure Time (Hour)**", 0, 24, (0, 24),1)

# Main Page Layout
col1, col2 = st.columns(2)

with col1:
    state_query = "SELECT DISTINCT State_TransportationName FROM BusRoutesAndLinks;"
    states = fetch_distinct_value(conn, state_query)
    state = st.selectbox("**States Transportation Name**", ['--- select state ---'] + states)

with col2:
    if state != '--- select state ---':
        route_query = f"SELECT Bus_Routes FROM BusRoutesAndLinks WHERE State_TransportationName = '{state}';"
        routes = fetch_distinct_value(conn, route_query)
        route = st.selectbox("**Routes**", ['--- select route ---'] + routes)
    else:
        route = st.selectbox("**Routes**", ['--- select route ---'])

# Search Button
if st.button("**Search**"):
    if state != '--- select state ---' and route != '--- select route ---':
        bus_type_condition = f"b.Bus_Type = '{bus_type}'" if bus_type != 'All' and bus_type != '--- select bus type ---' else "1=1"
        query = f"""
            SELECT r.Bus_Routes, r.Routes_Links, b.Bus_Name, b.Bus_Type, 
                   b.Departure_Time, b.Travelling_Time, b.Reaching_Time, 
                   b.Bus_rating, b.Ticket_Price, b.Seat_Availability
            FROM BusRoutesAndLinks r
            JOIN BusDetails b ON r.Route_NO = b.Bus_No
            WHERE r.State_TransportationName = '{state}' 
            AND r.Bus_Routes = '{route}'
            AND ({bus_type_condition})
            AND b.Bus_rating BETWEEN {rating_range[0]} AND {rating_range[1]}
            AND b.Ticket_Price BETWEEN {price_range[0]} AND {price_range[1]}
            AND HOUR(b.Departure_Time) BETWEEN {departure_range[0]} AND {departure_range[1]};
        """
        with st.spinner('Loading...'):
            time.sleep(2)
            result_df = fetch_filtered_value(conn, query)
        if not result_df.empty:
            st.dataframe(result_df)
        else:
            st.write("No buses available for the selected criteria.")
    else:
        st.write("Please select a state and route to search for buses.")