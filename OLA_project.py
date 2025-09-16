import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd

def create_connection():
    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["localhost"],
        port=st.secrets["mysql"]["3306"]
        user=st.secrets["mysql"]["root"],
        password=st.secrets["mysql"]["PAra!1001"],
        database=st.secrets["mysql"]["ola_project"]
    )
    return conn
predefined_queries = {
    "Retrieve all successful bookings": """
        SELECT * 
        FROM ride_bookings 
        WHERE Booking_Status = 'Success';
    """,
    "Find the average ride distance for each vehicle type": """
        SELECT Vehicle_Type, AVG(Ride_Distance) AS Average_ride_distance 
        FROM ride_bookings 
        GROUP BY Vehicle_Type
        order by Average_ride_distance desc;
    """,
    "Get the total number of cancelled rides by customers": """
        SELECT COUNT(*) AS Cancelled_Rides 
        FROM ride_bookings 
        WHERE Canceled_Rides_by_Customer <> 'Not canceled by Customer';
    """,
    "List the top 5 customers who booked the highest number of rides": """
        SELECT Customer_ID, COUNT(Customer_ID) as No_of_Ride_booking 
        FROM ride_bookings 
        GROUP BY Customer_ID 
        HAVING COUNT(*)
        ORDER BY No_of_Ride_booking DESC
        LIMIT 5;
    """,
    "Get the number of rides cancelled by drivers due to personal and car-related issues": """
        SELECT COUNT(*) AS Driver_Cancels 
        FROM ride_bookings 
        WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';
    """,
    "Find the maximum and minimum driver ratings for Prime Sedan Bookings": """
        SELECT MAX(Driver_Ratings) AS Max_Driver_Ratings, MIN(Driver_Ratings) AS Min_Driver_Ratings 
        FROM ride_bookings 
        WHERE Vehicle_Type = 'Prime Sedan';
    """,
    "Retrieve all rides where payment was made using UPI": """
        SELECT * 
        FROM ride_bookings 
        WHERE Payment_Method = 'UPI';
    """,
    "Find the average customer rating per vehicle type": """
        SELECT Vehicle_Type, AVG(Customer_Rating) AS Avg_Cus_rating_Vehical_type 
        FROM ride_bookings 
        GROUP BY Vehicle_Type;
    """,
    "Calculate the total booking value of rides completed successfully": """
        SELECT SUM(Booking_Value) AS Success_ride_booking_Value 
        FROM ride_bookings 
        WHERE Incomplete_Rides = 'No';
    """,
    "List all incomplete rides along with the reason": """
        SELECT Booking_ID, Booking_Status, Incomplete_Rides, Incomplete_Rides_Reason
        FROM ride_bookings 
        WHERE Incomplete_Rides = 'Yes';
    """
}

st.set_page_config(layout= "wide")

st.markdown(
    "<h1 style='font-size:56px;'>🚖 Ola Ride Insights Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h1 style='font-size:40px;'> Transforming ride-sharing data into actionable business intelligence</h1>",
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

with st.sidebar:
    select = option_menu("📂 Navigation",["🏠 Overview", "🛠 SQL Analytics", "📊 Power BI Dashboards"],
                         icons=["house", "terminal", "bar-chart"],
                         menu_icon="cast",
                        default_index=0
        )

if select == "🏠 Overview":

    st.header("Data-driven analytics for smarter ride-sharing decisions")
    st.write("""
            Urban mobility is rapidly evolving with the rise of ride-sharing platforms. 
    **Ola**, one of the leading ride-hailing services, generates massive amounts of data every day — 
    from bookings and cancellations to driver performance, pricing, and customer ratings.  

    This interactive application transforms raw ride data into **actionable business insights**, helping stakeholders:

    - 📊 Monitor booking trends and demand patterns  
    - 🚗 Analyze vehicle performance and utilization  
    - 💸 Track revenue by payment methods and ride types  
    - ❌ Identify cancellation reasons and reduce drop-offs  
    - ⭐ Understand customer and driver rating dynamics
             

    Combining SQL queries, Power BI visualizations, and Streamlit interactivity, this project delivers a comprehensive analytical view of Ola’s operations — empowering data-driven decision-making.
             
    ---
    **Technologies Tags:** Python | SQL | Power BI | Streamlit | Pandas | NumPy | Matplotlib | Seaborn | Data Visualization | Data Cleaning | Feature Engineering | EDA. 
""")

if select == "🛠 SQL Analytics":

    st.subheader("📌 Run Predefined SQL Query")

    option = st.selectbox("Select your SQL Query", list(predefined_queries.keys()))

    if st.button("Run Selected Query"):
        query = predefined_queries[option]
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(rows, columns=cols)
                st.dataframe(df)
            else:
                conn.commit()
                st.success("Query executed successfully ✅")

            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

    # ==============================
    # SECTION 2: Custom query input
    # ==============================
    st.subheader("✍️ Write Your Own SQL Query")

    txt = st.text_area("Enter SQL Query", "")

    if st.button("Run Custom Query"):
        if txt.strip() != "":
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute(txt)

                if txt.strip().lower().startswith("select"):
                    rows = cursor.fetchall()
                    cols = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(rows, columns=cols)
                    st.dataframe(df)
                else:
                    conn.commit()
                    st.success("Query executed successfully ✅")

                cursor.close()
                conn.close()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a SQL query.")

if select == "📊 Power BI Dashboards":
    st.subheader("📌 OLA riding insights")

    dashboards = {
    "Dashboard 1 - Ride Overview": "OLA_project_1.png",
    "Dashboard 2 - Vehicle Performance": "OLA_project_2.png",
    "Dashboard 3 - Customer Insights": "OLA_project_3.png",
    "Dashboard 4 - Cancellation Trends": "OLA_project_4.png",
    "Dashboard 5 - Revenue Analysis": "OLA_project_5.png"
}

    # Select dashboard
    option = st.selectbox("Select a Dashboard to View", list(dashboards.keys()))

    # Show selected dashboard
    st.image(dashboards[option], caption=option, use_container_width=True)
