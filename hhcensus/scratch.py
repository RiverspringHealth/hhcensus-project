#used to test out snippets before adding to main code.

import datetime

BED_STATUS_LOCK_TIME = 12

d = datetime.datetime.now()
d = d.replace(hour=8, minute=0, second=0, microsecond=0)

print(d)



