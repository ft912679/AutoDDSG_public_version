from ask_llama_local import AskLlamaLocal
from ask_llama_aws import AskLlamaAWS
class AskLLM:
    def __init__(self, _aws_llm, _model_name, _url, _num_ctx, _format=None):
        self.aws_llm = _aws_llm
        self.model_name = _model_name
        self.url = _url
        self.num_ctx = _num_ctx
        self.format = _format

    def ask(self, _prompt):
        
        if self.aws_llm:
            _response = AskLlamaAWS().ask(_prompt)
        else:
            _response = AskLlamaLocal().ask(
                _prompt=_prompt,
                _model_name=self.model_name,
                _url=self.url,
                _num_ctx=self.num_ctx,
                _format=self.format
            )

        return _response
        
