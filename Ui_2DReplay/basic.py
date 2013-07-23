# -*- coding: UTF-8 -*-
import random
import time
#常量采用全字母大写，变量及函数全字母小写，类名首字母大写，单词用‘―‘隔开
random.seed(time.time())
TURN_MAX=200
COORDINATE_X_MAX=20
COORDINATE_Y_MAX=20
SOLDIERS_NUMBER=10

TEMPLE_UP_TIME=9
TRAP_COST=2

PLAIN=0#平原
MOUNTAIN=1#山地
FOREST=2#森林
BARRIER=3#屏障
TURRET=4#跑ta
TRAP=5#陷阱
TEMPLE=6#神庙
GEAR=7#机关
FIELD_EFFECT={PLAIN:[1,0,0,0,0],
              MOUNTAIN:[2,0,0,0,1],
              FOREST:[2,0,0,1,0],
              BARRIER:[1,0,0,0,0],
              TURRET:[1,2,0,0,0],
              TRAP:[1,-1,0,0,0],
              TEMPLE:[1,3,0,0,0],
              GEAR:[1,2,0,0,0]}
#(move_consumption,score,attack_up,speed_up,defence_up)
HERO_UP_LIMIT=5#hero 's up limit of getting shenfu
BASE_UP_LIMIT=3
HERO_SCORE=3
BASE_SCORE=1

SABER=0#剑士
LANCER=1#枪兵
ARCHER=2#弓兵
DRAGON_RIDER=3#龙骑士
WARRIOR=4#战士
WIZARD=5#法师
HERO_1=6
HERO_2=7
HERO_3=8
ABILITY={SABER:[25,18,95,12,6,[1],5],
         LANCER:[25,17,90,13,7,[1],4],
         ARCHER:[25,17,90,12,6,[2],3],
         DRAGON_RIDER:[21,15,95,10,8,[1],2],
         WARRIOR:[30,20,85,15,5,[1],1],
         WIZARD:[21,10,90,12,6,[],0],
         HERO_1:[55,17,90,15,5,[1],6],
         HERO_2:[40,20,100,13,6,[1],6],
         HERO_3:[45,20,95,14,7,[1,2],6]}
#(LIFE,ATTACK,SPEED,DEFENCE,MOVE_RANGE,ATTACK_RANGE,MOVE_SPEED)
#WIZARD:不可攻击ATTACK表示回复生命数
ATTACK_EFFECT={SABER:{SABER:1,LANCER:0.5,ARCHER:1,DRAGON_RIDER:0.5,WARRIOR:1.5,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               LANCER:{SABER:1.5,LANCER:1,ARCHER:1,DRAGON_RIDER:1,WARRIOR:0.5,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               ARCHER:{SABER:1,LANCER:1,ARCHER:1,DRAGON_RIDER:2,WARRIOR:1,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               DRAGON_RIDER:{SABER:1.5,LANCER:1,ARCHER:1,DRAGON_RIDER:1,WARRIOR:0.5,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               WARRIOR:{SABER:0.5,LANCER:1.5,ARCHER:1,DRAGON_RIDER:1.5,WARRIOR:1,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               HERO_1:{SABER:1,LANCER:1,ARCHER:1,DRAGON_RIDER:2,WARRIOR:1,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               HERO_2:{SABER:1,LANCER:1,ARCHER:1,DRAGON_RIDER:2,WARRIOR:1,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1},
               HERO_3:{SABER:1,LANCER:1,ARCHER:1,DRAGON_RIDER:2,WARRIOR:1,WIZARD:1,HERO_1:1,HERO_2:1,HERO_3:1}}
#相克性
class Map_Basic:
    def __init__(self,kind):
        self.type=kind
        self.score=FIELD_EFFECT[kind][1]
        self.move_consumption=FIELD_EFFECT[kind][0]
        #不同地形分数、消耗移动力不同
        #(move_consumption,score,attack_up,speed_up,defence_up)
    def effect(self,w):
        w.attack+=FIELD_EFFECT[self.type][2]
        w.speed+=FIELD_EFFECT[self.type][3]
        w.defence+=FIELD_EFFECT[self.type][4]
        return []
        #地形效果
    def leave(self,w):
        w.attack-=FIELD_EFFECT[self.type][2]
        w.speed-=FIELD_EFFECT[self.type][3]
        w.defence-=FIELD_EFFECT[self.type][4]
        #离开地形后能力恢复
#基本地形：平原、山地、森林、屏障、陷阱
class Map_Turret(Map_Basic):
    def effect(self,w):
        if w.type==ARCHER:
            w.attack_range+=range(3,10)              #the attack range of archer increase
        return []
    def leave(self,w):
        if w.type==ARCHER:
            w.attack_range=[2]
class Map_Gear(Map_Basic):
    def __init__(self,kind,trap=[],barrier=[]):
        self.type=kind
        self.score=FIELD_EFFECT[kind][1]
        self.move_consumption=FIELD_EFFECT[kind][0]
        self.trap=trap
        self.barrier=barrier
        self.on=False
    def effect(self,w):
        if not self.on:
            for i in self.trap:
                m[i[0]][i[1]]=Map_Trap(TRAP)               #m is what
            for i in self.barrier:
                m[i[0]][i[1]]=Map_Basic(BARRIER)
            self.on=True
            return [(TRAP,x) for x in self.trap]+[(BARRIER,x) for x in self.barrier]
        else:
            return []
class Map_Temple(Map_Basic):
    def __init__(self,kind):
        self.type=kind
        self.score=FIELD_EFFECT[kind][1]
        self.move_consumption=FIELD_EFFECT[kind][0]
        self.time=0
        self.up=random.choice([1,2,3])
    def effect(self,w):
        if self.time>=TEMPLE_UP_TIME and ((w.type<6 and w.up<BASE_UP_LIMIT) or (w.type>5 and w.up<HERO_UP_LIMIT)):
            w.up+=1
            if self.up==1:
                w.attack+=1
            if self.up==2:
                w.speed+=1
            if self.up==3:
                w.defence+=1
            self.time=0
            self.up=random.choice([1,2,3])
            return []
#特殊地形：炮塔、机关、神庙
class Base_Unit:
    def __init__(self,kind,position=(0,0)):
        self.type=kind
        self.up=0
        self.position=position
        self.life=ABILITY[kind][0]
        self.attack=ABILITY[kind][1]
        self.speed=ABILITY[kind][2]
        self.defence=ABILITY[kind][3]
        self.move_range=ABILITY[kind][4]
        self.attack_range=ABILITY[kind][5]
        self.move_speed=ABILITY[kind][6]
#(LIFE,ATTACK,SPEED,DEFENCE,MOVE_RANGE,ATTACK_RANGE,MOVE_SPEED)        
    def move(self,x,y):
        self.position=(x,y)
        #移动至(x,y)
    def attack(self,enemy):
        r=random.uniform(0,100)
        enemy.life-=(self.attack-enemy.defence)*(r<=(self.speed*3-enemy.speed*2))*BASE_ATTACK_EFFECT[self.type][enemy.type]
        #¹¥»÷ enemy    
    def __lt__(self,orther):
        return self.move_speed>orther.move_speed
class Wizard(Base_Unit):
    def skill(self,other):
        other.life+=self.attack
        if other.life>ABILITY[other.type][0]:
            other.life=ABILITY[other.type][0]
        #对other使用回复技能
class Hero(Base_Unit):
    def skill(self,w):
        pass
        #英雄技能
class Begin_Info:
    def __init__(self,whole_map,base,hero_type=[6,6]):
        self.map=whole_map
        self.base=base
        self.hero_type=hero_type
class Round_Begin_Info:
    def __init__(self,move_unit,move_range):
        self.id=move_unit
        self.range=move_range
class Command:
    def __init__(self,move_position,order,target_id=0):
        self.move=move_position
        self.order=order
        self.target=target_id
class Round_End_Info:
    def __init__(self,base,map_change,route,score,over=-1):
        self.base=base
        self.change=map_change
        self.route=route
        self.score=score
        self.over=over
