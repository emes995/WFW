import unittest
from dependency.Dependency import Dependency
from dependency.DependencyManager import DependencyManager
from task.Task import Task
from scheduler.Scheduler import Scheduler

class TestDependency(unittest.TestCase):

    def test_dependency(self):

        t1 = Task('t1')
        dep_ = Dependency(t1)
        assert t1 == dep_.get_custodian_task

        t2 = Task('t1-1')
        t3 = Task('t1-2')
        t4 = Task('t1-3')

        dep_.add_tasks([t2, t3, t4])

        assert len(dep_) == 3

    def test_dependency_manager(self):
        dpm = DependencyManager()
        t1 = Task('t1')
        t2 = Task('t2')
        t3 = Task('t3')

        dp1: Dependency = dpm.create_dependency('dep_1', t1)
        dp2: Dependency = dpm.create_dependency('dep_2', t2)
        dp3: Dependency = dpm.create_dependency('dep_3', t3)

        assert len(dpm.get_tasks_in_dependency('dep_1')) == 0

        t11 = Task('t11')
        t12 = Task('t12')
        t13 = Task('t13')
        dpm.add_task_to_dependency('dep_1', t11)
        dpm.add_task_to_dependency('dep_1', t12)
        dpm.add_task_to_dependency('dep_1', t13)

        assert len(dpm.get_tasks_in_dependency('dep_1')) == 3

        t21 = Task('t21')
        t22 = Task('t22')
        t23 = Task('t23')
        dpm.add_task_to_dependency('dep_2', t21)
        dpm.add_task_to_dependency('dep_2', t11)
        dpm.add_task_to_dependency('dep_2', t12)
        dpm.add_task_to_dependency('dep_2', t22)
        dpm.add_task_to_dependency('dep_2', t23)

        t31 = Task('t31')
        t32 = Task('t32')
        dpm.add_task_to_dependency('dep_3', t31)
        dpm.add_task_to_dependency('dep_3', t32)

        t4 = Task('t4')
        dp4: Dependency = dpm.create_dependency('dep_4', t4)
        dpm.add_task_to_dependency('dep_4', t31)
        dpm.add_task_to_dependency('dep_4', t1)

        assert len(dpm.get_tasks_in_dependency('dep_4')) == 5
        assert len(t1.resolve_dependencies()) == 3

        sch = Scheduler(dpm)
        sch.add_task(t1)
        sch.add_task(t2)
        sch.add_task(t4)

        sch.execute_tasks()
