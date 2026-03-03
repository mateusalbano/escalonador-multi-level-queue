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
        if not self.__is_id_used(id):
            raise RuntimeError("can't retrive unused id")
        
        self.__next_ids.put(id)
        self.__used_ids.remove(id)


    def __is_id_used(self, id: int) -> bool:
        return id in self.__used_ids