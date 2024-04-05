# import the streamlit library
import streamlit as st
#import Archimitis_Dashboard

#cnx = sqlite3.connect('../OutputData/hackfest24.sqlite')

def get_code():
    ttt="""
import datetime, pandas, os, time, glob, sys, re, platform, warnings
from googletrans import Translator, constants
from nostril import nonsense
import xlrd
import openpyxl
from pprint import pprint
from nltk.corpus import words
from nltk.metrics import edit_distance
import string
import nltk
import time
import googletrans as gt
from profanity_check import predict, predict_prob
from transformers import pipeline

def main():
    print('system info-----------------------------------------------------------------------------------')
    warnings.simplefilter('ignore')
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    print("pandas version: {0} & googletrans: {1} & enchant: {2}".format(pandas.__version__,gt.__version__,"enchant"))
    print("python system: {0}".format(sys.version))
    print("[{0}],[{1}],[{2}],[{3}],[{4}],[{5}],[{6}]".format("system log:",platform.python_version(), platform.processor(), platform.system(),platform.node(), platform.machine(),platform.python_branch()))
    print('system info-----------------------------------------------------------------------------------')
    Xlsx_Output = pandas.ExcelWriter('./OutputData/hackfest_20231127_Categozied_HF_M31_T200.xlsx', engine='xlsxwriter')
    for infile in glob.glob("./InputData/hackfest_20231127_T200.xlsx"): print(infile,"\t")
    df = load_xlsx_sheet(infile,'Data')
    df = search_keyword(df)
    print(df.shape)
    t2 = pandas.DataFrame(df['Mrg'].value_counts(normalize=False, sort=True, ascending=False, bins=None,dropna=False))
    t2.reset_index(inplace=True)
    t2.columns = ['Mrg','Frequency']
    df = df.merge(t2, left_on=['Mrg'], right_on=['Mrg'], how='left', suffixes=('', '_copy_paste_suspect'), sort=False)

    flag0 = ( df[ 'Frequency' ] > 1 )
    df.loc[ flag0 , 'dups_rwise'] = True

    df.to_excel(Xlsx_Output, sheet_name='df', index_label='keyword', startcol=0)
    Xlsx_Output = freq_all_cols_to_xlsx(df,Xlsx_Output,'Freq')


    Xlsx_Output.close()

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

def translateToEnglish(item):
    detect = Translator()
    dec_lan = detect.detect(item)
    if dec_lan.lang == "en":
        return 'TRUE'
    else:
        # print(f'Detection Lngauge - {dec_lan.lang} and conf - {dec_lan.confidence}')
        translation = detect.translate(item)
        # print(f'{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})')
        return translation.text
        # print(f'{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})')


def testEnglishLanguageWord(response_words):
    print(f'responsewords - {response_words}')
    print('*******************************************************************')
    d = enchant.Dict("en_US")
    word_found = 0
    word_not_found = 0
    if response_words == '':
        return "Gibberish"
    else:
        response_words = remove_special_characters(response_words)
        res = response_words.split()
        for w in res:
            if w in words.words():
                #print(f'Word found - {w}')
                word_found = word_found + 1
            else:
                print(f'Word Not found - {w}')
                word_not_found = word_not_found + 1
                if len(w) < 7:
                    pass
                else:
                    if nonsense(w):
                        print(f'Word is really Nonsense found - {w}')
                        word_not_found = word_not_found + 1
                    else:
                        word_found = word_found + 1
                if d.check(w):
                    word_found = word_found + 1
                else:
                    print(f'Word is really Not in dict - {w}')
                    word_not_found = word_not_found + 1
        perc = ((word_found * 100) / (word_found + word_not_found))
        print('*******************************************************************')
        if perc >= 50:
            print(f'English by {perc} %')
            return 'English'
        else:
            print(f'Gibberish by {perc} %')
            return 'Gibberish'

def checkALlSpecialChar(text):
    correct = string.ascii_letters + string.digits
    status = True
    if text is not None:
        if isinstance(text, int):
            pass
        else:
            for char in text:
                if char in correct:
                    status = False
    return status

def check_Bad_word(text):
    if predict(text):
        # Cuss Word
        return 'Bad Language'
    else:
        # Normal
        return 'Fine'

def check_other_language(text):
    detect = Translator()
    dec_lan = detect.detect(text)
    if dec_lan.lang == "en":
        return 'English'
    else:
        return dec_lan.lang

def load_xlsx_sheet(file,wsheet1):
	log( "loading excel worksheets wsheet1)" )
	#web_kwrd1 = pandas.read_excel( file, sheet_name = wsheet1,skiprows=0,header=1)
	web_kwrd1 = pandas.read_excel( file, sheet_name = wsheet1)
	return web_kwrd1

def value_counts_to_df(df, col):
    df = pandas.DataFrame(df[col].value_counts(normalize=False, sort=True, ascending=False, bins=None,dropna=False))
    df.reset_index(inplace=True)
    df.columns = [col,'frequency']
    return df

def freq_all_cols_to_xlsx(df, XL, sh_name):
    t2 = df.dtypes.to_frame('dtypes').reset_index()
    t2.columns = ['col','dtype']
    t2.to_excel(XL, sheet_name=sh_name, index_label='indx', startcol=0)
    XL.sheets[ sh_name ].set_column(1, 2, 20)
    t3 = pandas.DataFrame(df.nunique(axis = 0, dropna = True))
    t3.to_excel(XL, sheet_name=sh_name, index_label='indx', startcol=4)

    for i, col in enumerate(df.columns, start=0):
        print("col_index:\t{0}\tTo Excel col:\t{1}\tCol Name:\t{2}\tCol Data Type:\t{3}".format(i,((i*3)+1),col,df[col].dtype))
        t2 = pandas.DataFrame(df[col].value_counts(normalize=False, sort=True, ascending=False, bins=None,dropna=False))
        if True:
            t2.reset_index(inplace=True)
            t2.columns = [col,'frequency']
            t2.to_excel(XL, sheet_name=sh_name, startcol=((i+1)*4+4))
            XL.sheets[ sh_name ].set_column(((i+1)*4+4)+1,((i+1)*4+4) + 2 , 20)
    return XL

def search_keyword( df ):
    world_lang      = ['en','es','fr','de','it','ja','ko','zh-CN','zh','zh-TW','ru','pt','nl','sv','ar','tr','el','pl','da','no','fi']
    world_lang_ne   = ['es','fr','de','it','ja','ko','zh-CN','zh','zh-TW','ru','pt','nl','sv','ar','tr','el','pl','da','no','fi']
    world_lang_good = ['en','es','fr','de','it']
    translator = Translator()
    print(df.columns)
    #Xlsx_Output  ['idnr', 'qcheck', 'x01_2', 'x01_3']
    log( "Search:\t working with verbatim" )
    pipe = pipeline("text-classification", "NCHS/SANDS")
    if True:
        df[ 'qcheck_en' ] = df[ 'qcheck' ]
        df[ 'x01_2_en' ]  = df[ 'x01_2' ]
        df[ 'x01_3_en' ]  = df[ 'x01_3' ]
        df[ 'qcheck_lang' ] = None
        df[ 'x01_2_lang' ] = None
        df[ 'x01_3_lang' ] = None
        df[ 'qcheck_Flag' ] = False
        df[ 'x01_2_Flag' ] = False
        df[ 'x01_3_Flag' ] = False
        df[ 'Flag' ] = False
        df[ 'Quality_Metric' ] = 0
        df[ 'Lang_Flag' ] = False
        df[ 'Lang_Combined' ] = None
        df[ 'qcheck_Profanity' ] = None
        df[ 'x01_2_Profanity' ] = None
        df[ 'x01_3_Profanity' ] = None
        df[ 'qcheck_en_Lbl'] = None
        df[ 'qcheck_en_LblScore'] = None
        df[ 'x01_2_en_Lbl'] = None
        df[ 'x01_2_en_LblScore'] = None
        df[ 'x01_3_en_Lbl'] = None
        df[ 'x01_3_en_LblScore'] = None
        df[ 'Mrg'] = None
        df[ 'dups'] = False
        df[ 'dups_rwise'] = False

        for index, row in df.iterrows():
            print( "Processing\t" + str(index) + ' of ' +  str(len(df.index)) + '\t[pid: ' + str(os.getpid()) + ']\t' + str(row['qcheck_en']) + '\t' + str(row['x01_2_en']) + '\t' + str(row['x01_3_en']) + '\t')
            
            my_lst = []
            txt      = str(row['qcheck']).strip()
            if not pandas.isnull(row['qcheck']) and len(txt) > 0:
                my_lst.append(txt)
                process_str(df,index,txt,'qcheck','qcheck_lang','qcheck_en','qcheck_Flag',translator,world_lang,world_lang_ne,world_lang_good)

            txt      = str(row['x01_2']).strip()
            if not pandas.isnull(row['x01_2']) and len(txt) > 0:
                my_lst.append(txt)
                process_str(df,index,txt,'x01_2','x01_2_lang','x01_2_en','x01_2_Flag',translator,world_lang,world_lang_ne,world_lang_good)
            
            txt      = str(row['x01_3']).strip()
            if not pandas.isnull(row['x01_3']) and len(txt) > 0:
                my_lst.append(txt)
                process_str(df,index,txt,'x01_3','x01_3_lang','x01_3_en','x01_3_Flag',translator,world_lang,world_lang_ne,world_lang_good)
            if len(my_lst) > 0:
                df.loc[index,'Mrg'] = ''.join(my_lst)
                if len(my_lst) == 2 and edit_distance(my_lst[0], my_lst[1]) <= 1:
                    df.loc[ index,'dups' ] = True    
                if len(my_lst) == 3 and ( edit_distance(my_lst[0], my_lst[1]) <= 1 or edit_distance(my_lst[0], my_lst[2]) <=1 or edit_distance(my_lst[1], my_lst[2]) <= 1):
                    df.loc[ index,'dups' ] = True    
            if  len(my_lst) > 1 and (len(my_lst) > len(set(my_lst))):
                df.loc[ index,'dups' ] = True
    #df['Flag'] = df[['qcheck_Flag','x01_2_Flag','x01_3_Flag']].any(axis=1)
    #df['Mrg'] = df['qcheck_en'].map(str) + df['x01_2_en'].map(str) + df['x01_3_en'].map(str)
    df.loc[ ( ( df['qcheck_Flag'] ) | ( df['x01_2_Flag'] ) | ( df['x01_3_Flag'] ) ),'Flag' ] = True

    return df

def process_str(df,indx,txt,col,col_lang,col_en,col_Flag,translator,world_lang,world_lang_ne,world_lang_good):
	pipe = pipeline("text-classification", "NCHS/SANDS")
	if (len(str(txt).strip()) == 0 ) or not re.search('[a-zA-Z]', str(txt)):
		df.loc[indx, col_Flag] = True
		df.loc[indx, 'Quality_Metric' ] = 2
	else:
		while True:
			try:
				detected_language = translator.detect(txt)
				translated        = translator.translate(txt, dest='en')
			except:
				continue
			else:
				break
		if str(detected_language.lang) in world_lang:
			df.loc[indx, col_lang] = detected_language.lang
		else:
			df.loc[indx, col_lang] = 'en'
		if str(detected_language.lang) in world_lang_ne:
			txt = translated.text
			df.loc[indx, col_en] = txt
		if str(detected_language.lang) not in world_lang_good:
			df.loc[indx, 'Lang_Flag' ] = True
			#df.loc[indx, 'Lang_Combined'] = col + '_' + str(df.loc[indx, 'Lang_Combined']) + '_' + str(detected_language.lang) + '_' + txt + '_' + str(world_lang_good) + '_'
			df.loc[indx, 'Lang_Combined'] = col + '_' + str(detected_language.lang) + '_'
		try:
			df.loc[indx, col+'_Profanity'] = predict_prob( [txt] )[0]
			df.loc[indx, col_Flag] = nonsense(txt)
			t2 = pipe(txt)[0]
			print(t2)
			lbl   = t2['label']
			score = t2['score']
			df.loc[indx, col_en+'_Lbl'] = lbl
			df.loc[indx, col_en+'_LblScore'] = score
		except:
			pass

def log( msg ):
	print( datetime.datetime.now().isoformat() + "  " + msg )

if __name__ == "__main__":
    main()
    """
    return ttt

if True:
    #settings.init()
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.header('HackFest Team ***Archimitis*** Presents - #1 CATCH ME IF YOU CAN')
        st.subheader('Model creation for Automizing our defense against deceptive data')
        st.header('', divider='rainbow')

        st.write("Singhal, Madhu (GfK)")
        st.write("Chiang, Jim (GfK)")
        st.write("Beniwal, Aakash (NIQ)")
        st.write("GHOSH, AYAN (NIQ)")
        st.write("Dhandore, Priyanka (NIQ)")
        st.header('', divider='rainbow')

        st.subheader('Source Code')
        st.code(get_code(),language="python")        


    with col2:
        st.image('./data/logo.png', width=160)
