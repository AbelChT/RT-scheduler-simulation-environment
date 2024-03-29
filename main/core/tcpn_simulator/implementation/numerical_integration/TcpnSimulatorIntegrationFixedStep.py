from typing import Optional

import scipy

from main.core.tcpn_simulator.template.AbstractTcpnSimulator import AbstractTcpnSimulator


class TcpnSimulatorIntegrationFixedStep(AbstractTcpnSimulator):
    """
    Time continuous Petri net simulator based on the Euler method
    WARNING: This is only an example, it is not used in the simulator but it may be useful if the Petri net model of the
    simulation change
    """

    def __init__(self, pre: scipy.ndarray, post: scipy.ndarray, pi: Optional[scipy.ndarray],
                 lambda_vector: scipy.ndarray, number_of_steps: int, dt: float):
        """
        Define the TCPN
        :param pre: pre matrix
        :param post: post matrix
        :param pi: pi matrix
        :param lambda_vector: lambda vector
        :param number_of_steps: number of steps in the integration
        :param dt: to solve the state equation, it will be integrated in the interval [0, dt]
        """
        self.__pre = pre
        self.__post = post
        self.__lambda_vector = lambda_vector
        self.__control = scipy.ones(len(lambda_vector))
        self.__pi = pi
        self.__c = self.__post - self.__pre
        self.__dt = dt
        self.__number_of_steps = number_of_steps
        self.__a = self.__calculate_a(self.__c, self.__lambda_vector, self.__pi,
                                      self.__dt / self.__number_of_steps) if self.__pi is not None else None

    def set_control(self, control: scipy.ndarray):
        """
        Apply a control action over transitions firing in the Petri net
        :param control: control
        """
        self.__control = control
        self.__a = self.__calculate_a(self.__c, self.__lambda_vector * control, self.__pi,
                                      self.__dt / self.__number_of_steps) if self.__pi is not None else None

    @staticmethod
    def __calculate_a(c: scipy.ndarray, lambda_vector: scipy.ndarray, pi: scipy.ndarray,
                      fragmented_dt: float) -> scipy.ndarray:
        """
        Calculate all constant values during the simulation
        """
        return (c * lambda_vector).dot(pi) * fragmented_dt

    def simulate_step(self, mo: scipy.ndarray) -> scipy.ndarray:
        """
        Simulate one step

        :param mo:  actual marking
        :return: next marking
        """
        a = self.__a if self.__a is not None else self.__calculate_a(self.__c, self.__lambda_vector * self.__control,
                                                                     self._calculate_pi(self.__pre, mo),
                                                                     self.__dt / self.__number_of_steps)

        mo_next = mo
        for _ in range(self.__number_of_steps):
            mo_next = a.dot(mo_next) + mo_next

        return mo_next
