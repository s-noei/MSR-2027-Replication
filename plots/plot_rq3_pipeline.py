"""Recreate the one-column RQ3 pipeline plot from reported checkpoints."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator


package_root = Path(__file__).resolve().parents[1]
parser = ArgumentParser(description=__doc__)
parser.add_argument(
    "--input",
    type=Path,
    default=package_root / "results/rq3/pipeline_checkpoints.csv",
)
parser.add_argument(
    "--output",
    type=Path,
    default=package_root / "results/rq3/rq3_feedback_loop.pdf",
)
parser.add_argument("--preview", type=Path, help="Optional PNG preview path")
args = parser.parse_args()

rows = pd.read_csv(args.input, dtype={"stage": str})
expected_stages = ["Base", "Static", "1", "2", "3", "10"]
if rows["stage"].tolist() != expected_stages:
    raise ValueError(f"Expected checkpoint stages {expected_stages}")
rates = rows["overall_pass_rate_pct"].to_numpy()
positions = [-1, 0, 1, 2, 3, 10]

plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "font.size": 8})
figure, ax = plt.subplots(figsize=(3.48, 2.90))
figure.subplots_adjust(left=0.17, right=0.99, bottom=0.22, top=0.94)

line_color = "#6487a7"
# Interpolation gives a smooth guide through reported checkpoints; iterations 4–9
# are not observed RQ3 measurements.
curve_x = np.linspace(positions[0], positions[-1], 400)
curve_y = PchipInterpolator(positions, rates)(curve_x)
ax.plot(curve_x, curve_y, color=line_color, linewidth=1.6)

ax.set_xlim(-1.5, 10.5)
ax.set_ylim(60, 100)
ax.set_xticks([-1, 0, *range(1, 11)], ["Base", "Static", *map(str, range(1, 11))])
ax.set_yticks([60, 70, 80, 90, 100])
ax.tick_params(axis="both", labelsize=7.8, pad=2, length=2.5)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
ax.set_xlabel("Repair stage", fontsize=8.3, labelpad=3)
ax.set_ylabel("Overall unit-test pass rate (%)", fontsize=8.3, labelpad=3)
ax.grid(axis="y", color="#d9dfe4", linewidth=0.5)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["bottom", "left"]].set_linewidth(0.6)

args.output.parent.mkdir(parents=True, exist_ok=True)
figure.savefig(args.output)
if args.preview:
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.preview, dpi=260)
plt.close(figure)
