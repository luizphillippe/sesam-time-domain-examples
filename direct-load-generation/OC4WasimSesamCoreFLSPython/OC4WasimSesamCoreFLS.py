import os, sys
root_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_folder, "../PythonModules"))

from pathlib import Path
import pandas as pd
import shutil
import json
from dnv.oneworkflow.utils.workunit_extension import *
from dnv.oneworkflow.utils import *
from dnv.sesam.commands import *
from dnv.oneworkflow import *
from WasimTaskCreator import *

# local workspace, all results will be put here after local or cloud runs
# location of common files for all analyses, has to be below workspacePath and in the folder named CommonFiles
workspacePath = str(Path(root_folder, 'Workspace'))
workspaceId = "SesamWasimCoreExample"
cloudRun = False # Change to True if you want to run the workflow in the cloud (support for cloud runs coming soon)
skipFLS = False # if True, run only sestra not sesam core
plot_results = False # Change to True if you want to plot the results

# If running locally the code below will also start the local workflow host.
workflow_client = one_workflow_client(workspace_id = workspaceId, workspace_path = workspacePath, cloud_run = cloudRun, inplace_execution=True)

parameter_input_file = "parameter_input.xlsx" 
parameters_from_excel = pd.read_excel(os.path.join(workspacePath, parameter_input_file), index_col=0)

# Some hardcoded template parameters (not read from Excel)
topsuper = 1
try:
    os.chdir(os.path.join(workspacePath,"LoadCases"))
except:
    print("LoadCases folder not found")

#Recognize the following column titles in Excel spreadsheet and map them to the correct input parameters given in Wasim template files
parameter_mapping = {'TimeStep': "timestep", "StartTime": "start_solve", "EndTime": "stop_solve", "NSteps": "nsteps"}
commands_info = []
local__result_path = Path(workspacePath, workflow_client.results_directory)
print(local__result_path)
if os.path.isdir(local__result_path):
   try:
       shutil.rmtree(local__result_path) 
   except:
       print("Could not delete the results folder")
shutil.copytree(os.path.join(workspacePath,"Input"),os.path.join(workspacePath),dirs_exist_ok=True)
print(parameters_from_excel)
for casename, case in parameters_from_excel.iterrows():
    casedict = case.to_dict()
    input_parameters = {}
    # find the values from the Excel sheet for give load case
    for key, value in case.items():
        input_parameters[parameter_mapping[key]] = str(value)
    input_parameters['stop_stru'] = input_parameters['stop_solve']
    input_parameters['mor_topsel'] = topsuper
    
    # Possibility to delay start of load transfer with a number of time steps, add to the floating numbers
    input_parameters['start_stru'] = float(input_parameters['start_solve'])+ 1. * float(input_parameters['timestep'])
    
    input_parameters['FATIGUESTART'] = float(input_parameters['start_solve'])
    input_parameters['FATIGUEEND'] = float(input_parameters['stop_solve'])
   
    print("The following parameters are used for load case: " + casename)
    print(json.dumps(input_parameters, indent=4, sort_keys=True))
    tasks = WasimTaskCreator().CreateTasks(input_parameters)
    if skipFLS:
        sestra_command = SestraCommand()
        sestra_command.arguments = "/dsf"
        tasks.append(sestra_command)
    else:
        #Update Sesam Core .jnl file
        sesam_core_template_command = CreateInputFileFromFileTemplateCommand(
            template_input_file  = "SesamCore_screening_template.jnl",
            input_filename  = "SesamCore_screening.jnl",
            parameters= input_parameters
            )
        tasks.append(sesam_core_template_command)
        score_command = SesamCoreCommand(command = "fatigue",input_file_name= "input.json", options = "-s -v")
        tasks.append(score_command)
    commands_info.append(CommandInfo(commands=tasks,load_case_foldername=casename))
    
print("Running commands in parallel")
asyncio.run(run_managed_commands_in_parallel_async(
            client=workflow_client,
            commands_info=commands_info,
            log_job=False,
            files_to_upload_from_client_to_blob=FileTransferOptions(max_size="11124MB",patterns=["**/sim*.*","CommonFiles/*.*","**/*.json","**/*.inp","**/*.ssg","**/*.FEM","**/*.jnl"]),
            files_to_download_from_blob_to_client=FileTransferOptions(max_size="11124MB",patterns=["**/sestra.inp", "**/wasim_setup.inp", "**/wasim_solve.inp", "**/wasim_snapshots.inp", "**/wasim_stru.inp", "**/*.csv", "**/*.lis", "**/*.mlg", "**/*.sin", "**/*.FEM","**/*.JNL"]),
            enable_common_files_copy_to_load_cases=True
    )
)



now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%d/%m/%Y")
print(current_time, current_date)
if plot_results:
    def format_time(value, _):
        return "{:.1e}".format(value)  # Format the time with two decimal places
    for loadcase_folder_name, _ in parameters_from_excel.iterrows():
        result_folder = os.path.join(workspacePath,workflow_client.results_directory, loadcase_folder_name)
        result_path = os.path.join(result_folder, "_reactions_history1.csv")
        reaction_history = pd.read_csv(result_path)
        df = pd.read_csv(result_path, delimiter=';') 
        from matplotlib import pylab as plt
        from matplotlib.ticker import FuncFormatter
        # Set the default font size for all labels

        time = df['Time']
        fx = df['FX']
        fy = df['FY']
        fz = df['FZ']
        mx = df['MX']
        my = df['MY']
        mz = df['MZ']

        # Define a custom formatting function for x-axis values
    

        # Plot a 2D graph
        plt.plot(time, fz, marker='o', label='FZ')

        # Add labels and title
        plt.xlabel('Result case id', fontsize=10)
        plt.ylabel('Force', fontsize=10)
        plt.xticks(fontsize=10)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_time))
        plt.yticks(fontsize=10)
        plt.title('Reaction z-force over time-history', fontsize=14)
        plt.legend(fontsize=10)  # Show legend with labels

        # Add gridlines
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.title('Reaction z-force over time-history for loadcase' + loadcase_folder_name, fontsize=14)
                
        # Set x-axis limits
        plt.xlim(min(time), max(time))


        # Show the plot
        plt.show()
        plt.savefig(os.path.join(result_folder,"reaction_forces_plot.png"))