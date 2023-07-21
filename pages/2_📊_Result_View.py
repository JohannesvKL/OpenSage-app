import streamlit as st

from src.common import *

from src.result_files import *

params = page_setup()

if "selected-result-files" not in st.session_state:
    st.session_state["selected-result-files"] = params.get("selected-result-files", [])

st.title("📊 Result Viewer")
tabs = ["Result files", "View files"]

tabs = st.tabs(tabs)

if st.session_state.location == "local":
    tabs.append("Files from local folder")

with tabs[0]:
    load_example_result_files()

    if any(Path(result_dir).iterdir()):
        v_space(2)
        # Display all result files currently in workspace
        df = pd.DataFrame(
            {"file name": [f.name for f in Path(result_dir).iterdir()]})
        st.markdown("##### result files in current workspace:")
        show_table(df)
        v_space(1)
        # Remove files
        copy_local_result_files_from_directory(result_dir)
        with st.expander("🗑️ Remove result files"):
            list_result_examples = list_result_example_files()
            session_files = [f.name for f in sorted(result_dir.iterdir())]
            Final_list = [item for item in session_files if item not in list_result_examples]

            to_remove = st.multiselect("select result files", options=Final_list)

            c1, c2 = st.columns(2)
            if c2.button("Remove **selected**", type="primary", disabled=not any(to_remove)):
                remove_selected_result_files(to_remove)
                st.experimental_rerun() 

            if c1.button("⚠️ Remove **all**", disabled=not any(result_dir.iterdir())):
                remove_all_result_files() 
                st.experimental_rerun() 


        with st.expander("⬇️ Download result files"):

            to_download = st.multiselect("select result files for download",
                                    options=[f.name for f in sorted(result_dir.iterdir())])
            
            c1, c2 = st.columns(2)
            if c2.button("Download **selected**", type="primary", disabled=not any(to_download)):
                download_selected_result_files(to_download, "selected_result_files")
                #st.experimental_rerun()

            if c1.button("⚠️ Download **all**", disabled=not any(result_dir.iterdir())):
                b64_zip_content = create_zip_and_get_base64()
                href = f'<a href="data:application/zip;base64,{b64_zip_content}" download="all_result_files.zip">Download All Files</a>'
                st.markdown(href, unsafe_allow_html=True)

with tabs[1]:

    session_file = [f.name for f in Path(st.session_state.workspace,"result-files").iterdir()]
    #st.write("all files in result_folder: ", session_files)
    
    fdr_list = [string for string in session_files if "0.0100_XLs" in string]
    #st.write("1% FDR files: ",fdr_list)

    unique_protocol_list = set([string.replace("_proteins0.0100_XLs.tsv", '').replace("_0.0100_XLs.idXML", '') for string in fdr_list])
    #st.write("Unique_protocol",unique_protocol_list)

    final_protocols = [i for i in unique_protocol_list if i+"_proteins0.0100_XLs.tsv" in fdr_list and i+"_0.0100_XLs.idXML" in fdr_list]
    #st.write("contain both protein PSMs", final_protocols)

    selected_file = st.selectbox(
    "choose a currently protocol file to view",
    final_protocols)

    if selected_file:
        tabs = st.sidebar.tabs(["CSMs", "Proteins"])
        with tabs[0]:
            csm_container = st.container()
            with csm_container:
                st.write("Table of 1% FDR CSMs")

        with tabs[1]:
            protein_container = st.container()
            with protein_container:
                st.write("Table of PRTs at 1% CSM FDR")


# At the end of each page, always save parameters (including any changes via widgets with key)
save_params(params)
