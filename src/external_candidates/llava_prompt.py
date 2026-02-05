def get_question_text(problem):
    return problem.get("question")


def get_context_text(problem, use_caption):
    txt_context = problem.get("hint", "")
    img_context = problem.get("caption", "") if use_caption else ""
    context = " ".join([txt_context, img_context]).strip()
    return context or "N/A"


def get_choice_text(problem, options):
    choices = problem.get("choices", [])
    choice_list = []
    for i, c in enumerate(choices):
        choice_list.append(f"({options[i]}) {c}")
    return " ".join(choice_list)


def get_answer(problem, options):
    return options[problem.get("answer")]
