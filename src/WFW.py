

if __name__ == '__main__':

    dpm = DependencyManager()
    t1 = Task('t1')
    t2 = Task('t2')
    t3 = Task('t3')

    dp1: Dependency = dpm.create_dependency('task_1', t1)
    dp2: Dependency = dpm.create_dependency('task_2', t2)
    dp3: Dependency = dpm.create_dependency('task_3', t3)

    print(dpm)

    t11 = Task('t11')
    t12 = Task('t12')
    t13 = Task('t13')

    dpm.add_task_to_dependency('task_1', t11)
    dpm.add_task_to_dependency('task_1', t12)
    dpm.add_task_to_dependency('task_1', t13)

    t21 = Task('t21')
    t22 = Task('t22')
    t23 = Task('t23')

    dpm.add_task_to_dependency('task_2', t21)
    dpm.add_task_to_dependency('task_2', t11)
    dpm.add_task_to_dependency('task_2', t12)
    dpm.add_task_to_dependency('task_2', t22)

    t31 = Task('t31')
    t32 = Task('t32')

    t4 = Task('t4')
    dp4: Dependency = dpm.create_dependency('task_4', t4)

    dpm.add_task_to_dependency('task_4', t31)
    dpm.add_task_to_dependency('task_4', t1)

    print(dpm)

    sch = Scheduler()
    sch.add_task(t1)
    sch.add_task(t2)
    sch.add_task(t4)

    sch.execute_tasks()

    sys.exit(0)