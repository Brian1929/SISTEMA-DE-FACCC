
from db import db

def update():
    try:
        res = db.productos.update_one(
            {"codigo": "TEST"}, 
            {"$set": {"stock": 100.0}}
        )
        print(f"Update modified: {res.modified_count}, matched: {res.matched_count}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update()
