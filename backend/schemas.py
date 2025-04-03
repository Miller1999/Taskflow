from pydantic import EmailStr, BaseModel, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)


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


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
