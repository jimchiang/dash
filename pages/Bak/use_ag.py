import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import plotly.express as px
import sqlite3, datetime
from src import agstyler, helper
from src.agstyler import PINLEFT, PRECISION_TWO
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Load data into a pandas DataFrame
#df = pd.read_csv('your_dataset.csv')

#def main():
if True:
    cnx = sqlite3.connect('../OutputData/hackfest24.sqlite')

    df = pd.read_sql_query("SELECT * FROM keyword", cnx)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

    print(grid_table)
    
    st.write('## Selected')
    selected_row = grid_table["selected_rows"]
    print(selected_row)
    st.dataframe(selected_row)
    st.write(selected_row)

def log( msg ):
	print( datetime.datetime.now().isoformat() + "  " + msg )

def db_work(id,score,status):
    cnx = sqlite3.connect('../OutputData/hackfest24.sqlite')
    cursor = cnx.cursor() 
    sql_update_QScore_Rev   = "UPDATE keyword SET QScore_Rev  = '{1}' WHERE idnr = '{0}';".format(str(id),str(score))
    sql_update_QStatus_Rev  = "UPDATE keyword SET QStatus_Rev = '{1}' WHERE idnr = '{0}';".format(str(id),str(status) )
    cursor.execute(sql_update_QScore_Rev)
    cursor.execute(sql_update_QStatus_Rev)
    #cursor.execute('''UPDATE EMPLOYEE SET INCOME = 5000 WHERE Age<25;''') 
    #print(sql_update_QScore_Rev)
    #print(sql_update_QStatus_Rev)
    cnx.commit() 
    cnx.close() 

#if __name__ == "__main__":
#    main()
