from enum import Enum

from core.tcpn_model_generator.thermal_model_energy import ThermalModelEnergy
from core.tcpn_model_generator.thermal_model_frequency import ThermalModelFrequencyAware


class ThermalModelSelector(Enum):
    """
    Select thermal model type
    """
    THERMAL_MODEL_ENERGY_BASED = ThermalModelEnergy
    THERMAL_MODEL_FREQUENCY_BASED = ThermalModelFrequencyAware