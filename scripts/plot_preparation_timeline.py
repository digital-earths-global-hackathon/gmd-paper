"""Generate the preparation-timeline Gantt chart for the paper.

Usage: python scripts/plot_preparation_timeline.py OUTPUT [OUTPUT ...]

Each output format is taken from its file extension. The figure is built once
and written to every path given, so all outputs (svg for the html build, pdf
for the LaTeX build) stay in sync.
"""

import sys
from datetime import date

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

# (label, group, [(start, end), ...]) -- bottom row first
TASKS = [
    ("Planning", "infra", [("2023-10-15", "2025-05-11")]),
    ("Install common\nsoftware stack", "infra", [("2024-11-01", "2025-01-01")]),
    ("Individual host\nweb pages setup", "infra", [("2024-12-15", "2025-01-10")]),
    (
        "Registration opens at\neach host's web site",
        "infra",
        [("2025-01-12", "2025-04-01")],
    ),
    (
        "Initial distribution\nof DYAMOND data",
        "data",
        [("2024-12-01", "2025-01-29")],
    ),
    (
        "Build catalogs",
        "data",
        [
            ("2024-12-15", "2025-01-01"),
            ("2025-02-01", "2025-02-17"),
            ("2025-03-15", "2025-04-01"),
        ],
    ),
    ("Perform experiments", "data", [("2024-12-15", "2025-03-15")]),
    (
        "Additional cross-node\ndata propagation",
        "data",
        [("2025-02-01", "2025-05-01")],
    ),
    ("Global hackathon", "event", [("2025-05-12", "2025-05-17")]),
]

GROUPS = {
    "infra": ("#4878a8", "Infrastructure and organization"),
    "data": ("#c8783c", "Simulations and data"),
    "event": ("#3c8c64", "Event"),
}

XLIM = ("2023-10-01", "2025-07-01")


def build_figure():
    """Return the Gantt chart figure."""
    fig, ax = plt.subplots(figsize=(6.5, 3.6))

    for row, (_label, group, spans) in enumerate(TASKS):
        bars = [
            (
                mdates.date2num(date.fromisoformat(start)),
                mdates.date2num(date.fromisoformat(end))
                - mdates.date2num(date.fromisoformat(start)),
            )
            for start, end in spans
        ]
        ax.broken_barh(bars, (row - 0.32, 0.64), facecolor=GROUPS[group][0])

    ax.set_yticks(range(len(TASKS)))
    ax.set_yticklabels([task[0] for task in TASKS], fontsize=8)
    ax.set_ylim(-0.8, len(TASKS) - 0.2)

    locator = mdates.MonthLocator(bymonth=(1, 4, 7, 10))
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.set_xlim(date.fromisoformat(XLIM[0]), date.fromisoformat(XLIM[1]))
    ax.tick_params(axis="x", labelsize=8)

    ax.grid(axis="x", color="0.85", linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=color) for color, _ in GROUPS.values()]
    ax.legend(
        handles,
        [label for _, label in GROUPS.values()],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.30),
        ncol=len(GROUPS),
        frameon=False,
        fontsize=8,
        handlelength=1.2,
    )

    fig.tight_layout()
    return fig


def main(argv):
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    fig = build_figure()
    for output in argv[1:]:
        fig.savefig(output, bbox_inches="tight")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
