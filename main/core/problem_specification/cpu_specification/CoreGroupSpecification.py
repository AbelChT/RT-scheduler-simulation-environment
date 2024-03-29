from typing import List, Optional

from main.core.problem_specification.cpu_specification.EnergyConsumptionProperties import EnergyConsumptionProperties
from main.core.problem_specification.cpu_specification.MaterialCuboid import MaterialCuboid
from main.core.problem_specification.cpu_specification.Origin import Origin


class CoreGroupSpecification(object):
    def __init__(self, physical_properties: MaterialCuboid,
                 energy_consumption_properties: EnergyConsumptionProperties,
                 available_frequencies: List[int], operating_frequencies: List[int],
                 cores_origins: Optional[List[Origin]] = None):
        """
        Specification of a group of cores with the same characteristics

        :param physical_properties: Cores physical properties
        :param energy_consumption_properties: Core construction properties relatives to the energy consumption
        :param available_frequencies: Cores available frequencies in Hz
        :param operating_frequencies: Cores operating frequencies in Hz. Each frequency must belong to the
         available_frequencies set
        :param cores_origins: Cores origins locations
        """
        self.physical_properties: MaterialCuboid = physical_properties
        self.energy_consumption_properties: EnergyConsumptionProperties = energy_consumption_properties
        self.available_frequencies: List[int] = available_frequencies
        self.operating_frequencies: List[int] = operating_frequencies
        self.operating_frequencies.sort()
        self.cores_origins: Optional[List[Origin]] = cores_origins
