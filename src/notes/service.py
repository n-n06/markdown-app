from markdown import markdown
from language_tool_python import LanguageTool

from src.notes.models import Note
from src.notes.schemas import GrammarCorrection


def render(note: Note) -> str:
    return markdown(note.content, extensions=["markdown.extensions.tables"])


class GrammarService:
    def __init__(self, language_mode: str = "auto"):
        self.tool = LanguageTool(language_mode)

    def check_grammar(self, content: str) -> list[GrammarCorrection]:
        matches = self.tool.check(content)  

        result = []

        for rule in matches:  
            if len(rule.replacements) > 0:
                result.append({
                    "start" : rule.offset,
                    "end" : rule.errorLength + rule.offset,
                    "mistake" : content[
                        rule.offset : rule.errorLength + rule.offset
                    ],
                    "replacements" : rule.replacements
                })

        return result 

