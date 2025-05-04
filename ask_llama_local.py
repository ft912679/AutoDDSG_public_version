import requests


class AskLlamaLocal:
    def __init__(self, _model_name, _url, _num_ctx, _format=None):
            self.chat_history = []
            self.model_name = _model_name
            self.url = _url
            self.num_ctx = _num_ctx
            self.format = _format
    def ask(self, _prompt, _model_name, _url, _num_ctx, _format=None):
        if _format is None:
            _data = {
                "model": _model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": _prompt
                    }
                ],
                "stream": False,
                # "format": "json",
                "options": {
                    "temperature": 0,
                    "num_ctx": _num_ctx,
                    # "mirostat_tau": 0.1,
                    # "repeat_penalty": 0.1
                },
            }
        else:
            _data = {
                "model": _model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": _prompt
                    }
                ],
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                    "num_ctx": _num_ctx,
                    # "mirostat_tau": 0.1,
                    # "repeat_penalty": 0.1
                },
            }

        _headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(_url, headers=_headers, json=_data)
        return response.json()["message"]["content"]
        

    def ask_with_history(self, _prompt, _model_name, _url, _num_ctx, _format=None):
        self.chat_history.append({"role": "user", "content": _prompt})
        if _format is None:
            _data = {
                "model": _model_name,
                "messages": self.chat_history,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_ctx": _num_ctx,
                },
            }
        else:
            _data = {
                "model": _model_name,
                "messages": self.chat_history,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                    "num_ctx": _num_ctx,
                },
            }

        _headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(_url, headers=_headers, json=_data)
        assistant_response = response.json()["message"]["content"]
        self.chat_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    
    def clear_history(self):
        self.chat_history = []










