import sys
from sqlalchemy import text
from database import engine, Base, SessionLocal

def test_connection():
    """Test database connection and basic operations"""
    print("Testing database connection...")
    
    # Test raw connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            print("✓ Database version:", result.scalar())
    except Exception as e:
        print("✗ Could not connect to database:", str(e))
        return False
    
    # Test ORM session
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✓ ORM session works")
        db.close()
    except Exception as e:
        print("✗ ORM session failed:", str(e))
        return False
    
    # Test model creation
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print("✗ Table creation failed:", str(e))
        return False
    
    return True

if __name__ == "__main__":
    if test_connection():
        print("\n✅ Database connection test passed!")
        sys.exit(0)
    else:
        print("\n❌ Database connection test failed")
        sys.exit(1)
