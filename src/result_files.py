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
def create_zip_and_get_base64_():
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


###################################
def remove_and_get_unique_elements(input_list):
    # Remove strings containing "_proteins0.0100_XLs.tsv" and "_0.0100_XLs.idXML"
    filtered_list = [item for item in input_list if "_proteins0.0100_XLs.tsv" not in item or "_0.0100_XLs.idXML" not in item]

    # Return the final unique elements
    unique_elements = list(set(filtered_list))

    return unique_elements



######################################
import pandas as pd
from pyopenms import IdXMLFile


# convert every string col into an int or float if possible
def strToFloat(df):
  for col in df:
    try:
      df[col] = [float(i) for i in df[col]]
    except ValueError:
      continue
  return df# convert every string col into an int or float if possible


def readAndProcessIdXML(input_file, top=1):
  """
  convert the (.idXML) format identification file to dataframe
  """
  prot_ids = []; pep_ids = []
  IdXMLFile().load(str(input_file), prot_ids, pep_ids)
  meta_value_keys = []
  rows = []
  #st.write("len of pep_ids:", len(pep_ids))
  if len(pep_ids)>0:
    for peptide_id in pep_ids:
        spectrum_id = peptide_id.getMetaValue("spectrum_reference")
        scan_nr = spectrum_id[spectrum_id.rfind('=') + 1 : ]

        hits = peptide_id.getHits()

        psm_index = 1
        for h in hits:
            if psm_index > top:
                break
            charge = h.getCharge()
            score = h.getScore()
            z2 = 0; z3 = 0; z4 = 0; z5 = 0

            if charge == 2:
                z2 = 1
            if charge == 3:
                z3 = 1
            if charge == 4:
                z4 = 1
            if charge == 5:
                z5 = 1
            if "target" in h.getMetaValue("target_decoy"):
                label = 1
            else:
                label = 0
            sequence = h.getSequence().toString()
            if len(meta_value_keys) == 0: # fill meta value keys on first run
                h.getKeys(meta_value_keys)
                meta_value_keys = [x.decode() for x in meta_value_keys]
                all_columns = ['SpecId','PSMId','Label','Score','ScanNr','Peptide','peplen','ExpMass','charge2','charge3','charge4','charge5','accessions'] + meta_value_keys
                #print(all_columns)
            # static part
            accessions = ';'.join([s.decode() for s in h.extractProteinAccessionsSet()])

            row = [spectrum_id, psm_index, label, score, scan_nr, sequence, str(len(sequence)), peptide_id.getMZ(), z2, z3, z4, z5, accessions]
            # scores in meta values
            for k in meta_value_keys:
                s = h.getMetaValue(k)
                if type(s) == bytes:
                    s = s.decode()
                row.append(s)
            rows.append(row)
            psm_index += 1
            break; # parse only first hit
  
    df =pd.DataFrame(rows, columns=all_columns)
    convert_dict = {'SpecId': str,
                    'PSMId': int,
                    'Label': int,
                    'Score': float,
                    'ScanNr': int,
                    'peplen': int                
                }
    
    df = df.astype(convert_dict)
    return df
  
  else: 
      return None
  

######################### Deal with TSV file of proteins #######
from io import StringIO

def read_protein_table(input_file):
    section_dfs = []
    current_section = []
    skip_next_line = False
    use_next_line_as_header = False

    # Read the TSV file line by line
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()

            # Check if the line is a section header
            if line.startswith('==') and line.endswith('=='):
                # Save the current section DataFrame to the list
                if current_section:
                    # If the section is 2, 3, or 5, use the next line as the header and remove the current header
                    if use_next_line_as_header:
                        try:
                            section_df = pd.read_csv(StringIO('\n'.join(current_section[1:])), delimiter='\t', header=None)
                            section_df.columns = current_section[0].split('\t')
                        except pd.errors.EmptyDataError:
                            # Handle the EmptyDataError by creating an empty DataFrame with appropriate headers
                            section_df = pd.DataFrame(columns=current_section[0].split('\t'))
                        section_dfs.append(section_df)
                        use_next_line_as_header = False
                    else:
                        try:
                            section_df = pd.read_csv(StringIO('\n'.join(current_section)), delimiter='\t')
                        except pd.errors.EmptyDataError:
                            # Handle the EmptyDataError by creating an empty DataFrame
                            section_df = pd.DataFrame()
                        section_dfs.append(section_df)

                    current_section = []
                    skip_next_line = True
            else:
                # Append the line to the current section content
                if not skip_next_line:
                    current_section.append(line)
                skip_next_line = False

                # Check if the next section should use the next line as the header
                if line.startswith("Protein summary") or line.startswith("Crosslink efficiency") or line.startswith("Precursor adduct summary"):
                    use_next_line_as_header = True

                # Check if section 4, then update header
                if line.startswith("Crosslink efficiency"):
                    use_next_line_as_header = False
                    header_line = next(f).strip()
                    header = ["AA", "Crosslink efficiency"]
                    current_section.append(header_line)
                    current_section[0] = "\t".join(header)

    # Append the last section to the list
    if current_section:
        try:
            section_df = pd.read_csv(StringIO('\n'.join(current_section)), delimiter='\t')
        except pd.errors.EmptyDataError:
            # Handle the EmptyDataError by creating an empty DataFrame
            section_df = pd.DataFrame()
        section_dfs.append(section_df)

    return section_dfs

def add_to_selected_result_files(filename: str):
    """
    Add the given filename to the list of selected result files.

    Args:
        filename (str): The filename to be added to the list of selected result-files.

    Returns:
        None
    """
    # Check if file in params selected mzML files, if not add it
    if filename not in st.session_state["selected-result-files"]:
        st.session_state["selected-result-files"].append(filename)

def save_uploaded_result(uploaded_files: list[bytes]) -> None:
    """
    Saves uploaded result files to the result-files directory.

    Args:
        uploaded_files (List[bytes]): List of uploaded result files (idXML and tsv).

    Returns:
        None
    """
    # A list of files is required, since online allows only single upload, create a list
    if st.session_state.location == "online":
        uploaded_files = [uploaded_files]
    # If no files are uploaded, exit early
    for f in uploaded_files:
        if f is None:
            st.warning("Upload some files first.")
            return
        
    # Write files from buffer to workspace mzML directory, add to selected files
    for f in uploaded_files:
        if f.name not in [f.name for f in result_dir.iterdir()] and f.name.endswith(".idXML"):
            with open(Path(result_dir, f.name), "wb") as fh:
                fh.write(f.getbuffer())
        add_to_selected_result_files(Path(f.name).stem)
    st.success("Successfully added uploaded files!")
