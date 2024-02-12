## An app to find the workflow manager you need

This repository includes a simple demo for an app to recommend workflow managers.

## Quickstart

Requirements:

-   Python 3.10+
-   Python packages: `shiny`, `faicons` and `pandas`

After cloning the repository, run the following command with the path to the `workflow-explorer` folder inside the repo:

```         
shiny run --reload app/app.py
```

## Install dependencies via conda

If you have [conda](https://docs.conda.io/projects/conda/en/latest/index.html) installed:

```         
conda create -n workflow-explorer python=3.10
conda activate workflow-explorer
pip install shiny faicons pandas
```

To run the app activate the environment:

```         
conda activate workflow-explorer
shiny run --reload app/app.py
```
