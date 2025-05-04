from ask_llm import AskLLM
from configs import Configs
from ask_llama_local import AskLlamaLocal
class SurveyEvaluator:
    def __init__(self):
        self.configs = Configs().configs
        self.ask_llm = AskLLM(
            _aws_llm=self.configs['use_aws_llama'],
            _model_name=self.configs['llm_model_name'],
            _url=self.configs['llm_api_url'],
            _num_ctx=self.configs['llm_context_length']
        )
    def chat(self,channel, _prompt,_format=None):
        return channel.ask(_prompt, self.configs['llm_model_name'], self.configs['llm_api_url'], self.configs['llm_context_length'], _format=_format)
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
    # Example usage
    survey_evaluator = SurveyEvaluator()
    channel = survey_evaluator.create_a_chat_channel()
    criteria_csv="ieee_itsc-main/data/criteria.csv"
    # read the criteria from the CSV file using pandas
    import pandas as pd
    criteria_df = pd.read_csv(criteria_csv)
    survey_saved_folder = "ieee_itsc-main/data/rated_surveys"
    # list all the files that ends with .json in the folder
    import os
    if not os.path.exists(survey_saved_folder):
        raise FileNotFoundError(f"The folder '{survey_saved_folder}' does not exist.")
    survey_files = [f for f in os.listdir(survey_saved_folder) if f.endswith('.json')]
    if not survey_files:
        raise FileNotFoundError(f"No .json files found in the folder '{survey_saved_folder}'.")
    # create an empty dataframe to store the survey ratings
    survey_ratings_df = pd.DataFrame()
    survey_ratings_details_df = pd.DataFrame()
    # loop through each survey file and evaluate it based on the criteria
    for survey_file in survey_files:
        survey_file_path = os.path.join(survey_saved_folder, survey_file)
        print(survey_file)
        # read the survey data from the JSON file using pandas
        survey_df = pd.read_json(survey_file_path)
        # create a myrow dataframe as an emplty dataframe
        myrow = pd.DataFrame()
        # loop through each criterion and evaluate the survey based on it 
        for index, row in criteria_df.iterrows():
            mycriteria = row['Criterion']
            mydescription = row['What to Check For']
            if mycriteria == "Response Quality":# since we don't have any response data, we skip this criterion
                continue
            example_answer="""{"criterion":"Validity","rating": 4, "explanation": "The survey is well-structured and covers most of the necessary topics. However, it could benefit from a few more open-ended questions to gather qualitative feedback."}"""
            prompt = f"We need to evaluate the survey based on the following criterion: {mycriteria}. The description is: {mydescription}. The survey is {survey_df}. Please rate the current survey between 1.0 and 5.0, where 1.0 is the worst and 5.0 is the best. Try to compare with the previous surveys (if there are) and compare with them to get a different rating. Please provide a detailed explanation of your rating. Example answer: {example_answer}"
            if mycriteria == "Data Analysis":
                prompt+="The data analysis is drafted in the 'data_driven_method' and 'data_driven_method_description' fields. If 'data_driven_method' equals to 'yes', that means this question has a data analysis potential and the corresponding 'data_driven_method_description' provides the detailed plan to incoorperate data analysis. Please check if the data analysis is correct and provide a rating and explanation."
            mypreferred_format="json"
            try:
                response = survey_evaluator.chat(channel,prompt,_format=mypreferred_format)
            except:
                print("this criteria has reached the ram limit.")
                response = "{'rating':-1, 'explanation':''}"
                rating = -1
                explanation = ''
            # parse the response to get the rating and explanation
            import json
            try:
                response_json = json.loads(response)
                rating = response_json['rating']
                explanation = response_json['explanation']
                print(f"Criterion: {mycriteria}, Rating: {rating}, Explanation: {explanation}")                
                temp_df = pd.DataFrame({mycriteria: [rating]}, index=[survey_file])
                # append the temporary dataframe to the main dataframe  
                myrow = pd.concat([myrow, temp_df], axis=1)
                # add the explanation to the survey_ratings_details_df
                survey_ratings_details_df = pd.concat([survey_ratings_details_df, pd.DataFrame({'Survey File':[survey_file],'Criterion':[mycriteria],'Rating':[rating],'Explanation':[explanation]})], axis=0)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response: {response}")
            except KeyError:
                print(f"Response format is incorrect: {response}")
        # concat myrow to the survey_ratings_df without resetting the index
        survey_ratings_df = pd.concat([survey_ratings_df, myrow], axis=0)
        survey_ratings_df.to_csv(f"survey_ratings_{survey_file.replace('.json', '')}_{survey_evaluator.configs['llm_model_name'].replace(':', '')}.csv", index=True)
        survey_ratings_details_df.to_csv(f"survey_ratings_details_{survey_file.replace('.json', '')}_{survey_evaluator.configs['llm_model_name'].replace(':', '')}.csv", index=True)
    

    # add a total_rating column survey_ratings_df which is the sum of all the columns
    survey_ratings_df['total_rating'] = survey_ratings_df.sum(axis=1) 
    # save the survey ratings to a CSV file named 'survey_ratings_{time}_{date}.csv'
    import datetime
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    survey_ratings_df.to_csv(f'survey_ratings_{current_time}.csv', index=True)
    # save the survey ratings details to a CSV file named 'survey_ratings_details_{time}_{date}.csv'
    survey_ratings_details_df.to_csv(f'survey_ratings_details_{current_time}.csv', index=True)