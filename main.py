from bluesky import Bluesky
from queue import Queue


def main():
    tasks = Queue()
    messages = Queue()
    bluesky = Bluesky(tasks, messages)
    bluesky.loop() # todo thread


if __name__ == "__main__":
    main()
