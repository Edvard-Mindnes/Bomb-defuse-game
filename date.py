from datetime import datetime
import time

start = datetime.today()

time.sleep(1)

end = datetime.today()

difference = end - start

seconds = difference.total_seconds()
print('difference in seconds is:', seconds)
