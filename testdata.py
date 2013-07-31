# -*- coding: UTF-8 -*-

from Ui_Units import *

m = Map_Basic
u = Base_Unit

maps = [[m(0), m(0), m(1), m(1)],
        [m(1), m(1), m(0), m(1)],
        [m(1), m(0), m(1), m(0)],
        [m(0), m(0), m(1), m(1)]]
units = [u(1, (0, 0)), u(2, (0, 1)), u(3, (0, 2)),
         u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]
units2 = [[u(1, (0, 0)), u(2, (0, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
iniInfo = Begin_Info(maps, units2)
begInfo = [Round_Begin_Info((0, 0), [], units2, None),
           Round_Begin_Info((1, 0), [], units2, None),
           Round_Begin_Info((0, 1), [], units2, None),
           Round_Begin_Info((1, 1), [], units2, None),
           Round_Begin_Info((0, 2), [], units2, None),
           Round_Begin_Info((1, 2), [], units2, None),
           Round_Begin_Info((0, 1), [], units2, None),
           Round_Begin_Info((1, 1), [], units2, None),
           Round_Begin_Info((0, 2), [], units2, None),
           Round_Begin_Info((1, 2), [], units2, None)]
cmd = [Command(0, (1, 0), 0),
       Command(0, (2, 3), 0),
       Command(0, (1, 1), 0),
       Command(0, (2, 2), 0),
       Command(0, (1, 2), 0),
       Command(0, (2, 1), 0),
       Command(1, (1, 1), (1, 2)),
       Command(1, (2, 2), (0, 2)),
       Command(1, (1, 2), (1, 1)),
       Command(1, (2, 1), (0, 1))]
endInfo = [Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 1, 1, -1),
           Round_End_Info(units2, None, 0, 0, -1),
           Round_End_Info(units2, None, 1, 2, 1)]
