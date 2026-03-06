import queue


class IdGenerator():

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