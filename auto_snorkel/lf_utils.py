import numpy as np
from inspect import getmembers, isfunction

def predict_by_majority_vote(LF_matrix: list, weight_list: list, is_soft_label: bool = False):
    """Merge the labeling results of all the labeling function by majority vote.
        Parameters
        ----------
        LF_matrix
            The labeling matrix.
        is_soft_label
            Whether to get a soft labeling result.

        Return
        ----------
        P_matrix
            The final labeling result for each data.
    """

    P_matrix = []
    for label_list in LF_matrix:
        label2vote = {}
        for i in range(label_list):
            label = label_list[i]
            weight = weight_list[i]
            if label not in label2vote:
                label2vote[label] = 0.0
            label2vote[label] += 1.0 * weight

        if is_soft_label:
            for label in label2vote:
                label2vote[label] /= len(LF_matrix[0])
            P_matrix.append(label2vote)
        else:
            sort_label2vote = sorted(label2vote.items(), key=lambda x: x[1], reverse=True)
            best_label = sort_label2vote[0][0]
            P_matrix.append(best_label)

    P_matrix = np.array(P_matrix)
    return P_matrix

def get_module(func_path: str):
    """import the module in the path.
        Parameters
        ----------
        func_path
            The path of the module.
        Returns
        -------
        module
            The import module.
    """
    import sys
    sys.path.append(func_path)
    module_name = func_path

    # get module name
    first_id = module_name.find('/')
    while first_id != -1:
        module_name = module_name[first_id+1:]
        first_id = module_name.find('/')

    second_id = module_name.find('.')
    module_name = module_name[:second_id]

    frame = __import__(module_name)
    return frame

def get_func_name(line: str):
    # discard 'def' and (data)
    para_id = line.find('(')
    def_id = line.find('def')
    line = line[def_id+3: para_id]
    line = line.strip()

    return line

def get_lf_name_list(func_path: str):
    """Get label functions' name from input path.
        Parameters
        ----------
        func_path
            the path that contains the definition of labeling function.

        Returns
        -------
        list
            the list of all the functions' name in the given file.

    """
    lf_list = []
    fp = open(func_path, 'r')
    for line in fp:
        if 'def ' in line:
            func_name = get_func_name(line)
            lf_list.append(func_name)
    fp.close()
    return lf_list
