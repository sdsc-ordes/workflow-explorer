# This script deploys the workflowExplorerApp to shinyapps

# libraries
library(rsconnect)
library(here)

# properly define working directory
here::i_am("workflowExplorer/")

# function to stop the script when one of the credentials cannot be found. 
# it strips quotation marks from the secrets if they were provided 
check_credentials <- function(name){
  var <- Sys.getenv(name, unset = NA)
  if(is.na(var)){
    stop(paste0("Error: cannot find ", 
                name, 
                " in the environment variables."),
         call. = FALSE)
  }
  gsub("\"", "", var)
}


# authentication
setAccountInfo(name   = check_credentials("SHINY_ACC_NAME"),
               token  = check_credentials("TOKEN"),
               secret = check_credentials("SECRET"))

# deploy workflowExplorerApp
deployApp(
  appDir = c("workflowExplorer"),
  appFiles = c("app.R", "workflowTable.tsv"),
  appName = check_credentials("MAIN_NAME"),
  appTitle = "workflowExplorerApp")
