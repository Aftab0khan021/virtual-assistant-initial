from pydantic import BaseModel

class ToolSpec(BaseModel):
    name: str
    description: str
    parameters: dict

class Skill:
    name: str = "base"

    @classmethod
    def manifest(cls) -> ToolSpec:
        return ToolSpec(
            name=cls.name,
            description=cls.__doc__ or "",
            parameters={},
        )

    async def run(self, **kwargs):
        raise NotImplementedError
