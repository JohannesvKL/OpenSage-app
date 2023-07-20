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
    for f in Path("example-data", "idXMLs").glob("*"):
        #st.write("f in load_example", f)
        shutil.copy(f, result_dir)
        #f.name will pass with format extention
        add_to_result(f.name)
    #st.success("Example result files loaded!")

def list_result_example_files() -> None:

    list_result_example_files = []
    for f in Path("example-data", "idXMLs").glob("*"):
        list_result_example_files.append(f.name)
    return list_result_example_files
    

def remove_selected_result_files(to_remove: list[str]) -> None:
    """
    Removes selected idXML files from the idXML directory.

    Args:
        to_remove (List[str]): List of result files to remove.

    Returns:
        None
    """
    # remove all given files from result workspace directory and selected files
    #st.write("print all files in session state: ", st.session_state["selected-result-files"])
    for f in to_remove:
        Path(result_dir, f).unlink() ##remove the specified format 
        #st.write("remove_selected_result_files: ", f)
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
    #st.write("result_dir", local_result_directory)
    # Check if local directory contains result files, if not exit early
    if not any(Path(local_result_directory).glob("*")):
        st.warning("No result files found in specified folder.")
        return
    # Copy all result files to workspace result directory, add to selected files
    files = Path(local_result_directory).glob("*")
    #st.write("files", local_result_directory)
    for f in files:
        #st.write("f", f.name)
        add_to_result(f.name) 
    #st.success("Successfully added local files!")

import base64
def download_file(file_path, download_link_text):
    with open(file_path, "rb") as file:
        file_content = file.read()
    b64_file_content = base64.b64encode(file_content).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64_file_content}" download="{download_link_text}">Download File</a>'
    return href

################# download all results file ####################
import io
from zipfile import ZipFile

## create zip files of all available files in result folder
def create_zip_and_get_base64():
    # Create a temporary in-memory zip file
    buffer = io.BytesIO()
    with ZipFile(buffer, 'w') as zip_file:
        for file_path in Path(result_dir).iterdir():
            zip_file.write(file_path, arcname=file_path.name)

    # Reset the buffer's file pointer to the beginning
    buffer.seek(0)

    # Encode the zip file content to base64
    b64_zip_content = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return b64_zip_content

## create zip file of selected files
def create_zip_and_get_base64(file_paths):
    # Create a temporary in-memory zip file
    buffer = io.BytesIO()
    with ZipFile(buffer, 'w') as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, arcname=file_path.name)
    
    # Reset the buffer's file pointer to the beginning
    buffer.seek(0)
    
    # Encode the zip file content to base64
    b64_zip_content = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return b64_zip_content


def download_selected_result_files(to_download: list[str], link_name: str) -> None:
    """
    download selected idXML files from current workspace.

    Args:
        to_download (List[str]): List of result files to download.

    Returns:
        None
    """
    file_paths = [result_dir / f"{file_name}" for file_name in to_download]  # Replace "your_extension" with the actual file extension
    b64_zip_content = create_zip_and_get_base64(file_paths)
    href = f'<a href="data:application/zip;base64,{b64_zip_content}" download="selected_files.zip">{link_name}</a>'
    st.markdown(href, unsafe_allow_html=True)
