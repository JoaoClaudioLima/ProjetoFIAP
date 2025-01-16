from sqlalchemy import create_engine

# Replace with your actual database URL
DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/mydatabase"

# Synchronous SQLAlchemy engine
sync_engine = create_engine(DATABASE_URL, future=True)

def test_sync_connection():
    """
    Test the synchronous database connection using SQLAlchemy.
    """
    try:
        with sync_engine.connect() as connection:
            # Execute a simple query to ensure the connection works
            result = connection.execute("SELECT 1").scalar()
            if result == 1:
                print("Synchronous connection to the database succeeded!")
            else:
                print("Unexpected result from the database!")
    except Exception as e:
        print(f"Failed to connect synchronously: {e}")

# Run the test
test_sync_connection()
