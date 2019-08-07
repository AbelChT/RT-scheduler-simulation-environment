import abc

import scipy


class AbstractTcpnSimulator(object, metaclass=abc.ABCMeta):
    """
    Time continuous petri net simulator
    """

    @abc.abstractmethod
    def set_control(self, control: scipy.ndarray):
        """
        Apply a control action over transitions firing in the Petri net
        :param control: control
        """

    @abc.abstractmethod
    def simulate_step(self, mo: scipy.ndarray) -> scipy.ndarray:
        """
        Simulate one step

        :param mo:  actual marking
        :return: next marking
        """
        pass

    @staticmethod
    def _calculate_pi(pre: scipy.ndarray, mo: scipy.ndarray) -> scipy.ndarray:
        """
        Calculate pi
        :param mo: actual marking
        :return: pi
        """
        pre_transpose = pre.transpose()
        pi = scipy.zeros(pre_transpose.shape)

        for i in range(len(pre_transpose)):
            places = pre_transpose[i]
            max_index = -1
            max_global = 0
            for j in range(len(places)):
                if places[j] != 0:
                    if mo[j] != 0:
                        max_interior = places[j] / mo[j]
                        if max_global < max_interior:
                            max_global = max_interior
                            max_index = j
                    else:
                        max_index = -1
                        break
            if max_index != -1:
                pi[i][max_index] = 1 / places[max_index]

        return pi
