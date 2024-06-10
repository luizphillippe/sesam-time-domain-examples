import subprocess,shutil, os
import pandas as pd
from matplotlib import pylab as plt
skipFatigue = False # if true, run only sestra not sesam core
plot_results = False
#this example demonstrates how to run Wasim and Sesam Core ULS for one analysis
#first input files will be copied from 'Input' folder to 'Execution' folder
workspacePath = os.path.dirname(os.path.abspath(__file__))
execution_folder_path = os.path.join(workspacePath,"ExecutionFolder")
#Search specified file types for specific text and report failures
def checkIfSuccessful(files_to_check: dict, success_text: str):
    print(f"Assuming results to be in folder  {os.getcwd()}")
    all_cases_succeeded = True
    for prog in files_to_check:
        filename = files_to_check[prog]
        if not os.path.exists(filename):
            print(f"File {filename} not found in folder {os.getcwd()}")
            all_cases_succeeded = False 
        else:
            with open(filename, 'r') as file:
                if not success_text in file.read():
                    print(f"{prog} failed ")
                    print(f"Please check {os.getcwd() +os.path.sep+filename}")
                    all_cases_succeeded = False                
    if all_cases_succeeded:
        print("Analysis was successful for all loadcases.")    
        return True
    else:
        print("Analysis was NOT successful for all loadcases.")    
        return False

def checkIfSesamCoreIsSucecssful():
    print("Verifying Sesam Core results:")
    score_succeeded_text = "Duration:"
    score_to_check = {"Sesam Core":'SCORE.MLG'}
    return checkIfSuccessful(score_to_check,score_succeeded_text)

def checkIfWasimStatusIsSuccessful():
    print("Verifying Wasim results:")
    wasim_succeeded_text = "FINISHED: SUCCESS"
    wasim_to_check = {"Wasim solve":'wasim_solve.lis', "Wasim stru" : 'wasim_stru.lis'}
    return checkIfSuccessful(wasim_to_check,wasim_succeeded_text)

def checkIfSestraIsSuccessful():
    print("Verifying Sestra results:")
    sestra_succeeded_text = "Execution completed successfully"
    sestra_to_check = {"Sestra":'sestra.mlg'}
    return checkIfSuccessful(sestra_to_check,sestra_succeeded_text)

# remove existing results if they exists and copy input files to execution folder
shutil.rmtree(execution_folder_path, ignore_errors=True)
shutil.copytree(os.path.join(workspacePath,"Input"),execution_folder_path,dirs_exist_ok=True)
print("Running Wasim setup")
os.chdir(execution_folder_path)
subprocess.run([r"C:\Program Files\DNV\Wasim V7.0-00\Bin\wasim_setup.exe",  "/input=wasim_setup"])
print("Running Wasim solve for hydrodynamic direct loads reconstruction")
subprocess.run([r"C:\Program Files\DNV\Wasim V7.0-00\Bin\wasim_solve.exe",  "/input=wasim_solve"])
subprocess.run([r"C:\Program Files\DNV\Wasim V7.0-00\Bin\wasim_snapshots.exe",  "/input=wasim_snapshots"])
print("Running Wasim load transfer onto structural model")
subprocess.run([r"C:\Program Files\DNV\Wasim V7.0-00\Bin\wasim_stru.exe",  "/input=wasim_stru"])
checkIfWasimStatusIsSuccessful()
if skipFatigue:
    print("Running Sestra")
    subprocess.run([r"C:\Program Files\DNV\Sestra V10.18-00\Bin\sestra.exe",  "/dsf"])
    checkIfSestraIsSuccessful()
else:
    print("Running Sesam Core")
    result= subprocess.run([r"C:\Program Files\DNV\Sesam Core V3.0-00\Bin\score.exe",  "fatigue", "-i input.json", "-s"])
    checkIfSesamCoreIsSucecssful()
# reading the reaction forces from the result file and plot graph
result_path = os.path.join(execution_folder_path, "_reactions_history1.csv")
reaction_history = pd.read_csv(result_path)
df = pd.read_csv(result_path, delimiter=';') 
if plot_results:
    plt.plot(df['Time'], df['FZ'], marker='o')
    plt.xlabel('Time [s]', fontsize=10)
    plt.ylabel('Force [N]', fontsize=10)
    plt.title('Reaction z-force over time-history', fontsize=14)
    plt.show()
    plt.savefig("reaction_forces_plot.png")
    os.chdir(workspacePath)# back to the workspace folder|