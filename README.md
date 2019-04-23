
### Introduction

The monitor collect exception and consumer's log, and then send email to developer.


### How to use it?

```bash
# configure the mail config
cp config.exmaple.py config.py

pip3 -r requriements.txt

python create_db.py

python monitor.py

# crontab -e
20 * * * * /usr/bin/python /mnt/hgfs/fwork/dev-error-monitor/monitor.py >> /tmp/logger_error.log
```