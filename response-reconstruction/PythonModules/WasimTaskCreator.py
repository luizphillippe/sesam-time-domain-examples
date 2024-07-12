import os
from dnv.sesam.commands import WasimStruCommand,  WasimSetupCommand, WasimSolveCommand, WasimSnapShotsCommand
from dnv.sesam.commands import SestraCommand
from dnv.oneworkflow import PythonCommand, CompositeExecutableCommand

class WasimTaskCreator:
    def __init__(self):
        pass     
    def CreateTasks(self,templateParameters: dict = {}, prefix:str = ""):
        if prefix != "":
            prefix = "_" + prefix 
               
        wasim_setup_cmd = WasimSetupCommand()
        wasim_setup_cmd.TemplateInputFile = f"Wasim_Setup{prefix}_template.inp"
        wasim_setup_cmd.Parameters = templateParameters #template_parameters todo fixme
        wasim_solve_cmd = WasimSolveCommand()
        wasim_solve_cmd.Parameters = templateParameters
        wasim_solve_cmd.TemplateInputFile =  f"Wasim_Solve{prefix}_template.inp"
        wasim_snapshots_cmd = WasimSnapShotsCommand()
        wasim_snapshots_cmd.Parameters = templateParameters
        wasim_snapshots_cmd.TemplateInputFile = f"wasim_snapshots{prefix}_template.inp"

        wasim_stru_cmd = WasimStruCommand()
        wasim_stru_cmd.Parameters = templateParameters
        wasim_stru_cmd.TemplateInputFile = f"Wasim_stru{prefix}_template.inp"

        return [wasim_setup_cmd, wasim_solve_cmd, wasim_snapshots_cmd,wasim_stru_cmd]
        

