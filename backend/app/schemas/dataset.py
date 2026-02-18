from pydantic import BaseModel


class DatasetOut(BaseModel):
    id: int
    name: str
    row_count: int
    metadata_json: dict

    class Config:
        from_attributes = True
