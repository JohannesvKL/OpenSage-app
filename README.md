# OpenMS NuXL App [![Open Template!](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://openms-template.streamlit.app/)

Welcome to the OpenMS NuXL App, a web application for the NuXL protein-nucleic acid search engine built using [OpenMS](https://openms.de/) and [pyOpenMS](https://pyopenms.readthedocs.io/en/latest/).<br/>
**website:** [https://abi-services.cs.uni-tuebingen.de/nuxl/](https://abi-services.cs.uni-tuebingen.de/nuxl/)

## NuXL

- **Description:** NuXL is a dedicated software package designed for the analysis of XL-MS (cross-linking mass spectrometry) data obtained from UV and chemically crosslinked protein–RNA/DNA samples. This powerful tool allows for reliable, FDR-controlled assignment of protein–nucleic acid crosslinking sites in samples treated with UV light or chemical crosslinkers. It offers user-friendly matched spectra visualization, including ion annotations.[more](https://ssp2022.com/index.php/timetable/event/henning-urlaub/)
  
**powered by:**

<img src="assets/OpenMS.png" width=20%>
  
## Running NuXL locally: Installation as stand-alone tool
### Windows
1. To get started, download and extract the [OpenMS-App.zip](https://github.com/Arslan-Siraj/nuxl-app/actions) file from latest successfull action.
2. Run the `run_app.exe`
3. Use app in your default browser <br/>

The workspaces for the project will be locally generated in the `workspaces-nuxl-app` directory, and the analysis will run using local resources.
   
## Quickstart 

You can start right away analyzing your data by following the steps below:

### 1. Create a workspace
On the left side of this page you can define a workspace where all your data including uploaded files will be stored. Entering a workspace will switch to an existing one or create a new one if it does not exist yet. In the web app, you can share your results via the unique workspace ID. Be careful with sensitive data, anyone with access to this ID can view your data.

### 2. 📁 Upload your files
Upload `mzML` and `fasta` files via the **File Upload** tab. The data will be stored in your workspace. With the web app you can upload only one file at a time.
Locally there is no limit in files. However, it is recommended to upload large number of files by specifying the path to a directory containing the files.

Your uploaded files will be shown on the same **File Upload** page in  **mzML files** and **Fasta files** tabs. Also you can remove the files from workspace.

### 3. ⚙️ Analyze your uploaded data

Select the `mzML` and `fasta` files for analysis, configure user settings, and start the analysis using the **Run-analysis** button.
You can terminate the analysis immediately using the **Terminate/Clear** button and you can review the search engine log on the page.
Once the analysis completed successfully, the output table will be displayed on the page, along with downloadable links for crosslink identification files.

#### 4. 📊 View your results
Here, you can visualize and explore the output of the search engine. All crosslink output files in the workspace are available on the **View Results** tab.
After selecting any file, you can view the `CSMs Table`, `PRTs Table`, `PRTs Summary`, `Crosslink efficiency` and `Precursor adducts summary`.

Note: Every table and plot can be downloaded, as indicated in the side-bar under ⚙️ Settings.

## How to accessing previously analysed results?
Under the **Result Files** tab, you can manage your results. You can `remove` or `download` files from the output files list.

## How to upload result files (e.g., from external sources/collaborator) for manual inspection and visualization?
At **Upload result files** tab, user can  `upload` the results files and can visualize in **View Results** tab.
In the web app, collaborators can visualize files by sharing a unique workspace ID.

⚠️ Note: In the web app, all users with a unique workspace ID have the same rights.

## Contact
For any inquiries or assistance, please feel free to reach out to us.<br/><br/>
[![Discord Shield](https://img.shields.io/discord/832282841836159006?style=flat-square&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=Discord)](https://discord.gg/4TAGhqJ7s5) [![Gitter](https://img.shields.io/static/v1?style=flat-square&message=on%20Gitter&color=ED1965&logo=Gitter&logoColor=FFFFFF&label=Chat)](https://gitter.im/OpenMS/OpenMS?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
<br/><br/>





