import queue


class IdGenerator():
    """
    Class responsible for generating unique ids for the user when they are not in use.
    When asked for a id, it will return the smallest available id.
    When an id is retrieved to the generator, it will be put back in the pool of available ids.
    """


    def __init__(self):
        self.__next_ids = queue.PriorityQueue()
        self.__next_ids.put(0)
        self.__used_ids = set()


    def get_next_id(self) -> int:
        id = self.__next_ids.get()
        self.__used_ids.add(id)

        if self.__next_ids.empty():
            self.__next_ids.put(id + 1)
        
        return id


    def retrieve_id(self, id: int):
        if id not in self.__used_ids:
            raise RuntimeError("can't retrieve unused id")
        
        self.__next_ids.put(id)
        self.__used_ids.remove(id)