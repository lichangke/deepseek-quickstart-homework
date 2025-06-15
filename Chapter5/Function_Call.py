import os
from openai import OpenAI

# 从环境变量获取 DeepSeek API Key
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")

# 定义工具
tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": { # parameters (JSON Schema 对象，定义⼯具所需的参数)
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        },
    }
]

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",  # DeepSeek API 的基地址
)

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

# 1. ⽤户发起请求，将请求和定义的 tools 传递给 DeepSeek。
messages = [{"role": "user", "content": "How's the weather in Shanghai?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")
# 2. DeepSeek 判断需要调⽤⼯具，返回⼀个包含 tool_calls 的响应。
# 3. 开发者解析 tool_calls， 根据 name 和 arguments 调⽤对应的实际⼯具。
tool = message.tool_calls[0]
print(tool)
# 执行 tool 工具 获取 结果
# 4. 将⼯具执⾏结果作为 tool_message 再次发送给 DeepSeek，让模型继续处理。
# 模拟 search_web 工具调用结果（直接返回24度）
messages.append(message)
messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
# 5. 模型返回最终结果
print(f"Model>\t {message.content}")
