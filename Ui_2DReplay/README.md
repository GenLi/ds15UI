目前，需用到的类是Ui_2DReplayWidget.py里面的Ui_2DReplayWidget.
会用到的成员和函数:

Ui_2DReplayView.UiD_BattleData self.data = None
所有战斗信息均储存于此。内部数据，初始化时默认值为None。

int self.nowRound = 0
int self.status = 0
以上两个值为widget的当前回合状态。是内部状态量，可以通过函数GoToRound改变，允许外部读取，但希望不要在外部直接改变此数值。

nowRound为当前正在展示第几回合。初始化时默认值为0。
status为当前正在展示的是回合开始的状态还是回合结束的状态。有两个取值：0（Ui_2DReplayWidget.BEGIN_FLAG）和1（Ui_2DReplayWidget.END_FLAG）。

int self.latestRound = -1
int self.latestStatus = 0
表示当前self.data更新到第几回合的数值。这两个数会随data的数据更新而改变。
不允许外部改变这两个值。

int self.animState = 0
当前动画播放的状态，0表示动画停止。不允许外部改变此值。


Ui_2DReplayWidget.__init__(self, QGraphicsScene scene, parent = None):
详见QGraphicsView的构造函数。

void Ui_2DReplayWidget.Initialize(self, basic.Begin_Info iniInfo, basic.Round_Begin_Info begInfo):
设置初始状态iniInfo为初始信息，begInfo为首回合信息。在这个函数被调用之前，调用后面的函数均会报错。
（目前在动画播放状态下调用此函数可能会导致程序出错，以后我可能会改，但当前务必在调用此函数前先把动画停止掉）

void Ui_2DReplayWidget.UpdateBeginData(self, basic.Begin_Info begInfo):
void Ui_2DReplayWidget.UpdateEndData(self, basic.Command cmd, basic.Round_End_Info endInfo):
更新data里的数据和latesRound、latestStatus的值。前者为更新回合开始的数据，后者为更新回合结束的数据，二者要轮流调用，否则会报错。

void Ui_2DReplayWidget.Play(self, int flag = None):
从当前的nowRound和status开始连续播放回放，直到latestRound时停止，并发出错误信息。
调用该函数时，当前正在进行的动画播放会强制停止。
flag是接受信号用的参数，外部不需关注。

void Ui_2DReplayWidget.GoToRound(self, int round = None, int flag = None):
通过改变widget的当前回合状态，直接跳转到round回合的flag状态并展示。
调用此函数会使当前动画强制停止。
若后两个参数有缺省，widget的当前回合状态的相应值不会改变。可以通过直接调用self.GoToRound()来实现暂停。
如果跳转的回合状态超过了最新的回合状态（latestRound、latestStatus）则操作无效并报错。

unitSelected = QtCore.pyqtSignal(Map_Basic)
mapGridSelected = QtCore.pyqtSignal(Base_Unit)
请求展示信息的信号，参数为待展示的信息。

目前还没有定义错误信息，而且信号模块等一些东西还没实现。我做好后再给大家发源码。
平台的接口过一阵我会发给大家。
另外，新发的basic里面，文件末最后四个类为平台传来信息的定义，大家看看。
