from invoke import task

def mytask(func):
    @task
    def wrapper(c):
        with c.cd(c.config['work_dir']):
            func(c)

    return wrapper

