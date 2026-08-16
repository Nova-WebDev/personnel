import secrets
from auth.core.interfaces.code_generator import ICodeGenerator


class CodeGenerator(ICodeGenerator):
    def __init__(self, length: int = 5):
        self.length = length

    async def generate(self) -> str:
        return ''.join(secrets.choice("0123456789") for _ in range(self.length))
