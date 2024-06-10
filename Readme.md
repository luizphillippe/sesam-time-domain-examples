# Sesam Time Domain Examples
Repository containing examples for Time Domain analyses for [Floating Offshore Wind](https://www.dnv.com/software/services/software-to-design-floating-wind-turbine-support-structures/) using Sesam. 
The repository contains various Jupyter notebook examples demonstrating how to run Sesam applications in a workflow including custom Python scripts using the Python library OneWorkflow developed by DNV.

The image below illustrates a typical Time Domain analysis workflow including a coupled analysis:

<img src="workflow.png" alt="image" width="100%" height="auto">
<br><br>

The following examples focus on the part of the workflow contained in the green box. They demonstrate various ways to read results for one or many design load cases from coupled analysis, then reconstruct the loads and run finite element analysis on the substructure, before doing fatigue and buckling checks.


**_Note:_**  For new users to Time Domain Buckling Analysis of FOWT structures we recommend to start with the tutorials before running other workflow examples.
<br>
<br>

# Table of contents 
* [Prerequisites](#Prerequisites)
* [Tutorials](#tutorials)
* [Other Examples](#other_examples)
* [Introduction to OneWorkflow](#oneworkflowIntro)
<br>
<br>

# Prerequisites (not needed for the general examples)<a id='Prerequisites'></a>

## Python

OneWorkflow supports Python versions 3.10, 3.11, and 3.12, which are available for download from the official [Python download page](https://www.python.org/downloads/). Please make sure that you have installed one of these versions and we recommend that you use Python version 3.12. To ensure a smooth development experience, it is essential that you enable the 'Add python.exe to the PATH' option during installation. This option is usually turned off by default, the image below highlights how to enable it.

<img src="pythonpath.png" alt="image" width="50%" height="auto">
<br>
<br>

You must verify the default Python version on your system, especially if you have multiple Python installations:

- Open the command line interface (Windows-start-menu --> type cmd --> enter)
- Type "python --version" and press enter to check the default Python version on your system.
<br>
<br>

## Jupyter notebook viewer

Several of the examples and tutorials provided use Jupyter notebooks to document the Python code. This requires a Jupyter notebook viewer, several are available online for download.
If you don't have a preferred viewer yet, we recommend downloading and installing [Visual Studio Code](https://code.visualstudio.com/download) from its official website. This open-source code editor is recognised by developers worldwide for its extensive language support and a vast array of extensions. After successful installation, install the following extensions:

- [Python Extension](https://code.visualstudio.com/docs/languages/python) - Enhance your Python development experience in VS Code. Download it from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
- [Jupyter Notebook Extension](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) - Seamlessly integrate Jupyter notebooks with VS Code. Download it from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter).
<br><br>

## Git

You need [git](https://git-scm.com/downloads) installed to be able to clone the repository. Once git is installed, open a command prompt in the desired folder and use the command:

`git clone https://github.com/dnv-opensource/sesam-time-domain-examples.git`
<br><br>

## Sesam Setup Guide

You need the relevant Sesam products with a license for local runs. Additionally, you need [Application Version Manager](https://sesam.dnv.com/download/windows/applicationversionmanager_3200_inst_win.zip), which does not require a license for local execution. You can download Sesam applications from [here](https://sesam.dnv.com/download/programs.html).

Refer to the [Python Tools Installation Guide](installation/installation.ipynb) for detailed steps on setting up the necessary tools. These are essential for running all notebooks.
<br>
<br>

# Tutorials <a id='tutorials'></a>

These tutorials include a step-by-step text description of the workflows as well as the necessary input files to run them. 

* [Plate buckling tutorial](https://myworkspace.dnv.com/download/public/sesam/sesam-workflows/downloads/SesamCore_plate_buckling_tutorial.zip) Learn how to set up and run plate buckling on a simple model. This tutorial shows how to export the capacity model from GeniE and then run Sestra and SesamCore from the command line. Python and a Jupyter notebook reader are NOT required to run this tutorial.

* [Time History Buckling Analysis of EMULF Delta Floater](direct-load-generation/EMULF_Buckling_Tutorial/EMULF_buckling_tutorial.pdf) This tutorial demonstrates how to export a capacity model from GeniE and run direct load generation in Wasim followed by a structural analysis and buckling assessment in SesamCore. The export of the capacity model is done using the GeniE GUI and the remaining steps are performed by running Python code cells in a Jupyter notebook. The notebook demonstrates how a spreadsheet can be used to define the parameters of the design load cases and how to use OneWorkflow to manage and run the analysis. Upon completing the analysis a couple of code examples show how to display selected results and scan for maximum usage factors.  
<br>
<br>


# Other Examples <a id='other_examples'></a>

Additional examples are available without a detailed description on how to run them. Here, the concepts and technologies applied in the tutorials are used and extended to create other workflows with varied complexity. 

## Buckling code check

* [EMULF Delta Floater extensive example](direct-load-generation/EMULF_DeltaFloater_Sesam_ULS/EMULF_DeltaFloater_Sesam_ULS.ipynb) This notebook illustrates how a spreadsheet can be used to define the parameters of the design load cases and how to use OneWorkflow to manage and run the analysis. Separate Wasim load generation runs allow to account for the load factors in the structural analysis. Upon completing the buckling assessment, a variety of methods to display results are demonstrated.  
<br>

## Fatigue analysis
These examples demonstrate how to run a simple Sesam Core Fatigue screening check for a Floating OWT model created in GeniE, exposed to time-dependent wave loads coming from a Sima coupled analysis results via load reconstruction in Wasim, using OneWorkflow locally or in the cloud. 
<br>

### Single load case Examples
These examples run only a single load case.
* [OC4 Wasim SesamCore FLS Python Example Only Python](direct-load-generation/OC4WasimSesamCoreFLSSingleLoadCase/OC4WasimSesamCoreFLSOnlyPython.py) Pure Python example using no external modules.
* [OC4 Wasim SesamCore FLS Python Example Commands](direct-load-generation/OC4WasimSesamCoreFLSSingleLoadCase/OC4WasimSesamCoreFLSOnlyUsingCommands.py) Python example using the Sesam Commands module but not OneWorkflow.


### Multiple load cases
The parameters to be used in each load case are specified in an Excel spreadsheet.

* [OC4 Wasim SesamCore FLS Jupyter Example ](direct-load-generation/OC4WasimSesamCoreFLSJupyter/OC4WasimSesamCoreFLSJupyter.ipynb) A Jupyter notebook example demonstrating how to run a few load cases.
* [OC4 Wasim SesamCore FLS Jupyter Example Stepwise](direct-load-generation/OC4WasimSesamCoreFLSJupyter/OC4WasimSesamCoreFLSJupyterStepwise.ipynb) A Jupyter notebook example demonstrating how to run a few load cases step wise, i.e. adding checking of results after load transfer before fatigue screening with Sesam Core.
* [OC4 Wasim SesamCore FLS Python Example](direct-load-generation/OC4WasimSesamCoreFLSPython/OC4WasimSesamCoreFLS.py) The same example as OC4WasimSesamCoreFLSJupyter but in pure Python.
* [OC4 Wasim SesamCore FLS Python Example Utility Class](direct-load-generation/OC4WasimSesamCoreFLSPython/OC4WasimSesamCoreFLSUtilityClass.py) A Python example demonstrating how to run a few load cases with the help of a utility class.
<br><br>

## Additional documentation
An overview of commonly used template parameters for Wasim, Sestra and Sesam Core [template_parameters_in_use.txt](template_parameters_in_use.txt).
<br>
<br>

# Introduction to OneWorkflow <a id='oneworkflowIntro'></a>
OneWorkflow is a comprehensive workflow development system that integrates various tools, modules and services seamlessly. This integration streamlines the workflow, enhances efficiency, and promotes a more unified approach to development. With its UI-less interface, OneWorkflow is designed to provide a robust backend for workflow automation. It also offers the flexibility to use the same code for local and cloud-based operations using OneCompute.

Support for Sesam on OneCompute will become public soon. Please contact us on software.support@dnv.com if you are interested in early access to our cloud services. 
<br>

For a more detailed explanation of OneWorkflow, please consult the [help pages](https://myworkspace.dnv.com/knowledge-centre/sesam-workflows/usermanual).  Here you can learn about the folder structure employed in the examples, explore relevant concepts such as asynchronous programming and find links to the API documentation.
