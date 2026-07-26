# Submission figures

The main paper expects these vector PDF files:

```text
figure1_visible_spectrum_mechanism.pdf
figure2a_qeff_visibility.pdf
figure2b_theta_risk.pdf
figure2c_hidden_spectrum_oracle.pdf
figure3a_compute_phase_transition.pdf
figure3b_allocation_exponents.pdf
figure3c_adamw_schedule.pdf
```

Generate them from the repository root with:

```bash
python experiments/make_figures.py
```

The conceptual Figure 1 can be replaced by a manually polished vector version with the same filename. The `.gitignore` intentionally allows PDF figures to be committed because they are source artifacts for the submission; PNG previews remain ignored.
