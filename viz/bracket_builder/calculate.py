import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection
from matplotlib.backends.backend_pdf import PdfPages

def compute_conditional_probs(sub_filepath, names_filepath):
    """
    Function to take the submission file and calculate conditional probabilities for each team/round.

    :param sub_filepath (str): location of Kaggle data submission
    :param names_filepath (str): location of team names for IDs in submission
    :return: DataFrame containing

    """

    ## Get the sample submission and break out the ID
    sub_df = pd.read_csv(sub_filepath)
    sub_df['Season'] = sub_df['ID'].apply(lambda x: x[0:4]).astype(int)
    sub_df['TeamID_1'] = sub_df['ID'].apply(lambda x: x[5:9]).astype(int)
    sub_df['TeamID_2'] = sub_df['ID'].apply(lambda x: x[10:]).astype(int)

    ## Get the team names to merge in
    team_names = pd.read_csv(names_filepath)
    team_names['TeamID'] = team_names['TeamID']

    ## Merge team 1 name
    team_names = team_names.rename(columns={'TeamName': 'TeamName_1',
                                            'TeamID': 'TeamID_1'})
    team_names.drop(columns=['FirstD1Season', 'LastD1Season'], inplace=True)
    sub_df = sub_df.merge(team_names, how='left', on='TeamID_1')

    ## Merge team 2 name
    team_names = team_names.rename(columns={'TeamName_1': 'TeamName_2',
                                            'TeamID_1': 'TeamID_2'})
    df = sub_df.merge(team_names, how='left', on='TeamID_2')

    return df