import streamlit as st
from streamlit_plotly_events import plotly_events
import subprocess
from src.common import *
from src.view import *
from src.fileupload import *
from src.result_files import *
import threading

params = page_setup()
st.title("⚙️ Run Analysis")

if "selected-mzML-files" not in st.session_state:
    st.session_state["selected-mzML-files"] = params.get("selected-mzML-files", [])

if "selected-fasta-files" not in st.session_state:
    st.session_state["selected-fasta-files"] = params.get("selected-fasta-files", [])

load_example_mzML_files()
mzML_files_ = [f.name for f in Path(st.session_state.workspace,
                          "mzML-files").iterdir()]
selected_mzML_file = st.selectbox(
    "choose mzML file",
    [item for item in mzML_files_ if not item.endswith(".csv")]
    ,
    help="If file not here, please upload at File Upload"
)

load_example_fasta_files()
selected_fasta_file = st.selectbox(
    "choose fasta file",
    [f.name for f in Path(st.session_state.workspace,
                          "fasta-files").iterdir()],
    help="If file not here, please upload at File Upload"
)

result_dir: Path = Path(st.session_state.workspace, "result-files")

if selected_mzML_file:
    mzML_file_path = str(Path(st.session_state.workspace, "mzML-files", selected_mzML_file))
if selected_fasta_file:
    database_file_path = str(Path(st.session_state.workspace, "fasta-files", selected_fasta_file))

preset_list = ( 'none', 'RNA-UV (U)', 'RNA-UV(UCGA)', 'RNA-UV Extended (U)', 'RNA-UV Extended (UCGA)',
    'RNA-UV (4SU)', 'RNA-UV Extended (4SU)', 'RNA-UV (6SG)',
    'RNA-UV Extended (6SG)', 'RNA-DEB', 'RNA-DEB Extended',
    'RNA-NM', 'RNA-NM Extended', 'DNA-UV', 'DNA-UV Extended',
    'DNA-DEB', 'DNA-DEB Extended', 'DNA-NM', 'DNA-NM Extended',
    'RNA-FA', 'RNA-FA Extended', 'DNA-FA', 'DNA-FA Extended')

Enzyme = ('Trypsin/P','TrypChymo', 'V8-DE', 'V8-E', 'Trypsin',
           'leukocyte elastase', 'proline endopeptidase', 'glutamyl endopeptidase',
           'Alpha-lytic protease', 'Lys-C/P', 'PepsinA', 'Chymotrypsin', 
           'Chymotrypsin/P', 'CNBr', 'Formic_acid', 'Lys-C', 'Lys-N',
           'Arg-C', 'Arg-C/P', 'Asp-N', 'Asp-N/B', 'Asp-N_ambic', 
           'elastase-trypsin-chymotrypsin', 'nocleavage', 'unspecific cleavage', 
           '2-iodobenzoate', 'iodosobenzoate', 'staphylococcal protease/D', 
           'proline-endopeptidase/HKR', 'Glu-C+P', 'PepsinA + P', 'cyanogen-bromide',
            'Clostripain/P') 

cols=st.columns(2)
with cols[0]:
    cols_=st.columns(2)
    with cols_[0]:
        Enzyme = st.selectbox('Enzyme',Enzyme, help=" The enzyme used for peptide digestion. (default: 'Trypsin/P')")
    with cols_[1]:
        Missed_cleavages = str(st.number_input("Missed_cleavages",value=2, help="Number of missed cleavages. (default: '2')"))
with cols[1]:
    cols_=st.columns(2)
    with cols_[0]:
        peptide_min = st.text_input('peptide min length', '6', help="Minimum size a peptide must have after digestion to be considered in the search. (default: '6')")
    with cols_[1]:
        peptide_max= st.text_input('peptide max length', '1000000', help="Maximum size a peptide may have after digestion to be considered in the search. (default: '1000000')")

cols=st.columns(2)
with cols[0]:
    cols_=st.columns(2)
    with cols_[0]:
        Precursor_MT = str(st.number_input("Precursor mass tolerance",value=6, help = "Precursor mass tolerance (+/- around precursor m/z). (default: '6.0')"))
    with cols_[1]:
        Precursor_MT_unit= st.selectbox(' ',['ppm', 'Da'])
with cols[1]:
    cols_=st.columns(2)
    with cols_[0]:
        Fragment_MT = str(st.number_input("Fragment mass tolerance",value=20, help = "Fragment mass tolerance (+/- around fragment m/z). (default: '20.0')"))
    with cols_[1]:
        Fragment_MT_unit= st.selectbox('',['ppm', 'Da'])
    

cols=st.columns(2)
with cols[0]:
    preset = st.selectbox('Select the suitable preset',preset_list, help = " Set precursor and fragment adducts form presets (recommended).")
with cols[1]:
    length= str(st.number_input("length",value=2, help = "Oligonucleotide maximum length.(default: '2')"))


cols=st.columns(2)
with cols[0]:
    Fixed_modification  = st.text_input('Enter fixed modifications', 'None', help="Fixed modifications, specified using UniMod (www.unimod.org) terms, e.g. 'Carbamidomethyl (C)'.")
with cols[1]:
    Variable_modification  = st.text_input('Enter variable modifications', 'Oxidation (M)', help="Variable modifications, specified using UniMod (www.unimod.org) terms, e.g. 'Oxidation (M)' (default: '[Oxidation (M)]')") 

cols=st.columns(2)
with cols[0]:
    Variable_max_per_peptide  = str(st.number_input("Variable_max_per_peptide",value=2, help="Maximum number of residues carrying a variable modification per candidate peptide.(default: '2')"))
with cols[1]:
    scoring  = st.selectbox('Select the scoring method',("slow", "fast"), help="Scoring algorithm used in prescoring (fast: total-loss only, slow: all losses). (default: 'slow') (valid: 'fast', 'slow')")

## take the exact name of file, create same file 
mzML_file_name = mzML_file_path.split('/')
protocol_name = mzML_file_name[len(mzML_file_name)-1].replace(".mzML", "")
result_path = str(result_dir)+"/"+protocol_name+".idXML"
#st.write(result_path)


################# Here we will run the NuXL command ###########################

# Use a dictionary to store the subprocess result
result_dict = {}
result_dict["success"] = False
result_dict["log"] = " "

def run_subprocess(args, variables, result_dict):
    st.write("inside run_subprocess")
    process = subprocess.Popen(args + list(variables), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        result_dict["success"] = True
        result_dict["log"] = stdout
    else:
        result_dict["success"] = False
        result_dict["log"] = stderr

terminate_flag = threading.Event()
terminate_flag.set()

def terminate_subprocess():
    global terminate_flag
    terminate_flag.set()

if st.button("Run-analysis"):
    if st.button("Terminate/Clear"):
        terminate_subprocess()
        st.warning("Process terminated. The analysis may not be complete.")
        st.experimental_rerun() 

    with st.spinner("Running analysis... Please wait until analysis done 😑"):
        args = ["OpenNuXL", "-in", mzML_file_path, "-database", database_file_path, "-out", result_path, "-NuXL:presets", preset, 
                        "-NuXL:length", length, "-NuXL:scoring", scoring, "-precursor:mass_tolerance",  Precursor_MT, "-precursor:mass_tolerance_unit",  Precursor_MT_unit,
                        "-fragment:mass_tolerance",  Fragment_MT, "-fragment:mass_tolerance_unit",  Fragment_MT_unit,
                        "-peptide:min_size",peptide_min, "-peptide:max_size",peptide_max, "-peptide:missed_cleavages",Missed_cleavages, "-peptide:enzyme", Enzyme,
                        "-modifications:variable", Variable_modification]  # Replace with the subprocess command and arguments
        variables = []  # Add any additional variables needed for the subprocess (if any)

        message = f"Running '{' '.join(args)}'"
        st.code(message)

        # Use st.experimental_thread to run the subprocess asynchronously
        terminate_flag = threading.Event()
        thread = threading.Thread(target=run_subprocess, args=(args, variables, result_dict))
        thread.start()
        thread.join()


if result_dict["success"]:
    st.success(f"Analyze done successfully of **{protocol_name}**")
    # Save the log to a text file in the result_dir
    log_file_path = result_dir / f"{protocol_name}_log.txt"
    with open(log_file_path, "w") as log_file:
        log_file.write(result_dict["log"])

    All_files = [f.name for f in sorted(result_dir.iterdir())]

    ### just show and download the identification_files of XLs PSMs/PRTs 
    perc_exec = any("_perc_" in string for string in All_files)
    if perc_exec :
        identification_files = [string for string in All_files if "_perc_0.0100_XLs"  in string or "_perc_0.1000_XLs" in string or "_perc_1.0000_XLs" in string or "_perc_proteins" in string]
    else:
        identification_files = [string for string in All_files if "_XLs"  in string or "_proteins" in string]
 
    ### file withour FDR control, we used in rescoring paper
    #identification_files.append(f"{protocol_name}.idXML")
    #st.write("identification_files", identification_files)

    ##showing all current files
    current_analysis_files = [s for s in All_files if protocol_name in s]
    df = pd.DataFrame({"output files ": current_analysis_files})
    show_table(df)

    download_selected_result_files(identification_files, f":arrow_down: {protocol_name}_XL_identification_files")

    #st.info(result_dict["log"])  
    st.text_area(f"{protocol_name} output log",value= str(result_dict["log"]), height=500)


####### This code for without threading implementation#######################
#button1 = st.button("Run-analysis")
def run_command(args, *variables):
    """Run command, transfer stdout/stderr back into Streamlit and manage error"""
    #st.info(repr(f"Running '{' '.join(args)}'"))
    message = f"Running '{' '.join(args)}'"
    st.code(message)
    process = subprocess.Popen(args + list(variables), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    terminate_button = st.button("Terminate/Clear", help="For termination of anlayze or clear everything")
    try:
        while process.poll() is None:
            if terminate_button:
                process.terminate()
                st.warning("Process terminated by user.")
                break
        else:
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                return True, stdout
            else:
                st.error(stderr)
                return False, stderr
    except KeyboardInterrupt:
        process.terminate()
        st.warning("Process terminated by user.")
        raise KeyboardInterrupt

#analyze_done = False
#log = ""
#if button1:
#  with st.spinner("Running analysis... Please wait until analysis done 😑"):    
#    analyze_done, log = run_command(["OpenNuXL", "-in", mzML_file_path, "-database", database_file_path, "-out", result_path, "-NuXL:presets", preset, 
#                    "-NuXL:length", length, "-NuXL:scoring", scoring, "-precursor:mass_tolerance",  Precursor_MT, "-precursor:mass_tolerance_unit",  Precursor_MT_unit,
#                    "-fragment:mass_tolerance",  Fragment_MT, "-fragment:mass_tolerance_unit",  Fragment_MT_unit,
#                    "-peptide:min_size",peptide_min, "-peptide:max_size",peptide_max, "-peptide:missed_cleavages",Missed_cleavages, "-peptide:enzyme", Enzyme,
#                    "-modifications:variable", Variable_modification])
#    #st.write("after analyze command", analyze_done)

#if analyze_done:
#    st.success(f"Analyze done successfully of **{protocol_name}**")
#    # Save the log to a text file in the result_dir
#    log_file_path = result_dir / f"{protocol_name}_log.txt"
#    with open(log_file_path, "w") as log_file:
#        log_file.write(log)
        
#    All_files = [f.name for f in sorted(result_dir.iterdir())]
#    current_analysis_files = [s for s in All_files if  protocol_name in s]
#    df = pd.DataFrame({"output files ": current_analysis_files})
#    show_table(df)
#    download_selected_result_files(current_analysis_files, "download_output_files")
#    st.info(log)'''

save_params(params)
