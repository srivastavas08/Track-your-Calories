
"""
Created on Sun May 21 11:41:15 2023
@author: kiranchandra
@email: srivastavas08@gmail.com
@Desc: Interactive Calorie Dashboard - Streamlit
"""

import pandas as pd
import streamlit as st



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Calories Dashboard", page_icon=":bar_chart:", layout="wide")


#Function to calculate the calories per gram serve
def calculator(servesize, calorie, inputvalue):
    
    outputvalue = (calorie/servesize)*inputvalue
    
    return round(outputvalue, 2)


# ---- READ EXCEL ----
@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url, index_col=False)
    return df

#Loading Dataset from git repo
df = load_data("https://raw.githubusercontent.com/srivastavas08/DataSets/main/India_Menu.csv")


#Removing extra spaces
df.columns = [column.replace(" ", "_") for column in df.columns]

#Converting column to list
columns = list([column.replace("_", " ") for column in df.columns])



# ---- SIDEBAR ----

st.sidebar.header("Please Filter Here :")
category = st.sidebar.selectbox(
    "Select the Menu Category:",
    options=df["Menu_Category"].unique())


#Applying Menu filter
df_selection = df.query(
    "Menu_Category == @category"
)


menuItem = st.sidebar.selectbox(
    "Select the Food Items:",
    options=df_selection["Menu_Items"].unique())


custom = st.sidebar.checkbox("Please confirm if you want to change the serve size")


if custom:
                                      
    slider = st.sidebar.slider('Select the Serve Size (g) : ', 0,1000,step = 1)

selected = df_selection.query("Menu_Items==@menuItem")



# ---- MAINPAGE ----
st.title(":bar_chart: Calories Dashboard")
st.markdown("##")


x = str(str(selected["Menu_Category"]).split("\n")[0]).split(" ")
x = x[4]+" "+x[5]


if  x in ["Beverages Menu", "McCafe Menu"]:
    ServeSize = float(str(str(selected['Per_Serve_Size']).replace(" ","").split("\n")[0][1:]).replace("ml", ""))

    perServeSize = str(ServeSize) + " ml"
    
else:
    
    ServeSize = float(str(str(selected['Per_Serve_Size']).replace(" ","").split("\n")[0][1:]).replace("g", ""))
    
    perServeSize = str(ServeSize) + " g"


# ----------------For Custom Values -------------------------------
if custom:
    
    d = {}
    bar_frame = selected[selected.columns.difference(['Menu_Category', 'Menu_Items', 'Per_Serve_Size',' '])]
    
    for column in bar_frame.columns:
        d[column] = float(str(bar_frame[column]).replace(" ", "").split("\n")[0][1:])
        
    for key in d.keys():
        d[key] = calculator(ServeSize, d[key], slider)
     
    #Quick Check Filter
    
    st.sidebar.header("Quick Filter")
    calories = st.sidebar.selectbox(
        "Choose the Calorie :",
        options=columns[3:])
    
    caloriess = calories.replace(" ", "_")
    
    value = calories + " : " + str(d[caloriess])
    
    st.sidebar.subheader(value)  
    
     

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Per Serve Size")
        if  x in ["Beverages Menu", "McCafe Menu"]:
            st.subheader(str(slider)+" ml")
        else:
            st.subheader(str(slider)+" g")
        
    with col2:
        st.subheader("Energy (kCal)")
        st.subheader(str(d["Energy_(kCal)"]))
        
    with col3:
        st.subheader("Proteins (g)")
        st.subheader(str(d["Protein_(g)"]))
        
    with col4:
        st.subheader("Total Fat (g)")
        st.subheader(str(d["Total_fat_(g)"]))
        
    st.markdown("""---""")
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.line_chart(d)
        
    with col2:
        st.bar_chart(d)
    
    st.markdown("""---""")
    
    col1, col2 =st.columns(2)
        
    with col1:
        
        check = st.checkbox("Please confirm if you want to see complete data set")
        
        if check:
            st.dataframe(df)
    
    with col2:
        
        check1 = st.checkbox("Please confirm if you want to see calculated values")
        
        if check1:
            st.table(d)
        

#---------------For Default values from datasets-----------------------

else:
    
    #TOP KPI's
    energy = str(selected['Energy_(kCal)']).split("\n")[0][1:]
    proteins = str(selected['Protein_(g)']).split("\n")[0][1:]
    totalFat = str(selected['Total_fat_(g)']).split("\n")[0][1:]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("Per Serve Size")
        st.subheader(str(perServeSize))
    
    with col2:
        st.subheader("Energy (kCal)")
        st.subheader(str(energy))
        
    with col3:
        st.subheader("Proteins (g)")
        st.subheader(str(proteins))
        
    with col4:
        st.subheader("Total Fat (g)")
        st.subheader(str(totalFat))

    st.sidebar.header("Quick Filter :")
    calories = st.sidebar.selectbox(
        "Choose the Calorie :",
        options=columns[3:])
    
    caloriess = calories.replace(" ", "_")
    
    value = calories + " : " + str(selected[caloriess]).split("\n")[0][1:]
    
    st.sidebar.subheader(value)  
        
    
    st.markdown("""---""")
    
    bar_frame = selected[selected.columns.difference(['Menu_Category', 'Menu_Items', 'Per_Serve_Size',' '])]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.line_chart(bar_frame.T)
        
    with col2:
        st.bar_chart(bar_frame.T)
    
    st.markdown("""---""")
    
    col1, col2 =st.columns(2)
        
    with col1:
        
        check = st.checkbox("Please confirm if you want to see complete data set")
        
        if check:
            st.dataframe(df)
    
    with col2:
        
        check1 = st.checkbox("Please confirm if you want to see calculated values")
        
        if check1:
            st.table(bar_frame)
    


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

