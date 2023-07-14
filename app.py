import streamlit as st
import subprocess
import tempfile
import os

from src.common import *
params = page_setup(page="main")


st.markdown(
    """# OpenNuXL

A protein nucleic acid crosslinking search engine"""
)

preset_list = ( 'none', 'RNA-UV (U)', 'RNA-UV(UCGA)', 'RNA-UV Extended (U)', 'RNA-UV Extended (UCGA)',
    'RNA-UV (4SU)', 'RNA-UV Extended (4SU)', 'RNA-UV (6SG)',
    'RNA-UV Extended (6SG)', 'RNA-DEB', 'RNA-DEB Extended',
    'RNA-NM', 'RNA-NM Extended', 'DNA-UV', 'DNA-UV Extended',
    'DNA-DEB', 'DNA-DEB Extended', 'DNA-NM', 'DNA-NM Extended',
    'RNA-FA', 'RNA-FA Extended', 'DNA-FA', 'DNA-FA Extended')

cols=st.columns(2)
with cols[0]:
    input_file = st.file_uploader("input_file")
    if input_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_file.read())
            # Get the temporary file path
            input_file_path = temp_file.name

with cols[1]:
    database = st.file_uploader("database")
    if database is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(database.read())
            # Get the temporary file path
            database_path = temp_file.name

cols=st.columns(2)
with cols[0]:
    preset = st.selectbox('Select the suitable preset',preset_list)
with cols[1]:
    st.number_input("length",value=2)

cols=st.columns(2)
with cols[0]:
    scoring  = st.selectbox('Select the scoring method',("Slow", "Fast"))
with cols[1]:
    decoys  = st.selectbox('Generate decoys internally',("True", "False"))

button1 = st.button("Run-analysis")

bash_script = """
#!/bin/bash
OpenNuXL -in {input_file_path} -database {database_path} -out "test.idXML" -NuXL:presets 'RNA-UV (U)'

"""

if button1:
  st.write(input_file_path)
  st.write(database_path)
  subprocess.run(['bash',"-c", bash_script])
  st.write("finished")

save_params(params)
