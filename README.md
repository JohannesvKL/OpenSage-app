# OpenMS NuXL App [![Open Template!](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://openms-template.streamlit.app/)
**powered by:**

<img src="assets/OpenMS.png" width=20%>

This is a web application of NuXL search engine build in [OpenMS](https://openms.de/).

## NuXL

- **Description:** NuXL, A dedicated software package for the analysis of XL-MS data obtained from UV and chemically crosslinked protein–RNA/DNA samples. It allows for reliable, FDR-controlled assignment of protein–nucleic acid crosslinking sites from samples treated with UV light or chemical crosslinkers and offers user-friendly matched spectra visualization including ion annotations.[more](https://ssp2022.com/index.php/timetable/event/henning-urlaub/#:~:text=NuXL%20is%20available%20in%20the,spectra%20visualization%20including%20ion%20annotations.)
  
  
## Installation
### Windows
1. Download and extract the [OpenMS-app.zip](https://github.com/Arslan-Siraj/nuxl-app/actions) file from latest successfull action.
2. Run the `run_app.exe`
3. Use app in your default browser
   
## Quickstart 

### Workspaces
On the left side of this page you can define a workspace where all your data including uploaded `mzML` files will be stored. Entering a workspace will switch to an existing one or create a new one if it does not exist yet. In the web app, you can share your results via the unique workspace ID. Be careful with sensitive data, anyone with access to this ID can view your data.

### 📁 File Upload
Upload `mzML` and `fasta` files via the **File Upload** tab. The data will be stored in your workspace. With the web app you can upload only one file at a time.
Locally there is no limit in files. However, it is recommended to upload large number of files by specifying the path to a directory containing the files.

Your uploaded files will be shown on the same **File Upload** page in  **mzML files** and **Fasta files** tabs. Also you can remove the files from workspace.

### ⚙️ Workflows
select the `mzML` and `fasta` file for analysis and also desire user configuration and run the analysis with **Run-analysis** button. Analysis can be terminate immediately via **Terminate/Clear** button also can look on search engine log on page.

Once the analysis done successfully, the output table will be appear on page and also downloadable link of crosslink identification files.

#### 📊 Result View
Here, you can visualize and look at the output of the search engine. All crosslink output files in workspace will appear on **View Results** tab. After selection of any file, user can look at `CSMs Table`, `PRTs Table`, `PRTs Summary`, `Crosslink efficiency` and `Precursor adducts summary`.

**Note:** Every table and plot can be downloadable as given option on side-bar **⚙️ Settings**.

At **Result files** tab, user can  `remove` and `download` file from output files.

At **Upload result files** tab, user can  `upload` the results files and can visualize in **View Results** tab.

## Contact

<br/><br/>





