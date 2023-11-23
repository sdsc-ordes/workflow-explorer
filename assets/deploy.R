# This script creates the workflow explorer webpage

# libraries
library(shinylive)

# export app to site/ folder

shinylive::export(app_dir = "app/", output_dir = "docs")