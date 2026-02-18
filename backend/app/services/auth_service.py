from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.entities import Organization, User
from app.schemas.auth import UserCreate


class AuthService:
    @staticmethod
    def register(db: Session, payload: UserCreate) -> str:
        organization = Organization(name=payload.organization_name)
        db.add(organization)
        db.flush()

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            role=payload.role,
            organization_id=organization.id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return create_access_token(str(user.id), user.organization_id, user.role.value)

    @staticmethod
    def login(db: Session, email: str, password: str) -> str | None:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return create_access_token(str(user.id), user.organization_id, user.role.value)
