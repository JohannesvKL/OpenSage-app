import streamlit as st
from src.common import *
from src.result_files import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt


params = page_setup()

if "selected-result-files" not in st.session_state:
    st.session_state["selected-result-files"] = params.get("selected-result-files", [])

result_dir: Path = Path(st.session_state.workspace, "result-files")

st.title("📊 Result Viewer")
tabs = ["View Results", "Result files", "Upload result files"]

tabs = st.tabs(tabs)

#if st.session_state.location == "local":
#    tabs.append("Files from local folder")

with tabs[0]:

    # first try (just show the file if both proteins and idXML table there)
    #load_example_result_files()
    #session_files = [f.name for f in Path(st.session_state.workspace,"result-files").iterdir()]
    #st.write("all files in result_folder: ", session_files)
    #fdr_list = [string for string in session_files if "0.0100_XLs" in string]
    
    #check if perc base files results
    #perc_exec = any("_perc_" in string for string in session_file)

    #Take the protocol results which contain both PSMs/PRTs file available in workspace
    #unique_protocol_list = set([string.replace("_proteins0.0100_XLs.tsv", '').replace("_0.0100_XLs.idXML", '') for string in fdr_list])

    #final_protocols = [i for i in unique_protocol_list if i+"_proteins0.0100_XLs.tsv" in fdr_list and i+"_0.0100_XLs.idXML" in fdr_list]
    #st.write("contain both protein PSMs", final_protocols)s

    #selected_file = st.selectbox("choose a currently protocol file to view",final_protocols)

    #workspace_path = Path(st.session_state.workspace)
    

    load_example_result_files()
    session_files = [f.name for f in Path(st.session_state.workspace,"result-files").iterdir() if (f.name.endswith(".idXML") and "_XLs" in f.name)]
    #st.write("all files in result_folder: ", session_files)
    selected_file = st.selectbox("choose a currently protocol file to view",session_files)

    workspace_path = Path(st.session_state.workspace)

    tabs_ = st.tabs(["CSMs", "Proteins"])
    if selected_file:
        with tabs_[0]:
            st.write("CSMs Table")
            #st.write("Path of selected file: ", workspace_path / "result-files" /f"{selected_file}_0.0100_XLs.idXML")
            CSM_= readAndProcessIdXML(workspace_path / "result-files" /f"{selected_file}")
            show_table(CSM_, os.path.splitext(selected_file)[0])

        with tabs_[1]:
            # Extracting components from the input filename
            parts = selected_file.split('_')
            prefix = '_'.join(parts[:-2])  # Joining all parts except the last two
            perc_value = parts[-2]  # Extracting the percentage value

            # Creating the new filename
            new_filename = f"{prefix}_proteins{perc_value}_XLs.tsv"

            #st.write("Path of selected file: ", workspace_path / "result-files" /f"{selected_file}_proteins0.0100_XLs.tsv")
            protein_path = workspace_path / "result-files" /f"{new_filename}"

            if protein_path.exists():
                st.write("PRTs Table")
                PRTs_section= read_protein_table(protein_path)
                show_table(PRTs_section[0], f"{os.path.splitext(new_filename)[0]}_PRTS_list")

                st.write("Protein summary")
                show_table(PRTs_section[2], f"{os.path.splitext(new_filename)[0]}_PRTS_summary")

                col1, col2 = st.columns(2)

                # Display the plots in the columns
                with col1:
                    st.write("Crosslink efficiency (AA freq. / AA freq. in all CSMs)")
                    #show_table(PRTs_section[3])

                    prts_efficiency = PRTs_section[3]
        
                    efficiency_fig = go.Figure(data=[go.Bar(x=prts_efficiency["AA"], y=prts_efficiency["Crosslink efficiency"], marker_color='rgb(55, 83, 109)')])

                    efficiency_fig.update_layout(
                        #title='Crosslink efficiency',
                        xaxis_title='Amino acids',
                        yaxis_title='Crosslink efficiency',
                        font=dict(family='Arial', size=12, color='rgb(0,0,0)'),
                        paper_bgcolor='rgb(255, 255, 255)',
                        plot_bgcolor='rgb(255, 255, 255)'
                    )

                    show_fig(efficiency_fig, f"{os.path.splitext(new_filename)[0]}_efficiency")

                with col2:
                    st.write("Precursor adduct summary")
                    #show_table(PRTs_section[4])

                    #print(PRTs_section[4])
                    precursor_summary = PRTs_section[4]

                    adducts_fig = go.Figure(data=[go.Pie(
                        labels=precursor_summary["Precursor adduct:"],
                        values=precursor_summary["PSMs(%)"],
                        hoverinfo='label+percent',
                        textinfo='label+percent',
                        #title='Percentage of PSMs for Each Index Precursor'
                    )])

                    show_fig(adducts_fig , f"{os.path.splitext(new_filename)[0]}_adduct_summary")

            else:
                st.warning(f"{protein_path.name} file not exist in current workspace")

with tabs[1]:
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
            ### remove selected files from workspace
            if c2.button("Remove **selected**", type="primary", disabled=not any(to_remove)):
                remove_selected_result_files(to_remove)
                st.experimental_rerun() 

            ### remove all files from workspace
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

            ### afraid if there are many files in workspace? should we removed this option?
            if c1.button("⚠️ Download **all**", disabled=not any(result_dir.iterdir())):
                #download from directory
                b64_zip_content = create_zip_and_get_base64_()
                href = f'<a href="data:application/zip;base64,{b64_zip_content}" download="all_result_files.zip">Download All Files</a>'
                st.markdown(href, unsafe_allow_html=True)

with tabs[2]:
    with st.form("Upload .idXML and .tsv", clear_on_submit=True):
        files = st.file_uploader(
            "NuXL result files", accept_multiple_files=(st.session_state.location == "local"), type=['.idXML', '.tsv'], help="Input file (Valid formats: 'idXML', 'tsv') ")
        cols = st.columns(3)
        if cols[1].form_submit_button("Add files to workspace", type="primary"):
            save_uploaded_result(files)

# At the end of each page, always save parameters (including any changes via widgets with key)
save_params(params)
