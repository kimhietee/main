
width = 1280
height = 720
a = 170
b = 0.1

def solve(print_res=False, sub=False, left=False, add=False):
    if print_res:
        # print('a / b = a/b')
        # print('where a = {a}, b = {b}')
        print('a = desired pos, b = size (width or height)')
        print(f'{a} / {b} = {a/b}')
        # print(((a/b)*b))
        
    if left:
        x = a*b
        return x
    elif sub:
        x = a-(a*b)
        return x
    elif add:
        x = a+(a*b)
        return x
    
print(solve(add=True))
# print(solve(left=True))
# print(width-int(width*0.039)-1)

# # Animation Counts
# WATER_PRINCESS_BASIC_COUNT = 10
# WATER_PRINCESS_JUMP_COUNT = 6
# WATER_PRINCESS_RUN_COUNT = 8 
# WATER_PRINCESS_IDLE_COUNT = 7
# WATER_PRINCESS_ATK1_COUNT = 8
# WATER_PRINCESS_SP_COUNT = 14
# WATER_PRINCESS_DEATH_COUNT = 6

# WATER_PRINCESS_ATK1 = 12 - 2 # reduce frame
# WATER_PRINCESS_ATK2 = 53
# WATER_PRINCESS_ATK3 = 34
# WATER_PRINCESS_SP = 28
# # ---------------------
# # print((WATER_PRINCESS_ATK2 * 0.01) * 4 * 5)
# WATER_PRINCESS_ATK1_MANA_COST = 50
# WATER_PRINCESS_ATK2_MANA_COST = 80
# WATER_PRINCESS_ATK3_MANA_COST = 100
# WATER_PRINCESS_SP_MANA_COST = 200

# WATER_PRINCESS_ATK1_SIZE = 3
# WATER_PRINCESS_ATK2_SIZE = 0.3
# WATER_PRINCESS_ATK3_SIZE = 0.3
# WATER_PRINCESS_SP_SIZE = 1.3

