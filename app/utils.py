from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def find_post(id: int, my_posts: list):
    post = None
    for p in my_posts:
        if p['id'] == id:
            post = p
            break
    return post

def find_index_post(id: int, my_posts: list):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None