import unittest

from core.kernel_generator.global_model import generate_global_model
from core.kernel_generator.kernel import SimulationKernel
from core.kernel_generator.processor_model import ProcessorModel, generate_processor_model
from core.kernel_generator.tasks_model import TasksModel, generate_tasks_model
from core.kernel_generator.thermal_model import ThermalModel, generate_thermal_model
from core.problem_specification_models.CpuSpecification import CpuSpecification, MaterialCuboid
from core.problem_specification_models.EnvironmentSpecification import EnvironmentSpecification
from core.problem_specification_models.GlobalSpecification import GlobalSpecification
from core.problem_specification_models.SimulationSpecification import SimulationSpecification
from core.problem_specification_models.TasksSpecification import TasksSpecification, Task
from core.schedulers.rt_tcpn_scheduler import RtTCPNScheduler
from output_generation.output_generator import plot_cpu_utilization, plot_task_execution, plot_cpu_temperature, \
    plot_accumulated_execution_time, draw_heat_matrix


class RtTcpnScheduler(unittest.TestCase):

    def test_rt_tcpn_scheduler(self):
        tasks_specification: TasksSpecification = TasksSpecification([Task(2, 4, 6.4),
                                                                      Task(3, 8, 8),
                                                                      Task(3, 12, 9.6)])
        cpu_specification: CpuSpecification = CpuSpecification(MaterialCuboid(x=50, y=50, z=1, p=8933, c_p=385, k=400),
                                                               MaterialCuboid(x=10, y=10, z=2, p=2330, c_p=712, k=148),
                                                               2, 1)

        environment_specification: EnvironmentSpecification = EnvironmentSpecification(0.001, 45, 110)

        simulation_specification: SimulationSpecification = SimulationSpecification(2, 0.01)

        processor_model: ProcessorModel = generate_processor_model(tasks_specification, cpu_specification)

        tasks_model: TasksModel = generate_tasks_model(tasks_specification, cpu_specification)

        thermal_model: ThermalModel = generate_thermal_model(tasks_specification, cpu_specification,
                                                             environment_specification,
                                                             simulation_specification)

        global_model, mo = generate_global_model(tasks_model, processor_model, thermal_model, environment_specification)

        simulation_kernel: SimulationKernel = SimulationKernel(tasks_model, processor_model, thermal_model,
                                                               global_model, mo)

        global_specification: GlobalSpecification = GlobalSpecification(tasks_specification, cpu_specification,
                                                                        environment_specification,
                                                                        simulation_specification)

        scheduler = RtTCPNScheduler()

        scheduler_simulation = scheduler.simulate(global_specification, simulation_kernel, None)

        draw_heat_matrix(global_specification, simulation_kernel, scheduler_simulation, "tcpn_heat_matrix.mp4")
        plot_cpu_utilization(global_specification, scheduler_simulation, "tcpn_cpu_utilization.png")
        plot_task_execution(global_specification, scheduler_simulation, "tcpn_task_execution.png")
        plot_cpu_temperature(global_specification, scheduler_simulation, "tcpn_cpu_temperature.png")
        plot_accumulated_execution_time(global_specification, scheduler_simulation, "tcpn_accumulated.png")


if __name__ == '__main__':
    unittest.main()
