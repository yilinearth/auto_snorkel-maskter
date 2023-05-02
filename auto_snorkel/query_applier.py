from query import Query
from query_utils import *
from label_function import LF
import time
import openai

class QueryApplier:
    def __init__(self,
                 query: Query,
                 api_key: str,
                 model_name: str,
                 func_path: str = ""):
        """Query the language model for labeling functions.
            Parameters
            ----------
            query
                The Query object that containing task specific information.
            api_key
                The user's api key to connect to the language model.
            model_name
                The name of language model.
            func_path (option)
                The path to write the labeling functions.
        """
        self.query = query
        self.api_key = api_key
        self.model_name = model_name

        if len(func_path) == 0:
            time_str = str(time.time()).replace('.', '_')
            func_path = 'label_func_{}.py'.format(time_str)

        self.func_path = func_path
        self.init_func_path()

    def init_func_path(self):
        """ Write the modules that need to be import to running the labeling functions."""
        f = open(self.func_path, 'a')
        if self.query.is_use_default_api:
            f.write('from {} import * \n'.format(self.query.default_api_define_path))
        if len(self.query.api_define_path) > 0:
            f.write('from {} import * \n'.format(self.query.api_define_path))

        f.close()

    def build_default_template(self, is_use_example_data: bool = False) -> str:
        """Get default template for building query.
            Parameters
            ----------
            is_use_example_data
                Whether the user wants to put the example data in the query.

            Return
            ----------
            str
                The default template
        """
        default_template_list = []

        if len(self.query.task_des) > 0:
            default_template_list.append("Task description: {task}. ")

        default_template_list.append("The inputs and outputs definitions of the task are shown as follow. "
                                     "The definition of inputs are: {input}. "
                                     "The definition of output labels are: {output}. ")

        if len(self.query.api_list) > 0:
            default_template_list.append("Available api function:\n {api}")

        if is_use_example_data:
            default_template_list.append("The example data list as follows: \n{data}")

        default_template_list.append("TODO: Write a labeling function for the label {label}. ")

        default_template = "\n\n".join(default_template_list)
        return default_template

    def build_prompt(self,
                     label,
                     example_list: list = None,
                     template: str = "") -> str:
        """Get default template for building query.
            Parameters
            ----------
            label
                The label that need to be queried for a labeling function.
            example_list (option)
                List of example data for this label.
            template (option)
                Template for building query.
                Notice that if the user does not input the template, the default one will be applied.

            Return
            ----------
            str
                The query that will input to the language model.
        """
        # build the default template, if the input template is empty
        if len(template) == 0:
            is_use_example_data = True if len(example_list) != 0 else False
            template = self.build_default_template(is_use_example_data)

        # instantiate the template with specific information
        query = self.query.generate_query(label, template=template, example_list=example_list)

        ######
        # file = 'sst/tmp_{}.txt'.format(label)
        # f = open(file, 'w')
        # f.write(query)
        # f.close()
        # pdb.set_trace()

        return query

    def get_request(self,
                    prompt: str,
                    max_token: int = 1000,
                    stop: str = None,
                    temperature: float = None,
                    timeout: float = 1000,
                    ) -> str:
        """Input the query into language model and get the request.
            Parameters
            ----------
            prompt
                The input query.
            max_token (option)
                The max token number of the request.
            stop (option)
                Where the API will stop generating further tokens.
            temperature (option)
                The sampling temperature.
            timeout (option)
                The timeout for getting the request.

            Return
            ----------
            str
                The output request.
        """
        completion = openai.Completion.create(
            engine=self.model_name,
            prompt=prompt,
            max_tokens=max_token,
            n=1,
            stop=stop,
            temperature=temperature,
            timeout=timeout,
        )

        response = str(completion.choices[0].text).strip()

        return response

    def predict_lf(self,
                   label: int,
                   example_list: list = None,
                   lf_num: int = 1,
                   example_num: int = 1,
                   example_strategy: str = "random",
                   template: str = "",
                   max_token: int = 1000,
                   stop: str = None,
                   temperature: float = 0.5,
                   timeout: float = 1000,
                   ) -> list:
        """Input the query into language model and get the request.
            Parameters
            ----------
            label
                The label that need to be queried for label functions.
            example_list (option)
                List of example data for this label.
            lf_num (option)
                Expect number of the label functions.
            example_num (option)
                Expect number of the example data for generating each labeling function.
            example_strategy (option)
                The strategy to sample example data.
            template (option)
                The template for building the query
            max_token (option)
                The max token number of the request.
            stop (option)
                Where the API will stop generating further tokens.
            temperature (option)
                The sampling temperature.
            timeout (option)
                The timeout for getting the request.

            Return
            ----------
            list
                The list of labeling function.
        """

        func_list = []

        for func_id in range(lf_num):
            # sample example data
            sample_list = []
            if len(example_list) > 0 and example_num > 0:
                sample_list = sample_example_list(example_list, example_num, example_strategy)

            # build prompt
            prompt = self.build_prompt(label, sample_list, template)

            ######
            # frame = __import__('sst_label_func')
            # label_func = getattr(frame, 'label_func_num_0_label_0')
            # import inspect
            # lf_str = inspect.getsource(label_func)

            lf_str = self.get_request(prompt,
                                      max_token=max_token,
                                      stop=stop,
                                      temperature=temperature,
                                      timeout=timeout)

            # fix label function's name
            lf_str = fix_func_str(lf_str, func_id, label)

            # write function and import function
            lf = LF(lf_str, self.func_path)

            func_list.append(lf)

        return func_list



    def predict_lfs(self,
                    example_list: list = None,
                    lf_num: int = 1,
                    example_num: int = 1,
                    example_strategy: str = "random",
                    template: str = "",
                    max_token: int = 1000,
                    stop: str = None,
                    temperature: float = 0.5,
                    timeout: float = 1000,
                    ) -> list:
        """Build query and get request for all the labels.
            Parameters
            ----------
            example_list (option)
                List of example data.
            lf_num (option)
                Expect number of the labeling functions (per label).
            example_num (option)
                Expect number of the example data for generating each labeling function (per label).
            example_strategy (option)
                The strategy to sample example data.
            template (option)
                The template for building the query
            max_token (option)
                The max token number of the request.
            stop (option)
                Where the API will stop generating further tokens.
            temperature (option)
                The sampling temperature.
            timeout (option)
                The timeout for getting the request.

            Return
            ----------
            list
                The list of labeling function.
        """

        label2example_list = get_label2example_list(example_list)
        lf_list = []

        for label in self.query.label2output:

            exp_list = []

            if label in label2example_list:
                exp_list = label2example_list[label]
            exp_num = min(len(exp_list), example_num)

            lfs = self.predict_lf(
                label,
                example_list=exp_list,
                lf_num=lf_num,
                example_num=exp_num,
                example_strategy=example_strategy,
                template=template,
                max_token=max_token,
                stop=stop,
                temperature=temperature,
                timeout=timeout)
            lf_list += lfs

        return lf_list
