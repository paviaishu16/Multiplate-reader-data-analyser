"""Test for report generator."""

import os
import tempfile

import pandas as pd

from report import generate_report


def test_generate_report():
    """Test that report has expected content."""
    input_observed_data = pd.DataFrame(
        {
            "A1": [4.5, 19.5, 29.2, 90.3, 50.5, 72.2],
            "A2": [5.5, 15.5, 19.2, 20.3, 50.5, 72.2],
        }
    )
    input_observed_data.index = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    input_gompertz_metrics = pd.DataFrame(
        {
            "N_0_opt": [4.511152, 4.2],
            "N_inf_opt": [1.397241, 3.1],
            "alpha_opt": [0.031169, 2.0],
            "R_2": [-0.342961, 1.1],
            "RMSE": [0.333926, 1.1],
            "AIC": [409.544346, 4.0],
            "BIC": [108.340329, 2.0],
        },
        index=["A1", "A2"],
    )
    input_richards_metrics = pd.DataFrame(
        {
            "A_opt": [1.607220, 2.1],
            "k_opt": [0.110140, 1.3],
            "t0_opt": [13.314109, 3.0],
            "A0_opt": [0.244298, 1.1],
            "R_2": [0.857320, 1.2],
            "RMSE": [0.108843, 1.1],
            "AIC": [86.450596, 1.1],
            "BIC": [-211.776687, 3.0],
        },
        index=["A1", "A2"],
    )
    with tempfile.TemporaryDirectory() as tempdir:
        generate_report(
            input_observed_data,
            input_gompertz_metrics,
            input_richards_metrics,
            dest_dir=tempdir,
        )

        print(os.listdir(tempdir))
        assert os.path.exists(os.path.join(tempdir, "report.html"))

        with open(os.path.join(tempdir, "report.html")) as f:
            html_page = f.read()

        print(html_page)

        assert "<td>1.60722</td>" in html_page
        assert "<td>4.511152</td>" in html_page
        assert 'alt="A1 plot"' in html_page
        assert "fvjz179sT27dtj69atcejQoTz9RPlz" in html_page
