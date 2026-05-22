"""Shared Matplotlib style helpers for course paper figures."""

from __future__ import annotations

from pathlib import Path


COURSE_PAPER_PALETTE = {
    "blue": "#2F5597",
    "red": "#C00000",
    "green": "#548235",
    "gold": "#BF9000",
    "teal": "#2A9D8F",
    "purple": "#6A5ACD",
    "ink": "#1F2937",
    "body": "#4B5563",
    "grid": "#D9E2F3",
}


def apply_course_paper_style(plt, *, font_family: str = "Microsoft YaHei") -> None:
    """Apply a restrained academic chart style to a Matplotlib pyplot module."""
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
            "font.family": "sans-serif",
            "font.sans-serif": [
                font_family,
                "SimHei",
                "DengXian",
                "Source Han Sans SC",
                "Noto Sans CJK SC",
                "Arial",
                "DejaVu Sans",
            ],
            "font.size": 9,
            "axes.titlesize": 12,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.linewidth": 0.8,
            "axes.edgecolor": COURSE_PAPER_PALETTE["ink"],
            "axes.labelcolor": COURSE_PAPER_PALETTE["ink"],
            "xtick.color": COURSE_PAPER_PALETTE["body"],
            "ytick.color": COURSE_PAPER_PALETTE["body"],
            "grid.color": COURSE_PAPER_PALETTE["grid"],
            "grid.linewidth": 0.5,
            "grid.alpha": 0.6,
            "legend.frameon": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def paper_figure_size(kind: str = "wide") -> tuple[float, float]:
    """Return practical figure sizes for A4 paper insertion."""
    sizes = {
        "wide": (6.8, 3.8),
        "half": (4.6, 3.0),
        "square": (4.2, 4.2),
        "tall": (4.4, 5.4),
    }
    return sizes.get(kind, sizes["wide"])


def save_paper_figure(fig, output_base: str | Path, *, transparent: bool = False) -> dict[str, str]:
    """Save PNG and PDF copies for paper insertion and future regeneration."""
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    png = base.with_suffix(".png")
    pdf = base.with_suffix(".pdf")
    fig.savefig(png, transparent=transparent)
    fig.savefig(pdf, transparent=transparent)
    return {"png": str(png), "pdf": str(pdf)}

