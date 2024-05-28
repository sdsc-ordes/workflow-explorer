""" Definitions and specifications of all input data """

# Answers
yn_choices = ["Not relevant", "yes", "no"]
format_choices = ["Python", "YAML", "R", "Groovy"]
goal_choices = ["Not relevant", "full automation", "reproducibility only"]


# Questions
questions = {
    "lang": {
        "group": "basic",
        "label": "Are you working with Python only?",
        "choices": yn_choices,
        "type": "select",
    },
    "k8": {
        "group": "advanced",
        "label": "Are you working or planning to work with Kubernetes?",
        "choices": yn_choices,
        "type": "select",
    },
    "ml": {
        "group": "basic",
        "label": "Are you using sklearn, tensorflow or other ML/AI libraries?",
        "choices": yn_choices,
        "type": "select",
    },
    "containers": {
        "group": "basic",
        "label": "Are you using or planning to use containers?",
        "choices": yn_choices,
        "type": "select",
    },
    "format": {
        "group": "basic",
        "label": "Which format and/or language are you comfortable with?",
        "choices": format_choices,
        "type": "checkbox",
    },
    "goal": {
        "group": "advanced",
        "label": "Is your end goal full automation (reproducibility+scheduling) or reproducibility only?",
        "choices": goal_choices,
        "type": "select",
    },
    "combo": {
        "group": "advanced",
        "label": "Would you like to combine workflow managers for different aspects of your workflow?",
        "choices": yn_choices,
        "type": "select",
    },
}

# Defaults

## Defaults select
default_select = {
    "lang": "Not relevant",
    "k8": "Not relevant",
    "ml": "Not relevant",
    "containers": "Not relevant",
    "goal": "Not relevant",
    "combo": "Not relevant",
}

## Defaults checkbox
default_checkbox = {"format": []}
