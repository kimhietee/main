
width = 1280
height = 720
a = 210
b = height

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
    
solve(True)
# print(solve(left=True))
print(width-int(width*0.039)-1)