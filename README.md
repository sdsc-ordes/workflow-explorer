## An app to find the workflow manager you need

This repository includes a simple demo for an app to recommend workflow managers.

## Quickstart

Requirements:

-   R version 4.2.2+
-   R libraries: `here` and `tidyverse`

After cloning the repository, run the following command with the path to the repo:

```         
R -e "shiny::runApp('~/path_to/workflowExplorer')"
```

## Install dependencies via conda

If you have [conda](https://docs.conda.io/projects/conda/en/latest/index.html) installed:

```         
conda create -n workflowApp -c conda-forge r-base r-shiny r-tidyverse r-here
```

To run the app, activate the environment as follows:

```         
conda activate workflowApp
```
