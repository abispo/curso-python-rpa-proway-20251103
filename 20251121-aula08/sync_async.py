import asyncio

from random import randint
import time

def sync_task(delay):
    time.sleep(delay)
    return f"Tarefa síncrona concluída em {delay} segundos."

async def async_task(delay):
    await asyncio.sleep(delay)
    return f"Tarefa assíncrona concluída em {delay} segundos."

def sync_main():
    start_time = time.time()
    delays = [randint(1, 10) for _ in range(5)]

    for delay in delays:
        print(sync_task(delay))

    end_time = time.time()
    print(f"Tempo total síncrono: {end_time - start_time}")

async def async_main():
    start_time = time.time()
    delays = [randint(1, 10) for _ in range(5)]

    tasks = [async_task(delay) for delay in delays]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

    end_time = time.time()
    print(f"Tempo total assíncrono: {end_time - start_time}")

if __name__ == "__main__":
    sync_main()

    asyncio.run(async_main())