# Python calling SOM.m under Matlab program
import subprocess

def run_matlab_script(script_name):
    matlab_command = f"matlab -nodisplay -nosplash -nodesktop -r \"run('{script_name}');exit;\""
    
    process = subprocess.Popen(matlab_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    try:
        decoded_stdout = stdout.decode('ISO-8859-1')
        decoded_stderr = stderr.decode('ISO-8859-1')
    except UnicodeDecodeError as e:
        print(f"Error decoding MATLAB output: {str(e)}")
        decoded_stdout = stdout.decode('ISO-8859-1', errors='ignore')
        decoded_stderr = stderr.decode('ISO-8859-1', errors='ignore')
    
    if process.returncode != 0:
        print(f"Error executing MATLAB script. STDERR: {decoded_stderr}")
    else:
        print(f"MATLAB script executed successfully. STDOUT: {decoded_stdout}")

script_name = " "
run_matlab_script(script_name)
