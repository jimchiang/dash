import streamlit as st
import pandas as pd
import sqlite3, random

#cnx = sqlite3.connect('./data/hackfest24.sqlite')

cnx = sqlite3.connect('./data/hackfest24.sqlite')

my_df = pd.read_sql_query("SELECT * FROM keyword", cnx)
df = my_df.copy(deep=True)

# Callback function for A and B
def onClick(selection_input):
    if selection_input == 'A':
        st.session_state['selection'] = 0
    if selection_input == 'B':
        st.session_state['selection'] = 1
t2 = """
# Initialize the session state
if 'selection' not in st.session_state:
    st.session_state['selection'] = 0

# Select box
selected = st.selectbox('Make a selection:', ('A', 'B'), index=st.session_state['selection'])

# Buttons
st.button('A', on_click=onClick, args='A')
st.button('B', on_click=onClick, args='B')

# Conditional display of data visualization
if selected == 'A':
    st.subheader('Data visualization for A')
    chart_data = pd.DataFrame(
        [0.31, 0.46, 0.86, 0.91, 0.96],
        columns=['A'])
    st.line_chart(chart_data)

if selected == 'B':
    st.subheader('Data visualization for B')
    chart_data = pd.DataFrame(
        [10, 26, 37, 56, 85],
        columns=['B'])
    st.line_chart(chart_data)

#lambda_func = lambda x: "<p style=\"color:rgb(255,0,0);\">{0}</p>".format(str(x)) if pd.notnull(x) else x

#df['qcheck'] = df['qcheck'].apply(lambda_func)
#print(df.head(10))

#styled = filtered_df.style.applymap(highlight_status, subset=pd.IndexSlice[:, ['Status']])
#edited_df=st.data_editor(styled,use_container_width=True,hide_index=True,disabled=["Host IP","Component","Validation_Command","Status"])

styled_df = df.style.format({'qcheck': "{:.2f}€"})

"""
jk = list()
def row_to_dict(row):
    return {col: row[col] for col in df.columns}

def dataframe_with_selections(df,mylst):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    tmp = (df_with_selections['Select'])
    print("jmc  -starts here X-",sum(tmp))
    print("jmc  -starts here Y-",str(mylst))
    for t in mylst:
        print("jmc----------> {0}".format(t))
        flag0 = (df_with_selections['idnr'] == t)
        df_with_selections.loc[t,'Select'] = False
    if sum(tmp) <= 1:
        edited_df = st.data_editor(
            df_with_selections,
            width=None,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True), "qcheck": st.column_config.Column(width="medium"), "x01_2": st.column_config.Column(width="medium"), "x01_2": st.column_config.Column(width="medium"),},
            disabled=df.columns,
        )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    selection_id = selected_rows['idnr'].dropna().unique().tolist()
    print("jmc  -starts here Z-",str(selection_id))
    if False and len(selection_id) == 1:
        jk.extend(selection_id)
        if len(jk) == 1:
            return selected_rows.drop('Select', axis=1),selection_id
            pass
    print(selected_rows)
    print(edited_df)
    print(selection_id)
    return selected_rows.drop('Select', axis=1),selection_id

selection,jk = dataframe_with_selections(df,jk)
print(selection.head(5))
print("hello jmc>",str(jk))
selection_keep = selection
st.write("Your selection: among" + str(df.shape) )
st.write(selection)

def checkOneResponse(x,y,z,row):
	st.header('Vacation Time', divider='rainbow')
	ans1 = st.text_area(
		'We are collecting suggestions for a study on the subject of vacations. How would you describe your perfect vacation?',
		x, key='ques1')
	if len(str(x))>0:
		st.write("SANS index:  :sunglasses: ** <span style='color:blue;background-color: #FFFF00;'>{0} - {1}</span> **".format(str(row['qcheck_en_Lbl']),str(row['qcheck_en_LblScore'])),unsafe_allow_html=True)
		st.write("Whether Gibberish or Profanity:  :sunglasses: ** <span style='color:blue;background-color: #FFFF00;'>{0} - {1}</span> **".format(str(row['qcheck_Flag']),str(row['qcheck_Profanity'])),unsafe_allow_html=True)

	st.header('Music Lover', divider='rainbow')
	ans2 = st.text_area(
		'Childhood memories are always special, and toys play an important role in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you??',
		y, key='ques2')
	if len(str(y))>0:
		st.write("SANS index:   :sunglasses: ** <span style='color:blue;background-color: #FFFF00;'>{0} - {1}</span> **".format(str(row['x01_2_en_Lbl']),str(row['x01_2_en_LblScore'])),unsafe_allow_html=True)
		st.write("Whether Gibberish or Profanity:  :sunglasses: ** <span style='color:blue;background-color: #FFFF00;'>{0} - {1}</span> **".format(str(row['x01_2_Flag']),str(row['x01_2_Profanity'])),unsafe_allow_html=True)

	st.header('Toy and Play Memory', divider='rainbow')
	ans3 = st.text_area(
		'Childhood memories are always special, and toys play an important role in shaping those memories. What was your favorite toy to play with as a child and why was it so special to you??',
		z, key='ques3')
	if len(str(z))>0:
		st.write("SANS index:  :sunglasses: ** <span style='color:blue;background-color: #FFFF00;background-color: #FFFF00;'>{0} - {1}</span> **".format(str(row['x01_3_en_Lbl']),str(row['x01_3_en_LblScore'])),unsafe_allow_html=True)
		st.write("Whether Gibberish or Profanity:  :sunglasses: ** <span style='color:blue;background-color: #FFFF00;'>{0} - {1}</span> **".format(str(row['x01_3_Flag']),str(row['x01_3_Profanity'])),unsafe_allow_html=True)

if len(jk)>0 and True:
	#st.title('Welcome to Survey')
	st.subheader('Welcome to Survey')

	for index, row in selection_keep.iterrows():
		if row['idnr'] == jk[0]:
			x = row['idnr']
			x = row['qcheck_en']
			y = row['x01_2_en']
			z = row['x01_3_en']
			xlst = (row['qcheck_Flag'],row['qcheck_Profanity'],row['qcheck_en_Lbl'])
			ylst = (row['x01_2_Flag'],row['x01_2_Profanity'],row['x01_2_en_Lbl'])
			zlst = (row['x01_3_Flag'],row['x01_3_Profanity'],row['x01_3_en_Lbl'])
			checkOneResponse(x,y,z,row)
	ttt = """
	genre = st.radio(
		"Select your way for survey",
		["***Single Response***", "Through a File :movie_camera:"],index =None,
		captions=["On site itself", "Upload a file."], horizontal=True)

	if genre == '***Single Response***':
		st.write('You selected Single Response.')
		checkOneResponse(x,y,z,xlst,ylst,zlst)
	elif False and genre == 'Through a File :movie_camera:':
		st.write("You  select File upload system.")
		checkFileResponse()
	else:
		pass
    """