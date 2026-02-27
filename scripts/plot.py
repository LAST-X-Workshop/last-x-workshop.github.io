import matplotlib.pyplot as plt
import numpy as np

def two_bar_plot(labels, values, colors, *,
                 title="",
                 ylabel="",
                 value_fmt="{:.2f}",
                 figsize=(4, 4),
                 dpi=200,
                 outpath=None):
    """
    labels : list[str]
    values : list[float]
    colors : list[str]  (e.g., ["#1f77b4", "#ff7f0e"] or ["tab:blue", "tab:orange"])
    """

    assert len(labels) == len(values) == len(colors), "labels, values, colors must match"

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    bars = ax.bar(labels, values, color=colors)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel(ylabel)

    # Clean look
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Value labels
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h,
            value_fmt.format(h),
            ha="center",
            va="bottom",
            fontsize=11,
        )

    ax.set_ylim(0, max(values) * 1.15)

    plt.tight_layout()
    if outpath:
        plt.savefig(outpath, bbox_inches="tight")
    # plt.show()


def barplot_varlen(
    values,
    *,
    labels=None,
    colors=None,
    title="",
    ylabel="",
    value_fmt="{:.2f}",
    figsize=(4.5, 4),
    dpi=200,
    rotation=0,
    outpath=None,
):
    """
    values : array-like of floats (any length)
    labels : array-like of str, optional (defaults to indices)
    colors : array-like of color specs, optional (cycled if shorter)
    """

    values = np.asarray(values, dtype=float)
    n = len(values)
    if n == 0:
        raise ValueError("values must be non-empty")

    if labels is None:
        labels = [f"{i}" for i in range(n)]
    if len(labels) != n:
        raise ValueError("labels length must match values length")

    # If colors not provided, use matplotlib default cycle
    if colors is None:
        colors = [None] * n
    # If fewer colors than bars, cycle them
    if len(colors) < n:
        colors = (colors * (n // len(colors) + 1))[:n]

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    bars = ax.bar(labels, values, color=colors)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel(ylabel)

    # Clean, publication-friendly style
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", rotation=rotation)

    # Value labels
    for bar, v in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            v,
            value_fmt.format(v),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # Headroom
    vmax = np.nanmax(values)
    ax.set_ylim(0, vmax * 1.15 if vmax > 0 else 1.0)

    plt.tight_layout()
    if outpath:
        plt.savefig(outpath, bbox_inches="tight")
    # plt.show()


def pieplot_varlen(
    values,
    *,
    labels=None,
    colors=None,
    title="",
    autopct="%1.1f%%",
    startangle=90,
    figsize=(4, 4),
    dpi=200,
    outpath=None,
):
    """
    values : array-like of numbers (e.g., [30, 14])
    labels : array-like of str, optional (e.g., ["0", "1"])
    colors : array-like of color specs, optional
    """

    values = np.asarray(values, dtype=float)
    if values.size == 0 or values.sum() == 0:
        raise ValueError("values must be non-empty and sum to > 0")

    if labels is None:
        labels = [str(i) for i in range(len(values))]
    if len(labels) != len(values):
        raise ValueError("labels length must match values length")

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    ax.pie(
        values,
        labels=[f"{l} ({int(v)})" for l, v in zip(labels, values)],
        colors=colors,
        autopct=autopct,
        startangle=startangle,
    )

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("equal")  # keep circle

    plt.tight_layout()
    if outpath:
        plt.savefig(outpath, bbox_inches="tight")
    # plt.show()


# -------- Example usage --------
labels = ["Submissions", "Accepted"]
values = [22, 10]
colors = ["#4C72B0", "#DD8452"]  # color-blind friendly

two_bar_plot(
    labels,
    values,
    colors,
    title="Submission Numbers",
    ylabel="Number",
    value_fmt="{}",
    outpath="Acceptance.png",
)


barplot_varlen(
    values=[2.5072, 3.0909, 1.97222],
    labels=["Overall", "Accepted", "Rejected"],
    colors=["#3DA5D9", "#73BFB8", "#3C3C3C"],  # cycles
    title="Scores",
    ylabel="Average Scores",
    value_fmt="{:.2f}",
    outpath="Scores.png",
)

countries = [
    "US", "DE", "AU", "CN", "SE", "BE", "GB",
    "AT", "IN", "PT", "CA", "JP", "TH", "TR"
]

counts = [
    25, 6, 5, 4, 4, 3, 3,
    2, 2, 2, 1, 1, 1, 1
]

colors = [
    "#4C72B0", "#55A868", "#C44E52", "#8172B3",
    "#CCB974", "#64B5CD", "#8C8C8C",
    "#4C72B0", "#55A868", "#C44E52",
    "#8172B3", "#CCB974", "#64B5CD", "#8C8C8C",
]

barplot_varlen(
    values=counts,
    labels=countries,
    colors=colors,
    title="Author Distribution by Country",
    ylabel="Count",
    value_fmt="{:.0f}",
    rotation=45,
    outpath="country_frequency.png",
)

countries = [
    "US", "DE", "AU", "BE",
    "CN", "AT", "PT", "IN",
    "SE", "GB"
]

counts = [
    17, 5, 4, 3,
    2, 2, 2, 2,
    1, 1
]

colors = [
    "#4C72B0", "#55A868", "#C44E52", "#8172B3",
    "#CCB974", "#64B5CD", "#8C8C8C", "#4C72B0",
    "#55A868", "#C44E52",
]

barplot_varlen(
    values=counts,
    labels=countries,
    colors=colors,
    title="Accepted Papers: Author Distribution by Country",
    ylabel="Count",
    value_fmt="{:.0f}",
    rotation=45,
    outpath="accepted_country_distribution.png",
)

barplot_varlen(
    values=[3.05, 4.40, 1.92],
    labels=["Overall", "Accepted", "Rejected"],
    colors=["#4C72B0", "#55A868", "#C44E52"],
    title="Average Number of Authors per Paper",
    ylabel="Average Authors",
    value_fmt="{:.2f}",
    outpath="avg_authors_per_paper.png",
)

pieplot_varlen(
    values=[30, 14],
    labels=["Academia", "Industry"],
    colors=["#1F7A8C", "#DB222A"],
    title="",
    outpath="industry_vs_academia.png",
)