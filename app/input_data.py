""" Definitions and specifications of all input data """

# Answers
yn_choices = ["Not relevant", "yes", "no"]
format_choices = ["Python", "YAML", "R", "Groovy"]
goal_choices = ["Not relevant", "full automation", "reproducibility only"]


# Questions
questions = {
    "lang": {
        "label": "Is your workflow using only Python as language?",
        "choices": yn_choices,
        "type": "select",
    },
    "k8": {
        "label": "Are you working or planning to work with Kubernetes?",
        "choices": yn_choices,
        "type": "select",
    },
    "ml": {
        "label": "Are you using sklearn, tensorflow or other ML/AI libraries?",
        "choices": yn_choices,
        "type": "select",
    },
    "containers": {
        "label": "Are you using or planning to use containers?",
        "choices": yn_choices,
        "type": "select",
    },
    "format": {
        "label": "Which format and/or language are you comfortable with?",
        "choices": format_choices,
        "type": "checkbox",
    },
    "goal": {
        "label": "Is your end goal full automation (reproducibility+scheduling) or reproducibility only?",
        "choices": goal_choices,
        "type": "select",
    },
    "combo": {
        "label": "Would you like to combine workflow managers for different aspects of your workflow?",
        "choices": yn_choices,
        "type": "select",
    },
}

# Defaults select
default_select = {
    "lang": "Not relevant",
    "k8": "Not relevant",
    "ml": "Not relevant",
    "containers": "Not relevant",
    "goal": "Not relevant",
    "combo": "Not relevant",
}

# Defaults checkbox
default_checkbox = {"format": []}
