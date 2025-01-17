# -*- coding: UTF-8 -*-
import base64
import hmac
import json, logging
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from websocket import create_connection, WebSocketConnectionClosedException
from sparkdesk_api.utils import get_prompt, process_response, is_support_version


class SparkAPI:
    __api_url = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 默认为Spark Max
    __domain = 'generalv3.5'
    __max_tokens = 4096 # 取值为[1,8192]，默认为4096。 模型回答的tokens的最大长度
    __temperature = 0.5  # 取值为(0.0,1.0]，默认为0.5。 核采样阈值。用于决定结果随机性，取值越高随机性越强即相同的问题得到的不同答案的可能性越高

    def __init__(self, app_id, api_key, api_secret, version=None, assistant_id=None):
        self.__app_id = app_id
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__history = []
        # 配置版本
        if version is not None and is_support_version(version):
            self.__set_version(version)

        # 助手API
        if assistant_id is not None:
            self.__api_url = f'wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/{assistant_id}'
            self.__domain = 'general'

    def __set_temperature(self, temperature):
        if isinstance(temperature, float) is False or temperature <= 0 or temperature > 1:
            print("set_temperature() error: temperature should be a float between 0 and 1!")
            return
        self.__temperature = temperature

    def __set_version(self, version):
        # Spark Lite
        if version == 1.1:
            self.__api_url = 'wss://spark-api.xf-yun.com/v1.1/chat'
            self.__domain = 'general'
        # Spark V2.0
        elif version == 2.1:
            self.__api_url = 'wss://spark-api.xf-yun.com/v2.1/chat'
            self.__domain = 'generalv2'
        # Spark Pro
        elif version == 3.1:
            self.__api_url = 'wss://spark-api.xf-yun.com/v3.1/chat'
            self.__domain = 'generalv3'
        # Spark Max
        elif version == 3.5:
            self.__api_url = 'wss://spark-api.xf-yun.com/v3.5/chat'
            self.__domain = 'generalv3.5'
        # Spark Ultra
        elif version == 4.0:
            self.__api_url = 'wss://spark-api.xf-yun.com/v4.0/chat'
            self.__domain = '4.0Ultra'

    def __set_max_tokens(self, token):
        if isinstance(token, int) is False or token < 0:
            print("set_max_tokens() error: tokens should be a positive integer!")
            return
        self.__max_tokens = token

    def update_config(self,app_id=None, api_secret=None, api_key=None, version=None, token=None, temperature=None):
        if app_id is not None:
            self.__app_id = app_id
        if api_key is not None:
            self.__api_key = api_key
        if api_secret is not None:
            self.__api_secret = api_secret
        if version is not None:
            self.__set_version(version)
        if token is not None:
            self.__set_max_tokens(token)
        if temperature is not None:
            self.__set_temperature(temperature)
    
    """
    doc url: https://www.xfyun.cn/doc/spark/general_url_authentication.html
    """

    def __get_authorization_url(self):
        authorize_url = urlparse(self.__api_url)
        # 1. generate data
        date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %Z')

        """
        Generation rule of Authorization parameters
            1) Obtain the APIKey and APISecret parameters from the console.
            2) Use the aforementioned date to dynamically concatenate a string tmp. Here we take Huobi's URL as an example, 
                the actual usage requires replacing the host and path with the specific request URL.
        """
        signature_origin = "host: {}\ndate: {}\nGET {} HTTP/1.1".format(
            authorize_url.netloc, date, authorize_url.path
        )
        signature = base64.b64encode(
            hmac.new(
                self.__api_secret.encode(),
                signature_origin.encode(),
                digestmod='sha256'
            ).digest()
        ).decode()
        authorization_origin = \
            'api_key="{}",algorithm="{}",headers="{}",signature="{}"'.format(
                self.__api_key, "hmac-sha256", "host date request-line", signature
            )
        authorization = base64.b64encode(authorization_origin.encode()).decode()
        params = {
            "authorization": authorization,
            "date": date,
            "host": authorize_url.netloc
        }

        ws_url = self.__api_url + "?" + urlencode(params)
        return ws_url

    def __build_inputs(
            self,
            message: dict,
            user_id: str = "001",
            temperature: float = 0.5,
            max_tokens: int = 2048
    ):
        temperature = self.__temperature
        max_tokens = self.__max_tokens
        
        input_dict = {
            "header": {
                "app_id": self.__app_id,
                "uid": user_id,
            },
            "parameter": {
                "chat": {
                    "domain": self.__domain,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            },
            "payload": {
                "message": message
            }
        }
        return json.dumps(input_dict)

    def chat(
            self,
            query: str,
            history: list = None,  # store the conversation history
            user_id: str = "001",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        temperature = self.__temperature
        max_tokens = self.__max_tokens
        
        if history is None:
            history = []

        # the max of max_length is 8192
        max_tokens = min(max_tokens, 8192)
        url = self.__get_authorization_url()
        ws = create_connection(url)
        message = get_prompt(query, history)
        input_str = self.__build_inputs(
            message=message,
            user_id=user_id,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        ws.send(input_str)
        response_str = ws.recv()
        try:
            while True:
                response, history, status = process_response(response_str, history)
                """
                The final return result, which means a complete conversation.
                doc url: https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
                """
                if len(response) == 0 or status == 2:
                    if not response and history and history[-1]["role"] == "assistant":
                        response = history[-1]["content"]
                    break
                response_str = ws.recv()
            return response

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()

    # Stream output statement, used for terminal chat.
    def __streaming_output(
            self,
            query: str,
            history: list = None,  # store the conversation history
            user_id: str = "001",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        max_tokens = self.__max_tokens
        temperature = self.__temperature
        
        if history is None:
            history = []

        # the max of max_length is 4096
        max_tokens = min(max_tokens, 4096)
        url = self.__get_authorization_url()
        ws = create_connection(url)

        message = get_prompt(query, history)
        input_str = self.__build_inputs(
            message=message,
            user_id=user_id,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # send question or prompt to url, and receive the answer
        ws.send(input_str)
        response_str = ws.recv()

        # Continuous conversation
        try:
            while True:
                response, history, status = process_response(response_str, history)
                yield response, history
                if len(response) == 0 or status == 2:
                    break
                response_str = ws.recv()

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()

    def chat_stream(self):
        history = []
        print("Enter exit or stop to end the converation.\n")
        try:
            while True:
                query = input("Ask: ")
                if query == "exit" or query == "stop":
                    break
                for response, _ in self.__streaming_output(query, history):
                    print("\r" + response, end="")
                print("\n")
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                print(e)
        finally:
            print("\nThank you for using the SparkDesk AI. Welcome to use it again!")
    
    def chat_stream_api(self, query):
        try:
            return_response = []
            for response, _ in self.__streaming_output(query, self.__history):
                return_response.append(response)
            return return_response[-1]
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                print(e)

app_id="e8bd2492"
api_secret="MGY1MjIzMDk1MTQ4Y2U1YzUxMWI5Yzk1"
api_key="28b98e55ec8e83daddf1e591952e2614"

if __name__ == '__main__':
    test_ai = SparkAPI(
        app_id=app_id,
        api_secret=api_secret,
        api_key=api_key
    )
    print(test_ai.chat_stream_api("我叫小明，今年18岁了。"))
    print(test_ai.chat_stream_api("我叫什么，今年多少岁了？"))
    