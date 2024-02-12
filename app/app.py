from shiny import App, ui, render
from faicons import icon_svg
import pandas as pd

# Front end: User interface

# We define choices options for all questions
yn_choices = ["Not relevant", "yes", "no"]
format_choices = ["Python", "YAML", "R", "Groovy"]
goal_choices = ["Not relevant", "full automation", "reproducibility only"]

app_ui = ui.page_fluid(
    ui.panel_title("Workflow Explorer"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(
                "lang", 
                "Is your workflow using only Python as language?",
                yn_choices),
            ui.input_select(
                "k8", 
                "Are you working or planning to work with Kubernetes?",
                yn_choices),
            ui.input_select(
                "ml", 
                "Are you using sklearn, tensorflow or other ML/AI libraries?",
                yn_choices),
            ui.input_select(
                "containers", 
                "Are you using or planning to use containers?",
                yn_choices),
            ui.input_checkbox_group(
                "format", 
                "Which format and/or language are you comfortable with?",
                format_choices),
            ui.input_select(
                "goal", 
                "Is your end goal full automation (reproducibility+scheduling) or reproducibility only?",
                goal_choices),
            ui.input_select(
                "combo",
                "Would you like to combine workflow managers for different aspects of your workflow?",
                yn_choices),
        ),
        ui.panel_main(
            ui.dataframe.output_data_frame("filter")
        )
    ),
    ui.panel_absolute(
        ui.div(
            ui.tags.style(
                """

                 /* unvisited link */
                a:link {
                color: black;
                }

                /* visited link */
                a:visited {
                color: black;
                }

                /* mouse over link */
                a:hover {
                color: hotpink;
                }

                /* selected link */
                a:active {
                color: black;
                } 
                """
            ),
            ui.tags.a(
                icon_svg("github", width="45px", height="48px"), 
                href="https://github.com/SDSC-ORD/workflow-explorer", 
                target="_blank"
                ),
    
        ),
        bottom="0%",
        right="1%"
    )
)

# Back end: server

def server(input,output, session):
    @output
    @render.data_frame
    def filter():
        filtered_wf = pd.read_csv("app/workflowTable.tsv", sep="\t")
        if input.lang() != "Not relevant":
            if input.lang() == "yes":
                filtered_wf = filtered_wf[(filtered_wf['language'] == "Python") | (filtered_wf['language'] == "Language-agnostic")]
            else:
                filtered_wf = filtered_wf[(filtered_wf['language'] != "Python")]
        if input.k8() != "Not relevant":
            if input.k8() == "yes":
                filtered_wf = filtered_wf[(filtered_wf['k8'] == "yes") | (filtered_wf['k8'] == "yes-but")]
            else:
                filtered_wf = filtered_wf[(filtered_wf['k8'] == "no")]
        if input.ml() != "Not relevant":
            if input.ml() == "yes":
                filtered_wf = filtered_wf[(filtered_wf['ML-compatible'] == "yes") | (filtered_wf['ML-compatible'] == "yes-but")]
            else:
                filtered_wf = filtered_wf[(filtered_wf['ML-compatible'] == "no")]
        if input.containers() != "Not relevant":
            if input.containers() == "yes":
                filtered_wf = filtered_wf[(filtered_wf['containers'] == "yes") | (filtered_wf['containers'] == "yes-but")]
            else:
                filtered_wf = filtered_wf[(filtered_wf['containers'] == "no")]
        if input.format():
            formats = []
            for format in input.format():
                formats.append(format)
            filtered_wf = filtered_wf[(filtered_wf['format'].isin(formats))]
        if input.goal() != "Not relevant":
            if input.goal() == "full automation":
                filtered_wf = filtered_wf[(filtered_wf['goal'] == "auto")]
            else:
                filtered_wf = filtered_wf[(filtered_wf['goal'] == "pipeline")]
        if input.combo() != "Not relevant":
            if input.combo() == "yes":
                filtered_wf = filtered_wf[(filtered_wf['combo'] == "yes")]
            else:
                filtered_wf = filtered_wf[(filtered_wf['combo'] == "no")]

        return render.DataTable(filtered_wf)

app = App(app_ui, server)