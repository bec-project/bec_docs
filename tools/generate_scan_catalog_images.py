"""Render the catalog's example trajectories using BEC's position generators.

Run from the repository root with bec-lib and matplotlib installed:
    python tools/generate_scan_catalog_images.py
"""

from pathlib import Path

import numpy as np

from bec_lib import position_generators as positions

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "docs/assets/scan-catalog"


def example_positions():
    """Positions corresponding to the ten step-scan examples in the catalog."""
    return {
        "line_scan": positions.line_scan_positions([(-1, 1), (-1, 1)], steps=5),
        "grid_scan": positions.nd_grid_positions([(-1, 1, 5), (-1, 1, 3)]),
        "list_scan": np.column_stack(([-1, 0.5, 0, 1], [-0.5, -0.5, 1, 0])),
        "log_scan": positions.log_scan_positions([(-1, 1)], steps=7),
        "round_scan": positions.round_scan_positions(0, 1, 3, 6),
        "round_roi_scan": positions.get_round_roi_scan_positions(-1, 1, -0.5, 0.5, 0.25, 6),
        "fermat_scan": positions.fermat_spiral_pos(-1, 1, -1, 1, 0.25),
        "hexagonal_scan": positions.hex_grid_2d([(-1, 1, 0.5), (-1, 1, 3**0.5 / 4)]),
        "multi_region_line_scan": positions.multi_region_line_positions([(-1, 0, 3), (0, 1, 5)]),
        "multi_region_grid_scan": positions.multi_region_grid_positions(
            [((-1, 0, 3), (-1, 0, 3)), ((0.5, 1, 3), (0.5, 1, 2))]
        ),
    }


def render(name, targets):
    """Draw targets and their visit order; connecting lines are travel between points."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 11, "svg.hashsalt": "bec-scan-catalog"})
    fig, ax = plt.subplots(figsize=(5.6, 3.6), layout="constrained")
    if targets.shape[1] == 1:
        x = np.arange(1, len(targets) + 1)
        y = targets[:, 0]
        ax.set_xlabel("Visit index")
        ax.set_ylabel("samx target position")
        ax.set_xticks(x)
    else:
        x, y = targets[:, 0], targets[:, 1]
        ax.set_xlabel("samx target position")
        ax.set_ylabel("samy target position")
        ax.set_aspect("equal", adjustable="box")
    ax.plot(x, y, linestyle="--", color="#64748b", linewidth=0.8, alpha=0.65)
    points = ax.scatter(x, y, c=np.arange(1, len(targets) + 1), cmap="viridis", s=32, zorder=3)
    colorbar = fig.colorbar(points, ax=ax, ticks=[1, len(targets)], pad=0.03)
    colorbar.set_label("Visit index")
    ax.set_title(f"{name}: {len(targets)} positions")
    ax.grid(alpha=0.2)
    ax.margins(0.1)
    output = OUTPUT_DIR / f"{name}.svg"
    fig.savefig(output, metadata={"Date": None})
    output.write_text("\n".join(line.rstrip() for line in output.read_text().splitlines()) + "\n")
    plt.close(fig)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for scan_name, targets in example_positions().items():
        render(scan_name, targets)
