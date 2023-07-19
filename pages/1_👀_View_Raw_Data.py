import streamlit as st
from streamlit_plotly_events import plotly_events
import subprocess
from src.common import *
from src.view import *

params = page_setup()
st.title("View raw MS data")

selected_mzML_file = st.selectbox(
    "choose mzML file",
    [f.name for f in Path(st.session_state.workspace,
                          "mzML-files").iterdir()],
)

selected_fasta_file = st.selectbox(
    "choose fasta file",
    [f.name for f in Path(st.session_state.workspace,
                          "fasta-files").iterdir()],
)


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

button1 = st.button("Run-analysis")

def run_command(args, *variables):
    """Run command, transfer stdout/stderr back into Streamlit and manage error"""
    st.info(f"Running '{' '.join(args)}'")
    result = subprocess.run(args + list(variables), capture_output=True, text=True)
    try:
        result.check_returncode()
        st.info(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error(result.stderr)
        raise e

if button1:
  run_command(["OpenNuXL", "-in", mzML_file_path, "-database", database_file_path, "-out", "./src/test.idXML", "-NuXL:presets", preset, 
               "-NuXL:length", length, "-NuXL:scoring", scoring, "-precursor:mass_tolerance",  Precursor_MT, "-precursor:mass_tolerance_unit",  Precursor_MT_unit,
               "-fragment:mass_tolerance",  Fragment_MT, "-fragment:mass_tolerance_unit",  Fragment_MT_unit,
               "-peptide:min_size",peptide_min, "-peptide:max_size",peptide_max, "-peptide:missed_cleavages",Missed_cleavages, "-peptide:enzyme", Enzyme,
               "-modifications:variable", Variable_modification])
  
  st.write("finished")
  

save_params(params)
