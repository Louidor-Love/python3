from dotenv import load_dotenv
import os

load_dotenv('.env')

# sqlite_file_name = "database.db"
sqlite_url = os.getenv('postgresql://ecommerce_db_n48b_user:ljLooAWfGpzLP20RTsb6tWfea9cnXNkk@dpg-crd2lbt2ng1s73fndht0-a.oregon-postgres.render.com/ecommerce_db_n48b')

# connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)