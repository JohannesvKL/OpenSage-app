import streamlit as st

from src.common import *
from src.captcha_ import *

params = page_setup(page="main")

def main():
    st.markdown(
        """
        # OpenMS SageAdapter App
        ### SageAdapter: Integrating the proteomics search engine into the OpenMS framework. 
        Welcome to the OpenMS SageAdapter App, a web application for the Sage search engine, built using [OpenMS](https://openms.de/) and [pyOpenMS](https://pyopenms.readthedocs.io/en/latest/).

        """
    )
    #st.image("assets/NuXL_image.png")
    st.markdown(
        """
        In this web-app the Sage search engine is presented in a simple and easy-to-use graphical interface. Sage is a fast and reliable proteomics search engine for the anaylsis of MS data, for more see: (link to Sage here). 
        This tool allows for annotation of various ions, fast discovery of PTMs, and FDR-filtering of results! 
        """
    )
    #In docker, OpenMS-app (executable) can be downloadable from github
    #TODO: make zip possible 
    if Path("OpenMS-NuXL.zip").exists():
        st.markdown(
            """
            ## Installation

            ### Download for Windows

            Simply download and extract the zip file. The folder contains an executable run_app file. No need to install anything.
            """)
        with open("OpenMS-NuXL.zip", "rb") as file:
            st.download_button(
                        label="Download for Windows",
                        data=file,
                        file_name="OpenMS-NuXL.zip",
                        mime="archive/zip",
                        type="primary"
                    )
    st.markdown("""
        ## Quickstart 

        You can start right away analyzing your data by following the steps below:

        ### 1. Create a workspace
        On the left side of this page a workspace  defined where all your data including uploaded files will be stored. In the web app, you can share your results via the unique workspace ID. Be careful with sensitive data, anyone with access to this ID can view your data.

        ⚠️ Note: In the web app, all users with a unique workspace ID have the same rights.
                
        ### 2. 📁 Upload your files
        Upload `mzML` and `fasta` files via the **File Upload** tab. The data will be stored in your workspace. With the web app you can upload only one file at a time.
        Locally there is no limit in files. However, it is recommended to upload large number of files by specifying the path to a directory containing the files.

        Your uploaded files will be shown on the same **File Upload** page in  **mzML files** and **Fasta files** tabs. Also you can remove the files from workspace.

        ### 3. ⚙️ Analyze your uploaded data

        Select the `mzML` and `fasta` files for analysis, configure user settings, and start the analysis using the **Run-analysis** button.
        You can terminate the analysis immediately using the **Terminate/Clear** button and you can review the search engine log on the page.
        Once the analysis completed successfully, the output table will be displayed on the page, along with downloadable links for crosslink identification files.

        #### 4. 📊 View your results
        Here, you can visualize and explore the output of the search engine. All crosslink output files in the workspace are available on the **View Results** tab.
        After selecting any file, you can view the `CSMs Table`, `PRTs Table`, `PRTs Summary`, `Crosslink efficiency` and `Precursor adducts summary`.

        Note: Every table and plot can be downloaded, as indicated in the side-bar under ⚙️ Settings.

        #### How to accessing previously analysed results?
        Under the **Result Files** tab, you can manage your results. You can `remove` or `download` files from the output files list.

        #### How to upload result files (e.g., from external sources/collaborator) for manual inspection and visualization?
        At **Upload result files** tab, user can  `upload` the results files and can visualize in **View Results** tab.
        In the web app, collaborators can visualize files by sharing a unique workspace ID.
        
        #### Contact
        For any inquiries or assistance, please feel free to reach out to us.  
        [![Discord Shield](https://img.shields.io/discord/832282841836159006?style=flat-square&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=Discord)](https://discord.gg/4TAGhqJ7s5) [![Gitter](https://img.shields.io/static/v1?style=flat-square&message=on%20Gitter&color=ED1965&logo=Gitter&logoColor=FFFFFF&label=Chat)](https://gitter.im/OpenMS/OpenMS?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

    """)
                
            
    save_params(params) 

if "local" in sys.argv:
    params["controllo"] = True
    st.session_state["controllo"] = True
    main()

# If not in local mode, assume it's hosted/online mode
else:
    # If captcha control is not in session state or set to False
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        # hide app pages as long as captcha not solved
        #delete_all_pages("app")

        # Apply captcha control to verify the user
        captcha_control()

    else:     
        # Run the main function
        main()

        # Restore all pages (assuming "app" is the main page)
        #restore_all_pages("app")
        