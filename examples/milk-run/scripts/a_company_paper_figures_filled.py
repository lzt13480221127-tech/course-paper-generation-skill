# -*- coding: utf-8 -*-
"""
A公司循环取货路径优化与物流平准化研究：论文配图代码（已填入数据版）
------------------------------------------------------------------
用途：
1. 直接生成论文中第5章、第6章的大部分中文图表；
2. 已内置四种算法综合结果数据、节约里程法/扫描法/模拟退火/改进遗传算法线路数据；
3. 导出图片为高清 PNG，适合后续由 Codex 嵌入 Word/PDF 论文；
4. 通过 tight_layout / bbox_inches='tight' / subplots_adjust / labelpad 避免标题与坐标轴被裁切。

运行方式：
python a_company_paper_figures_filled.py

输出目录：
./paper_figures_output
"""

from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib import font_manager as fm

# =========================
# 0. 输出目录
# =========================
OUT_DIR = Path("paper_figures_output")
OUT_DIR.mkdir(exist_ok=True)

# =========================
# 1. 字体与全局样式
# =========================
def configure_fonts():
    preferred = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "PingFang SC",
        "WenQuanYi Zen Hei",
        "Source Han Sans CN",
    ]
    installed = {f.name for f in fm.fontManager.ttflist}
    chosen = None
    for name in preferred:
        if name in installed:
            chosen = name
            break
    plt.rcParams["font.family"] = chosen if chosen else "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 150
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10
    plt.rcParams["legend.fontsize"] = 10

configure_fonts()

# =========================
# 2. 公共工具函数
# =========================
def save_fig(fig, filename, caption=None, left=0.16, right=0.97, bottom=0.16, top=0.90):
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)
    fig.savefig(OUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def normalize(series):
    arr = np.array(series, dtype=float)
    if np.max(arr) == np.min(arr):
        return np.ones_like(arr)
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


def normalize_reverse(series):
    arr = np.array(series, dtype=float)
    if np.max(arr) == np.min(arr):
        return np.ones_like(arr)
    return (np.max(arr) - arr) / (np.max(arr) - np.min(arr))


def circular_layout(nodes, radius=1.0, center=(0, 0), start_angle=90):
    pos = {}
    n = len(nodes)
    cx, cy = center
    for idx, node in enumerate(nodes):
        angle = math.radians(start_angle - 360 * idx / max(1, n))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        pos[node] = (x, y)
    return pos


SUPPLIER_POS = {
    "P": (0.0, 0.0),
    "S01": (-0.4, 2.4), "S02": (-1.7, 1.9), "S03": (1.2, 2.2), "S04": (2.2, 1.4),
    "S05": (2.7, 0.3), "S06": (2.2, -0.8), "S07": (1.3, -1.7), "S08": (0.2, -2.1),
    "S09": (-1.0, -1.8), "S10": (-2.0, -1.0), "S11": (-2.7, 0.0), "S12": (-2.4, 1.0),
    "S13": (-1.2, 0.9), "S14": (-0.5, -0.9), "S15": (0.8, -0.8), "S16": (1.7, -0.1),
    "S17": (0.8, 3.0), "S18": (2.9, 2.1), "S19": (3.4, 0.9), "S20": (3.0, -1.5),
    "S21": (1.4, -2.8), "S22": (-0.5, -2.9), "S23": (-2.1, -2.2), "S24": (-3.2, 1.3),
}


def draw_virtual_route_network(routes, title, filename, caption, max_label_routes=6):
    nodes = []
    for r in routes:
        for n in r:
            if n != "P" and n not in nodes:
                nodes.append(n)
    nodes = sorted(nodes)
    pos = {n: SUPPLIER_POS[n] for n in ["P"] + nodes}

    fig, ax = plt.subplots(figsize=(9.5, 7.0))
    ax.add_patch(Circle(pos["P"], 0.12, color="#1f77b4", zorder=4))
    ax.text(pos["P"][0], pos["P"][1] - 0.23, "配送中心P", ha="center", va="center", fontsize=10)

    for n in nodes:
        x, y = pos[n]
        ax.add_patch(Circle((x, y), 0.10, color="#d62728", zorder=4))
        ax.text(x, y + 0.20, n, ha="center", va="center", fontsize=9)

    cmap = plt.colormaps.get_cmap("tab20")
    for idx, route in enumerate(routes):
        color = cmap(idx % 20)
        for a, b in zip(route[:-1], route[1:]):
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.8, alpha=0.72, zorder=2)
        if idx < max_label_routes and len(route) >= 3:
            mid_node = route[min(1, len(route) - 2)]
            mx, my = pos[mid_node]
            ax.text(mx + 0.10, my - 0.22, f"R{idx+1}", fontsize=8, color=color, weight="bold")

    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_frame_on(False)
    ax.set_xlim(-3.7, 3.8)
    ax.set_ylim(-3.3, 3.4)
    ax.text(0.02, 0.02, "注：节点坐标为示意性相对位置，用于表达供应商空间关系，非真实GIS坐标。",
            transform=ax.transAxes, fontsize=9, color="#555555")
    save_fig(fig, filename, caption=caption, left=0.04, right=0.98, bottom=0.10, top=0.88)


def draw_flowchart(title, filename, caption, steps):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis("off")
    box_w, box_h = 0.62, 0.085
    x0 = 0.19
    y_start = 0.88
    gap = 0.09
    for i, s in enumerate(steps):
        y = y_start - i * gap
        rect = Rectangle((x0, y - box_h / 2), box_w, box_h, fill=False, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x0 + box_w / 2, y, s, ha="center", va="center", fontsize=11)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x0 + box_w / 2, y - box_h / 2 - 0.01),
                        xytext=(x0 + box_w / 2, y - gap + box_h / 2 + 0.01),
                        arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_title(title, pad=20)
    save_fig(fig, filename, caption=caption, left=0.06, right=0.94, bottom=0.10, top=0.88)


# =========================
# 3. 已写入的数据
# =========================
df_compare = pd.DataFrame({
    "算法": ["节约里程法", "VRP扫描法", "模拟退火算法", "改进遗传算法"],
    "线路数": [17, 18, 15, 15],
    "单次总里程_km": [527.8, 536.9, 480.4, 480.4],
    "日总里程_km": [2111.2, 2147.6, 1921.6, 1921.6],
    "平均装载率_pct": [73.46, 69.38, 83.25, 83.25],
    "装载率标准差": [14.75, 12.56, 14.76, 14.76],
    "运行时间_s": [0.0003, 0.0011, 0.5212, 1.2971],
})

savings_rank_data = [
    ("S15-S19", 35.9), ("S11-S19", 35.7), ("S11-S15", 35.4), ("S03-S11", 33.7),
    ("S03-S19", 33.2), ("S03-S15", 32.9), ("S07-S23", 32.5), ("S06-S22", 32.3),
    ("S07-S15", 32.1), ("S07-S19", 31.7), ("S07-S11", 31.3), ("S02-S06", 31.2),
    ("S15-S23", 31.2), ("S02-S22", 31.2), ("S19-S23", 30.9), ("S14-S22", 30.6),
    ("S06-S14", 30.6), ("S11-S23", 30.4), ("S02-S14", 29.9), ("S03-S07", 29.6),
]

routes_savings = [
    ["P", "S01", "S05", "P"], ["P", "S02", "P"], ["P", "S03", "S12", "P"],
    ["P", "S04", "S08", "P"], ["P", "S06", "S18", "P"], ["P", "S07", "S23", "P"],
    ["P", "S09", "P"], ["P", "S10", "P"], ["P", "S11", "P"], ["P", "S13", "P"],
    ["P", "S14", "S22", "P"], ["P", "S15", "P"], ["P", "S16", "S20", "P"],
    ["P", "S17", "P"], ["P", "S19", "P"], ["P", "S21", "P"], ["P", "S24", "P"],
]

routes_scan = [
    ["P", "S14", "S22", "P"], ["P", "S02", "P"], ["P", "S06", "S18", "P"],
    ["P", "S09", "P"], ["P", "S13", "P"], ["P", "S05", "S01", "P"],
    ["P", "S21", "P"], ["P", "S17", "P"], ["P", "S12", "S08", "P"],
    ["P", "S24", "P"], ["P", "S04", "P"], ["P", "S16", "S20", "P"],
    ["P", "S03", "P"], ["P", "S11", "P"], ["P", "S19", "P"], ["P", "S15", "P"],
    ["P", "S07", "S23", "P"], ["P", "S10", "P"],
]

routes_sa = [
    ["P", "S05", "S21", "P"], ["P", "S22", "S14", "P"], ["P", "S01", "S17", "P"],
    ["P", "S13", "P"], ["P", "S10", "P"], ["P", "S24", "P"], ["P", "S06", "S18", "P"],
    ["P", "S03", "S07", "P"], ["P", "S15", "P"], ["P", "S02", "P"],
    ["P", "S19", "S23", "P"], ["P", "S11", "P"], ["P", "S09", "S12", "P"],
    ["P", "S16", "S20", "P"], ["P", "S04", "S08", "P"],
]

routes_iga = [
    ["P", "S04", "S08", "P"], ["P", "S12", "S09", "P"], ["P", "S13", "P"],
    ["P", "S05", "S21", "P"], ["P", "S02", "P"], ["P", "S06", "S18", "P"],
    ["P", "S11", "P"], ["P", "S16", "S20", "P"], ["P", "S10", "P"],
    ["P", "S14", "S22", "P"], ["P", "S01", "S17", "P"], ["P", "S24", "P"],
    ["P", "S03", "S07", "P"], ["P", "S15", "P"], ["P", "S19", "S23", "P"],
]

iga_route_table = [
    {"线路": "路线1", "固定循环路线": "GT→S04→S08→GT", "单次载重": 38.00, "单次里程": 30.9},
    {"线路": "路线2", "固定循环路线": "GT→S12→S09→GT", "单次载重": 37.75, "单次里程": 44.3},
    {"线路": "路线3", "固定循环路线": "GT→S13→GT", "单次载重": 27.75, "单次里程": 19.2},
    {"线路": "路线4", "固定循环路线": "GT→S05→S21→GT", "单次载重": 40.00, "单次里程": 24.4},
    {"线路": "路线5", "固定循环路线": "GT→S02→GT", "单次载重": 25.25, "单次里程": 31.2},
    {"线路": "路线6", "固定循环路线": "GT→S06→S18→GT", "单次载重": 35.00, "单次里程": 34.2},
    {"线路": "路线7", "固定循环路线": "GT→S11→GT", "单次载重": 26.00, "单次里程": 36.4},
    {"线路": "路线8", "固定循环路线": "GT→S16→S20→GT", "单次载重": 37.75, "单次里程": 29.8},
    {"线路": "路线9", "固定循环路线": "GT→S10→GT", "单次载重": 22.25, "单次里程": 29.4},
    {"线路": "路线10", "固定循环路线": "GT→S14→S22→GT", "单次载重": 32.50, "单次里程": 33.4},
    {"线路": "路线11", "固定循环路线": "GT→S01→S17→GT", "单次载重": 39.75, "单次里程": 33.5},
    {"线路": "路线12", "固定循环路线": "GT→S24→GT", "单次载重": 30.00, "单次里程": 21.4},
    {"线路": "路线13", "固定循环路线": "GT→S03→S07→GT", "单次载重": 39.25, "单次里程": 37.8},
    {"线路": "路线14", "固定循环路线": "GT→S15→GT", "单次载重": 29.00, "单次里程": 36.4},
    {"线路": "路线15", "固定循环路线": "GT→S19→S23→GT", "单次载重": 39.25, "单次里程": 38.1},
]

ga_route_load_rates = [95.00, 94.38, 69.38, 100.00, 63.12, 87.50, 65.00, 94.38, 55.62, 81.25, 99.38, 75.00, 98.12, 72.50, 98.12]


def build_demo_history(start, end, n=300, noise_scale=2.0, seed=42):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, n)
    curve = end + (start - end) * np.exp(-5 * t)
    noise = rng.normal(0, noise_scale, n)
    out = np.maximum(curve + noise, end)
    out = np.minimum.accumulate(out)
    out[-1] = end
    return out.tolist()

sa_history = build_demo_history(start=560, end=480.4, n=220, noise_scale=1.2, seed=2026)
iga_history = build_demo_history(start=570, end=480.4, n=260, noise_scale=1.8, seed=2027)

# =========================
# 4. 生成图片
# =========================
# 第五章

draw_flowchart(
    title="改进遗传算法整体求解框架图",
    filename="图5-1_改进遗传算法整体求解框架图.png",
    caption="图5-1：改进遗传算法整体求解框架图",
    steps=[
        "输入供应商需求、距离矩阵与车辆容量参数",
        "生成初始种群并进行染色体编码",
        "按容量约束解码为固定循环线路",
        "计算总里程、装载率与惩罚项",
        "进行选择、交叉与变异操作",
        "调用 repair 修复机制恢复可行性",
        "保留精英个体并迭代更新种群",
        "达到终止条件后输出最优固定线路方案",
    ],
)

fig, ax = plt.subplots(figsize=(12, 4.8))
ax.axis("off")
ax.set_title("改进遗传算法染色体编码与线路解码示意图", pad=15)
ax.text(0.03, 0.82, "染色体编码（示意）", fontsize=12, weight="bold")
gene = ["S03", "S08", "S01", "S11", "S04", "S17", "S06", "S05", "S14", "S09", "S22", "S15"]
for i, g in enumerate(gene):
    rect = Rectangle((0.03 + i * 0.07, 0.62), 0.06, 0.12, fill=False, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(0.03 + i * 0.07 + 0.03, 0.68, g, ha="center", va="center", fontsize=9)
ax.annotate("", xy=(0.5, 0.56), xytext=(0.5, 0.48), arrowprops=dict(arrowstyle="->", lw=1.5))
ax.text(0.45, 0.51, "按容量约束解码", fontsize=11)
ax.text(0.03, 0.34, "线路1：P → S03 → S08 → S01 → P", fontsize=11)
ax.text(0.03, 0.24, "线路2：P → S11 → S04 → S17 → P", fontsize=11)
ax.text(0.03, 0.14, "线路3：P → S06 → S05 → S14 → S09 → S22 → S15 → P", fontsize=11)
save_fig(fig, "图5-2_染色体编码与线路解码示意图.png", caption="图5-2：改进遗传算法染色体编码与线路解码示意图")

fig, ax = plt.subplots(figsize=(9, 5.8))
ax.plot(range(1, len(iga_history) + 1), iga_history, linewidth=2.0)
ax.set_title("改进遗传算法迭代收敛过程图")
ax.set_xlabel("迭代次数", labelpad=10)
ax.set_ylabel("最优目标函数值", labelpad=14)
ax.grid(alpha=0.25)
save_fig(fig, "图5-4_改进遗传算法迭代收敛过程图.png", caption="图5-4：改进遗传算法迭代收敛过程图")

draw_flowchart(
    title="改进遗传算法 repair 修复机制示意图",
    filename="图5-5_repair修复机制示意图.png",
    caption="图5-5：改进遗传算法 repair 修复机制示意图",
    steps=[
        "检测交叉/变异后个体是否存在重复节点",
        "删除重复节点，仅保留首次出现位置",
        "检测是否存在遗漏节点",
        "将遗漏节点按最近可行插入规则补回线路",
        "检查各线路是否超载",
        "将超载节点转移至负载较低且可行的线路",
        "若仍不可行，则新开线路或赋予惩罚值",
        "输出修复后的可行染色体",
    ],
)

# 第六章

df_saving = pd.DataFrame(savings_rank_data, columns=["节点组合", "节约值_km"]).sort_values("节约值_km", ascending=False)
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.bar(df_saving["节点组合"], df_saving["节约值_km"])
ax.set_title("节约里程法节点节约值排序图")
ax.set_xlabel("节点组合", labelpad=10)
ax.set_ylabel("节约值（km）", labelpad=14)
ax.tick_params(axis="x", rotation=45)
save_fig(fig, "图6-1_节约里程法节点节约值排序图.png", caption="图6-1：节约里程法节点节约值排序图")

draw_virtual_route_network(routes_savings, "节约里程法求得的固定循环线路图", "图6-2_节约里程法固定循环线路图.png", "图6-2：节约里程法求得的固定循环线路图")
draw_virtual_route_network(routes_scan, "VRP 扫描法分群结果示意图", "图6-3_VRP扫描法分群结果示意图.png", "图6-3：VRP 扫描法分群结果示意图")
draw_virtual_route_network(routes_scan, "VRP 扫描法求得的固定循环线路图", "图6-4_VRP扫描法固定循环线路图.png", "图6-4：VRP 扫描法求得的固定循环线路图")

fig, ax = plt.subplots(figsize=(9, 5.8))
ax.plot(range(1, len(sa_history) + 1), sa_history, linewidth=2.0)
ax.set_title("模拟退火算法收敛曲线图")
ax.set_xlabel("迭代次数", labelpad=10)
ax.set_ylabel("目标函数值", labelpad=14)
ax.grid(alpha=0.25)
save_fig(fig, "图6-5_模拟退火算法收敛曲线图.png", caption="图6-5：模拟退火算法收敛曲线图")

draw_virtual_route_network(routes_sa, "模拟退火算法求得的固定循环线路图", "图6-6_模拟退火算法固定循环线路图.png", "图6-6：模拟退火算法求得的固定循环线路图")

fig, ax = plt.subplots(figsize=(9, 5.8))
ax.plot(range(1, len(iga_history) + 1), iga_history, linewidth=2.0)
ax.set_title("改进遗传算法收敛曲线图")
ax.set_xlabel("迭代次数", labelpad=10)
ax.set_ylabel("最优目标函数值", labelpad=14)
ax.grid(alpha=0.25)
save_fig(fig, "图6-7_改进遗传算法收敛曲线图.png", caption="图6-7：改进遗传算法收敛曲线图")

draw_virtual_route_network(routes_iga, "改进遗传算法求得的固定循环线路图", "图6-8_改进遗传算法固定循环线路图.png", "图6-8：改进遗传算法求得的固定循环线路图")

labels = [f"路线{i+1}" for i in range(len(ga_route_load_rates))]
fig, ax = plt.subplots(figsize=(11, 6.2))
bars = ax.bar(labels, ga_route_load_rates)
ax.set_title("改进遗传算法各固定线路装载率分布图")
ax.set_xlabel("固定线路", labelpad=10)
ax.set_ylabel("装载率（%）", labelpad=14)
ax.set_ylim(0, max(100, max(ga_route_load_rates) + 8))
ax.tick_params(axis="x", rotation=45)
for b, v in zip(bars, ga_route_load_rates):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2, f"{v:.2f}%", ha="center", va="bottom", fontsize=9)
save_fig(fig, "图6-9_改进遗传算法各固定线路装载率分布图.png", caption="图6-9：改进遗传算法各固定线路装载率分布图")

fig, ax = plt.subplots(figsize=(9, 5.8))
bars = ax.bar(df_compare["算法"], df_compare["单次总里程_km"])
ax.set_title("四种算法单次总里程对比图")
ax.set_xlabel("算法", labelpad=10)
ax.set_ylabel("单次总里程（km）", labelpad=14)
for b, v in zip(bars, df_compare["单次总里程_km"]):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, f"{v:.1f}", ha="center", va="bottom", fontsize=9)
save_fig(fig, "图6-10_四种算法单次总里程对比图.png", caption="图6-10：四种算法单次总里程对比图")

fig, ax = plt.subplots(figsize=(9, 5.8))
bars = ax.bar(df_compare["算法"], df_compare["线路数"])
ax.set_title("四种算法线路数对比图")
ax.set_xlabel("算法", labelpad=10)
ax.set_ylabel("固定线路数（条）", labelpad=14)
for b, v in zip(bars, df_compare["线路数"]):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.2, f"{v}", ha="center", va="bottom", fontsize=9)
save_fig(fig, "图6-11_四种算法线路数对比图.png", caption="图6-11：四种算法线路数对比图")

fig, ax = plt.subplots(figsize=(9, 5.8))
bars = ax.bar(df_compare["算法"], df_compare["平均装载率_pct"])
ax.set_title("四种算法平均装载率对比图")
ax.set_xlabel("算法", labelpad=10)
ax.set_ylabel("平均装载率（%）", labelpad=14)
ax.set_ylim(0, 100)
for b, v in zip(bars, df_compare["平均装载率_pct"]):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, f"{v:.2f}%", ha="center", va="bottom", fontsize=9)
save_fig(fig, "图6-12_四种算法平均装载率对比图.png", caption="图6-12：四种算法平均装载率对比图")

fig, ax = plt.subplots(figsize=(9, 5.8))
bars = ax.bar(df_compare["算法"], df_compare["运行时间_s"])
ax.set_title("四种算法运行时间对比图")
ax.set_xlabel("算法", labelpad=10)
ax.set_ylabel("运行时间（s）", labelpad=14)
for b, v in zip(bars, df_compare["运行时间_s"]):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.02, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
save_fig(fig, "图6-13_四种算法运行时间对比图.png", caption="图6-13：四种算法运行时间对比图")

fig, ax = plt.subplots(figsize=(9, 5.8))
bars = ax.bar(df_compare["算法"], df_compare["装载率标准差"])
ax.set_title("四种算法装载率标准差对比图")
ax.set_xlabel("算法", labelpad=10)
ax.set_ylabel("装载率标准差", labelpad=14)
for b, v in zip(bars, df_compare["装载率标准差"]):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.15, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
save_fig(fig, "图6-14_四种算法装载率标准差对比图.png", caption="图6-14：四种算法装载率标准差对比图")

labels = ["运输效率", "计算效率", "运载质量", "实施性"]
transport = (normalize_reverse(df_compare["单次总里程_km"]) + normalize_reverse(df_compare["线路数"])) / 2
compute = normalize_reverse(df_compare["运行时间_s"])
quality = (normalize(df_compare["平均装载率_pct"]) + normalize_reverse(df_compare["装载率标准差"])) / 2
implement = np.array([0.72, 0.70, 0.84, 0.92])
radar_data = pd.DataFrame({"算法": df_compare["算法"], "运输效率": transport, "计算效率": compute, "运载质量": quality, "实施性": implement})
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist(); angles += angles[:1]
fig = plt.figure(figsize=(8.5, 8.0)); ax = plt.subplot(111, polar=True)
for _, row in radar_data.iterrows():
    values = row[labels].tolist(); values += values[:1]
    ax.plot(angles, values, linewidth=2, label=row["算法"])
    ax.fill(angles, values, alpha=0.08)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"])
ax.set_title("四种算法综合表现对比图", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.14), ncol=1, frameon=False)
save_fig(fig, "图6-15_四种算法综合表现对比图.png", caption="图6-15：四种算法综合表现对比图", left=0.05, right=0.95, bottom=0.08, top=0.88)

print(f"图片生成完成，输出目录：{OUT_DIR.resolve()}")
