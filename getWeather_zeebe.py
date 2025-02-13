import asyncio

from pyzeebe import ZeebeWorker, Job, JobController, create_insecure_channel


channel = create_insecure_channel(grpc_address="localhost:26500")
worker = ZeebeWorker(channel)

async def on_error(exception: Exception, job: Job, job_controller: JobController):
    """
    on_error will be called when the task fails
    """
    print(exception)
    await job_controller.set_error_status(job, f"Failed to handle job {job}. Error: {str(exception)}")


@worker.task(task_type="example", exception_handler=on_error)
def example_task(input: str) -> dict:
    return {"output": f"Hello world, {input}!"}


@worker.task(task_type="example2", exception_handler=on_error)
async def another_example_task(name: str) -> dict: # Tasks can also be async
    return {"output": f"Hello world, {name} from async task!"}

loop = asyncio.get_running_loop()
loop.run_until_complete(worker.work()) # Now every time that a task with type `example` or `example2` is called, the corresponding function will be called
