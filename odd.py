from datetime import datetime
import time
import random

odds = [ 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29 ,31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59]


for i in range(5):
    right_this_minute = datetime.today().minute


    print(right_this_minute)

    if right_this_minute in odds:
        print("This minute seens a little odd.")
    else:
        print("Not an odd number") 

        wait_time = random.randint(1, 60)
        print(wait_time)
        time.sleep(wait_time)



# def f(p1, p2 = 10):
#     print(p1)
#     print(p2)


# for i in range(10)