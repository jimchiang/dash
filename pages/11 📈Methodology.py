from pathlib import Path
import streamlit as st

CHANGELOG_LINES_TO_SKIP = 6  # header lines
DISPLAY_LATEST = 1  # number or latest versions to display


def show_changelog():
    # --- PATH SETTINGS ---
    #current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    #css_file = current_dir / "styles" / "main.css"

    #st.markdown("<div style='text-align: left'>     #Semi-Automated Non-response Detection for Surveys </div>",unsafe_allow_html=True) 
    st.subheader('#Semi-Automated Non-response Detection for Surveys')

    #video_file = open('myvideo.mp4', 'rb')
    #video_bytes = video_file.read()

    st.header('Video Demo', divider='rainbow')
    video_file = open('./data/CATCH_ME_IF_YOU_CAN_Team_Archimitis.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.title('Methodology - Unbounded Data Quality Validation')
    st.header('', divider='rainbow')
    st.header('Flag Status Definition and Important Keywords Used')
    st.image('./data/Img0.PNG', caption='')
    st.image('./data/KeywordsUsed03.PNG', caption='')
    st.header('', divider='rainbow')
    st.image('./data/Img1.PNG', caption='')
    st.header('', divider='rainbow')
    st.image('./data/Img3.PNG', caption='')
    st.header('', divider='rainbow')
    st.image('./data/Img4.PNG', caption='')
    st.header('', divider='rainbow')
    st.image('./data/Img5.PNG', caption='')
    st.header('', divider='rainbow')
    st.image('./data/Img6.PNG', caption='')
    st.header('', divider='rainbow')
    ttt = """
    st.image('./data/Img7.PNG', caption='')
    st.header('', divider='rainbow')
    st.image('./data/Img8.PNG', caption='')
    st.header('', divider='rainbow')
    """
    # suppose that ChangeLog.md is located at the same folder as Streamlit app
    with open('./DevLog.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()[CHANGELOG_LINES_TO_SKIP:]

    # lines which contain version numbers
    version_numbers = [line for line in lines if line.startswith('## [')]

    # index of line, which separates displayed entries from hidden ones
    version_idx = lines.index(version_numbers[DISPLAY_LATEST])

    # write displayed entries
    st.subheader('Release Notes')
    st.markdown(''.join(lines[:version_idx]))

    # hide others with expander
    with st.expander('Previous Versions'):
        st.markdown(''.join(lines[version_idx:]))


show_changelog()