"""Contains class for handling the global song queue

Authors:
    Chance Nelson <chance-nelson@nau.edu>
"""


from multiprocessing import Queue


class SongQueue:
    def __init__(self):
        """Constructor
        """
        self.__queue = Queue()

    def add(self, song):
        """Add a song to the queue
        """
        self.__queue.put(song)

    def remove(self, song):
        """Remove a song from the queue

        Args:
            song (Song): song to add
        """
        try:
            self.__queue.remove(song)

        except ValueError:
            # song to remove was not found
            pass

    def pop(self):
        """Remove the current song from the queue

        Returns: 
            Song popped from queue
        """
        return self.__queue.get()
