import random
import time
import math
# from heroes import Fire_Knight


class Chance:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.last_time = 0.0
        self.last_result = False

    def update(self, chance: int = 100):
        current_time = time.time()
        if current_time - self.last_time >= self.interval:
            self.last_time = current_time
            self.last_result = random.random() <= chance / 100
        return self.last_result



# def chance(interval=1.0, chance=100):
#     """
#     A decorator that adds a chance to a function.
    
#     Args:
#         interval (float): The time interval in seconds for the chance to be checked.
#         chance (int): The chance of the function being executed, as a percentage (0-100).
    
#     Returns:
#         function: The decorated function that will only execute based on the chance.
#     """
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             if random.random() <= chance / 100:
#                 return func(*args, **kwargs)
#             return None
#         return wrapper
#     return decorator

# from pprint import pprint

# ha = Fire_Knight(1)
# # Print the Fire Knight __dict__ format nicely
# pprint(ha.__dict__)
# chance = Chance(0.1)

# while True:
#     time.sleep(1/60)
#     print(chance.update(50))

#problems
#1. ang pos nako mabilin kung mo quit ko then balik dayon sa gameplay(pygame not closed)
# inheritance problems, proper ang inherit dapat sa bot ug sa instantiation sa bot didto sa heroes na file

# unya nako mag code kay naay bug egg ug paradise egg nag dungan 7/9/25 10:32PM



    








































# import time
# a = time.time()

# date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))
# print(date)



# print(time.time())
# print(random.random() * 100)


# y = 0
# # Example usage
# x = ChanceTimer(1,0.1)  # 50% chance every 1 second

# while True:
#     # time.sleep(0.1 / FPS)  # simulate 60 FPS
    
#     result = x.update()
#     if result is True:
#         print()
#         print('hatching bug egg:')
#         print("WIN  !")
#         print('total hatches:', y +1)
#         break
        
#     elif result is False:
#         y +=1
#         print()
#         print('hatching bug egg:')
#         print("LOSE !")
#         print('total hatches:', y)
#     # else: do nothing when interval hasn't passed
    




# class Haha:
#     pass

# class Bruh:
#     def __init__(self, aww:Haha):
#         pass

# ez = Bruh()