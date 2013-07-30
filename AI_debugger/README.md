调试器工作汇报:
        调试器包含程序文件:
                 1.ai_debugger.py:主界面,连接各组件
                 2.info_widget.py:信息类的定义,在主界面中是dockwidget
                 3.AI_ReplayWidget.py:一个复合窗口,复合了自定义进度条(CtrlSlider)以及Lindex工作的回放界面
                 4.Ai_Thread.py:一个线程类,平台组的接口实现在里面[我现在把这个类放到了主界面程序里,方便访问共有的数据(但我还没有设置共有数据,详情见问题部分1)]

        暂时调试器运作方法:
                1.主程序在接到用户开始游戏的指令后,initialize与平台交互的线程pltThread,pltThread将地图路径,ai路径发给平台,开始游戏.
                2.pltThread接到的所有数据都以信号的方式发给主界面,由主界面设置信息(infoWidget的信息展示),由主界面调用replaywindow(AI_ReplayWIdget的instance)包装回放界面的各种方法(比如Initialize,UpdateBeginData等)。
                3.进度条(封装在replayWindow里)可以在特定播放模式下(连续或不连续)通过发送"next"和"pause"命令让pltThread接受下一个平台传来的信息,或者停止连续接受平台传来的信息.[暂时实现方式为:通过信号调用主界面的nextRound这些方法,利用QWaitCondition的全局变量实现线程间的条件唤醒]

        存在一些问题和没有完成的部分:
                1.现在的调试器版本明显缺少对global变量的利用.所以感觉都不需要用multithread的lock,但是隐隐觉得这个会有很大隐患(不同层次的widget里面维护了一些同一个作用而且应该是同样的独立的变量),还是要把isPaused,Continuous这样的变量改成global的,用lock来改正读取.
                2.设定debug和非debug模式的工作还没有做:ai_debugger.setDebugMode(self)。
                3.胜利的结果出来的时候的胜利展示。
                4.在游戏胜利结果没有出来之前强制结束的功能:ai_debugger.endGame(self)。
                5.加载AI程序路径的功能还没有完善,(要加载两个ai):要加载两个ai对战,现在ai_debugger里的loadAIdlg方法只可以在已加载ai少于两个时加载新的ai.没有设置替换某个已加载ai的功能。
                6.进度条跳转到以前回合的时候的游戏信息展示(由于我没有仔细研究回放界面以前回合的游戏数据嵌套方法...所以没有做)在AI_ReplayWidget的setNowRound方法里的注释处发出信号给主界面,让主界面在infoWidget里展示当前跳转回合的信息.
                7.进度条回放的时候还没有调用过回放界面play方法(现在回放只是调用了goToRound没有调用从当前回合开始连续播放,如果需要可以调用)
                8.不重要:进度条里回放时暂停点的设置(这个可以完全取消掉,进度条类CtrlSlider里的pausepoint数据和addPausePoint方法,contextmenuEvent都是为这个服务(所以可以一起删掉)

水平问题...有些代码肯定写的过于冗杂(自己都觉得好繁琐。。。）如果有要问我关于这些代码的问题的，尽管发邮件给我，虽然在遥远的西藏，只要有网我就会接邮件的...
