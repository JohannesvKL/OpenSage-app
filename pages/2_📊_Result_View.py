import streamlit as st
from src.common import *
from src.result_files import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt


params = page_setup()

# Make sure "selected-result-files" is in session state
if "selected-result-files" not in st.session_state:
    st.session_state["selected-result-files"] = params.get("selected-result-files", [])

# result directory path in current session state
result_dir: Path = Path(st.session_state.workspace, "result-files")

#title of page
st.title("📊 Result Viewer")

#tabs on page
tabs = ["View Results", "Result files", "Upload result files"]
tabs = st.tabs(tabs)

#with View Results tab
with tabs[0]:  

    #make sure load all example result files
    load_example_result_files()
    # take all .idXML files in current session files; .idXML is CSMs 
    session_files = [f.name for f in Path(st.session_state.workspace,"result-files").iterdir() if (f.name.endswith(".idXML") and "_XLs" in f.name)]
    # select box to select .idXML file to see the results
    selected_file = st.selectbox("choose a currently protocol file to view",session_files)

    #current workspace session path
    workspace_path = Path(st.session_state.workspace)
    #tabs on page to show different results
    tabs_ = st.tabs(["CSMs Table", "PRTs Table", "PRTs Summary", "Crosslink efficiency", "Precursor adducts summary"])

    ## selected .idXML file
    if selected_file:
        #with CSMs Table
        with tabs_[0]:
            #st.write("CSMs Table")
            #take all CSMs as dataframe
            CSM_= readAndProcessIdXML(workspace_path / "result-files" /f"{selected_file}")
            #show and download button of all CSMs
            show_table(CSM_, os.path.splitext(selected_file)[0])

        #with PRTs Table
        with tabs_[1]:
            # Extracting components from the input filename to show the result of corresponding proteins file
            parts = selected_file.split('_')
            prefix = '_'.join(parts[:-2])  # Joining all parts except the last two
            perc_value = parts[-2]  # Extracting the same FDR file

            # Creating the new filename as same as selected idXML file
            new_filename = f"{prefix}_proteins{perc_value}_XLs.tsv"

            #path of corresponding protein file
            protein_path = workspace_path / "result-files" /f"{new_filename}"

            #if file exist
            if protein_path.exists():
                #st.write("PRTs Table")
                #take list of dataframs different results 
                PRTs_section= read_protein_table(protein_path)
                #from 1st dataframe PRTs_List; shown on page with download button
                show_table(PRTs_section[0], f"{os.path.splitext(new_filename)[0]}_PRTS_list")
            
                #with PRTs Summary
                with tabs_[2]:       
                        #st.write("Protein summary")
                        #from wnd dataframe PRTs_summary; shown on page with download button
                        show_table(PRTs_section[2], f"{os.path.splitext(new_filename)[0]}_PRTS_summary")
                
                #with Crosslink efficiency
                with tabs_[3]:
                        #st.write("Crosslink efficiency (AA freq. / AA freq. in all CSMs)")
                        #from 3rd dataframe PRTs_efficiency
                        prts_efficiency = PRTs_section[3]

                        #create crosslink efficiency plot
                        efficiency_fig = go.Figure(data=[go.Bar(x=prts_efficiency["AA"], y=prts_efficiency["Crosslink efficiency"], marker_color='rgb(55, 83, 109)')])
                        #update the layout of plot
                        efficiency_fig.update_layout(
                            #title='Crosslink efficiency',
                            xaxis_title='Amino acids',
                            yaxis_title='Crosslink efficiency (AA freq. / AA freq. in all CSMs)',
                            font=dict(family='Arial', size=12, color='rgb(0,0,0)'),
                            paper_bgcolor='rgb(255, 255, 255)',
                            plot_bgcolor='rgb(255, 255, 255)'
                        )
                        #show figure, with download
                        show_fig(efficiency_fig, f"{os.path.splitext(new_filename)[0]}_efficiency")
                        #show button of download table from where above plot came
                        download_table(prts_efficiency, f"{os.path.splitext(new_filename)[0]}_efficiency")

                #with Precursor adducts summary
                with tabs_[4]:
                            #st.write("Precursor adduct summary")
                            #show_table(PRTs_section[4])
                            #from 4th dataframe mass_adducts efficiency
                            precursor_summary = PRTs_section[4]

                            #create mass adducts efficiency plot
                            adducts_fig = go.Figure(data=[go.Pie(
                                labels=precursor_summary["Precursor adduct:"],
                                values=precursor_summary["PSMs(%)"],
                                hoverinfo='label+percent',
                                textinfo='label+percent',
                                #title='Percentage of PSMs for Each Index Precursor'
                            )])

                            #show figure, with download
                            show_fig(adducts_fig , f"{os.path.splitext(new_filename)[0]}_adduct_summary")
                            #show button of download table from where above plot came
                            download_table(precursor_summary, f"{os.path.splitext(new_filename)[0]}_adduct_summary")

            #if the same protein file not available
            else:
                st.warning(f"{protein_path.name} file not exist in current workspace")

    _ ="""
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
                    download_table(prts_efficiency, f"{os.path.splitext(new_filename)[0]}_efficiency")

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
                    download_table(precursor_summary, f"{os.path.splitext(new_filename)[0]}_adduct_summary")

            else:
                st.warning(f"{protein_path.name} file not exist in current workspace")
            """
#with "Result files" 
with tabs[1]:
    #make sure to load all results example files
    load_example_result_files()

    if any(Path(result_dir).iterdir()):
        v_space(2)
        #  all result files currently in workspace
        df = pd.DataFrame(
            {"file name": [f.name for f in Path(result_dir).iterdir()]})
        st.markdown("##### result files in current workspace:")

        show_table(df)
        v_space(1)
        # Remove files
        copy_local_result_files_from_directory(result_dir)
        with st.expander("🗑️ Remove result files"):
            #take all example result files name
            list_result_examples = list_result_example_files()
            #take all session result files
            session_files = [f.name for f in sorted(result_dir.iterdir())]
            #filter out the example result files
            Final_list = [item for item in session_files if item not in list_result_examples]

            #multiselect for result files selection
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
            #multiselect for result files selection
            to_download = st.multiselect("select result files for download",
                                    options=[f.name for f in sorted(result_dir.iterdir())])
            
            c1, c2 = st.columns(2)
            if c2.button("Download **selected**", type="primary", disabled=not any(to_download)):
                #download selected files will display download hyperlink
                download_selected_result_files(to_download, "selected_result_files")
                #st.experimental_rerun()

            ### afraid if there are many files in workspace? should we removed this option?
            if c1.button("⚠️ Download **all**", disabled=not any(result_dir.iterdir())):
                #create the zip content of all result files in workspace
                b64_zip_content = create_zip_and_get_base64_()
                #display the download hyperlink
                href = f'<a href="data:application/zip;base64,{b64_zip_content}" download="all_result_files.zip">Download All Files</a>'
                st.markdown(href, unsafe_allow_html=True)

#with "Upload result files"
with tabs[2]:
    #form to upload file
    with st.form("Upload .idXML and .tsv", clear_on_submit=True):
        files = st.file_uploader(
            "NuXL result files", accept_multiple_files=(st.session_state.location == "local"), type=['.idXML', '.tsv'], help="Input file (Valid formats: 'idXML', 'tsv') ")
        cols = st.columns(3)
        if cols[1].form_submit_button("Add files to workspace", type="primary"):
            save_uploaded_result(files)
            st.experimental_rerun()

# At the end of each page, always save parameters (including any changes via widgets with key)
save_params(params)
