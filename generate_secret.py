import secrets

print("SECRET_KEY=" + secrets.token_urlsafe(32))
print("JWT_SECRET=" + secrets.token_urlsafe(32))
