from multiprocessing.dummy import Pool
import requests
     
import requests
pool = Pool(22) # Creates a pool with 21 threads;
if __name__ == '__main__':
        futures = []
        for x in range(22):
                futures.append(pool.apply_async(requests.get, ['http://challenge01.root-me.org:54017/']))
        # futures is now a list of 22 futures.
        for future in reversed(futures):
                print(future.get().text)
                # we dont want to wait for other threads to end, so let's just exit
                exit(0)