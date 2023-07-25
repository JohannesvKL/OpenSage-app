from pathlib import Path

import streamlit as st
import pandas as pd

from src.common import *
from src.fileupload import *

params = page_setup()

# Make sure "selected-mzML-files" is in session state
if "selected-mzML-files" not in st.session_state:
    st.session_state["selected-mzML-files"] = params["selected-mzML-files"]

if "selected-fasta-files" not in st.session_state:
    st.session_state["selected-fasta-files"] = params.get("selected-fasta-files", [])

st.title("📂 File Upload")

tabs = ["mzML files", "Fasta files"]
if st.session_state.location == "local":
    tabs.append("Files from local folder")

tabs = st.tabs(tabs)

with tabs[0]:
    with st.form("mzML-upload", clear_on_submit=True):
        files = st.file_uploader(
            "mzML files", accept_multiple_files=(st.session_state.location == "local"), type=['.mzML', '.raw'], help="Input file (Valid formats: 'mzML', 'raw') ")
        cols = st.columns(3)
        if cols[1].form_submit_button("Add files to workspace", type="primary"):
            save_uploaded_mzML(files)
            #load_example_mzML_files()

    
    load_example_mzML_files()
        
    # Local file upload option: via directory path
    if st.session_state.location == "local":
        with tabs[2]:
            # with st.form("local-file-upload"):
            st.markdown("Short information text about the example data.")
            local_mzML_dir = st.text_input(
                "path to folder with mzML files")
            # raw string for file paths
            local_mzML_dir = r"{}".format(local_mzML_dir)
            cols = st.columns(3)
            if cols[1].button("Copy files to workspace", type="primary", disabled=(local_mzML_dir == "")):
                copy_local_mzML_files_from_directory(local_mzML_dir)

    if any(Path(mzML_dir).iterdir()):
        v_space(2)
        # Display all mzML files currently in workspace
        file_names_ = [f.name for f in Path(mzML_dir).iterdir()]
        df = pd.DataFrame(
            {"file name": [item for item in file_names_  if not item.endswith(".csv")]})
        st.markdown("##### mzML files in current workspace:")
        show_table(df)
        v_space(1)
        # Remove files
        with st.expander("🗑️ Remove uploaded mzML files"):
            to_remove = st.multiselect("select mzML files",
                                    options=[f.stem for f in sorted(mzML_dir.iterdir())])
            c1, c2 = st.columns(2)
            if c2.button("Remove **selected**", type="primary", disabled=not any(to_remove)):
                remove_selected_mzML_files(to_remove)
                st.experimental_rerun()

            if c1.button("⚠️ Remove **all**", disabled=not any(mzML_dir.iterdir())):
                remove_all_mzML_files()
                st.experimental_rerun()
                #load_example_mzML_files()

with tabs[1]:
    with st.form("fasta-upload", clear_on_submit=True):
        file = st.file_uploader("fasta file", type=['.fasta'], help = "The protein database used for identification. (valid formats: 'fasta')")
        cols = st.columns(3)
        if cols[1].form_submit_button("Add fasta to workspace", type="primary"):
            save_uploaded_fasta(file)

    load_example_fasta_files()
    # Local file upload option: via directory path
    if st.session_state.location == "local":
        with tabs[2]:
            # with st.form("local-file-upload"):
            local_fasta_dir = st.text_input(
                "path to folder with fasta files")
            # raw string for file paths
            local_fasta_dir = r"{}".format(local_fasta_dir)
            cols = st.columns(3)
            if cols[1].button("Copy fasta to workspace", type="primary", disabled=(local_fasta_dir == "")):
                copy_local_fasta_files_from_directory(local_fasta_dir)

    if any(Path(fasta_dir).iterdir()):
        v_space(2)
        # Display all fasta files currently in workspace
        df = pd.DataFrame(
            {"file name": [f.name for f in Path(fasta_dir).iterdir()]})
        st.markdown("##### fasta files in current workspace:")
        show_table(df)
        v_space(1)
        # Remove files
        with st.expander("🗑️ Remove uploaded fasta files"):
            to_remove = st.multiselect("select fasta files",
                                    options=[f.stem for f in sorted(fasta_dir.iterdir())])
            c1, c2 = st.columns(2)
            if c2.button("Remove **selected** from workspace", type="primary", disabled=not any(to_remove)):
                remove_selected_fasta_files(to_remove)
                st.experimental_rerun()

            if c1.button("⚠️ Remove **all** from workspace", disabled=not any(fasta_dir.iterdir())):
                remove_all_fasta_files()
                st.experimental_rerun()

        
save_params(params)
