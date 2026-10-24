"""Recreate the one-column RQ1 boxplot from project-level pass-rate data."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


package_root = Path(__file__).resolve().parents[1]
parser = ArgumentParser(description=__doc__)
parser.add_argument(
    "--input",
    type=Path,
    default=package_root / "results/rq1/rq1_llm_refactoring_results.csv",
)
parser.add_argument(
    "--output",
    type=Path,
    default=package_root / "results/rq1/fewshot_pass_rates_boxplot_spec.pdf",
)
parser.add_argument("--preview", type=Path, help="Optional PNG preview path")
args = parser.parse_args()

rows = pd.read_csv(args.input)
# Combine method- and class-level counts for each project/model/shot boxplot.
project_rates = (
    rows.groupby(["project_id", "model", "shot_count"], as_index=False)[
        ["n_pass", "n_valid_refactorings"]
    ]
    .sum()
)
project_rates["pass_rate"] = (
    100 * project_rates["n_pass"] / project_rates["n_valid_refactorings"]
)

models = [
    ("StarCoder2", "StarCoder2", "#6487a7"),
    ("Qwen2.5-Coder-32B-Instruct", "Qwen2.5-Coder-32B", "#e89748"),
    ("Claude Sonnet", "Claude 3.5 Sonnet", "#d97176"),
    ("GPT-4o", "GPT-4o", "#79aaa6"),
]
shots = [0, 1, 3, 5]
offsets = [-0.33, -0.11, 0.11, 0.33]

plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "font.size": 8})
figure, ax = plt.subplots(figsize=(3.48, 2.90))
figure.subplots_adjust(left=0.17, right=0.99, bottom=0.16, top=0.86)

for model_index, (model, label, color) in enumerate(models):
    samples = [
        project_rates.loc[
            (project_rates["model"] == model) & (project_rates["shot_count"] == shot),
            "pass_rate",
        ].to_numpy()
        for shot in shots
    ]
    positions = [shot_index + offsets[model_index] for shot_index in range(4)]
    plot = ax.boxplot(
        samples,
        positions=positions,
        widths=0.17,
        patch_artist=True,
        showfliers=False,
        whis=(0, 100),
        medianprops={"color": "#20272d", "linewidth": 1.0},
        whiskerprops={"color": "#30383f", "linewidth": 0.7},
        capprops={"color": "#30383f", "linewidth": 0.7},
        boxprops={"color": "#30383f", "linewidth": 0.7},
    )
    for box in plot["boxes"]:
        box.set_facecolor(color)
        box.set_alpha(0.85)
    for position, sample in zip(positions, samples):
        ax.text(
            position,
            sample.max() + 0.7,
            f"{pd.Series(sample).median():.0f}",
            ha="center",
            va="bottom",
            color="#30383f",
            fontsize=6.3,
            fontweight="bold",
        )

ax.set_xlim(-0.63, 3.63)
ax.set_ylim(54, 93)
ax.set_xticks(range(4), [f"{shot}-shot" for shot in shots])
ax.set_yticks([55, 65, 75, 85])
ax.tick_params(axis="both", labelsize=7.8, pad=2, length=2.5)
ax.set_ylabel("Unit-test pass rate (%)", fontsize=8.3, labelpad=3)
ax.set_xlabel("Prompting setting", fontsize=8.3, labelpad=3)
ax.grid(axis="y", color="#d9dfe4", linewidth=0.5)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["bottom", "left"]].set_linewidth(0.6)

figure.legend(
    handles=[Patch(facecolor=color, edgecolor="#30383f", label=label) for _, label, color in models],
    loc="upper center",
    bbox_to_anchor=(0.55, 0.995),
    ncol=2,
    fontsize=7.3,
    frameon=False,
    handlelength=1.2,
    columnspacing=0.7,
    handletextpad=0.4,
)

args.output.parent.mkdir(parents=True, exist_ok=True)
figure.savefig(args.output)
if args.preview:
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.preview, dpi=260)
plt.close(figure)
