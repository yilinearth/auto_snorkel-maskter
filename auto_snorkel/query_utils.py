from random import sample

def data2str(data) -> str:
    """Turn a data into string.
        Parameters
        ----------
        data
            The input data.

        Return
        -------
        str
            The string format of the data.
    """
    data_str = ""
    for key in data.keys():
        data_str += "{}: {}".format(key, data[key])
        data_str += '\n'
    return data_str


def data_list2str(data_list: list) -> str:
    """Turn a data list into string.
        Parameters
        ----------
        data_list
            The input data list.

        Return
        -------
        str
            The string format of the data list.
    """
    if len(data_list) == 0:
        return ""

    data_list_str = ""
    for data in data_list:
        data_str = data2str(data)
        data_list_str += data_str + '\n'

    return data_list_str


# TODO: add more strategy
def sample_example_list(example_list: list,
                        example_num: int,
                        example_strategy: str
                        ) -> list:
    """Sample example data.
        Parameters
        ----------
        example_list
            List of example data for this label.
        example_num
            The sample number of example data.
        example_strategy
            The sample strategy.
        Return
        -------
        list
            The list of sampled example data.
    """
    if example_strategy == "random":
        sample_list = sample(example_list, example_num)
        return sample_list
    else:
        raise ValueError(f"Unrecognized example strategy: {example_strategy}")


# fix the name of label function
def fix_func_str(org_func_str: str, func_id: int, label: int) -> str:
    """Standardize the labeling function's name.
        Parameters
        ----------
        org_func_str
            Original labeling function.
        func_id
            The index of the labeling function.
        label
            The label of the labeling function.
        Return
        -------
        str
            Standardize labeling function.
    """
    func_name = 'def label_func_num_{}_label_{}'.format(func_id, label)
    first_idx = org_func_str.find('(')
    lf_str = org_func_str[first_idx:]
    lf_str = func_name + lf_str
    return lf_str

def get_label2example_list(example_list) -> dict:
    """Group the example data by their labels.
        Parameters
        ----------
        example_list
            List of example data.

        Return
        ----------
        dict
            The key is the label and the value is the corresponding example list.
    """
    label2exp_list = {}
    for data in example_list:
        curr_label = data.label
        if curr_label not in label2exp_list:
            label2exp_list[curr_label] = []
        label2exp_list[curr_label].append(data)
    return label2exp_list

