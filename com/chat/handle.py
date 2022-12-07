import hashlib
import json
import os
import web
from web.template import ALLOWED_AST_NODES
from wechatpy import parse_message, create_reply
from wechatpy.replies import ImageReply

from revChatGPT import Chatbot

with open("config.json", "r", encoding='utf-8') as f:
    config = json.load(f)
chatbot = Chatbot(config)
chatbot.refresh_session()

def sendChatGPT(question, msg):
    message = chatbot.get_chat_response(question)
    print(message['message'])
    reply = create_reply(message['message'], message=msg)
    xml = reply.render()
    return xml


class Handle(object):

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        ALLOWED_AST_NODES.append('Constant')

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "wangzai"
            list = [token, timestamp, nonce]
            list.sort()
            s = list[0] + list[1] + list[2]
            hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except Exception as Argument:
            return Argument

    def POST(self):
        xml_data = web.data()
        msg = parse_message(xml_data)
        if msg.type == 'text':
            msg_content = msg.content
            xml = sendChatGPT(msg_content, msg)
            return xml
