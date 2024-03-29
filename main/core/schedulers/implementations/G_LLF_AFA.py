from typing import List, Optional

import scipy

from main.core.problem_specification.GlobalSpecification import GlobalSpecification
from main.core.schedulers.templates.abstract_base_scheduler.AbstractBaseScheduler import AbstractBaseScheduler
from main.core.schedulers.templates.abstract_base_scheduler.BaseSchedulerAperiodicTask import BaseSchedulerAperiodicTask
from main.core.schedulers.templates.abstract_base_scheduler.BaseSchedulerPeriodicTask import BaseSchedulerPeriodicTask
from main.core.schedulers.templates.abstract_base_scheduler.BaseSchedulerTask import BaseSchedulerTask


class GlobalLeastLaxityFirstAFAScheduler(AbstractBaseScheduler):
    """
    Implements a revision of the global least laxity first scheduler where affinity of tasks to processors have been
    got in mind and frequency too
    """

    def __init__(self) -> None:
        super().__init__()
        self.__m = None
        self.__operating_frequencies = None
        self.__max_frequency = None

    def offline_stage(self, global_specification: GlobalSpecification,
                      periodic_tasks: List[BaseSchedulerPeriodicTask],
                      aperiodic_tasks: List[BaseSchedulerAperiodicTask]) -> float:
        """
        Method to implement with the offline stage scheduler tasks
        :param aperiodic_tasks: list of aperiodic tasks with their assigned ids
        :param periodic_tasks: list of periodic tasks with their assigned ids
        :param global_specification: Global specification
        :return: 1 - Scheduling quantum (default will be the step specified in problem creation)
        """
        self.__m = len(global_specification.cpu_specification.cores_specification.operating_frequencies)
        self.__operating_frequencies = global_specification.cpu_specification.cores_specification.operating_frequencies
        self.__max_frequency = global_specification.cpu_specification.cores_specification.available_frequencies[-1]
        return super().offline_stage(global_specification, periodic_tasks, aperiodic_tasks)

    def aperiodic_arrive(self, time: float, aperiodic_tasks_arrived: List[BaseSchedulerTask],
                         actual_cores_frequency: List[float], cores_max_temperature: Optional[scipy.ndarray]) -> bool:
        """
        Method to implement with the actual on aperiodic arrive scheduler police
        :param actual_cores_frequency: Frequencies of cores
        :param time: actual simulation time passed
        :param aperiodic_tasks_arrived: aperiodic tasks arrived in this step (arrive_time == time)
        :param cores_max_temperature: temperature of each core
        :return: true if want to immediately call the scheduler (schedule_policy method), false otherwise
        """
        # Nothing to do
        return False

    def schedule_policy(self, time: float, executable_tasks: List[BaseSchedulerTask], active_tasks: List[int],
                        actual_cores_frequency: List[int], cores_max_temperature: Optional[scipy.ndarray]) -> \
            [List[int], Optional[float], Optional[List[int]]]:
        """
        Method to implement with the actual scheduler police
        :param actual_cores_frequency: Frequencies of cores
        :param time: actual simulation time passed
        :param executable_tasks: actual tasks that can be executed ( c > 0 and arrive_time <= time)
        :param active_tasks: actual id of tasks assigned to cores (task with id -1 is the idle task)
        :param cores_max_temperature: temperature of each core
        :return: 1 - tasks to assign to cores in next step (task with id -1 is the idle task)
                 2 - next quantum size (if None, will be taken the quantum specified in the offline_stage)
                 3 - cores relatives frequencies for the next quantum (if None, will be taken the frequencies specified
                  in the problem specification)
        """
        alive_tasks = [x for x in executable_tasks if x.next_arrival <= time]
        task_order = scipy.argsort(
            list(map(lambda x: x.next_deadline - (x.pending_c / self.__max_frequency), alive_tasks)))
        tasks_to_execute = ([alive_tasks[i].id for i in task_order] + (self.__m - len(alive_tasks)) * [-1])[0:self.__m]

        # Assign highest priority task to faster processor
        tasks_to_execute = [x for _, x in sorted(zip(actual_cores_frequency, tasks_to_execute), reverse=True)]

        # Do affinity
        for i in range(self.__m):
            actual = active_tasks[i]
            for j in range(self.__m):
                if tasks_to_execute[j] == actual and actual_cores_frequency[j] == actual_cores_frequency[i]:
                    tasks_to_execute[j], tasks_to_execute[i] = tasks_to_execute[i], tasks_to_execute[j]
        return tasks_to_execute, None, None
