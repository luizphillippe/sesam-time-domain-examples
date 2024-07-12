from pathlib import Path
import os
from dnv.oneworkflow.utils.workunit_extension import *
from dnv.oneworkflow.utils import *
import pandas as pd
from dnv.sesam.commands import *
import shutil
import asyncio
from WasimTaskCreator import *
from dnv.oneworkflow import *
import glob
class WasimSesamCoreExecution:
    def __init__(self,  workspace_path: str, workspace_ID: str, top_super_element = 1, files_to_download = ["**/*.csv","**/*.txt", "**/*.lis","**/*"
                                                                               "mlg"] ):
        self.workspace_ID = workspace_ID
        self.workspace_path = workspace_path
        self.cloudRun = False
        self.workflow_client = one_workflow_client(workspace_id = self.workspace_ID, 
                                                   cloud_run = self.cloudRun, 
                                                   workspace_path = self.workspace_path,
                                                   inplace_execution=True
                                                )
        self.input_parameters = {'mor_topsel': top_super_element}
        self.files_to_download = files_to_download
        self.results_directory = os.path.join(self.workspace_path,"LoadCases")


    def copying_input_files_to_working_directory(self):
        local__result_path = Path(self.workspace_path, self.workflow_client.results_directory)
        print(local__result_path)
        if os.path.isdir(local__result_path):
            try:
                shutil.rmtree(local__result_path) 
            except:
                print("Could not delete the results folder")
        shutil.copytree(os.path.join(self.workspace_path,"Input"),os.path.join(self.workspace_path),dirs_exist_ok=True)
       
    def create_fatigue_workflow(self, skip_fatigue):
        tasks = WasimTaskCreator().CreateTasks(self.input_parameters)

        if skip_fatigue:
            sestra_command = SestraCommand()
            sestra_command.arguments = "/dsf"
            tasks.append(sestra_command)
        else:
                #Update Sesam Core .jnl file
            sesam_core_template_command = CreateInputFileFromFileTemplateCommand(
                    template_input_file  = "SesamCore_screening_template.jnl",
                    input_filename  = "SesamCore_screening.jnl",
                    parameters= self.input_parameters
                )
            tasks.append(sesam_core_template_command)
            score_command = SesamCoreCommand(command = "fatigue",input_file_name= "input.json", options = "-s -v")
            tasks.append(score_command)
        return tasks
    
    def run_wasim_sesam_core_for_loadcase(self, casename:str, skip_fatigue = False):
        print("Setting up workflow")
        tasks = self.crete_FLS_Workflow(skip_fatigue)
        tasks.append(SesamCoreCommand(command = "uls",input_file_name= "input.json", options = "-v"))
        commands_info =[(CommandInfo(commands=tasks,load_case_foldername=casename))]
        print("Running workflow")
        asyncio.run(run_managed_commands_in_parallel_async(
            client=self.workflow_client,
            commands_info=commands_info,
          ))
        
    def run_wasim_sesam_core_for_all_parameters(self, parameter_mapping: dict, data: pd.DataFrame, skipFLS = False):
        commands_info = []
        
        print("Create workflow")
        for casename, case in data.iterrows():
            casedict = case.to_dict()
            for key, value in casedict.items():
                self.input_parameters[parameter_mapping[key]] = str(value)
            self.input_parameters['stop_stru'] = self.input_parameters['stop_solve']
            self.input_parameters['FATIGUESTART'] = float(self.input_parameters['start_solve'])
            self.input_parameters['FATIGUEEND'] = float(self.input_parameters['stop_solve'])
            # Possibility to delay start of load transfer with a number of time steps, add to the floating numbers
            self.input_parameters['start_stru'] = float(self.input_parameters['start_solve'])+ 1. * float(self.input_parameters['timestep'])
            tasks = self.create_fatigue_workflow(skipFLS)
            commands_info.append(CommandInfo(commands=tasks,load_case_foldername=casename))
        print("Running workflow")
        asyncio.run(run_managed_commands_in_parallel_async(
        client=self.workflow_client,
        commands_info=commands_info,
        log_job=False,
        files_to_upload_from_client_to_blob=FileTransferOptions(max_size="11124MB",patterns=["**/sim*.*","CommonFiles/*.*","**/*.json","**/*.inp","**/*.ssg","**/*.FEM"]),
        files_to_download_from_blob_to_client=FileTransferOptions(max_size="11124MB",patterns=self.files_to_download),
        enable_common_files_copy_to_load_cases=True,
        ))

    

    def plot_reaction_forces(self):
        os.chdir(self.results_directory)
        from datetime import datetime

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")
        print("Current Time =", current_time)
        print("Current Date =", current_date)
        counter = 0
        def format_time(value, _):
            return "{:.1e}".format(value)  # Format the time with two decimal places
        for loadcase_folder_name in os.listdir():
            result_path = os.path.join(loadcase_folder_name, "_reactions_history1.csv")
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

            counter += 1
            # Plot a 2D graph
            plt.figure(counter)
            plt.plot(time, fz, marker='o', label='FZ')

            # Add labels and title
            plt.xlabel('Result case id', fontsize=10)
            plt.ylabel('Force', fontsize=10)
            plt.xticks(fontsize=10)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(format_time))
            plt.yticks(fontsize=10)
            plt.title('Reaction z-force over time-history for loadcase ' + loadcase_folder_name, fontsize=14)
            plt.legend(fontsize=10)  # Show legend with labels

            # Add gridlines
            plt.grid(True, linestyle='--', alpha=0.7)

            # Set x-axis limits
            plt.xlim(min(time), max(time))


            # Show the plot
            plt.savefig(os.path.join(loadcase_folder_name,"reaction_forces_plot.png"))
        plt.show()
            
    def remove_log_files(self):
        os.chdir(self.workspace_path)
        for f in glob.glob('*.log'):
            try:
                os.remove(f)
            except:
                print(f"Could not delete file {f}")