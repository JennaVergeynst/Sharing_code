# -*- coding: utf-8 -*-
"""
Created on Fri June 30 2017

@author: jennavergeynst
"""

import pandas as pd


def classify_receiver_clusters(fixed_tags, acc_goal, confidence_level, min_group_size=10):
    """
    All fixed positions are grouped per receiver cluster used for calculation of the position. 
    For each receiver cluster, the percentage of positions with error <= accuracy_goal is calculated. 
    Only clusters with a groupsize >= min_group_size are classified:
        - as good performers if this percentage is >= confidence_level; 
        - as bad performers if this percentage is < confidence_level.
    
    Parameters:
    -----------
    fixed_tags = dataframe with positions of the fixed transmitters, with at least columns HPEm and URX
        URX = list of receivers used to calculate the position
    acc_goal = maximum allowed error
    confidence_level = minimum proportion of the group that has to meet the acc_goal
    group_size = minimum number of positions calculated by a receiver cluster as a prerequisite to be classified, default 10
    
    Returns:
    --------
    URX_groups = dataframe with for each receiver cluster (URX-group) the percentage of positions with error <= accuracy goal and the groupsize
    good_performers = list with good performing receiver clusters
    bad_performers = list with bad performing receiver clusters
    
    """
    fixed_tags.loc[:,'acc_check'] = [error <= acc_goal for error in fixed_tags['HPEm']]
    URX_groups = fixed_tags.groupby(by=['URX'])['acc_check'].agg(['mean', 'count'])
    URX_groups = URX_groups.reset_index().rename(columns = {'mean': 'percentage', 'count': 'groupsize'})
    URX_subset = URX_groups[URX_groups['groupsize']>=min_group_size].reset_index(drop = True)
    
    good_performers = list(pd.DataFrame(URX_subset[URX_subset['percentage'] >= confidence_level])['URX'])
    bad_performers = list(pd.DataFrame(URX_subset[URX_subset['percentage'] < confidence_level])['URX'])
    
    return URX_groups, good_performers, bad_performers