from sugar import ProgressBar as pb
import time

bar = pb()
total = 10000
i = 0
bar.start(total)
while i != total:
    time.sleep(0.01)
    i += 1
    bar.update(i)
bar.stop()