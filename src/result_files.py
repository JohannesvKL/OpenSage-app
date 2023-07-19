import shutil
from pathlib import Path

import streamlit as st
from src.common import reset_directory


# Specify result file location in workspace
result_dir: Path = Path(st.session_state.workspace, "result-files")


def add_to_result(filename: str):
    """
    Add the given filename to the list of view.

    Args:
        filename (str): The filename to be added to the list of selected result files.

    Returns:
        None
    """
    # Check if file in params selected result files, if not add it
    if filename not in st.session_state["selected-result-files"]:
        st.session_state["selected-result-files"].append(filename)

def load_example_result_files() -> None:
    """
    Copies example result files to the result directory.

    Args:
        None

    Returns:
        None
    """
    # Copy files from example-data/result to workspace result directory, add to selected files
    for f in Path("example-data", "idXMLs").glob("*.idXML"):
        shutil.copy(f, result_dir)
        add_to_result(f.stem)
    #st.success("Example result files loaded!")


def remove_selected_result_files(to_remove: list[str]) -> None:
    """
    Removes selected idXML files from the idXML directory.

    Args:
        to_remove (List[str]): List of result files to remove.

    Returns:
        None
    """
    # remove all given files from result workspace directory and selected files
    for f in to_remove:
        Path(result_dir, f+".idXML").unlink()
        st.session_state["selected-result-files"].remove(f)
    st.success("Selected result files removed!")


def remove_all_result_files() -> None:
    """
    Removes all result files from the result directory.

    Args:
        None

    Returns:
        None
    """
    # reset (delete and re-create) result directory in workspace
    reset_directory(result_dir)
    # reset selected result list
    st.session_state["selected-result-files"] = []
    st.success("All result files removed!")

@st.cache_data
def copy_local_result_files_from_directory(local_result_directory: str) -> None:
    """
    Copies local fasta files from a specified directory to the result directory.

    Args:
        local_result_directory (str): Path to the directory containing the result files.

    Returns:
        None
    """
    # Check if local directory contains result files, if not exit early
    if not any(Path(local_result_directory).glob("*.result")):
        st.warning("No result files found in specified folder.")
        return
    # Copy all result files to workspace result directory, add to selected files
    files = Path(local_result_directory).glob("*.result")
    for f in files:
        if f.name not in result_dir.iterdir():
            shutil.copy(f, result_dir)
        add_to_result(f.stem)
    st.success("Successfully added local files!")

