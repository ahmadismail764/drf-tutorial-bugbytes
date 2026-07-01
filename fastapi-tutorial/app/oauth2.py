from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "a_very_long_and_arbitrary_secret_key_for_jwt_token_signing_1234567890abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Convert datetime to Unix timestamp for JWT
    expire_timestamp = expire_time.timestamp()
    to_encode.update({"exp": expire_timestamp})
    
    print(f"Creating token with expiration: {expire_time}")
    print(f"Expiration timestamp: {expire_timestamp}")
    print(f"Current time: {datetime.now()}")
    print(f"Current timestamp: {datetime.now().timestamp()}")
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception):
    try:
        # jwt.decode automatically validates expiration time
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Additional explicit expiration check
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            current_timestamp = datetime.now().timestamp()
            if current_timestamp > exp_timestamp:
                print(f"Token expired! Current: {current_timestamp}, Exp: {exp_timestamp}")
                raise credentials_exception
        
        id = payload.get("user_id")
        if id is None:
            print("No user_id in token")
            raise credentials_exception
            
        print(f"Token valid for user_id: {id}")
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(f"JWT Error: {e}")  # Debug: see what type of error
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()  # type: ignore
    return user