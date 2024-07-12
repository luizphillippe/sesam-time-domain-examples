import os

#Search specified file types for specific text and report failures
def checkStatus(files_to_check: dict, success_text: str):
    print(f"Assuming results to be in folder  {os.getcwd()}")
    all_cases_succeeded = True
    for casename in os.listdir():
        if os.path.exists(casename) and os.path.isdir(casename):
            os.chdir(casename)
            for prog in files_to_check:
                filename = files_to_check[prog]
                all_cases_succeeded = all_cases_succeeded and checkIfAnalysisOk(success_text, filename)
            os.chdir("..")
    if all_cases_succeeded:
        print(f"Analysis was successful for all loadcases for program {prog}.")
        return True
    else:
        print("Analysis was NOT successful for all loadcases.")
        return False


def checkExpectedFiles(files_to_check):
    '''Check if the expected files are present'''
    all_ok = True
    for filename in files_to_check:
        if not os.path.exists(filename):
            print(f"File {filename} not found")
            all_ok = False
    return all_ok

def checkIfAnalysisOk(success_text, filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found in folder {os.getcwd()}")
        return False
    else:
        with open(filename, 'r') as file:
            if not success_text in file.read():
                print(f"Please check {os.getcwd() +os.path.sep+filename}")
                return False
    return True

def checkSesamCoreStatus():
    print("Verifying Sesam Core results:")
    score_succeeded_text = "Duration:"
    score_to_check = {"Sesam Core":'SCORE.MLG'}
    return checkStatus(score_to_check,score_succeeded_text)

def checkWasimStatus():
    print("Verifying Wasim results:")
    wasim_succeeded_text = "FINISHED: SUCCESS"
    wasim_to_check = {"Wasim solve":'wasim_solve.lis', "Wasim stru" : 'wasim_stru.lis'}
    return checkStatus(wasim_to_check,wasim_succeeded_text)

def checkSestraStatus():
    print("Verifying Sestra results:")
    sestra_succeeded_text = "Execution completed successfully"
    sestra_to_check = {"Sestra":'sestra.mlg'}