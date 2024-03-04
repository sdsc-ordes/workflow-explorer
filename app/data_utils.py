"""Utils function related to input data management"""

import pandas as pd
from typing import Iterable, List, Union, Optional
from shiny import ui
from input_data import questions

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
