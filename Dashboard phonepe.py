# Requried libararys
import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu
import plotly.express as px
import json
from PIL import Image
import os
import subprocess
import requests
from sqlalchemy import create_engine as ce

# CLONING THE PHONEPE--PULSE GITHUB REPOSITORY

# response = requests.get('https://api.github.com/repos/PhonePe/pulse')
# repo = response.json()
# clone_url = repo['clone_url']

# # #DIRECTING THE REPOSITORY TO THE LOCAL DIRECTORY
# repo_name = "pulse"
# clone_dir = os.path.join(os.getcwd(), repo_name)

# -------------------------or----------------------------

user = "root"
password = "gigabyte"
host = "localhost"
port = 3306
database = "phonepe_database"
connection = ce(
    "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)
)

df = pd.read_csv(
    "C:/Users/Workstation/Documents/Phonepe/data/Agg_Trans.csv",
    index_col=0,
)
state = pd.read_csv(
    "C:/Users/Workstation/Documents/Phonepe/data/Longitude_Latitude_State_Table.csv"
)
districts = pd.read_csv(
    "C:/Users/Workstation/Documents/Phonepe/data/Data_Map_Districts_Longitude_Latitude.csv"
)

districts_trans = pd.read_csv(
    "C:/Users/Workstation/Documents/Phonepe/data/district_map_transaction.csv",
    index_col=0,
)
app_opening = pd.read_csv(
    "C:/Users/Workstation/Documents/Phonepe/data extracted/district_registering_map.csv",
    index_col=0,
)

user_device = pd.read_csv(
    "C:/Users/Workstation/Documents/Phonepe/data/user_by_device.csv", index_col=0
)
SELECT = option_menu(
    menu_title=None,
    options=["Users Insight", "About"],
    icons=["sun", "moon"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "white",
            "size": "cover",
        },
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {
            "font-size": "20px",
            "text-align": "center",
            "margin": "-2px",
            "--hover-color": "#6F36AD",
        },
        "nav-link-selected": {"background-color": "#6F36AD"},
    },
)


if SELECT == "About":
    st.write("---")
    st.title("Thank you for seeing my GitHub repository")
    st.write("---")
    st.subheader("Here Data extraction is done and stored in MySQL database")
    st.image(Image.open("C:/Users/Workstation/Downloads/1285769.jpg"), width=400)
    st.subheader("and data visualization is performed with Plotly and Streamlit")
    with open("C:/Users/Workstation/Downloads/PhonePe_Pulse_BCG_report.pdf", "rb") as f:
        data = f.read()
        st.download_button("DOWNLOAD REPORT", data, file_name="annual_report.pdf")

state = state.sort_values(by="state")
state = state.reset_index(drop=True)
df2 = df.groupby(["State"]).sum()[["Transacion_count", "Transacion_amount"]]
df2 = df2.reset_index()

choropleth_data = state.copy()

for column in df2.columns:
    choropleth_data[column] = df2[column]
choropleth_data = choropleth_data.drop(labels="State", axis=1)

df.rename(columns={"State": "state"}, inplace=True)
sta_list = [
    "andaman-&-nicobar-islands",
    "andhra-pradesh",
    "arunachal-pradesh",
    "assam",
    "bihar",
    "chandigarh",
    "chhattisgarh",
    "dadra-&-nagar-haveli-&-daman-&-diu",
    "delhi",
    "goa",
    "gujarat",
    "haryana",
    "himachal-pradesh",
    "jammu-&-kashmir",
    "jharkhand",
    "karnataka",
    "kerala",
    "ladakh",
    "lakshadweep",
    "madhya-pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "puducherry",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil-nadu",
    "telangana",
    "tripura",
    "uttar-pradesh",
    "uttarakhand",
    "west-bengal",
]
state["state"] = pd.Series(data=sta_list)
state_final = pd.merge(df, state, how="outer", on="state")
districts_final = pd.merge(
    districts_trans, districts, how="outer", on=["State", "District"]
)


# ------------------------------------------ Streamlit app Plot 1 Scatter plot of registered user and app opening ----------------------------
with st.container():
    st.title(":violet[PhonePe Usage all over india]")
    st.write(" ")
    st.subheader(
        ":violet[Registered user & App installed of  State and District wise:]"
    )
    st.write(" ")
    scatter_year = st.selectbox(
        "Please select the Year", ("2018", "2019", "2020", "2021", "2022")
    )
st.write(" ")
scatter_state = st.selectbox(
    "Please select State",
    (
        "andaman-&-nicobar-islands",
        "andhra-pradesh",
        "arunachal-pradesh",
        "assam",
        "bihar",
        "chandigarh",
        "chhattisgarh",
        "dadra-&-nagar-haveli-&-daman-&-diu",
        "delhi",
        "goa",
        "gujarat",
        "haryana",
        "himachal-pradesh",
        "jammu-&-kashmir",
        "jharkhand",
        "karnataka",
        "kerala",
        "ladakh",
        "lakshadweep",
        "madhya-pradesh",
        "maharashtra",
        "manipur",
        "meghalaya",
        "mizoram",
        "nagaland",
        "odisha",
        "puducherry",
        "punjab",
        "rajasthan",
        "sikkim",
        "tamil-nadu",
        "telangana",
        "tripura",
        "uttar-pradesh",
        "uttarakhand",
        "west-bengal",
    ),
    index=10,
)
scatter_year = int(scatter_year)
scatter_reg_df = app_opening[
    (app_opening["Year"] == scatter_year) & (app_opening["State"] == scatter_state)
]

scatter_register = px.data.iris()
fig = px.scatter(
    scatter_reg_df,
    x="District",
    y="Registered_user",
    color="District",
    hover_name="District",
    hover_data=["Year", "Quater"],
    size_max=10,
)
fig

geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(
    [
        "Geographical analysis",
        "User device analysis",
        "Payment Types analysis",
        "Transacion analysis of States",
    ]
)
# ------------------------------------------- Geo-analysis --------------------------------------#
with geo_analysis:
    st.subheader(":violet[Transaction analysis of State and District wise:]")
    st.write(" ")
    Year = st.radio(
        "Please select the Year",
        ("2018", "2019", "2020", "2021", "2022"),
        horizontal=True,
    )
st.write(" ")
Quarter = st.radio("Please select the Quarter", ("1", "2", "3", "4"), horizontal=True)
st.write(" ")
Year = int(Year)
Quarter = int(Quarter)
plot_district = districts_final[
    (districts_final["Year"] == Year) & (districts_final["Quater"] == Quarter)
]
plot_state = state_final[
    (state_final["Year"] == Year) & (state_final["Quater"] == Quarter)
]
plot_state_total = plot_state.groupby(
    ["state", "Year", "Quater", "Latitude", "Longitude"]
).sum()
plot_state_total = plot_state_total.reset_index()
state_code = [
    "AN",
    "AD",
    "AR",
    "AS",
    "BR",
    "CH",
    "CG",
    "DNHDD",
    "DL",
    "GA",
    "GJ",
    "HR",
    "HP",
    "JK",
    "JH",
    "KA",
    "KL",
    "LA",
    "LD",
    "MP",
    "MH",
    "MN",
    "ML",
    "MZ",
    "NL",
    "OD",
    "PY",
    "PB",
    "RJ",
    "SK",
    "TN",
    "TS",
    "TR",
    "UP",
    "UK",
    "WB",
]
plot_state_total["code"] = pd.Series(data=state_code)
# ------------------------------------------- Geo-visualization of transacion data ----------------------------------#
fig1 = px.scatter_geo(
    plot_district,
    lon=plot_district["Longitude"],
    lat=plot_district["Latitude"],
    color=plot_district["Transaction_amount"],
    size=plot_district["Transaction_count"],
    hover_name="District",
    hover_data=[
        "State",
        "Transaction_amount",
        "Transaction_amount",
        "Transaction_count",
        "Year",
        "Quater",
    ],
    title="District",
    size_max=22,
)
fig1.update_traces(marker={"color": "#ff0019", "line_width": 1})
fig2 = px.scatter_geo(
    plot_state_total,
    lon=plot_state_total["Longitude"],
    lat=plot_state_total["Latitude"],
    hover_name="state",
    text=plot_state_total["code"],
    hover_data=["Transacion_count", "Transacion_amount", "Year", "Quater"],
)
fig2.update_traces(marker=dict(color="#87f5ff", size=0.3))
fig = px.choropleth(
    choropleth_data,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey="properties.ST_NM",
    locations="state",
    color="Transacion_amount",
    color_continuous_scale="twilight",
    hover_data=["Transacion_count", "Transacion_amount"],
)

fig.update_geos(fitbounds="locations", visible=False)
fig.add_trace(fig1.data[0])
fig.add_trace(fig2.data[0])
fig.update_layout(height=1080, width=1080)
st.write(" ")
st.write(" ")

# if st.button('Click here to see map clearly'):
#              fig.show()

st.plotly_chart(fig)
# --------------------------------------------------- Device analysis statewise -----------------------------------------------------------#
with Device_analysis:
    st.subheader(":violet[User Device analysis->Statewise:]")
    tree_map_state = st.selectbox(
        "Please select State",
        (
            "andaman-&-nicobar-islands",
            "andhra-pradesh",
            "arunachal-pradesh",
            "assam",
            "bihar",
            "chandigarh",
            "chhattisgarh",
            "dadra-&-nagar-haveli-&-daman-&-diu",
            "delhi",
            "goa",
            "gujarat",
            "haryana",
            "himachal-pradesh",
            "jammu-&-kashmir",
            "jharkhand",
            "karnataka",
            "kerala",
            "ladakh",
            "lakshadweep",
            "madhya-pradesh",
            "maharashtra",
            "manipur",
            "meghalaya",
            "mizoram",
            "nagaland",
            "odisha",
            "puducherry",
            "punjab",
            "rajasthan",
            "sikkim",
            "tamil-nadu",
            "telangana",
            "tripura",
            "uttar-pradesh",
            "uttarakhand",
            "west-bengal",
        ),
        index=10,
        key="tree_map_state",
    )
    tree_map_state_year = int(
        st.radio(
            "Please select the Year",
            ("2018", "2019", "2020", "2021", "2022"),
            horizontal=True,
            key="tree_map_state_year",
        )
    )
    tree_map_state_quater = int(
        st.radio(
            "Please select the Quarter",
            ("1", "2", "3", "4"),
            horizontal=True,
            key="tree_map_state_quater",
        )
    )
    user_device_treemap = user_device[
        (user_device["State"] == tree_map_state)
        & (user_device["Year"] == tree_map_state_year)
        & (user_device["Quater"] == tree_map_state_quater)
    ]
    user_device_treemap["Brand_count"] = user_device_treemap["Brand_count"].astype(str)
    # ----------------------------------------- Treemap view of user device ----------------------------------------------------------------
    user_device_treemap_fig = px.treemap(
        user_device_treemap,
        path=["State", "Brand"],
        values="Brand_percentage",
        hover_data=["Year", "Quater"],
        color="Brand_count",
        title="User device distribution in "
        + tree_map_state
        + " in "
        + str(tree_map_state_year)
        + " at "
        + str(tree_map_state_quater)
        + " quater",
    )
    st.plotly_chart(user_device_treemap_fig)
    # ---------------------------------------- Barchart view of user device -----------------------------------------------------------------
    bar_user = px.bar(
        user_device_treemap,
        x="Brand",
        y="Brand_count",
        color="Brand",
        title="Bar chart analysis",
        color_continuous_scale="sunset",
    )
    st.plotly_chart(bar_user)


# ----------------------------------------- Payment type analysis of Transacion data ----------------------------------------------------------
with payment_analysis:
    st.subheader(":violet[Payment type Analysis -> 2018 - 2022:]")
    payment_mode = pd.read_csv(
        "C:/Users/Workstation/Documents/Phonepe/data/Agg_Trans.csv", index_col=0
    )
    pie_pay_mode_state = st.selectbox(
        "Please select State",
        (
            "andaman-&-nicobar-islands",
            "andhra-pradesh",
            "arunachal-pradesh",
            "assam",
            "bihar",
            "chandigarh",
            "chhattisgarh",
            "dadra-&-nagar-haveli-&-daman-&-diu",
            "delhi",
            "goa",
            "gujarat",
            "haryana",
            "himachal-pradesh",
            "jammu-&-kashmir",
            "jharkhand",
            "karnataka",
            "kerala",
            "ladakh",
            "lakshadweep",
            "madhya-pradesh",
            "maharashtra",
            "manipur",
            "meghalaya",
            "mizoram",
            "nagaland",
            "odisha",
            "puducherry",
            "punjab",
            "rajasthan",
            "sikkim",
            "tamil-nadu",
            "telangana",
            "tripura",
            "uttar-pradesh",
            "uttarakhand",
            "west-bengal",
        ),
        index=10,
        key="pie_pay_mode_state",
    )
    pie_pay_mode_year = int(
        st.radio(
            "Please select the Year",
            ("2018", "2019", "2020", "2021", "2022"),
            horizontal=True,
            key="pie_pay_year",
        )
    )
    pie_pay_mode__quater = int(
        st.radio(
            "Please select the Quarter",
            ("1", "2", "3", "4"),
            horizontal=True,
            key="pie_pay_quater",
        )
    )
    pie_pay_mode_values = st.selectbox(
        "Please select the values to visualize",
        ("Transacion_count", "Transacion_amount"),
    )
    pie_payment_mode = payment_mode[
        (payment_mode["Year"] == pie_pay_mode_year)
        & (payment_mode["Quater"] == pie_pay_mode__quater)
        & (payment_mode["State"] == pie_pay_mode_state)
    ]
    # -------------------------------- Pie chart analysis of Payment mode --------------------------------------------------------------------
    pie_pay_mode = px.pie(
        pie_payment_mode,
        values=pie_pay_mode_values,
        names="Transacion_type",
        hole=0.5,
        hover_data=["Year"],
    )
    # ------------------------------------- Bar chart analysis of payment mode ----------------------------------------------------------------
    pay_bar = px.bar(
        pie_payment_mode,
        x="Transacion_type",
        y=pie_pay_mode_values,
        color="Transacion_type",
    )
    st.plotly_chart(pay_bar)
    st.plotly_chart(pie_pay_mode)


# --------------------------------------- Transacion data analysis statewise ------------------------------------------------------------------
with transac_yearwise:
    st.subheader(":violet[Transaction analysis->Statewise:]")
    transac_state = st.selectbox(
        "Please select State",
        (
            "andaman-&-nicobar-islands",
            "andhra-pradesh",
            "arunachal-pradesh",
            "assam",
            "bihar",
            "chandigarh",
            "chhattisgarh",
            "dadra-&-nagar-haveli-&-daman-&-diu",
            "delhi",
            "goa",
            "gujarat",
            "haryana",
            "himachal-pradesh",
            "jammu-&-kashmir",
            "jharkhand",
            "karnataka",
            "kerala",
            "ladakh",
            "lakshadweep",
            "madhya-pradesh",
            "maharashtra",
            "manipur",
            "meghalaya",
            "mizoram",
            "nagaland",
            "odisha",
            "puducherry",
            "punjab",
            "rajasthan",
            "sikkim",
            "tamil-nadu",
            "telangana",
            "tripura",
            "uttar-pradesh",
            "uttarakhand",
            "west-bengal",
        ),
        index=10,
        key="transac",
    )
    transac__quater = int(
        st.radio(
            "Please select the Quarter",
            ("1", "2", "3", "4"),
            horizontal=True,
            key="trans_quater",
        )
    )
    transac_type = st.selectbox(
        "Please select the Mode",
        (
            "Recharge & bill payments",
            "Peer-to-peer payments",
            "Merchant payments",
            "Financial Services",
            "Others",
        ),
        key="transactype",
    )
    transac_values = st.selectbox(
        "Please select the values to visualize",
        ("Transacion_count", "Transacion_amount"),
        key="transacvalues",
    )
    payment_mode_yearwise = pd.read_csv(
        "C:/Users/Workstation/Documents/Phonepe/data/Agg_Trans.csv", index_col=0
    )
    new_df = payment_mode_yearwise.groupby(
        ["State", "Year", "Quater", "Transacion_type"]
    ).sum()
    new_df = new_df.reset_index()
    chart = new_df[
        (new_df["State"] == transac_state)
        & (new_df["Transacion_type"] == transac_type)
        & (new_df["Quater"] == transac__quater)
    ]
    # ------------------------------- Bar chart analysis of transacion data statewise --------------------------------------------------------
    year_fig = px.bar(
        chart,
        x=["Year"],
        y=transac_values,
        color=transac_values,
        color_continuous_scale="armyrose",
        title="Transacion analysis " + transac_state + " regarding to " + transac_type,
    )
    st.plotly_chart(year_fig)


# -------------------------------------------- Sidebar --> for overall india Data comparisons -------------------------------------------------
with st.sidebar:
    # -------------------------- Bar chart ofoverall india transacion data  -----------------------------------------------------------------
    st.subheader(":violet[Overall India Analysis:]")
    overall_values = st.selectbox(
        "Please select the values to visualize",
        ("Transacion_count", "Transacion_amount"),
        key="values",
    )
    overall = new_df.groupby(["Year"]).sum()
    overall.reset_index(inplace=True)

    overall = px.bar(
        overall,
        x="Year",
        y=overall_values,
        color=overall_values,
        title="Overall pattern of Transacion all over India",
        color_continuous_scale="sunset",
    )
    overall.update_layout(height=350, width=350)
    st.plotly_chart(overall)

    # --------------------------Bar chart of overall india user device analysis --------------------------------------------------------------

    user_device_overall = pd.read_csv(
        "C:/Users/Workstation/Documents/Phonepe/data/user_by_device.csv", index_col=0
    )
    overall_device = user_device_overall.groupby(["Brand", "Year"]).sum()
    overall_device.reset_index(inplace=True)

    overall_dev_fig = px.bar(
        overall_device,
        x="Year",
        y="Brand_count",
        color="Brand",
        title="Customer Device pattern from 2018 - 2022",
    )
    overall_dev_fig.update_layout(height=350, width=350)
    st.plotly_chart(overall_dev_fig)

    # --------------------------Bar chart of overall india registered and app opening --------------------------------------------------------

    overall_reg = pd.read_csv(
        "C:/Users/Workstation/Documents/Phonepe/data/district_registering_map.csv"
    )
    overall_reg = overall_reg.groupby(["State", "Year"]).sum()
    overall_reg.reset_index(inplace=True)

    overall_reg = px.bar(
        overall_reg,
        x="Year",
        y=["Registered_user", "App_opening"],
        barmode="group",
        title="Phonepe installation from 2018 - 2022",
    )
    overall_reg.update_layout(height=350, width=350)
    st.plotly_chart(overall_reg)
