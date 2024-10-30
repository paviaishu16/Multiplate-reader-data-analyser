"""Functions related to generating a report with plots."""

import os
from typing import Any

import pandas as pd
from jinja2 import Environment, FileSystemLoader  # type: ignore

from exceptions import MTPAnalyzerException
from plotting import create_all_plots

EXPORT_DIR = "exports"


def generate_report(
    cleaned_observed_data: pd.DataFrame,
    gompertz_metrics: pd.DataFrame,
    richards_metrics: pd.DataFrame,
    dest_dir: str = EXPORT_DIR,
) -> None:
    """Generate a HTML report with and model fit data for samples."""
    if not gompertz_metrics.index.equals(richards_metrics.index):
        raise MTPAnalyzerException("Misaligned dataframes")
    if not cleaned_observed_data.columns.equals(gompertz_metrics.index):
        raise MTPAnalyzerException("Misaligned dataframes")

    plots = create_all_plots(cleaned_observed_data, gompertz_metrics, richards_metrics)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("src/report_template.html")

    template_data: list[dict[str, Any]] = []
    for sample_name in gompertz_metrics.index:
        gompertz_table = gompertz_metrics.loc[
            [sample_name],
            ["N_0_opt", "N_inf_opt", "alpha_opt"],
        ].to_html(index=False)
        richards_table = richards_metrics.loc[
            [sample_name],
            ["A_opt", "k_opt", "t0_opt", "A0_opt"],
        ].to_html(index=False)
        template_data.append(
            {
                "name": sample_name,
                "plot": plots[sample_name],
                "gompertz": gompertz_table,
                "richards": richards_table,
            }
        )

    html_out = template.render(
        title="Plots and data for Richards and Gompertz model fitting",
        data=template_data,
    )

    HTML_FILE = "report.html"
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(os.path.join(dest_dir, HTML_FILE), "w") as f:
        f.write(html_out)
