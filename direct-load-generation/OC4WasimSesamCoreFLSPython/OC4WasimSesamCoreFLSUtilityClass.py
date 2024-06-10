import pandas as pd
import sys
sys.path.append("../PythonModules")
from WasimSesamCoreExecution import *
import analysisStatusChecker 
run_analysis = True #set to True to run the analysis
skip_fatigue = False # if true, run only sestra not sesam core
plot_results = False
#this example demonstrates how to run Wasim and Sesam Core for a set of loadcases  
#the Wasim time periods are specified in an ascii file test_cases_wasim_input.txt
#load case specific input files are located in folder Workspace\Input
#shared input files are located in folder Workspace\CommonFiles
#a utility calss called WasimSesamCoreExecution is used to run the analysis and check the status

#create workflowclient that orchestrates the execution
root_folder = os.path.dirname(os.path.abspath(__file__))
workspace_path = str(Path(root_folder, 'Workspace'))
wasimSesamCoreExecution = WasimSesamCoreExecution(workspace_path = workspace_path, workspace_ID= "SesamWasimCoreExample")

#read parameter variation from text file, could easily be replaced with input from Excel or a regular Python dictionary
parametrized_loadcases = pd.read_table(os.path.join(workspace_path,"test_cases_wasim_input.txt"), index_col=0)
#add additional data if needed 
#data.loc['LC004'] = {'TimeStep': 0.3, 'StartTime': 2,'EndTime':7,'NSteps':2}
print("Loadcases with parameters to be run:")
print(parametrized_loadcases) 


if run_analysis:
    #Recognize the following column titles in Excel spreadsheet and map them to the correct input parameters given in Wasim template files
    parameter_mapping = {'TimeStep': "timestep", "StartTime": "start_solve", "EndTime": "stop_solve", "NSteps": "nsteps"}
    
    #copy input files to working directory, Workspace\Loadcases, existing files will be removed
    wasimSesamCoreExecution.copying_input_files_to_working_directory()

    #run all loadcase specified in loadcases_with_parameter
    #the run will be executed in folder workspacePath\LoadCases\LC001, workspacePath\LoadCases\LC002, etc.
    wasimSesamCoreExecution.run_wasim_sesam_core_for_all_parameters(parameter_mapping, parametrized_loadcases, skip_fatigue)
os.chdir(wasimSesamCoreExecution.results_directory)
#check if analysis was successful
analysisStatusChecker.checkWasimStatus()
if skip_fatigue:
    analysisStatusChecker.checkSestraStatus()
else:
    analysisStatusChecker.checkSesamCoreStatus()

if plot_results:
#plot reaction forces for all loadcases
    wasimSesamCoreExecution.plot_reaction_forces()

wasimSesamCoreExecution.remove_log_files()