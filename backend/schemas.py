from pydantic import EmailStr, BaseModel, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(c.isupper() for c in value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not any(c.islower() for c in value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        if not any(c.isdigit() for c in value):
            raise ValueError("La contraseña debe contener al menos un número")
        if not any(c in "@$!%*?&" for c in value):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial (@$!%*?&)"
            )
        return value


class UserUpdate(UserCreate):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    description: str = Field(max_length=50)
    user_id: int = Field(ge=0)


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True


class ProjectUpdate(ProjectCreate):
    name: str | None = None
    description: str | None = None
    user_id: int | None = None


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=20)
    description: str = Field(max_length=50)
    project_id: int = Field(ge=0)
    user_id: int = Field(ge=0)


class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True


class TaskUpdate(TaskCreate):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None
    project_id: int | None = None
