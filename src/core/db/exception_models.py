from pydantic import BaseModel


class Message404(BaseModel):
    message: str
