import pygsheets
import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
import os
class Autologger:
  
  JSON_ENC_PATH = "sec.json"
  ENC = "gAAAAABlP1B3OfXA1Il0ONGu_UmRh_opyHYhSi72DNxgZ0dNB9pjp3Emq9fWOcoH96XLgkxCm8NVdYl4mwt2ZW-qFr1FPR9ZosoiiFtrk0Torse0KvWpeeVLghASIEYPRwwODINQB_rECUQZMi4RsM1_HXozknT2OwzVXNRkBW651cUMHcCA0mGcuDrCqa3OelCvItPY0HRkA-tcpg6IHx9BBnomqJMXSdgYG7P-TAeY4IwfrrEfXrF2PFCkDFM1B-vFTpgYlPcgz6ApPK7WPy-4AoYP6rioUHE6h1If68ijXbcrQm_8ZpEPJ_zSIM8t4JLwnEej_1LX1DemocCt_e5GM0EjcEiw8GfZsmBAs4oLaRNByoetOIkZ3DUvagvrbtfsRzWk0Br_L-R7i6PVkjxzEdggb5Gc5AcwBnq9UAoLNfRe4NfglcrmxEbkvnYV3qSKFaWfMbQeex5bjza7D53PDIztXLlf9cLtJh7DVIvV7Uy-rl_ij38GFVXfi-kq-4AEgI_8OkgriP2EDDPCzTmkd-KtWW3orbScP--ZlUyPq5uqfg7a85ch2EfMdErDPU_aXGwx9uWFFSlyOeiuRsXmqvb6_-JP4CvvfMrT2N46cfbfPHlwjqlIY1eaW9dRP33KN5DKFlblsK8xkzHVgxHCrIThlpEbwzRlhnZu7xOMS2Tbgsb5mdc29b1GIBmiS7xaAHZMj-4ajdEkCMnQo47Q_cv7GHAdo9VQ0yKvGmJa8bpdedxMrVUc-I_baOSuAmSJRKr5regh_BeCcpsmPaO4JwlXya1q_9xqv3USkjW35cJpEZnI35G2vm3kevkdVKOyo1uF3jtRC0npdLpDz_Bgme-RKFX5F2NTn7xBd9FFEAua5hFcL_oiz4YFlcq9RpSkad47cw_3rJvuwhKFjNn9RsqnoAJGFMXmkeppiDXBYHAj4c7yVti_Sey0JoM3dFBc6LD-1Mqug83i8NER07m6IbDcrMZdn6YnRGf8zoKVsaQm3lRLhfwGMio33fU9EjeR0rMRoibJFvsqI4G4j1ciZZxRg2zkhfjtcgUcIfWQcfJb4K0k_FdrMdtxnxwK61GQL3oLjGXeulRm7L6tPcSxb7DH5M1ABEgm-SAbJBboVO2lQmo_eMr4waTJSUEl-04-5_4474nkqFK4o8ffuoThyWUfhKzLTXkpmACpLQN4A7AlFYDdZ1yM7VpyDGJxHhJvEvXjcbnOlGEDi5Li5Iu-048L81WK3czTJLqCoF3f0xpLUJQFUEOHXAC-DUBJpYn_m2t4mfDcArFUkVh4obWzB9sBU70ZEo_Ju3zm2L-yWSqiTayXA8w63Kk58GKhPLt3TEGFIWilz1zyYlutGCJZyfkavBCH1G-GjptbyiBjTZT2GptGwXiO1DO_c_0i2xJXv--KXHKIroH2jPjjKhFNvSvcAaIBvtUqkJ7Vmb0whsLObZNSPaR3rsT13kseFr2Kdiym8ut7QBSLwJNnZ3iTfNuF4hvLS6AJcu_XhDrXK-9BD7m6y9ZyrXnjKG6UmAzKKfE0edKlc7WhuCKfqiHf50XSY6UQVCNSAy9tllHPK9SPfydGSSI3CEeM7UyUR3Uv03Na2LcZ9ujS37MH5_aoZgvPoE8fY15fQPACG-41OSmlG_1Q_4bQlPkW5mzN2HtvOyfn32v0Vn_g6n7DSu_llSa28s2pe-0A3KVo2V9VvMjV7ZCLqMafWUc0J0RmnDL0wy78adUakuVBTXDDLlX-EfqXJZUIQZ3cObwDMGZvU3gQn7nHu1Wcd9Mn1aMRYbDtNBY7WhELTrfuB3-Mi7_93fCH5_Kjr4WQa1K6RR_DDLTlFt5mofHmCUDqS9B2S03pe0vJtSxKQMFa4K3nStQI-4OAVtq7AXSeP-uVQLnpG4aMRsFf7_tDnnBcyyqSmWNlZddQFVtOINIDP_0-NgUvJBb9JOMoDVF9c5IK6cYo40Q_7eJfKS7RQlai1fK1L70tXkk5uc2b3O--x9aN6mziiy00GXeRvTKu7Ql4xtYd3F7ar0ZQQChq9gewJo_odyA1Fm2Qjw1XXLCnd_iPGPcd-rhr4vFu1XICmlBIw9O5pCvfPiByfmPjvtxo6Arruegr1G68WuB3Q68waqdifW9aWGo6H1x7yQV4BlwgmLHDTqesPcKO0Tnt1Qn6yF41FigLS6ZUsmSkasiSLrRYvsapjLFDMOpgax2Gyxqj_Y3pmH94mdyidU-btXpSGOpt0CpZ0SOszJScGEiT-KEejQxotmQd4AxfesysLK0GEW3wgpoPoIgWfigPFFG6Rhnfrs4lPiRHjpydjHyl4wkV0r9_MGjQTaU6mgO2qMi8_XG7eg4RwnTFUOxnVMgndJvzqFN6AYd08RPOIL0lmlU8GCheCxzwINPClBJcrk1-YPJHa_C4OhEz3Ys3w9iRBOd5YNu3O_wtJf0bGsTcJkJvGWie44Mtg_iz3T0S6wkKGYv1N3TwB0a8ig8ewRK-j506LBJG0f9abeyqWK-bB9YKgzwifht73IY_36mZza8SHoj83agjR2VJzwBJc80KfzIJImaHziZ8QBnmQ7IN6RVmG7xrj3Lv0rArIZogKSxBCuB1YMgAi5WDjSbGyyl0VtFFm7oWG7914jrn6E5MovSzEPaqSG9Db5ylbEJjSS8A-gfsIiGufU-XcqN9wfyRQtvaKFVhofcO-7M5CMpC83mZ5DaidaNFpaSDavVi2pamH0B5uWFYQf2WVzUTYU8b4Wa8NeXcA831KhvXnJQF6GVx_NNd0tUtzYgji7wZd78fJir-p8B6030Edm5XVfq0GdZ7pJmTfEnad6bJLQUfTm9v0jEKgN0eZdR4960RJBLkUyu2TD8rOK6UbYm1cjAvdCuEoSadYmE5REc_HqW-WRq8bHfsejm1-rqt11ooPmn3MeEtVjcNkflZrhNYbUVAZEfHHhl7iM9AKRuvTPXHVUi-3iE-MJg15m5o48b0piXrqgpFCbc0VtreDP4cKJyyp1NA-14AlkZvErCN8orcOR0TQ38_-fUk-FoT6WHEKuWG3wDXesanvc9pDc82Zyuzk8a_EQLCwZBEoPW8G09fKDoi_klaghPqYHhsvHaX53lQdq8DrbVaunDf5Iu5DTEIVIhSrZ8Yh1-2_tXGWeXMv3__eObVEpJJBaaH3Wuec9EKQ_GXyB_YUz7JuHw91YvrxgMzEJtvgx3oQlDY0qV9zCCxEmIg_hEEXOsznwAF85jofoCF87ca0gisJ4U="
  FERNET_KEY = b'h_pORVoUU5T1nLNKdjKV5YivgsdbxddoIg9XrKVq6Wo='

  def decrypt(self):

    fernet = Fernet(self.FERNET_KEY)

    # with open("sec.json",'rb') as file:
    #   enc = file.read()

    unenc = fernet.decrypt(self.ENC)

    with open('tmp.json','wb') as f:
      f.write(unenc)

  #Reads the master data sheet as a dataframe
  @classmethod
  def read_trial_data_from_sheet(self):
    #authorization
    self.decrypt(self)
    gc = pygsheets.authorize(service_file="tmp.json")
    os.remove('tmp.json')
    sh = gc.open("ASEN5519_Project_Data")
    #select the first sheet 
    wks = sh.worksheet('title','MasterData')
    df = wks.get_as_df()
    return(df)

  

  #get group number and most recent trial completed
  @classmethod
  def find_previous_trial_results(self, df, ID):
    # filter rows based on condition 
    prev_results = df[df['ID'] == int(ID)]

    #get the group num and latest trial num for the given ID
    if not prev_results.empty:
      group_num = prev_results.tail(n=1).iloc[0,1]
      trial_num = prev_results.tail(n=1).iloc[0,2]
      datetime_str = prev_results.tail(n=1).iloc[0,3]
      #test_num = test_num.at[0,"Trial_N"]
    else:
      group_num = None
      trial_num = 0
      datetime_str = None

    return(group_num, trial_num, datetime_str)
  
  #from the group num and trial_num, determine which trial/task sequence should be served next
  @classmethod
  def determine_next_trial(self, group_num, trial_num):
    #group_num: which group participant is part of
    #trial_num: participant's last completed trial number
    self.decrypt(self)
    gc = pygsheets.authorize(service_file="tmp.json")
    os.remove('tmp.json')
    sh = gc.open("ASEN5519_Project_Data")
    #select the first sheet 
    wks = sh.worksheet('title','TrialKey')
    df = wks.get_as_df()

    df = df[df['Group_Num']==group_num]

    if trial_num >= 5:
      task_sequence = None
    else: 
      task_sequence = df.tail(n=1).iloc[0,trial_num+1]

    if task_sequence == "Control":
      task_sequence = "222222"

    return(task_sequence)

  #writes high-level trial performance data to the MasterData google sheet
  @classmethod
  def write_trial_data_to_sheet(self, ID, group_num, trial_num, trial_datetime, trial_Ns, trial_accuracies):
    #authorization
    self.decrypt(self)
    gc = pygsheets.authorize(service_file="tmp.json")
    os.remove('tmp.json')
    # Create empty dataframe
    df = pd.DataFrame()


    # Create columns in dataframe
    df['ID'] = ID
    df['Group_Num'] = np.asarray([group_num])
    df['Trial_Num'] = np.asarray([trial_num])
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

  #write individual task responses/results to the TaskData google sheet
  @classmethod
  def write_task_data_to_sheet(self, ID, group_num, trial_num, task_datetime, task_num, task_N, task_prompts, task_matches, task_responses, task_successes,	task_accuracy):
    self.decrypt(self)
    #authorization
    gc = pygsheets.authorize(service_file="tmp.json")
    os.remove('tmp.json')    
    # Create empty dataframe
    df = pd.DataFrame()

    # Create columns in dataframe
    df['ID'] = ID
    df['Group_Num'] = np.asarray([group_num])
    df['Trial_Num'] = np.asarray([trial_num])
    df['Task_Datetime'] = task_datetime
    df['Task_Num'] = np.asarray([task_num])
    df['Task_N'] = np.asarray([task_N])
    df['Task_Prompts'] = str(task_prompts)
    df['Task_Matches'] = str(task_matches)
    df['Task_Responses'] = str(task_responses)
    df['Task_Successes'] = str(task_successes)
    df['Task_Accuracy'] = np.asarray([task_accuracy])

    #open the google spreadsheet
    sh = gc.open("ASEN5519_Project_Data")

    #select the first sheet 
    wks = sh.worksheet('title','TaskData')

    #values = [df.columns.values.tolist()]
    #get the values to write into a list, then write to next available row
    values = df.values.tolist()
    wks.append_table(values, start='A1', end=None, dimension='ROWS', overwrite=False)
