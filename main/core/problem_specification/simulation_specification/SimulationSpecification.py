import scipy

from main.core.problem_specification.simulation_specification.SimulationPrecision import SimulationPrecision


class SimulationSpecification(object):

    def __init__(self, mesh_step: float, dt: float, simulate_thermal: bool, dt_fragmentation_processor_task: int = 128,
                 dt_fragmentation_thermal: int = 128, float_decimals_precision: int = 5,
                 type_precision: SimulationPrecision = SimulationPrecision.HIGH_PRECISION):
        """
        Specification of some simulation' variables

        :param dt: Minimum time unit simulated by the framework
        :param mesh_step: Minimum physical size unit simulated by the framework
        :param simulate_thermal: True if want to simulate the thermal model
        :param dt_fragmentation_processor_task: Simulation step fragmentation for tasks-processors model
        :param dt_fragmentation_thermal: Simulation step fragmentation for thermal model
        :param float_decimals_precision: Number of decimal precision to maintain while doing float operations
        :param type_precision: Float type selected
        """
        self.dt: float = dt
        self.mesh_step: float = mesh_step
        self.simulate_thermal: bool = simulate_thermal
        self.dt_fragmentation_processor_task: int = dt_fragmentation_processor_task
        self.dt_fragmentation_thermal: int = dt_fragmentation_thermal
        self.float_decimals_precision: int = float_decimals_precision
        self.type_precision: scipy.dtype = type_precision.value[0]
