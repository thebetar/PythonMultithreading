import multiprocessing
import os
import time
import random

def producer(shared_value, topping):
    print(f'Producer process ID: {os.getpid()}')
    
    while True:
        shared_value.release()
        
        print(f'Producer with process ID: {os.getpid()} - created some {topping} (total {shared_value})')

        time.sleep(random.uniform(1,5))
        
def consumer(bread_value, topping_value, topping):
    print(f'Consumer process ID: {os.getpid()}')
    
    while True:
        bread_value.acquire()
        topping_value.acquire()
            
        print(f'Baker with process ID: {os.getpid()} - created a {topping} sandwich (bread: {bread_value}, {topping}: {topping_value})')

        time.sleep(random.uniform(1,5))
        
def main():
    PRODUCERS = 3
    CONSUMERS = 2
    
    bread_value = multiprocessing.Semaphore(0)
    cheese_value = multiprocessing.Semaphore(0)
    hummus_value = multiprocessing.Semaphore(0)
    
    print(f'Parent process ID: {os.getpid()}')
    
    processes = []
    
    producers = [
        (cheese_value, 'cheese'),
        (hummus_value, 'hummus'),
        (bread_value, 'bread')
    ]
    
    for i in range(PRODUCERS):
        p = multiprocessing.Process(target=producer, args=producers[i])
        p.start()
        processes.append(p)
    
    consumers = [
        (bread_value, cheese_value, 'cheese'),
        (cheese_value, hummus_value, 'hummus')
    ]
    
    for i in range(CONSUMERS):
        p = multiprocessing.Process(target=consumer, args=consumers[i])
        p.start()
        processes.append(p)
        
    time.sleep(60)
    
    for p in processes:
        p.terminate()
    
if __name__ == '__main__':
    main()