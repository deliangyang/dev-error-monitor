import os
import datetime
import requests

from config import *
from send_mail import MailSender


class JobMonitor(object):

    def __init__(self):
        self.intervals = [
            {
                'name': 'StatHourlyUserSendGift',
                'rate': 1,
            }
        ]
        self.datetime = datetime.datetime.now() + datetime.timedelta(hours=-2)

    def filename(self):
        return '/yuechang_log/%s/%s/%s/job-%s.gz' % (
            self.datetime.strftime('%Y'),
            self.datetime.strftime('%m'),
            self.datetime.strftime('%d'),
            self.datetime.strftime('%Y%m%d%H')
        )

    def parse_ftp_download_url(self):
        return 'wget --ftp-user=%s --ftp-password=%s ftp://%s@%s%s' % (
            ftp_username,
            ftp_password,
            ftp_username,
            ftp_ip,
            self.filename()
        )

    def collect(self):
        filename = self.filename()
        local_file = '/tmp/' + filename.replace('/', '_')
        command = 'rm -rf %s && %s -N -O %s && cd /tmp && gunzip %s' % (
            local_file.replace('.gz', ''),
            self.parse_ftp_download_url(),
            local_file,
            local_file)
        _ = os.popen(command).readlines()
        local_file = local_file.replace('.gz', '')

        for item in self.intervals:
            command = 'grep %s "%s" | wc -l' % (
                item['name'],
                local_file
            )
            res = os.popen(command).readlines()
            count = res.pop().strip()
            res = (command, item['name'] + ':' + count)
            if int(count) >= 2 * item['rate']:
                print('success execute!!!')
            else:
                mail_sender = MailSender(
                    '线上定时任务监控',
                    "\n" + '\n'.join(res),
                    send_from, to_backend)
                mail_sender.new_send()

    @staticmethod
    def download(url, dist):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dist, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                f.close()


if __name__ == '__main__':
    monitor = JobMonitor()
    monitor.collect()
