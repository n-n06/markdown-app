import asyncio
from aiocache import Cache, cached
from aiocache.serializers import JsonSerializer
from markdown import markdown
from language_tool_python import LanguageTool

from src.notes.models import Note
from src.notes.schemas import GrammarCorrection
from src.redis.utils import make_key


def render(note: Note) -> str:
    return markdown(note.content, extensions=["markdown.extensions.tables"])


class GrammarService:
    def __init__(self, language_mode: str = "auto"):
        self.tool = LanguageTool(language_mode)

    def __check_grammar(self, content: str) -> list[GrammarCorrection]:
        print("Checking Grammar here...")

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


    @cached(
        ttl=1000,
        cache=Cache.REDIS,
        key_builder=make_key,
        serializer=JsonSerializer(),
        port=6379,
        namespace="main")
    async def check_grammar_async(self, content: str)->list[GrammarCorrection]:
        return await asyncio.to_thread(self.__check_grammar, content)
