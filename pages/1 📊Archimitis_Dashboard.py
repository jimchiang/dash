import streamlit as st
import numpy as np
import pandas as pd
import sqlite3, random, io
import plotly.express as px

st.set_page_config(
    page_title="Archimitis' Greetings",
    page_icon="👋",
)

cnx = sqlite3.connect('./data/hackfest24.sqlite')

#st.sidebar.markdown("# Categorized Dataset")
st.sidebar.title("Explore Categorized Dataset")
if True:
	default_value = "1. All Respondents"
	choices = ["1. All Respondents", "2. Valid Responses", "3. Dups - Across Question/Respondents","4. AI or Generic Responses","5. Gibberish/Profanity/Offensive Language","6. Edited Responses"]
	app_mode = st.sidebar.selectbox( "Choose an Action", choices, index=choices.index(default_value))

# Initialize the session state
if 'selection' not in st.session_state:
    st.session_state['selection'] = 0

st.sidebar.success("Select an option above.")


def checkFileResponse():
	uploaded_file = st.file_uploader("Choose a file", type={"xlsx","csv"})
	wb = Workbook()
	if uploaded_file is not None:
		df_data = pd.read_excel(uploaded_file)
		st.write(df_data)

def checkOneResponse():
	st.header('Vacation Time', divider='rainbow')
	ans1 = st.text_area(
		'We are collecting suggestions for a study on the subject of vacations. How would you describe your perfect vacation?',
		'', key='ques1')
	st.write('Your Answer is - ', ans1)
	st.write('Your Answer is - ', (ans1))

	st.header('Music Lover', divider='rainbow')
	ans2 = st.text_area(
		'Childhood memories are always special, and toys play an important role in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you??',
		'', key='ques2')

	st.header('Toy and Play Memory', divider='rainbow')
	ans3 = st.text_area(
		'Childhood memories are always special, and toys play an important role in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you??',
		'', key='ques3')

def db_work(id,score,status):
    cnx = sqlite3.connect('./data/hackfest24.sqlite')
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

my_df = pd.read_sql_query("SELECT * FROM keyword", cnx)
df = my_df.copy(deep=True)
print(app_mode)
print(my_df.shape)
print(df.shape)
# Conditional display of data visualization
if app_mode == '1. All Respondents':
    df = my_df.copy(deep=True)
    st.write("#All Respondents - " + str(df.shape) )
if app_mode == '2. Valid Responses':
    flag0 = (my_df['QScore'] == 1)
    df = my_df[(flag0)]
    st.write("#Valid Responses - " + str(df.shape) )
if app_mode == '3. Dups - Across Question/Respondents':
    flag0 = (my_df['QScore'] == 2)
    df = my_df[(flag0)]
    st.write("#Dups - Across Question/Respondents - " + str(df.shape) )
if app_mode == '4. AI or Generic Responses':
    flag0 = (my_df['QScore'] == 3)
    df = my_df[(flag0)]
    st.write("#AI or Generic Responses - " + str(df.shape) )
if app_mode == '5. Gibberish/Profanity/Offensive Language':
    flag0 = (my_df['QScore'] == 4)
    df = my_df[(flag0)]
    st.write("#Gibberish/Profanity/Offensive Language - " + str(df.shape) )
if app_mode == '6. Edited Responses':
    flag0 = ~(my_df['QScore'] == 1)
    flag1 = (my_df['QScore_Rev'] == 1)
    df = my_df[(flag0 & flag1)]
    st.write("#Edited Responses - " + str(df.shape) )

#flag0 = (df['qcheck_Flag'])
#df = df[ (flag0)]

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        width=None,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True), "qcheck": st.column_config.Column(width="medium"), "x01_2": st.column_config.Column(width="medium"), "x01_2": st.column_config.Column(width="medium"),},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    print(selected_rows)
    print(edited_df)
    return selected_rows.drop('Select', axis=1)



selection = dataframe_with_selections(df)

if app_mode == '1. All Respondents':
    flag0 = (my_df['QScore'] == 1)
    dfx = pd.DataFrame(df['QStatus'].value_counts(normalize=False, sort=True, ascending=False, bins=None,dropna=False))
    dfx = df['QStatus'].value_counts().rename_axis('QStatus').reset_index(name='counts')
    #st.plotly_chart(dfx, theme=None)
    #print(dfx.columns)
    #print(dfx)
    #dfx = dfx.sort_values(['counts'], ascending=[False])
    print(dfx)
    dfx.loc[ ( dfx['QStatus'] == 'Valid Response' ), 'QStatus']                          = '1. Valid Responses'
    dfx.loc[ ( dfx['QStatus'] == 'Dups - Across Question/Respondents' ), 'QStatus']      = '2. Dups - Across Question/Respondents'
    dfx.loc[ ( dfx['QStatus'] == 'AI or Generic Responses' ), 'QStatus']                 = '3. AI or Generic Responses'
    dfx.loc[ ( dfx['QStatus'] == 'Gibberish/Profanity/Offensive Language' ), 'QStatus']  = '4. Gibberish/Profanity/Offensive Language'
    print(dfx)
    st.bar_chart(dfx,y='counts',x='QStatus',width=0, height=450)
    st.line_chart(df[['qcheck_Profanity', 'x01_2_Profanity', 'x01_3_Profanity']],width=0, height=450)
    #st.bar_chart(dfx, x=None, y=None, sort_by=None, ascending=False, width=200, height=0, use_container_width=True)

print(selection.head(5))
print(selection)
st.write("Your selection: among" + str(df.shape) )
st.write(selection)

col1, buff, col2 = st.columns([2,1,2])

if False:
	#st.title('Welcome to Survey')
	st.subheader('Welcome to Survey')

	genre = st.radio(
		"Select your way for survey",
		["***Single Response***", "Through a File :movie_camera:"],index =None,
		captions=["On site itself", "Upload a file."], horizontal=True)

	if genre == '***Single Response***':
		st.write('You selected Single Response.')
		checkOneResponse()
	elif genre == 'Through a File :movie_camera:':
		st.write("You  select File upload system.")
		checkFileResponse()
	else:
		pass


def fav1random(fav__1):
    convert1 = list(fav__1.split(' '))
    random1 = random.choice(convert1)
    if 'random1' not in st.session_state:
        st.session_state.random1 = random1
    elif 'random1' in st.session_state:
        st.session_state.random1 = random1
    return random1
    
def fav2random(fav__2):
    convert2 = list(fav__2.split(' '))
    random2 = random.choice(convert2)
    if 'random2' not in st.session_state:
        st.session_state.random1 = random2
    elif 'random2' in st.session_state:
        st.session_state.random2 = random2
    return random2

with col1:
    if len(selection) != 0:
        selection_id = selection['idnr'].dropna().unique().tolist()
        fav__1 = st.text_input('Respondent Reclassify as Valid:', str(selection_id), key='fav1')
    else:
        fav__1 = st.text_input('Respondent Reclassify as Valid:', key='fav1')
    sub1 = st.button("Submit", key='rand1')
    if sub1:
        random1 = fav1random(fav__1)
        #st.write('Favorite:', fav__1)
        #st.write('fav_txt:', random1)
        st.write('Reclassify to #valid response', str(selection_id))
        if len(selection) != 0:
            selection_id = selection['idnr'].dropna().unique().tolist()
            if len(selection_id) != 0:
                for txt in selection_id:
                    db_work(txt,1,"Valid Response")

with col2:
    fav__2 = st.text_input('Respondent Removal:', key='fav2')
    sub2 = st.button("Submit", key='rand2')
    if sub2:
        random2 = fav2random(fav__2)
        st.write('Favorite:', fav__2)
        st.write('fav_txt:', random2)

df = pd.read_sql_query("SELECT * FROM keyword", cnx)

with io.BytesIO() as buffer:
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write the DataFrame to a different worksheet
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='large_df.xlsx',
        mime='application/vnd.ms-excel'
    )