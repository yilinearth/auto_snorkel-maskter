import numpy as np
import sklearn.metrics as cls_metric
from lf_utils import *
from label_function import LF

class LFAnalysis:
    def __init__(self, lfs: list = None, lf_func_path: str = "", is_load_from_file: bool = False):
        """Analysis the labeling functions performance.
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

    def eval(self, gold_labels, pred_labels):
        """Evaluate the labeling performance based on the gold labels and predicted labels
            Parameters
            ----------
            gold_labels
                The list of ground truth labels
            pred_labels
                The list of predicted labels.

            Return
            ----------
            dict
                The evaluated results for each criteria.
        """
        mic_prec = cls_metric.precision_score(gold_labels, pred_labels, average='micro')
        mic_f1 = cls_metric.f1_score(gold_labels, pred_labels, average='micro')
        mic_rec = cls_metric.recall_score(gold_labels, pred_labels, average='micro')
        return {'mic_prec': mic_prec, 'mic_rec': mic_rec, 'mic_f1': mic_f1}




    #get the predict precision and recall for each label function
    def eval_on_data (self, gold_labels: list, LF_matrix: np.array, is_display: bool = False):
        """Evaluate the labeling performance
            Parameters
            ----------
            gold_labels
                The list of ground truth labels.
            LF_matrix
                The labeling result for each data given by each labeling function.
            is_display
                Whether to display the evaluated result.

            Return
            ----------
            list
                The evaluated result for each labeling function.
        """
        res_list = []
        LF_num = LF_matrix.shape[1]

        for i in range(LF_num):
            pred_labels = LF_matrix[:, i]
            res = self.eval(gold_labels, pred_labels)
            res_list.append(res)

        if is_display:
            print(res_list)

        return res_list


    def reweight_lfs (self, weight_list: list):
        """reweight the labeling functions based on their performance.
            Parameters
            ----------
            weight_list
                The new weight for each labeling function.

        """
        for i in range(len(weight_list)):
            self.lf_list[i].weight = weight_list[i]







