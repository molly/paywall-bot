from bluesky import Bluesky
import logging
from logging.handlers import TimedRotatingFileHandler
from process import notifications_worker
from queue import Queue
import threading


def main():
    logger = logging.getLogger('paywall-bot')
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(filename='paywall-bot.log', when='D', interval=1, backupCount=5)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    tasks = Queue()
    messages = Queue()
    bsky = Bluesky(tasks, messages)
    bsky.loop() # todo thread

    # Begin processor with 10 workers
    for i in range(10):
        threading.Thread(target=notifications_worker, args=(tasks, bsky))


if __name__ == "__main__":
    main()
