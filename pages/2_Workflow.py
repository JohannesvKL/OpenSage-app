import streamlit as st

from src.common import *

from src.result_files import *

params = page_setup()

if "selected-result-files" not in st.session_state:
    st.session_state["selected-result-files"] = params.get("selected-result-files", [])

st.title("Result Viewer")
tabs = ["idXML files", "recent results"]

tabs = st.tabs(tabs)

if st.session_state.location == "local":
    tabs.append("Files from local folder")

with tabs[0]:
    st.markdown("Short information text about the example data.")
    cols = st.columns(3)
    load_example_result_files()

    cols = st.columns(3)
    if cols[1].button("Load recent .idXML file", type="primary"):
        load_example_result_files() #####... TODo for recent files to shown (.idXML) (selected-result-files-->> selected idXML files)

    # Local file upload option: via directory path
    if st.session_state.location == "local":
        with tabs[2]:
            # with st.form("local-file-upload"):
            local_result_dir = st.text_input(
                "path to folder with result files")
            # raw string for file paths
            local_result_dir = r"{}".format(local_result_dir)
            cols = st.columns(3)
            if cols[1].button("Copy files to workspace", type="primary", disabled=(local_result_dir == "")):
                copy_local_result_files_from_directory(local_result_dir)

    if any(Path(result_dir).iterdir()):
        v_space(2)
        # Display all result files currently in workspace
        df = pd.DataFrame(
            {"file name": [f.name for f in Path(result_dir).iterdir()]})
        st.markdown("##### result files in current workspace:")
        show_table(df)
        v_space(1)
        # Remove files
        with st.expander("🗑️ Remove result files"):
            to_remove = st.multiselect("select result files",
                                    options=[f.stem for f in sorted(result_dir.iterdir())])
            c1, c2 = st.columns(2)
            if c2.button("Remove **selected**", type="primary", disabled=not any(to_remove)):
                remove_selected_result_files(to_remove)
                st.experimental_rerun()

            if c1.button("⚠️ Remove **all**", disabled=not any(result_dir.iterdir())):
                remove_all_result_files()
                st.experimental_rerun()

with tabs[1]:
    st.markdown("Check for new results added")



# At the end of each page, always save parameters (including any changes via widgets with key)
save_params(params)
