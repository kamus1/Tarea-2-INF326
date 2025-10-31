from .database import insert_hit

# solo se llama a esta funcion para guardar los hits de las urls
def save_url_hit(hash_str: str, long_url: str, timestamp: str):
    insert_hit(hash_str, long_url, timestamp)
