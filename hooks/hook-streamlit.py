from PyInstaller.utils.hooks import copy_metadata
datas = []
datas += copy_metadata('streamlit')
datas += copy_metadata('streamlit_plotly_events')
datas += copy_metadata('pyopenms')  
datas += copy_metadata('captcha') 
datas += copy_metadata('pyarrow') 
datas += copy_metadata('xlsxwriter') 
datas += copy_metadata('streamlit_aggrid')
datas += copy_metadata('python_decouple')