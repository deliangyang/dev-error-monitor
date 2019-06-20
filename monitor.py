# -*-- coding:utf-8 -*--
import os
import re
import time
import datetime
import hashlib
from create_db import ErrorLog
from send_mail import MailSender
from config import *
from pony.orm import *


class LogCollection:

    __slots__ = ('exception_command', 'consume_command', 'data', 'date', 'filter_re', 'error_map', 'line_re', 'env')

    def __init__(self):
        self.error_map = {
            'consumer': '"Consume Error Occurred .+\\\"errors\\\":"',
            'exception': '"exception.ERROR.+\\\"errors\\\":"',
        }
        self.line_re = re.compile(r'^(\d+)\s(.+$)')
        _filter_re = [
            r'exception_code_\d+',
            r' api_',
            r'model_exception_',
            r'[\u4e00-\u9fa5]{2,}',
            r'exception_incorrect_telphone_password',
            r' Not Found ',
            r'Database connect failed',
            r'"code":\d{6}',
            r'"code":40\d',
        ]
        self.data = []
        self.filter_re = []
        for _item in _filter_re:
            self.filter_re.append(re.compile(_item))
        self.date = datetime.datetime.now().strftime('%Y%m%d')

    def collect(self, environment, _path):
        self.data = []

        def error_md5(err):
            md5 = hashlib.md5()
            md5.update(err.encode('utf-8'))
            md5_str = md5.hexdigest()
            return md5_str

        for _key in self.error_map:
            command = '%s \'grep -oP %s %s/%s-%s | sort | uniq -c\'' % (
                'ssh dev@192.168.1.21',
                self.error_map[_key], _path, _key, self.date)
            print(command)
            lines = os.popen(command).readlines()
            self.parse(error_md5, environment, lines)

    def get_data(self):
        return self.data

    @db_session
    def parse(self, error_md5, _env, lines):
        for line in lines:
            datum = line.strip()
            items = self.line_re.findall(datum)
            if len(items):
                times, error = items[0]
                times = int(times)
                has_been_filter = False
                for _re in self.filter_re:
                    if len(_re.findall(line)):
                        has_been_filter = True
                        break
                if has_been_filter:
                    continue
                _md5 = error_md5(error)
                try:
                    ErrorLog(md5=_md5, times=times, error=error, create_time=int(time.time()), env=_env)
                    commit()
                    self.data.append(line)
                except Exception as e:
                    error_log = ErrorLog.get(md5=_md5, env=_env)
                    if error_log and times > error_log.times:
                        error_log.times = times
                        commit()
                        self.data.append(line)
                    print(e)


if __name__ == '__main__':
    paths = {
        'test': '/data/logs/yuechang/test',
        'newtest': '/data/logs/yuechang/newtest',
        'testdress': '/data/logs/yuechang/testdress',
    }
    error_info = ''
    monitor = LogCollection()
    for env in paths:
        monitor.collect(env, paths[env])
        error_data = monitor.get_data()
        if len(error_data):
            error_info += "环境:%s\n%s\n\n" % (env, ''.join(error_data))

    if len(error_info):
        mail_sender = MailSender('测试环境错误信息收集', "\n" + error_info, send_from, to_backend)
        mail_sender.send()
    else:
        print('empty data!!!')
    print('done')
