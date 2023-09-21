import streamlit as st

from src.common import *
from src.captcha_ import *

params = page_setup(page="main")

def main():
    st.markdown(
        """# OpenNuXL"""
    )
    st.image("assets/NuXL_image.png")
    #In docker, OpenMS-app (executable) can be downloadable from github
    if Path("OpenMS-App.zip").exists():
        st.markdown("## Installation")
        with open("OpenMS-App.zip", "rb") as file:
            st.download_button(
                    label="Download for Windows",
                    data=file,
                    file_name="OpenMS-App.zip",
                    mime="archive/zip",
                )
    save_params(params) 

if "local" in sys.argv:
    main()

else:

    # WORK LIKE MULTIPAGE APP     
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        #delete pages
        delete_page("app", "File_Upload")
        delete_page("app", "Analyze")
        delete_page("app", "Result_View")
        #apply captcha
        captcha_control()
    else:
        #run main
        main()
        #add all pages back
        add_page("app", "File_Upload")
        add_page("app", "Analyze")
        add_page("app", "Result_View")