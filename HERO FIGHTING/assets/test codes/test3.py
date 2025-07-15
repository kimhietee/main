# Trying conditions for skill 1 for Fire Knight bot logic
r = 10
y = lambda r: r > 5

def lumbda(r):
    return r > 5

# print(y)
# print(lumbda(r))

def ha(): return True

def is_ready(now):
    cd = 10
    return True if now == 0 else False

skl1 = is_ready(0)
skl2 = is_ready(2)
skl3 = is_ready(0)
skl4 = is_ready(20)

# # lest = [skl2,skl3,skl4]
# lest = list
# for i in range(1, 4):
#     print(f'skill {i+1} = [{i}]')
#     lest.append()

sample1 = {
    
    'skel1': {
        'cast_range': 69,
        'a list': [1,2,3]
        
    }
           
           }


# if self.attacks[0].is_ready():
#     halaka
attacks = [
    True,
    True
]

class Attacks:
    def __init__(self,mana_cost, skill_rect, skill_img, cooldown, mana):
        self.mana_cost = mana_cost
        self.skill_rect = skill_rect
        self.skill_img = skill_img
        self.cooldown = cooldown
        self.mana = mana
    def is_ready(self, now):
        return True if now == 0 else False
    
class Sample:
    def __init__(self):
        self.mana = 2
        self.attacks = [
                    Attacks(
                        mana_cost=1,
                        skill_rect=3,
                        skill_img=3,
                        cooldown=1,
                        mana=self.mana
                    ),
                    Attacks(
                        mana_cost=2,
                        skill_rect=3,
                        skill_img=3,
                        cooldown=1,
                        mana=self.mana
                    ),
                    Attacks(
                        mana_cost=3,
                        skill_rect=3,
                        skill_img=3,
                        cooldown=1,
                        mana=self.mana
                    ),
                    Attacks(
                        mana_cost=4,
                        skill_rect=3,
                        skill_img=3,
                        cooldown=1,
                        mana=self.mana
                    )
                ]
    def display(self):
        # print([klasses.is_ready(j) for klasses in self.attacks for i, j in zip(range(1, len(self.attacks)), [0,2,4])])
        # yo = [f'skill {lenn+1} = {klasses.is_ready(j)}' for klasses, j, lenn in zip(self.attacks, [1,2,4], range(1, len(self.attacks)))]
        # yo = [klasses.is_ready(j) for klasses, j, lenn in zip(self.attacks, [1,2,4], range(0, len(self.attacks)))]








        
        #--------------------------------------------------------------------------------------------------------------------------------------------------
        yo = lambda x: [self.attacks[i].is_ready(j) if not self.attacks[i].is_ready(j) else True for klasses in self.attacks for i, j in zip(range(1,4), [0,10,4])] # skill 2,3,4 , sample cooldowns= 0, 4, 4
        print(yo)
        # print(f'DONT') if any(yo) else print('ATTACK')
        print(callable(yo))
        #--------------------------------------------------------------------------------------------------------------------------------------------------
        nah = []
        for klasses in self.attacks:
            for i in range(4):
                nah.append(klasses.mana_cost)
        # print(nah)
        #--------------------------------------------------------------------------------------------------------------------------------------------------
        # lambda bot: 










        # haha = []
        # for klasses in self.attacks:
        #     for i in range(1, len(self.attacks)):
            
        #         if i > 2:
        #             haha.append(klasses.is_ready(0))
        #         else:
        #             haha.append(2)
                
        # print(haha)

        # print({x:y for x, y in zip(range(2), range(3))})

main = Sample()
main.display()
# print([i for i in attacks])

# if any(lest) and skl1:
#     print(lest)
#     print('DONT')
    
# else:
#     print(lest)
#     print('EXECUTE')
    

#print(f'bot.is_ready() -> {is_ready(0)}')
a = {'skill_1': {
        'cast_range': 800,
        'min_cast_range': 50,
        # 'require_all': True,  # Keep this as True since custom logic is inside conditions
        'conditions': [
            ha()
                    ]
                }
    }

skills = a
skill_key = 'skill_1'
config = skills[skill_key]
conditions = config.get('conditions', [])
require_all = config.get('require_all', True)

if callable(require_all):
    result = require_all()
else:
    result = require_all 

# print(result)
# print([(cond for cond in conditions)])
# print((result and all(cond for cond in conditions)))
# print(conditions)
# if  == True:
#     print('assa')



# print(ha())
