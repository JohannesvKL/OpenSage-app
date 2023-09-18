import streamlit as st
from captcha.image import ImageCaptcha
import random, string

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
    # define the costant
    length_captcha = 5
    width = 400
    height = 180

    # define the function for the captcha control
    def captcha_control():
        #control if the captcha is correct
        if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
            st.title("Makesure you are not a robot🤖")
            
            # define the session state for control if the captcha is correct
            st.session_state['controllo'] = False
            col1, col2 = st.columns(2)
            
            # define the session state for the captcha text because it doesn't change during refreshes 
            if 'Captcha' not in st.session_state:
                    st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))

            #setup the captcha widget
            image = ImageCaptcha(width=width, height=height)
            data = image.generate(st.session_state['Captcha'])
            col1.image(data)
            capta2_text = col2.text_area('Enter captcha text', height=10, placeholder="captcha text")

            col3, col4 = st.columns(2)
            with col4:
                if st.button("Verify the code"):
                    capta2_text = capta2_text.replace(" ", "")
                    # if the captcha is correct, the controllo session state is set to True
                    if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                        del st.session_state['Captcha']
                        col1.empty()
                        col2.empty()
                        st.session_state['controllo'] = True
                        st.experimental_rerun()
                    else:
                        # if the captcha is wrong, the controllo session state is set to False and the captcha is regenerated
                        st.error("🚨 Captcha is wrong")
                        del st.session_state['Captcha']
                        del st.session_state['controllo']
                        st.experimental_rerun()
                else:
                    #wait for the button click
                    st.stop()

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