import asyncio
from typing import List, Any, Callable, Coroutine
from dataclasses import dataclass
from collections import deque

@dataclass
class Task:
    func: Callable[..., Coroutine]
    args: tuple
    kwargs: dict

class TaskQueue:
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.queue = deque()
        self.active = 0
        self.results = []

    async def add_task(self, func: Callable[..., Coroutine], *args, **kwargs):
        task = Task(func, args, kwargs)
        self.queue.append(task)

    async def process_queue(self):
        while self.queue or self.active > 0:
            while self.queue and self.active < self.max_concurrent:
                task = self.queue.popleft()
                asyncio.create_task(self._execute_task(task))
                self.active += 1
            await asyncio.sleep(0.1)

    async def _execute_task(self, task: Task):
        try:
            result = await task.func(*task.args, **task.kwargs)
            self.results.append(result)
        except Exception as e:
            print(f'Task failed: {str(e)}')
        finally:
            self.active -= 1

class GitBrain:
    def __init__(self):
        self.task_queue = TaskQueue()

    async def process_files(self, files: List[str]):
        for file in files:
            await self.task_queue.add_task(self.process_file, file)
        await self.task_queue.process_queue()
        return self.task_queue.results

    async def process_file(self, filepath: str) -> dict:
        # Simulated file processing
        await asyncio.sleep(1)  # Simulate work
        return {
            'filepath': filepath,
            'status': 'processed'
        }

async def main():
    brain = GitBrain()
    files = ['file1.txt', 'file2.txt', 'file3.txt']
    results = await brain.process_files(files)
    print(f'Processed {len(results)} files')

if __name__ == '__main__':
    asyncio.run(main())