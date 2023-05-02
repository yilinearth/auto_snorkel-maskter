from lf_utils import *
import os

class LF:
    def __init__(self,
                 lf_str: str = "",
                 func_path: str = "",
                 weight: float = 1.0,
                 lf_name: str = "",
                 is_load_func: bool = False,
                 ):
        """Save the labeling function information and predict data.
            Parameters
            ----------
            lf_str
                The definition of labeling function.
            func_path
                The path to write and save the labeling function.
            weight
                The weight of the labeling function.
            lf_name
                Function's name.
            is_load_func
                Whether to load the function directly from the func_path.
        """
        self.weight = weight
        self.func_path = func_path

        # just need to import function
        if is_load_func:
            if len(lf_name) == 0 or not os.path.exists(self.func_path):
                raise ValueError(f"There is no existed function to load.")

            self.lf_name = lf_name
            frame = get_module(self.func_path)
            self.lf = getattr(frame, self.lf_name)

        # need to write function and import it
        else:
            if len(lf_str) == 0:
                raise ValueError(f"The function definition is missed.")

            self.lf_str = lf_str
            # get the function's name
            if lf_name == "":
                start_idx = lf_str.find('def')
                end_idx = lf_str.find('(')
                self.lf_name = lf_str[start_idx + 3: end_idx].strip()
            else:
                self.lf_name = lf_name

            self.lf = self.write_and_import_func()


    def write_and_import_func(self):
        """Write the function's definition and import the function."""
        f = open(self.func_path, "a")
        f.write(self.lf_str + '\n')
        f.close()

        # get module name
        frame = get_module(self.func_path)

        # get label function
        label_func = getattr(frame, self.lf_name)

        return label_func

    def predict(self, data) -> int:
        """Predict the data.
            Parameters
            ----------
            data
                The input data

            Return
            ----------
            label
                The predicted label of the data.
        """
        label = self.lf(data)
        return label


