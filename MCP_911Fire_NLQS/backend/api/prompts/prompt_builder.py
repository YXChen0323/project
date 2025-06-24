from .template import get_template
from ..context.memory import get as get_context

def format_history(context: list) -> str:
    return "\n".join([
        f"{entry['role'].capitalize()}: {entry['content']}" for entry in context
    ])

def build_prompt(task: str, user_input: str, user_id: str) -> str:
    context = get_context(user_id)
    history_str = format_history(context)
    template = get_template(task)

    return template.format(history=history_str, input=user_input)
