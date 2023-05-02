import inspect
from query_utils import *

class Query:

    def __init__(self,
                 input_des: dict,
                 label2output: dict,
                 task_des: str = "",
                 api: list = None,
                 api_define_path = "",
                 is_use_default_api: bool = False):
        """Save the task definition and existed api definition.
            Parameters
            ----------
            input_des
                The input description of the task, the key refers to an attribute's name in data
                and the value refers to the meaning of the attribute.
            label2output
                The output description of the task, the key refers to the label
                and the value refers to the corresponding class description.
            task_des (option)
                The task description.
            api (option)
                Existed api functions' declaration.
            api_define_path (option)
                Path of api functions' definition.
            is_use_default_api
                Whether to use default api functions.
        """

        self.input2des = input_des
        self.label2output = label2output
        self.task_des = task_des
        self.is_use_default_api = is_use_default_api
        self.api_list = []

        if is_use_default_api:
            self.api_list = self.get_default_api()
            self.default_api_define_path = 'default_api_define'

        if api is not None:
            self.api_list += api

        self.api_define_path = api_define_path

    def get_default_api(self) -> list:
        """Get default api functions.
            Returns
            -------
            list
                Default api functions.
                Notice that to use the default api, you should have 'text' attribute in data
        """
        from default_api import Label_Func
        func_list = inspect.getmembers(Label_Func, inspect.isfunction)
        api_list = []
        for func in func_list:
            api_list.append(func[1])
        return api_list


    def generate_query(self,
                       label: int,
                       template: str = "",
                       example_list: list = None) -> str:
        """Build query by filling the specific information into corresponding position in the template.
            Parameters
            ----------
            label
                The label that need to be queried for a labeling function.
            template
                The template for building query.
            example_list (option)
                List of example data for this label.

            Returns
            -------
            str
                Query that will be input to the language model.
        """

        input_str = str(self.input2des)
        output_str = str(self.label2output)

        api_str = ""
        if len(self.api_list) > 0:
            for api in self.api_list:
                func_str = inspect.getsource(api)
                api_str += func_str + '\n\n'

        data_str = data_list2str(example_list)

        query = template
        query = query.replace('{input}', input_str)\
                .replace('{output}', output_str)\
                .replace('{task}', self.task_des)\
                .replace('{api}', api_str)\
                .replace('{label}', str(label))\
                .replace('{data}', data_str)
        return query


    def add_api(self, add_api_list):
        """Add new api functions.
            Parameters
            ----------
            add_api_list
                List of added api functions declaration.
        """
        self.api_list += add_api_list








