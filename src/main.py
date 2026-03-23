import asyncio
from typing import List, Callable, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import logging

@dataclass
class Task:
    func: Callable
    args: tuple
    kwargs: dict
    future: asyncio.Future

class GitBrainWorkerPool:
    def __init__(self, num_workers: int = 4):
        self.task_queue: Queue[Task] = Queue()
        self.workers: List[asyncio.Task] = []
        self.num_workers = num_workers
        self.thread_pool = ThreadPoolExecutor(max_workers=num_workers)
        self.running = False
        self._setup_logging()

    def _setup_logging(self):
        self.logger = logging.getLogger('GitBrainWorker')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    async def start(self):
        """Start the worker pool"""
        self.running = True
        self.workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.num_workers)
        ]
        self.logger.info(f'Started worker pool with {self.num_workers} workers')

    async def stop(self):
        """Stop the worker pool"""
        self.running = False
        for _ in range(len(self.workers)):
            await self.task_queue.put(None)
        await asyncio.gather(*self.workers)
        self.thread_pool.shutdown()
        self.logger.info('Worker pool stopped')

    async def _worker(self, worker_id: int):
        """Worker process that handles tasks from the queue"""
        while self.running:
            try:
                task = await asyncio.get_event_loop().run_in_executor(
                    None, self.task_queue.get
                )
                if task is None:
                    break

                self.logger.debug(f'Worker {worker_id} processing task {task.func.__name__}')
                try:
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.thread_pool,
                        task.func,
                        *task.args,
                        **task.kwargs
                    )
                    task.future.set_result(result)
                except Exception as e:
                    task.future.set_exception(e)
                    self.logger.error(f'Error in worker {worker_id}: {str(e)}')
                finally:
                    self.task_queue.task_done()

            except Exception as e:
                self.logger.error(f'Worker {worker_id} error: {str(e)}')

    async def submit(self, func: Callable, *args, **kwargs) -> Any:
        """Submit a task to the worker pool"""
        future = asyncio.get_event_loop().create_future()
        task = Task(func=func, args=args, kwargs=kwargs, future=future)
        await asyncio.get_event_loop().run_in_executor(
            None, self.task_queue.put, task
        )
        return await future

# Example usage
worker_pool = GitBrainWorkerPool()

async def main():
    await worker_pool.start()
    
    # Example task
    def example_task(x: int) -> int:
        return x * 2
    
    # Submit tasks
    results = await asyncio.gather(*[
        worker_pool.submit(example_task, i)
        for i in range(10)
    ])
    
    print(f'Results: {results}')
    await worker_pool.stop()

if __name__ == '__main__':
    asyncio.run(main())
