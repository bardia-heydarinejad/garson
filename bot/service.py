__author__ = 'bardia'

#!/usr/bin/env python

import sys
import logging
import time

from daemon import Daemon


class MyDaemon(Daemon):
    def run(self):
        logging.basicConfig(filename='example.log',
                            level=logging.DEBUG,
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%m/%d %I:%M')
        while True:
            time.sleep(1)
            logging.info('Task begin!')
            logging.info('Task end!')


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-garson.pid')
    daemon.run()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)