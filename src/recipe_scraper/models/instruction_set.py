from pydantic import BaseModel


class InstructionSet(BaseModel):
    def __init__(self, step_list):
        pass
