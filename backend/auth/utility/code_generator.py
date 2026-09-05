import secrets
from auth.core.interfaces.code_generator import ICodeGenerator


class CodeGenerator(ICodeGenerator):
    def __init__(self, length: int = 5):
        self.length = length

    async def generate(self) -> str:
        return "".join(str(secrets.randbelow(10)) for _ in range(self.length))