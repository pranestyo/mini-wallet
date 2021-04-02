import datetime
import time

def timectime(s):
    d = datetime.datetime.strptime(time.ctime(s),"%a %b %d %H:%M:%S %Y")
    
    return d.strftime('%Y-%-m-%-d %H:%M:%S')