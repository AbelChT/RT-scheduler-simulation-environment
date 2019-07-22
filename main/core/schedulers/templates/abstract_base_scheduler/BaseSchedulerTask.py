class BaseSchedulerTask(object):
    def __init__(self, d: float, a: float, c: float, task_id: int):
        """
        Task information managed by the schedulers
        :param d: deadline
        :param a: arrival
        :param c: execution time
        :param task_id: id
        """
        self.next_deadline = d  # next task deadline in absolute seconds (since simulation start)
        self.next_arrival = a  # next task arrival in absolute seconds (since simulation start)
        self.pending_c = c  # pending execution seconds at base frequency
        # self.instances = 0  # Number of executed task instances
        self.id = task_id  # task id (always natural integer)