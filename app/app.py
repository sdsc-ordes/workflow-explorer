from shiny import App, ui, render, reactive
from faicons import icon_svg
import pandas as pd
import data_utils as du
import shinyswatch
from pathlib import Path
from input_data import default_checkbox, default_select, questions

### ----- Front end: User interface ----- ###

app_ui = ui.page_fluid(
    # TODO: select theme? shinyswatch.theme.sketchy(),
    shinyswatch.theme_picker_ui(),
    ui.panel_title("Workflow Explorer"),
    ui.layout_sidebar(
        # Question panel
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
        # Answer table
        ui.panel_main(
            ui.output_ui("workflow_cards")
            ),
    ),
    # Styling
    ui.include_css(Path(__file__).parent / "static/styles/main.css"),
    ui.panel_absolute(
        ui.div(
            ui.tags.a(
                icon_svg("github", width="45px", height="48px"),
                href="https://github.com/sdsc-ordes/workflow-explorer",
                target="_blank",
            ),
        ),
        top="1%",
        right="1%",
    ),
)

### ---------------------------- ###

### ----- Back end: server ----- ###


def server(input, output, session):
    wf_tab = pd.read_csv(Path(__file__).parent / "workflowTable.tsv", sep="\t")

    # TODO: remove to use a fixed theme
    shinyswatch.theme_picker_server()

    # Reset event
    @reactive.Effect
    @reactive.event(input.reset)
    def _():
        for id, value in default_select.items():
            ui.update_select(id=id, selected=value)
        for id, value in default_checkbox.items():
            ui.update_checkbox_group(id, selected=value)

    # Workflow filter
    def filter():
        filtered_wf = wf_tab.copy()
        for q_name in questions:
            filtered_wf = du.filter_replies(q_name, input[q_name](), filtered_wf)
        return filtered_wf
    
    # Render workflow cards
    @output
    @render.ui
    def workflow_cards():
        filtered_wf = filter()
        cards = du.generate_cards(filtered_wf)
        return ui.layout_column_wrap(*cards, width=1 / 3)

### ---------------------------- ###

app = App(app_ui, server)
