from ask_llm import AskLLM
from configs import Configs
from ask_llama_local import AskLlamaLocal

class SurveyReviser:
    def __init__(self):
        self.configs = Configs().configs
        self.ask_llm = AskLLM(
            _aws_llm=self.configs['use_aws_llama'],
            _model_name=self.configs['llm_model_name'],
            _url=self.configs['llm_api_url'],
            _num_ctx=self.configs['llm_context_length']
        )
        
    def create_a_chat_channel(self):
        self.ask_llm = AskLlamaLocal(_model_name=self.configs['llm_model_name'],
            _url=self.configs['llm_api_url'],
            _num_ctx=self.configs['llm_context_length'])
        return self.ask_llm
    def chat_with_history(self,channel, _prompt,_format=None):
        return channel.ask_with_history(_prompt, self.configs['llm_model_name'], self.configs['llm_api_url'], self.configs['llm_context_length'], _format=_format)
    def clear_chat_history(self, channel):
        channel.chat_history = []
        return True
    def check_chat_history(self,channel):
        return channel.chat_history

if __name__ == "__main__":
    import pandas as pd
    # load the big data base
    # big_db= pd.read_csv(r"C:\Users\142685_admin\OneDrive - UTS\Future Transport Mobility Work\WORK - PROJECTS\2024\JETCHARGE\Data-Illuminate\0_big_Illuminate_data_2025Mar.csv")
    big_db= pd.read_csv("data/big_data.txt",sep='\t')
    big_db['transaction_start'] = pd.to_datetime(big_db['transaction_start'])
    big_db['IntervalStartUtc'] = pd.to_datetime(big_db['IntervalStartUtc'])
    # convert the data.describe() to a string
    # convert the dataframe big_db.describe() to a string that explains the data
    csv_description = ""
    for each in big_db.describe().columns:
        csv_description += f"{each}: {big_db[each].describe()}\n".replace("\n",",")
        csv_description += ".\n"
    # for the columns that are not in the describe, we need to add them to the csv_description by using the top 5 unique values of the column
    csv_description2 = ""
    for each in big_db.columns:
        if each not in big_db.describe().columns:
            csv_description2 += f"{each}: {big_db[each].unique()[:5]}\n".replace("\n",",")
            csv_description2 += ".\n"
    # read the criteria from the CSV file using pandas
    criteria_csv="data/criteria.csv"
    criteria_df = pd.read_csv(criteria_csv)
    # create a string to contain all the criteria and what to check for
    criteria_str = ""
    for index, row in criteria_df.iterrows():
        mycriteria = row['Criterion']
        mydescription = row['What to Check For']
        criteria_str += f"{mycriteria}: {mydescription}.\n".replace("\n",",")
        criteria_str += ".\n"

    number_of_trials=3
    # read the baseline survey from the json file
    base_survey_file_path = "revised_survey_llama3.1_2025-04-28_11-32-21.json"
    # read the survey data from the JSON file using json
    import json
    with open(base_survey_file_path, 'r') as f:
        base_survey = json.load(f)
    previous_survey = base_survey
    # # create a survey generator object
    # survey_generator = SurveyGenerator()
    # # create a chat channel
    # mychannel = survey_generator.create_a_chat_channel()
    # # clear the chat history
    # survey_generator.clear_chat_history(mychannel)
    for i in range(number_of_trials):
        # create a survey generator object
        survey_generator = SurveyReviser()
        # create a chat channel
        mychannel = survey_generator.create_a_chat_channel()
        # clear the chat history
        survey_generator.clear_chat_history(mychannel)
        question = "Generate a survey for customer satisfaction for a Electric Vehicle charger."
        preferred_format = "json"
        preferred_example = """{
        "title": "Customer Satisfaction Survey",

    "description": "We appreciate your feedback! Please take a few minutes to answer the following questions.",
    "questions": [
        {
        "id": 1,
        "type": "single_choice",
        "question": "How satisfied are you with our service?",
        "options": [
            "Very satisfied",
            "Satisfied",
            "Neutral",
            "Dissatisfied",
            "Very dissatisfied"
        ],
        "data_driven_method": "No",
        "data_driven_method_description": ""
        },
        {
        "id": 2,
        "type": "multiple_choice",
        "question": "Which of the following products have you used? (Select all that apply)",
        "options": [
            "Product A",
            "Product B",
            "Product C",
            "Product D"
        ],
        "data_driven_method": "No",
        "data_driven_method_description": ""
        },
        {
        "id": 3,
        "type": "rating",
        "question": "Rate the quality of our customer support:",
        "scale": {
            "min": 1,
            "max": 5,
            "labels": {
            "1": "Very poor",
            "5": "Excellent"
            }
        },
        "data_driven_method": "No",
        "data_driven_method_description": ""
        },
        {
        "id": 4,
        "type": "text",
        "question": "What can we do to improve your experience?",
        "placeholder": "Your feedback here...",
        "data_driven_method": "No",
        "data_driven_method_description": ""
        }
    ]
    }"""
        data_description="""
    The available dataset contains detailed operational and transactional records for a network of electric vehicle (EV) chargers, collected at 15-minute intervals for a whole year between 1 Dec 2023 and 1 Dec 2024. Each row represents a snapshot of a charger’s status and activity at a specific time. The columns DeviceIdentity, DeviceType, and ConnectorIndex define the charger identity, the type of device (such as Level 2 AC or DC fast charger), and the specific connector used in the session. ManagedBy specifies the entity responsible for managing the device, whether an operator, third-party service, or internal team.
    The transaction-related columns, including transaction_start, transaction_end, MeterStart, and MeterStop, record the exact start and end times of charging sessions and the corresponding meter readings. These readings are used to calculate the energy delivered during the session. ReservationId associates the session with a reservation when applicable. Odometer captures the mileage of the vehicle at the time of charging, while VehicleId uniquely identifies the vehicle connected to the charger. StopTransactionReason records the reason why a charging session concluded, such as user termination, full charge, or error.
    Device metadata is stored in device_create_t, device_update_t, and device_operational_t, tracking when the device was registered, last updated, and last became operational (if a device has been offline and repaired). device_lat and device_lon provide the latitude and longitude coordinates of the charger. device_add, Vendor, Model, Status, and TimeZone further detail the device's address, manufacturer, model name, current status (active, maintenance, offline), and its timezone setting.
    IntervalStartUtc marks the start of each 15-minute reporting window. FrequencyHz captures the electrical frequency, while PowerkW measures the real-time delivered power. Voltage and current across the three electrical phases are monitored via L1VoltageRmsV, L2VoltageRmsV, L3VoltageRmsV, L1CurrentRmsA, L2CurrentRmsA, and L3CurrentRmsA. Active and reactive power measurements (L1ActivePowerRmsW, L2ActivePowerRmsW, L3ActivePowerRmsW, L1ReactivePowerRmsVar, L2ReactivePowerRmsVar, L3ReactivePowerRmsVar) allow for detailed power quality analysis.
    Energy accumulations are tracked through TotalActiveEnergyImportWh and TotalActiveEnergyExportWh, as well as TotalReactiveEnergyImportWh and TotalReactiveEnergyExportWh. The system also monitors renewable energy contributions with SolarActivePowerImportW and SolarEnergyImportWh. The SoC (State of Charge) records the battery level of the connected EV. ProfileCurrentOfferedA specifies the maximum current that the charger is offering to the vehicle at that interval.
    Finally, grid interactions are captured with GridActiveEnergyExportWh, GridActiveEnergyImportWh, GridActivePowerExportW, and GridActivePowerImportW. Pricing information is stored in TotalCost, which reflects the cost incurred during the session, and PricingScheduleId, which identifies the pricing model (hour-of-the-day dependent price profiles) applied to the transaction.
    """
        if previous_survey is None:
            prompt = f"Generate a survey for customer satisfaction, charging behavior, preferred charging time, preferred unplug time,  for a Electric Vehicle charger provider considering the available dataset and think about the data-driven method to revise the survey. The case study topic is defined as 'the satisfaction of the user for an EV charger in an EV fleet within a company'. The major target of this survey is to identify whether the customer is satisfied with the charging experience for a certain brand of EV charger in their company, which operates EV fleets for various purposes.  The requirements and available dataset description are: {data_description}. Detailed description of the current investigated company are: {csv_description}. Example values of each column in the dataset are: {csv_description2}. The survey should be in the following format: {preferred_example}"
        else:
            prompt = f"Based on the previous survey: {previous_survey}. Improve the survey for customer satisfaction, charging behavior, preferred charging time, preferred unplug time, for a Electric Vehicle charger provider considering the available dataset and think about the data-driven method to revise the survey.  The case study topic is defined as 'the satisfaction of the user for an EV charger in an EV fleet within a company'. The major target of this survey is to identify whether the customer is satisfied with the charging experience for a certain brand of EV charger in their company, which operates EV fleets for various purposes. The improvements can be based on the criteria: {criteria_str}. The improvement can be adding or deleting questions, the revision of the 'data_driven_method_description', the revision of the question based on previous 'data_driven_method_description'.  The available dataset description are: {data_description}. Detailed description of the current investigated company are: {csv_description}. Example values of each column in the dataset are: {csv_description2}. The survey should be in the following format: {preferred_example}"
        response = survey_generator.chat_with_history(mychannel,prompt,_format=preferred_format)
        print(response)

        # start revision of the survey
        import json
        v0 = json.loads(response)
        # for eachQ in v0['questions']:
        #     # Check if the question can be revised based on the dataset
        #     preferred_example1= """{"question": "How satisfied are you with our service?", "type":"single_choice", "options":["Very satisfied",
        #     "Satisfied",
        #     "Neutral",
        #     "Dissatisfied",
        #     "Very dissatisfied"],"data_driven_method": "No", "data_driven_method_description": ""}"""
        #     prompt1= f"Revise the survey question {eachQ['id']}: {eachQ}. Revise its contents and improve the 'data_driven_method_description' based on the available dataset, the dataset description is: {data_description}.The answer should be in the following format: {preferred_example1}"
        #     response1 = survey_generator.chat_with_history(mychannel,prompt1,_format=preferred_format)
        #     print(response1)
        #     json1 = json.loads(response1)
        #     # replace the question with the revised question
        #     eachQ['question'] = json1['question']
        #     eachQ['type'] = json1['type']
        #     # check if the type is rating, then add the scale and labels
        #     if eachQ['type'] == "rating":
        #         eachQ['scale'] = json1['scale']
        #     else:
        #         # remove the scale and labels if the type is not rating
        #         eachQ.pop('scale', None)
        #         eachQ.pop('labels', None)
        #     # check if the type is text, then add the placeholder
        #     if eachQ['type'] == "text":
        #         eachQ['placeholder'] = json1['placeholder']
        #     else:
        #         # remove the placeholder if the type is not text
        #         eachQ.pop('placeholder', None)
        #     # check if the type is multiple_choice, then add the options
        #     if eachQ['type'] == "multiple_choice":
        #         eachQ['options'] = json1['options']
        #     else:
        #         # remove the options if the type is not multiple_choice
        #         eachQ.pop('options', None)
        #     # check if the type is single_choice, then add the options
        #     if eachQ['type'] == "single_choice":
        #         eachQ['options'] = json1['options']
        #     else:
        #         # remove the options if the type is not single_choice
        #         eachQ.pop('options', None)
        #     eachQ['data_driven_method'] = json1['data_driven_method']
        #     try:
        #         eachQ['data_driven_method_description'] = json1['data_driven_method_description']
        #     except KeyError as e:
        #         print(f"KeyError: {e} - 'data_driven_method_description' not found in the response.")
        #         # eachQ['data_driven_method_description'] = "No data-driven method applied."
        #     if eachQ['data_driven_method'] == "Yes":
        #         # ask the llm to write me a python script to analyze the data and generate a llm readable output
        #         preffered_example2 = """{"python_script": "import pandas as pd\n\ndef analyze_data(data):\n    # Perform data analysis here\n    result = data.describe()\n    return result\n\n# Load the dataset\ndata = pd.read_csv('dataset.csv')\n\n# Analyze the data\nresult = analyze_data(data)\nprint(result)"}"""
        #         current_data_reading_code="""import pandas as pd \nbig_db= pd.read_csv(r"C:\\Users\\142685_admin\\OneDrive - UTS\\Future Transport Mobility Work\\WORK - PROJECTS\\2024\\JETCHARGE\\Data-Illuminate\\big_data.txt",sep='\t')"""
        #         prompt2 = f"Write a python script to analyze the data and generate a llm readable output for the question: {eachQ['question']} based on the dataset description: {data_description}. The method is {eachQ['data_driven_method_description']}. The data reading code is {current_data_reading_code}. The preferred example is: {preffered_example2}"
        #         response2 = survey_generator.chat_with_history(mychannel,prompt2,_format="json")
        #         print(response2)
        #         json2 = json.loads(response2)
        #         mycode = json2['python_script']
        #         # try to run the python code and get the output
        #         try:
        #             exec(mycode)
        #             # get the result from the code
        #             result = locals()['result']
        #             # convert the result to a string
        #             result_str = str(result)
        #             eachQ['data_driven_method_description'] += f"Data-driven method applied. Python code generated is: {mycode}. The result is: {result_str}"
        #         except Exception as e:
        #             print(f"Error executing code: {e}")
        #             eachQ['data_driven_method_description'] += f"Data-driven method applied. Python code generated is: {mycode}. The code returns an error: {e}"
                    
        #     else:
        #         eachQ['data_driven_method_description'] = "No data-driven method applied."
        #     # update V0 with the revised question
        #     v0['questions'][eachQ['id']-1] = eachQ
        


        
        import datetime
        now = datetime.datetime.now()
        # save the revised survey to a json file
        with open(f'revised_survey_{survey_generator.configs['llm_model_name'].replace(":","_").replace("-","_")}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json', 'w') as f:
            json.dump(v0, f, indent=4)
        previous_survey = v0
        # save the chatting history to a txt file with the name of current time and date and the config.model_name
        
        filename = f"chat_history_{survey_generator.configs['llm_model_name'].replace(":","_").replace("-","_")}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, 'w') as f:
            for each in mychannel.chat_history:
                f.write(f"{each['role']}: {each['content']}\n")
    