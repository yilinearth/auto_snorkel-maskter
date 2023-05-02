from lf_utils import *
from label_function import LF
import numpy as np

class LFApplier:
    def __init__(self, lfs: list = None, lf_func_path: str = "", is_load_from_file: bool = False):
        """Apply the labeling functions to predict labels for data.
            Parameters
            ----------
            lfs
                The list of available labeling functions.
            lf_func_path
                The path of file that contains the definition of the available labeling functions.
            is_load_from_file
                Whether to import labeling function from lf_func_path.
        """
        if is_load_from_file:
            if len(lf_func_path) == 0:
                raise ValueError(f"Couldn't load label functions from empty file !")

            lf_name_list = get_lf_name_list(lf_func_path)
            lfs = []
            for func_name in lf_name_list:
                lf = LF(func_path=lf_func_path, lf_name=func_name, is_load_func=True)
                lfs.append(lf)

        self.lf_list = lfs

    def apply(self, data_list: list):
        """Apply the labeling functions to predict labels for each data in the list.
            Parameters
            ----------
            data_list
                The list of data that need labels.
            Return
            ----------
            LF_matrix: [data num, label func num]
                The labeling result for each data given by each labeling function.

        """
        LF_matrix = []
        for data in data_list:
            data_lf_list = []
            for lf in self.lf_list:
                label = lf.predict(data)
                data_lf_list.append(label)
            LF_matrix.append(data_lf_list)

        LF_matrix = np.array(LF_matrix)

        return LF_matrix

    def predict(self, LF_matrix: np.array, strategy: str = "majority_vote", is_soft_label: bool = False):
        """Merge the labeling results of all the labeling function into a final result.
            Parameters
            ----------
            LF_matrix
                The labeling matrix, which contains the labeling results for each data given by each labeling function.
            strategy
                The strategy to merge final labeling result.
            is_soft_label
                Whether to get a soft labeling result.

            Return
            ----------
            P_matrix
                The final labeling result for each data.
        """
        P_matrix = None
        weight_list = []
        for lf in self.lf_list:
            weight_list.append(lf.weight)

        if strategy == "majority_vote":
            P_matrix = predict_by_majority_vote(LF_matrix, weight_list, is_soft_label)

        return P_matrix


