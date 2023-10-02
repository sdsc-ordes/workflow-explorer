# workflowExplorer app demo

library(shiny)
library(tidyverse)
library(here)

here::i_am("app.R")

ui <- fluidPage(
  titlePanel("Workflow explorer"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Select features of interest to find a workflow manager for you"),
      
      selectInput("lang", "Programming language:",
                 choices = c("Any",
                             "Python", 
                             "Language-agnostic")
                 ),
      
      selectInput("scale", "Workflow scale:",
                  choices = c("Any",
                              "micro", 
                              "macro")
                  ),
      
      selectInput("k8", "Kubernetes compatible:",
                  choices = c("Any",
                              "yes", 
                              "no")
      ),
      
      selectInput("cloud", "Cloud compatible:",
                  choices = c("Any",
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
      
      workflowTable <- read.delim("~/Documents/workflowExplorer/workflowTable.tsv")
      if (input$lang != "Any") {
        workflowTable <- workflowTable %>%
          filter(language == input$lang)
      }
      
      if (input$scale != "Any") {
        workflowTable <- workflowTable %>%
          filter(scale == input$scale)
      }
      
      if (input$k8 != "Any") {
        workflowTable <- workflowTable %>%
          filter(k8 == input$k8)
      }
      
      if (input$cloud != "Any") {
        workflowTable <- workflowTable %>%
          filter(cloud == input$cloud)
      }
      workflowTable
    }
  )
  
}

# Run the application 
shinyApp(ui = ui, server = server, options = list(launch.browser = TRUE))
