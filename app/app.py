from shiny import App, ui, render, reactive
from faicons import icon_svg
import pandas as pd
import data_utils as du
from pathlib import Path
from input_data import default_checkbox, default_select, questions

### ----- Front end: User interface ----- ###

app_ui = ui.page_fluid(
    ui.panel_title("Workflow Explorer"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            [
                du.input_question(id, q.get("label"), q.get("choices"), q.get("type"))
                for id, q in questions.items()
            ],
            ui.input_action_button(
                "reset",
                "Clear choices",
                width="30%",
            ),
        ),
        ui.panel_main(ui.dataframe.output_data_frame("filter")),
    ),
    ui.include_css(Path(__file__).parent / "static/styles/main.css"),
    ui.panel_absolute(
        ui.div(
            ui.tags.a(
                icon_svg("github", width="45px", height="48px"),
                href="https://github.com/SDSC-ORD/workflow-explorer",
                target="_blank",
            ),
        ),
        bottom="0%",
        right="1%",
    ),
)

### ---------------------------- ###

### ----- Back end: server ----- ###


def server(input, output, session):
    wf_tab = pd.read_csv("app/workflowTable.tsv", sep="\t")
    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        for id, value in default_select.items():
            ui.update_select(id=id, selected=value)
        for id, value in default_checkbox.items():
            ui.update_checkbox_group(id, selected=value)

    @output
    @render.data_frame
    def filter():
        filtered_wf = wf_tab.copy()
        for q_name in questions:
            filtered_wf = du.filter_replies(q_name, input[q_name](), filtered_wf)
        return render.DataTable(filtered_wf)


app = App(app_ui, server)
