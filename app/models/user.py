import enum # Esto permite que el user puede tener un rol de user o admin
from datetime import datetime

from sqlalchemy import String, DateTime, Enum
# Este import permite crear un mapeo de la clase a la base de datos
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# Esta clase permite crear un rol de usuario
class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

# Esta clase permite crear un usuario
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

