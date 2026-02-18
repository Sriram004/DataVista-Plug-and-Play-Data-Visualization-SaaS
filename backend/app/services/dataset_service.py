from io import BytesIO

import pandas as pd
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import Dataset, User


class DatasetService:
    @staticmethod
    async def ingest_upload(db: Session, user: User, file: UploadFile) -> Dataset:
        content = await file.read()
        if len(content) > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File exceeds max allowed size")

        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif file.filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are supported")

        cleaned = df.fillna("")
        metadata = {
            "columns": [
                {"name": col, "dtype": str(cleaned[col].dtype), "non_null": int(cleaned[col].ne("").sum())}
                for col in cleaned.columns
            ],
            "preview": cleaned.head(10).to_dict(orient="records"),
        }

        dataset = Dataset(
            name=file.filename,
            organization_id=user.organization_id,
            owner_id=user.id,
            row_count=len(cleaned),
            metadata_json=metadata,
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def list_datasets(db: Session, org_id: int) -> list[Dataset]:
        return db.query(Dataset).filter(Dataset.organization_id == org_id).all()
