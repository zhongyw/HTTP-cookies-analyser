# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus
import dashscope

dashscope.api_key="sk-db84f4d1c5e848bcb9702aca07782b14"
def call_with_messages():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '请猜测一下下面的cookie中BIDUPSID的含义，回答要简洁，在20个字以内: https://www.baidu.com BIDUPSID F914DD687D9A7C11380F6FE708F3AE0F .baidu.com'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

def call_with_messages_short(info):
    messages = [{'role': 'system', 'content': '你是一cookie隐私合规专家.'},
                {'role': 'user', 'content': info}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    print(info)
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return '';

if __name__ == '__main__':
    call_with_messages_short('请猜测一下下面的cookie中BIDUPSID的含义，回答要简洁，在20个字以内: https://www.baidu.com BIDUPSID F914DD687D9A7C11380F6FE708F3AE0F .baidu.com')