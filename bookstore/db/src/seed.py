from app.src.database import SessionLocal as session, get_db
from app.src.models import BookStore
import pandas as pd
from pathlib import Path


def seed():
    """function to load data into db"""
    db_dir = Path(__file__).resolve().parent.parent
    csv_path = db_dir / 'misc/bookstore_seed.csv'
    df = pd.read_csv(csv_path)
    session.query(BookStore).delete()
    session.flush()
    max_id = 0
    try:
        for index, row in df.iterrows():
            item = BookStore(**row.to_dict())
            session.add(item)
            session.flush()
            max_id = max(max_id, row.id)
        session.execute(f'ALTER SEQUENCE t_bookstore_id_seq RESTART WITH {max_id + 1}')
        session.commit()
    except Exception as exception:
        print(" EXCEPTION : ", exception)
        session.rollback()
