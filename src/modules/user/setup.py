from typing import Annotated
from fastapi import Depends, FastAPI

from src.db.schemas import User
from src.modules.auth.services import get_request_user
from src.modules.user import services
from src.utils.omit import omit

def setup_users_module(app: FastAPI):
  app.patch("/user/update")(services.update_user)

  @app.get("/user/current")
  def get_current_user(user: Annotated[User, Depends(get_request_user)] ):
    return omit(user.model_dump(), ['password'])
  
