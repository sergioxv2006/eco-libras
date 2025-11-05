from APP import create_app, db
from APP.models import User
from werkzeug.security import generate_password_hash
import os

def create_admin_user(username, password):
    """Create an admin user if it doesn't exist."""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            
            # Check if user exists
            existing_user = User.query.filter_by(user_admin=username).first()
            if existing_user:
                print(f"Admin user '{username}' already exists!")
                return

            # Create new admin
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_admin = User(
                user_admin=username,
                password_admin=hashed_password
            )
            
            db.session.add(new_admin)
            db.session.commit()
            print(f"Admin user '{username}' created successfully!")
            print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            raise

if __name__ == "__main__":
    admin_user = os.environ.get("ADMIN_USER", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    create_admin_user(admin_user, admin_password)