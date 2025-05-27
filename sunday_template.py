# coding: utf-8 import json
import pprint
from sunday.core import getConfig, getParser
from sunday.login.template import getLoginHandler

CMDINFO = {
    "version": '0.0.1',
    "description": "命令行工具",
    "epilog": "",
    'params': {
        'DEFAULT': [
            {
                'name': ['-m', '--mobile'],
                'help': '手机号',
                'dest': 'mobile',
                'required': True,
            },
            {
                'name': ['-p', '--pass'],
                'help': '密码',
                'dest': 'password',
            },
        ],
    }
}


cryptoKey = getConfig('CRYPTO')('key')

class Template():
    def __init__(self, mobile=None, password=None, *args, **kwargs):
        self.mobile = mobile
        self.password = password

    def getData(self):
        loginer = getLoginHandler('TemplateLogin')(
                phone=self.mobile,
                password=self.password).login()
        data = loginer.rs.get_json('https://target.site')
        if data.get('stat') != 1: return
        return data

    def console(self, data):
        pprint.pprint(data)

    def run(self, isCmd=False):
        ans = self.getData()
        if isCmd:
            self.console(ans)
        else:
            return ans


def runcmd():
    parser = getParser(**CMDINFO)
    handle = parser.parse_args(namespace=Template())
    handle.run(True)

if __name__ == "__main__":
    runcmd()

