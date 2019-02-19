from task_generator.TaskGeneratorAlgorithm import TaskGeneratorAlgorithm
from task_generator.UUniFast import UUniFast

tga: TaskGeneratorAlgorithm = UUniFast(12, 0.12)

taskList: list = tga.generate()

print(taskList)