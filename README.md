# Causal Logic and DAGs: Diagnosing Bad Controls

## Objective
I evaluated how improper control choices introduce bias in regression models by analyzing synthetic and observational datasets with Directed Acyclic Graphs (DAGs).

## Methodology
* Diagnosed collider bias by evaluating a model where adding a variable caused by both the treatment and outcome altered the coefficient estimate.
* Showed that a variable measured before treatment can still bias an estimate when it is a collider of two unobserved causes (M-bias).
* Estimated total versus direct causal effects by isolating the path through a mediator variable.
* Analyzed real-world observational bias by comparing non-experimental CPS control estimates against the experimental LaLonde job-training benchmark.
* Applied a `dag_utils.py` module to identify valid covariate adjustment sets directly from causal graph structures.
* Evaluated AI-assisted control selection by prompting an LLM to propose control variables for a job-training study and testing those sets against the study's DAG.

## Key Findings
* Adding a collider control moved the estimate from -0.012 to -0.593 and raised the R-squared to 0.585, despite the true effect being 0.
* Controlling for a pre-treatment variable still resulted in a biased estimate of -0.201 against a true effect of 0.
* Separated the total effect (3.978 against a true effect of 4.0) from the direct effect through a mediator (0.988 against a true effect of 1.0).
* In the LaLonde study, adjusting for covariates moved the observational estimate from -$8,498 to $699, compared to the experimental benchmark of $1,794.
* The AI's first proposed control set gave an estimate of 3.622 against the true effect of 4.0; after I revised the prompt once, the estimate was 4.047.
