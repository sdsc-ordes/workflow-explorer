# workflowExplorer app demo

library(shiny)
library(tidyverse)
library(here)

here::i_am("app.R")

ui <- fluidPage(
  titlePanel("Workflow explorer"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Select different constraints to find a workflow manager for you"),
      
      selectInput("lang", "Is your workflow using only Python as language?",
                 choices = c("Not relevant",
                             "yes", 
                             "no")
                 ),
      
      selectInput("k8", "Are you working or planning to work with Kubernetes?",
                  choices = c("Not relevant",
                              "yes", 
                              "no")
      ),
      
      selectInput("ml", "Are you using sklearn, tensorflow or other ML/AI libraries?",
                  choices = c("Not relevant",
                              "yes", 
                              "no")
      ),
      
      selectInput("containers", "Are you using or planning to use containers?",
                  choices = c("Not relevant",
                              "yes", 
                              "no")
      ),

      checkboxGroupInput("format", "Which format and/or language are you comfortable with?",
                  choices = c("Python",
                              "YAML", 
                              "JSON",
                              "R",
                              "Groovy")
      ),
      
      selectInput("goal", "Is your end goal full automation (reproducibility+scheduling) or reproducibility only?",
                  choices = c("Not relevant",
                              "full automation", 
                              "reproducibility only")
      ),
      
      selectInput("combo", "Would you like to separate the pipeline and the automated scheduling?",
                  choices = c("Not relevant",
                              "yes", 
                              "no")
      )

    ),
    mainPanel(
      tableOutput("filtered_workflow_list")
    )
  )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  output$filtered_workflow_list <- renderTable(
    {
      
      workflowTable <- read.delim(here("workflowTable.tsv"))
      if (input$lang != "Not relevant") {
        if (input$lang == "yes") {
          workflowTable <- workflowTable %>%
            filter(language == "Python")
        } else {
          workflowTable <- workflowTable %>%
            filter(language != "Python")
        }
        
      }
      
      if (input$k8 != "Not relevant") {
        if (input$k8 == "yes") {
          workflowTable <- workflowTable %>%
            filter(k8 == input$k8 | k8 == "yes-but")
        } else {
        workflowTable <- workflowTable %>%
          filter(k8 == input$k8)
        }
      }
      
      if (input$containers != "Not relevant") {
        workflowTable <- workflowTable %>%
          filter(containers == input$containers)
      }
      
      if (input$ml != "Not relevant") {
        workflowTable <- workflowTable %>%
          filter(ML-compatible == input$ml)
      }
      
      if (!is.null(input$format)) {
        workflowTable <- workflowTable %>%
          filter(format %in% input$format)
      }
      
      if (input$goal != "Not relevant") {
        if (input$goal == "full automation") {
          workflowTable <- workflowTable %>%
            filter(goal == "auto")
        } else {
          workflowTable <- workflowTable %>%
            filter(goal == "pipeline")
        }
      }
      
      if (input$combo != "Not relevant") {
        workflowTable <- workflowTable %>%
          filter(combo == input$combo)
      }
      
      workflowTable
    }
  )
  
}

# Run the application 
shinyApp(ui = ui, server = server, options = list(launch.browser = TRUE))
