from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import User
from app.schemas.dataset import DatasetOut
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetOut)
async def upload_dataset(
    file: UploadFile = File(...),
    user: User = Depends(require_roles("admin", "analyst")),
    db: Session = Depends(get_db),
) -> DatasetOut:
    dataset = await DatasetService.ingest_upload(db, user, file)
    return DatasetOut.model_validate(dataset)


@router.get("", response_model=list[DatasetOut])
def list_datasets(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[DatasetOut]:
    datasets = DatasetService.list_datasets(db, user.organization_id)
    return [DatasetOut.model_validate(item) for item in datasets]
