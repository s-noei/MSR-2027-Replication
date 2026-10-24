# RefactorAssist Replication Package

This repository is the replication package for RefactorAssist.

## Package Scope

The active package contains four components:

1. Pipeline implementation:
   - [feedback_loop](feedback_loop)
2. Dataset and repository metadata used by the pipeline:
   - [data/dataset.csv](data/dataset.csv)
   - [data/repositories.csv](data/repositories.csv)
   - [data/repository_stats.csv](data/repository_stats.csv)
3. Final results organized by research question:
   - [results](results)
4. The RQ1 zero-shot prompt template:
   - [appendix/rq1_zero_shot.txt](appendix/rq1_zero_shot.txt)

## Repository Layout

- [feedback_loop](feedback_loop): RefactorAssist runtime and repair loop.
- [appendix/rq1_zero_shot.txt](appendix/rq1_zero_shot.txt): Zero-shot prompt shown for the initial RQ1 model comparison.
- [data](data): CSV inputs and repository metadata.
- [results/rq1](results/rq1): RQ1 pass-rate artifacts.
- [results/rq2](results/rq2): RQ2 failure-category artifact.
- [results/rq3](results/rq3): RQ3 feedback-loop artifacts.
- [results/rq4](results/rq4): RQ4 ablation artifacts.

The RQ1 template is separate from the stage-specific prompts in `feedback_loop`.

## Running the Pipeline

Entry point:

- [feedback_loop/main.py](feedback_loop/main.py)

The pipeline supports two initial-refactor modes:

- generate: run the initial StarCoder refactor in the loop.
- precomputed: start from pre-generated iter1 files.

Example:

```bash
python feedback_loop/main.py \
  --cuda-device cuda:0 \
  --input-csv data/dataset.csv \
  --output-file results_new.csv \
  --initial-refactor-mode generate
```

## Input CSV Expectations

The pipeline expects rows with:

- repository identifier: repo or repository
- method path: method
- test path: test_method

## Recreating the RQ1 Figures

With pandas and Matplotlib installed, run the following from the package root:

```bash
python plots/plot_rq1_prompting.py
```

The script combines method- and class-level counts into project-level pass rates for each model and shot count. It writes the one-column boxplot to `results/rq1/fewshot_pass_rates_boxplot_spec.pdf`.

To recreate the matching refactoring-scope boxplot, run:

```bash
python plots/plot_rq1_scope.py
```

This script pools prompting settings into project-level pass rates for each model and scope. It writes `results/rq1/rq1_method_vs_class_pass_boxplot.pdf`.

## Recreating the RQ3 Pipeline Figure

Run the following from the package root:

```bash
python plots/plot_rq3_pipeline.py
```

The script plots the reported pipeline checkpoints in `results/rq3/pipeline_checkpoints.csv` and writes `results/rq3/rq3_feedback_loop.pdf`. It requires pandas, Matplotlib, and SciPy. The smooth curve interpolates between reported checkpoints; the package does not report intermediate RQ3 values for iterations 4--9. The checkpoint CSV reproduces the manuscript figure; it is not a per-refactoring results file. The more detailed RQ4 ablation plot remains in `results/rq4/ablation_cumulative_trendlines.pdf`.
