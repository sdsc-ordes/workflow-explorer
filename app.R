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
      ),
      
      selectInput("ml", "Machine learning compatible:",
                  choices = c("Any",
                              "yes", 
                              "no")
      ),
      
      selectInput("complexity", "Workflow complexity:",
                  choices = c("Any",
                              "low", 
                              "high")
      ),
      
      selectInput("data", "Amount of data:",
                  choices = c("Any",
                              "low", 
                              "high")
      ),
      
      selectInput("containers", "Compatible with multi-container use:",
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
      
      workflowTable <- read.delim(here("workflowTable.tsv"))
      if (input$lang != "Any") {
        workflowTable <- workflowTable %>%
          filter(language == input$lang)
      }
      
      if (input$scale != "Any") {
        workflowTable <- workflowTable %>%
          filter(scale == input$scale)
      }
      
      if (input$k8 != "Any") {
        if (input$k8 == "yes") {
          workflowTable <- workflowTable %>%
            filter(k8 == input$k8 | k8 == "yes-paid" | k8 == "yes-dev")
        } else {
        workflowTable <- workflowTable %>%
          filter(k8 == input$k8)
        }
      }
      
      if (input$cloud != "Any") {
        if (input$cloud == "yes") {
          workflowTable <- workflowTable %>%
            filter(cloud == input$k8 | cloud == "yes-paid")
        } else {
        workflowTable <- workflowTable %>%
          filter(cloud == input$cloud)
        }
      }
      
      if (input$complexity != "Any") {
        workflowTable <- workflowTable %>%
          filter(wf.complexity == input$complexity |
                   wf.complexity == "low_and_high")
      }
      
      if (input$data != "Any") {
        workflowTable <- workflowTable %>%
          filter(data.amount == input$data.amount |
                   data.amount == "low_and_high")
      }
      
      if (input$containers != "Any") {
        workflowTable <- workflowTable %>%
          filter(containers == input$containers)
      }
      
      workflowTable
    }
  )
  
}

# Run the application 
shinyApp(ui = ui, server = server, options = list(launch.browser = TRUE))
