import numpy as np
import matplotlib.animation as ma
import matplotlib.pyplot as plt

# 自定义一种可以存放在ndarray里的类型，用于保存一个球
ball_type = np.dtype([
    ('position', float, 2),  # 位置(水平和垂直坐标)
    ('size', float, 1),  # 大小
    ('growth', float, 1),  # 生长速度
    ('color', float, 4)])  # 颜色(红、绿、蓝和透明度)

# 随机生成100个点对象
n = 100
balls = np.zeros(100, dtype=ball_type)
balls['position'] = np.random.uniform(0, 1, (n, 2))
balls['size'] = np.random.uniform(40, 70, n)
balls['growth'] = np.random.uniform(10, 20, n)
balls['color'] = np.random.uniform(0, 1, (n, 4))

plt.figure("Animation", facecolor='lightgray')
plt.title("Animation", fontsize=14)
plt.xticks(())
plt.yticks(())

sc = plt.scatter(
    balls['position'][:, 0],
    balls['position'][:, 1],
    balls['size'],
    color=balls['color'], alpha=0.5)


# 定义更新函数行为
def update(number):
    balls['size'] += balls['growth']
    # 每次让一个气泡破裂，随机生成一个新的
    boom_ind = number % n
    balls[boom_ind]['size'] = np.random.uniform(40, 70, 1)
    balls[boom_ind]['position'] = np.random.uniform(0, 1, (1, 2))
    # 重新设置属性
    sc.set_sizes(balls['size'])
    sc.set_offsets(balls['position'])


# 每隔30毫秒执行一次update更新函数，作用于mp.gcf()当前窗口对象
# plt.gcf()：	获取当前窗口
# update：		更新函数
# interval：	间隔时间（单位：毫秒）
anim = ma.FuncAnimation(plt.gcf(), update, interval=10)
plt.show()
