import matplotlib.pyplot as plt
import random
import math
from typing import List, Tuple


def bezier_3rd_order(p0: Tuple[float, float],
                     p1: Tuple[float, float],
                     p2: Tuple[float, float],
                     p3: Tuple[float, float],
                     t: float) -> Tuple[float, float]:
    """
    计算三阶贝塞尔曲线上的点
    B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
    """
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return (x, y)


def generate_bezier_points(start: Tuple[float, float],
                           end: Tuple[float, float],
                           control_points: List[Tuple[float, float]] = None,
                           num_points: int = 50) -> List[Tuple[float, float]]:
    """
    生成贝塞尔曲线上的点集
    :param start: 起点坐标
    :param end: 终点坐标
    :param control_points: 控制点列表（1-3个，自动补全）
    :param num_points: 生成点的数量
    """
    if control_points is None:
        # 自动生成随机控制点，制造自然弧度
        control_points = generate_natural_control_points(start, end)

    points = []
    for i in range(num_points):
        t = i / (num_points - 1)  # 0到1均匀分布

        if len(control_points) == 1:
            # 二阶贝塞尔
            p0, p1, p2 = start, control_points[0], end
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            points.append((x, y))

        elif len(control_points) == 2:
            # 三阶贝塞尔（最常用）
            p0, p1, p2, p3 = start, control_points[0], control_points[1], end
            points.append(bezier_3rd_order(p0, p1, p2, p3, t))

        elif len(control_points) >= 3:
            # 四阶以上（简化处理，只用前三个）
            points.append(bezier_3rd_order(start, control_points[0], control_points[1], end, t))

    return points


def generate_natural_control_points(start: Tuple[float, float],
                                    end: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    生成自然的控制点（模拟人类手部运动）
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # 随机决定曲线类型
    curve_type = random.choice(['slight_arc', 'overshoot', 's_shape', 'random'])

    if curve_type == 'slight_arc':
        # 轻微弧度（最常见）
        offset_x = random.uniform(-distance * 0.1, distance * 0.1)
        offset_y = random.uniform(-distance * 0.2, distance * 0.1)
        p1 = (start[0] + dx * 0.33 + offset_x, start[1] + dy * 0.33 + offset_y)
        p2 = (start[0] + dx * 0.66 + offset_x, start[1] + dy * 0.66 + offset_y)

    elif curve_type == 'overshoot':
        # 过冲（超出目标再回来）
        overshoot = distance * random.uniform(0.05, 0.15)
        p1 = (start[0] + dx * 0.4, start[1] + dy * 0.4 - overshoot)
        p2 = (start[0] + dx * 0.7, start[1] + dy * 0.7 + overshoot)

    elif curve_type == 's_shape':
        # S形曲线
        p1 = (start[0] + dx * 0.3, start[1] + dy * 0.2 - distance * 0.1)
        p2 = (start[0] + dx * 0.7, start[1] + dy * 0.8 + distance * 0.1)

    else:
        # 完全随机
        p1 = (start[0] + dx * random.uniform(0.2, 0.5),
              start[1] + dy * random.uniform(0.2, 0.5) + random.uniform(-distance * 0.2, distance * 0.2))
        p2 = (start[0] + dx * random.uniform(0.5, 0.8),
              start[1] + dy * random.uniform(0.5, 0.8) + random.uniform(-distance * 0.2, distance * 0.2))

    return [p1, p2]

def visualize_bezier():
    """可视化不同控制点生成的曲线"""
    start = (100, 500)
    end = (700, 500)

    # 不同曲线类型
    curves = {
        'straight line': None,  # 无控制点
        'Up the arc': [(400, 300)],
        'Down the arc': [(400, 700)],
        'S-like': [(300, 400), (500, 600)],
        'Overshoot': [(400, 450), (600, 550)]
    }

    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()

    for idx, (name, ctrl_points) in enumerate(curves.items()):
        if ctrl_points is None:
            # 直线
            points = [(start[0] + i / 100 * (end[0] - start[0]), start[1]) for i in range(101)]
        else:
            points = generate_bezier_points(start, end, ctrl_points, 100)

        x = [p[0] for p in points]
        y = [p[1] for p in points]

        axes[idx].plot(x, y, 'b-', linewidth=2, label='track')
        axes[idx].scatter([start[0], end[0]], [start[1], end[1]],
                          color='red', s=100, label='strat/end')
        if ctrl_points:
            ctrl_x, ctrl_y = zip(*ctrl_points)
            axes[idx].scatter(ctrl_x, ctrl_y, color='green', s=80,
                              marker='s', label='contral_point')

        axes[idx].set_title(f'{name}curve')
        axes[idx].set_xlim(0, 800)
        axes[idx].set_ylim(200, 800)
        axes[idx].invert_yaxis()
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


visualize_bezier()










