import streamlit as st
import os
import subprocess

def run_subprocess(args: list[str], variables: list[str], result_dict: dict) -> None:
    """
    Run a subprocess and capture its output.

    Args:
        args (list[str]): The command and its arguments as a list of strings.
        variables (list[str]): Additional variables needed for the subprocess (not used in this code).
        result_dict dict: A dictionary to store the success status (bool) and the captured log (str).

    Returns:
        None
    """

    # Run the subprocess and capture its output
    
    st.write("Running command with args:", args)


    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    st.write("Standard Output:\n", stdout)
    st.write("Standard Error:\n", stderr)
    
    stdout = str(stdout.decode("utf-8"))
    stderr = str(stderr.decode("utf-8"))

    # Lists to store the captured standard output and standard error
    stdout_ = []
    stderr_ = []
    st.text("Gets to the arrays")
    # Capture the standard output of the subprocess
    output = stdout
        #st.write("Come to true")
    #if output == '' and process.poll() is not None:
    #    break
    if output:
            # Print every line of standard output on the Streamlit page
            #st.text(output.strip())
            # Append the line to store in the log
            stdout_.append(output.strip())


    # Capture the standard error of the subprocess
    
    error = stderr
    #if error == '' and process.poll() is not None:
        #break
    if error:
            # Print every line of standard error on the Streamlit page, marking it as an error
            #st.error(error.strip())
            # Append the line to store in the log of errors
            stderr_.append(error.strip())

    # Check if the subprocess ran successfully (return code 0)
    if process.returncode == 0:
        st.write("Sucches")
        st.write("Current files in cwd: ", st.write(os.listdir(os.getcwd())))

        result_dict["output_path"] = os.getcwd()
        result_dict["success"] = True
        # Save all lines from standard output to the log
        result_dict["log"] = " ".join(stdout_)
    else:
        st.write("Failuyre")
        result_dict["success"] = False
        # Save all lines from standard error to the log, even if the process encountered an error
        result_dict["log"] = " ".join(stderr_)
