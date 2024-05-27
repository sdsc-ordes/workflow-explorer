"""Utils function related to input data management"""

import pandas as pd
from typing import Iterable, List, Union, Optional
from shiny import ui
from input_data import questions
from faicons import icon_svg

# Input functions


def input_question(id: str, label: str, choices: List[str], type: str):
    """Select ui group based on the question type"""
    if type == "select":
        return ui.input_select(id, label, choices)
    elif type == "checkbox":
        return ui.input_checkbox_group(id, label, choices)
    else:
        raise ValueError(f"Unknown question type: {type}")


# Filter functions


def filter_replies(
    q_name: str, answer: Optional[Union[str, Iterable]], workflows: pd.DataFrame
) -> pd.DataFrame:
    """Apply specific filter functions for each question"""
    match q_name:
        case "lang":
            return filter_lang(answer, workflows)
        case "k8" | "containers" | "combo":
            return filter_CEQ(q_name, answer, workflows)
        # TODO: Maybe worth changing the name in workflowTable.tsv
        case "ml":
            return filter_CEQ("ML-compatible", answer, workflows)
        case "format":
            return filter_format(answer, workflows)
        case "goal":
            return filter_goal(answer, workflows)
        case _:
            Warning(f"No filter for {q_name} defined.")
            return workflows


def filter_CEQ(q_name: str, answer: str, workflows: pd.DataFrame) -> pd.DataFrame:
    """Workflow filter for closed-ended questions with only yes(yes-but) and no as possible answers"""
    if answer == "Not relevant":
        return workflows
    elif answer == "yes":
        return workflows[
            (workflows[q_name] == "yes") | (workflows[q_name] == "yes-but")
        ]
    else:
        return workflows[(workflows[q_name] == "no")]


def filter_lang(answer: str, workflows: pd.DataFrame) -> pd.DataFrame:
    """Workflow filter for language question"""
    if answer == "Not relevant":
        return workflows
    elif answer == "yes":
        return workflows[
            (workflows["language"] == "Python")
            | (workflows["language"] == "Language-agnostic")
        ]
    else:
        return workflows[(workflows["language"] != "Python")]


def filter_format(answer: Optional[Iterable], workflows: pd.DataFrame) -> pd.DataFrame:
    """Workflow filter based on selected formats"""
    if not answer:
        return workflows
    else:
        formats = [format for format in answer]
    return workflows[(workflows["format"].isin(formats))]


def filter_goal(answer: str, workflows: pd.DataFrame) -> pd.DataFrame:
    """Workflow filter based on teh overall goal"""
    if answer == "Not relevant":
        return workflows
    elif answer == "full automation":
        return workflows[(workflows["goal"] == "auto")]
    else:
        return workflows[(workflows["goal"] == "pipeline")]

# Workflow cards generator

def generate_cards(filtered_wf: pd.DataFrame) -> List[ui.card]:
    """Generate cards for each workflow in the filtered data frame"""
    cards = []
    for i, row in filtered_wf.iterrows():
        cards.append(
            ui.card(
                ui.card_header(
                    ui.tags.img(src=row["icon"], class_="center"),
                ),
                ui.p(
                    ui.span("Name: ", 
                             row["name"],
                    ),
                    ui.span("Docs: ",
                        ui.tags.a(
                                icon_svg("book"),
                                href=row["docs"],
                                target="_blank",
                        ),
                        class_="cardpane",
                    ),
                    ui.span("Website: ",
                        ui.tags.a(
                                icon_svg("globe"),
                                href=row["website"],
                                target="_blank",
                        ),
                        class_="cardpane",
                    ),
                    class_="text",
                ),

                ui.p(icon_svg("code"), row["format"], class_="text"),
                
                # TODO: consider if footer can be used for more details
                # ui.card_footer
            ),
        ),
    return cards