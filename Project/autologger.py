import pygsheets
import pandas as pd


class Autologger:
    
  #Reads the master data sheet as a dataframe
  @classmethod
  def read_trial_data_from_sheet(self):
    #authorization
    gc = pygsheets.authorize(service_file="C:/Users/hesse/Desktop/Code/ASEN5519-005/Project/asen5519-nback-project-d1f333490854.json")
    sh = gc.open("ASEN5519_Project_Data")
    #select the first sheet 
    wks = sh.worksheet('title','MasterData')
    df = wks.get_as_df()
    return(df)

  #get group number and most recent trial so we know what trial to give next
  @classmethod
  def find_previous_trial_results(self, df, ID):
    # filter rows based on condition 
    prev_results = df[df['ID'] == ID]
    print(prev_results)

    #get the group num and latest trial num for the given ID
    if not prev_results.empty:
      group_num = prev_results.tail().iloc[0,1]
      trial_num = prev_results.tail().iloc[0,2]
      #test_num = test_num.at[0,"Trial_N"]
    else:
      raise "No previous test results for the specified ID"

    return(group_num, trial_num)
  
  #from the group num and trial_num, determine which trial should be served next
  @classmethod
  def determine_next_trial(self, group_num, trial_num):
    #group_num: which group participant is part of
    #trial_num: participant's last completed trial number

    gc = pygsheets.authorize(service_file="C:/Users/hesse/Desktop/Code/ASEN5519-005/Project/asen5519-nback-project-d1f333490854.json")
    sh = gc.open("ASEN5519_Project_Data")
    #select the first sheet 
    wks = sh.worksheet('title','TrialKey')
    df = wks.get_as_df()

    df = df[df['Group_Num']==group_num]
    print(df)

    if trial_num >= 5:
      trial = "COMPLETE. NO MORE TRIALS."
    else: 
      trial = df.tail().iloc[0,trial_num+1]

    return(trial)

    
    




  @classmethod
  def write_trial_data_to_sheet(self, ID, group_num, trial_num, trial_datetime, trial_Ns, trial_accuracies):
    #authorization
    gc = pygsheets.authorize(service_file="C:/Users/hesse/Desktop/Code/ASEN5519-005/Project/asen5519-nback-project-d1f333490854.json")
    # Create empty dataframe
    df = pd.DataFrame()


    # Create columns in dataframe
    df['ID'] = ID
    df['Group_Num'] = group_num
    df['Trial_Num'] = trial_num
    df['Trial_Datetime'] = trial_datetime
    df['Trial_N'] = str(trial_Ns)
    df['Trial_Accuracies'] = str(trial_accuracies)

    
    #open the google spreadsheet
    sh = gc.open("ASEN5519_Project_Data")

    #select the first sheet 
    wks = sh.worksheet('title','MasterData')

    #values = [df.columns.values.tolist()]
    #get the values to write into a list, then write to next available row
    values = df.values.tolist()
    wks.append_table(values, start='A1', end=None, dimension='ROWS', overwrite=False)

  #write individual task responses to 
  @classmethod
  def write_task_data_to_sheet(self, ID, group_num, trial_num, task_datetime, task_num, task_N, task_prompts, task_matches, task_responses, task_successes,	task_accuracy):
    
    #authorization
    gc = pygsheets.authorize(service_file="C:/Users/hesse/Desktop/Code/ASEN5519-005/Project/asen5519-nback-project-d1f333490854.json")
    # Create empty dataframe
    df = pd.DataFrame()

    # Create columns in dataframe
    df['ID'] = ID
    df['Group_Num'] = group_num
    df['Trial_Num'] = trial_num
    df['Task_Datetime'] = task_datetime
    df['Task_Num'] = task_num
    df['Task_N'] = task_N
    df['Task_Prompts'] = str(task_prompts)
    df['Task_Matches'] = str(task_matches)
    df['Task_Responses'] = str(task_responses)
    df['Task_Successes'] = str(task_successes)
    df['Task_Accuracy'] = task_accuracy

    #open the google spreadsheet
    sh = gc.open("ASEN5519_Project_Data")

    #select the first sheet 
    wks = sh.worksheet('title','TaskData')

    #values = [df.columns.values.tolist()]
    #get the values to write into a list, then write to next available row
    values = df.values.tolist()
    wks.append_table(values, start='A1', end=None, dimension='ROWS', overwrite=False)
