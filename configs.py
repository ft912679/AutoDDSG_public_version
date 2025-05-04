class Configs:
    def __init__(self):
        self.configs = dict()
        # set your llm model name here
        self.configs['llm_model_name'] ='llama3.1:70b'
        #'llama3.1:70b'
        #'gemma3:4b' not working 
        # #' working
        # deepseek-r1:8b' working but with error in replied json format, the answer may not use the sample format provided in the prompt.
        # qwq return "Response format is incorrect: {}"

        # set your llm api url here
        self.configs['llm_api_url'] = 'http://localhost:11434/api/chat'
        # set context length here
        self.configs['llm_context_length'] = 20480
        # set using local or aws Llama here
        self.configs['use_aws_llama'] = False
        # self.configs['use_aws_llama'] = False

        ####################################
        # Yuming's configurations
        ####################################
        # # set your data root folder here
        # self.configs['data_root_folder'] = '/Users/999551/UTS/PIA/email_classification/'
        # # class list file
        # self.configs['class_list_file_path'] = 'class_list/Repair portal_Maintenance Types_3.csv'
        # # yuming debugging mode
        # self.configs['yuming_debug_mode'] = True


        ####################################
        # Tuo's configurations
        ####################################
        # set your data root folder here
        self.configs['data_root_folder'] = r'/home/tmao/Data/2024 PIA'
        # class list file
        self.configs['class_list_file_path'] = r"/home/tmao/Data/2024 PIA/Repair portal_Maintenance Types_3.csv"#r"Repair portal_Maintenance Types_3.csv"
        # yuming debugging mode
        self.configs['yuming_debug_mode'] = False

    # return root folder
    def get_data_root_folder(self):
        return self.configs['data_root_folder']

    # return llm model name
    def get_llm_model_name(self):
        return self.configs['llm_model_name']

    # return llm api url
    def get_llm_api_url(self):
        return self.configs['llm_api_url']

    # return llm context length
    def get_llm_num_ctx(self):
        return self.configs['llm_context_length']

    # return class list file path
    def get_class_list_file_path(self):
        return self.configs['class_list_file_path']

    # return if it is using aws llama
    def get_is_aws_llm_used(self):
        return self.configs['use_aws_llama']

    def get_yuming_debug_mode(self):
        return self.configs['yuming_debug_mode']