from database import SessionLocal
from models import Message

def test_crud_operations():
    """Test CRUD operations on Message model"""
    db = SessionLocal()
    
    try:
        # Create
        print("Creating test message...")
        test_msg = Message(
            tier="test",
            query="Test query",
            response="Test response"
        )
        db.add(test_msg)
        db.commit()
        db.refresh(test_msg)
        print(f"✓ Created message with ID: {test_msg.id}")
        
        # Read
        print("\nReading message...")
        msg = db.query(Message).filter(Message.id == test_msg.id).first()
        print(f"✓ Read message: {msg}")
        
        # Update
        print("\nUpdating message...")
        msg.response = "Updated response"
        db.commit()
        db.refresh(msg)
        print(f"✓ Updated message: {msg}")
        
        # List all
        print("\nListing all messages:")
        messages = db.query(Message).all()
        for m in messages:
            print(f"- {m.id}: {m.query} -> {m.response}")
            
        return True
        
    except Exception as e:
        print("✗ CRUD test failed:", str(e))
        return False
    finally:
        # Cleanup
        if 'test_msg' in locals():
            db.delete(test_msg)
            db.commit()
        db.close()

if __name__ == "__main__":
    if test_crud_operations():
        print("\n✅ CRUD test passed!")
    else:
        print("\n❌ CRUD test failed")
