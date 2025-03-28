from pydantic import EmailStr, BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(
        pattern="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )


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


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=20)
    description: str = Field(max_length=50)
    project_id: int = Field(ge=0)
    user_id: int = Field(ge=0)


class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True
