"""
Authentication module for Smart Task Optimizer
Handles user authentication and session management
"""

class Authenticator:
    """Handles user authentication and session management"""
    
    def __init__(self, users_file="security/users.json"):
        """Initialize authenticator with users file"""
        self.users_file = users_file
        self.sessions = {}
        
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with username and password"""
        import json
        import hashlib
        
        # Check if users file exists
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        
        # Check if user already exists
        if username in users:
            return False
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Store user
        users[username] = {
            'password': hashed_password,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
        
        # Save users
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
            
        return True
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user with username and password"""
        import json
        import hashlib
        
        # Check if users file exists
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            return False

        # Check if user exists
        if username not in users:
            return False
        
        # Hash password and compare
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        return users[username]['password'] == hashed_password
    
    def create_session(self, username: str) -> str:
        """Create a new session for user"""
        import uuid
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'username': username,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
        return session_id
    
    def validate_session(self, session_id: str) -> str:
        """Validate session and return username if valid"""
        if session_id not in self.sessions:
            return None
            
        # Check session age (expire after 24 hours)
        import datetime
        session = self.sessions[session_id]
        created_at = datetime.datetime.fromisoformat(session['created_at'])
        if (datetime.datetime.now() - created_at).total_seconds() > 86400:  # 24 hours
            del self.sessions[session_id]
            return None
            
        return session['username']
    
    def logout(self, session_id: str) -> bool:
        """Logout user by destroying session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False