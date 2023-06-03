# 2006 by Defiant, Kobayashi Maru project
# if you wonder about this file check http://bckobayashimaru.de/phpBB2/viewtopic.php?t=1083

import nt

# from threading import Lock

DEBUG = 0
logfile = "scripts/Custom/bcdebug.log"

NonSerializedObjects = ("lock",)


# lock = Lock()
def debug(s):
    if not DEBUG:
        return

    file = nt.open(logfile, nt.O_WRONLY | nt.O_APPEND | nt.O_CREAT)
    nt.write(file, s + "\n")
    nt.close(file)


def debug_save(s):
    if not DEBUG:
        return

    lock.acquire()
    file = nt.open(logfile, nt.O_WRONLY | nt.O_APPEND | nt.O_CREAT)
    nt.write(file, s + "\n")
    nt.close(file)
    lock.release()
