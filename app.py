import streamlit as st
import subprocess
import tempfile
import os
#from captcha.image import ImageCaptcha
#from pyopenms import *

from src.common import *
params = page_setup(page="main")

# Increase the maximum upload file size to 1000MB
#st.set_option("server.maxUploadSize", 1000 * 1024 * 1024)

st.markdown(
    """# OpenNuXL

A protein nucleic acid crosslinking search engine"""
)

save_params(params) 
