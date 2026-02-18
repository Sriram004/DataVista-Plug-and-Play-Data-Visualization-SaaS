from pydantic import BaseModel, Field


class DashboardCreate(BaseModel):
    name: str
    description: str = ""
    layout_json: dict = Field(default_factory=dict)


class DashboardOut(BaseModel):
    id: int
    name: str
    description: str
    layout_json: dict

    class Config:
        from_attributes = True
