from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import constants

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
}

router = APIRouter()


def fake_hash_password(password: str):
    """
    Génère un mot de passe hashé factice à partir du mot de passe fourni.
    
    @param (str) password : Mot de passe non hashé
    @return (str) : Mot de passe hashé factice
    """
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{constants.TOKEN}")


class User(BaseModel):
    """
    Modèle de données pour un utilisateur.
    
    @param (str) username : Nom d'utilisateur
    @param (str | None) email : Adresse e-mail (facultatif)
    @param (str | None) full_name : Nom complet de l'utilisateur (facultatif)
    @param (bool | None) disabled : Indique si l'utilisateur est désactivé (facultatif)
    """
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """
    Modèle de données pour un utilisateur enregistré dans la base de données.
    
    @param (str) hashed_password : Mot de passe hashé de l'utilisateur
    """
    hashed_password: str


def get_user(db, username: str):
    """
    Obtient les informations d'un utilisateur à partir de la base de données factice.
    
    @param (dict) db : Base de données factice des utilisateurs
    @param (str) username : Nom d'utilisateur de l'utilisateur à rechercher
    @return (UserInDB | None) : Les informations de l'utilisateur ou None si l'utilisateur n'existe pas
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    """
    Décodage factice d'un jeton d'authentification.
    
    @param (str) token : Jeton d'authentification factice
    @return (UserInDB | None) : Les informations de l'utilisateur associé au jeton ou None si le jeton est invalide
    """
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Obtient l'utilisateur actuel en fonction du jeton d'authentification fourni.
    
    @param (str) token : Jeton d'authentification
    @return (UserInDB) : Les informations de l'utilisateur actuel
    @raise (HTTPException) : Erreur HTTP 401 si l'authentification échoue
    """
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Obtient l'utilisateur actif actuel en fonction de l'utilisateur courant.
    
    @param (User) current_user : L'utilisateur actuel
    @return (User) : L'utilisateur actif actuel
    @raise (HTTPException) : Erreur HTTP 400 si l'utilisateur est inactif
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Authentification de l'utilisateur et génération d'un jeton d'accès.
    
    @param (OAuth2PasswordRequestForm) form_data : Informations d'authentification de l'utilisateur
    @return (dict) : Jeton d'accès et type de jeton
    @raise (HTTPException) : Erreur HTTP 400 en cas d'échec de l'authentification
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Obtient les informations de l'utilisateur actif actuel.
    
    @param (User) current_user : L'utilisateur actif actuel
    @return (User) : Les informations de l'utilisateur actif actuel
    @raise (HTTPException) : Erreur HTTP 400 si l'utilisateur est inactif
    """
    return current_user