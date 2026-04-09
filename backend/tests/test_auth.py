def test_register(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  assert response.status_code == 201 
  assert response.json()["name"] == "Test"
  assert response.json()["email"] == "test@test.com"
 
def test_duplicate_register(test_app): 
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})

  assert response.status_code == 409 
  assert response.json()["detail"] == "Email has already been registered."

def test_empty_namme(test_app):
  response = test_app.post("/auth/register", json = {"name": "", "email": "test@test.com", "password": "password123"})
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Name can't be left empty."

def test_nonalphabetical_name(test_app):
  response = test_app.post("/auth/register", json = {"name": "12@", "email": "test@test.com", "password": "password123"})
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Name can only contain alphabetical characters."

def test_login(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})

  assert response.status_code == 200
  assert response.json()["access_token"]
  assert response.json()["refresh_token"]
  assert response.json()["name"] == "Test"

def test_wrong_password(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "passwod123"})

  assert response.status_code == 401
  assert response.json()["detail"] == "Email or password incorrect."

def test_wrong_email(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "tet@test.com", "password": "password123"})

  assert response.status_code == 401
  assert response.json()["detail"] == "Email or password incorrect."

def test_generate_categories(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})
  token = response.json()["access_token"]
  response = test_app.get("/categories", headers =  {"Authorization": f"Bearer {token}"})

  assert response.status_code == 200 
  assert len(response.json()) == 13

def test_refresh(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})
  refresh_token = response.json()["refresh_token"]
  response = test_app.post("/auth/refresh", json = {"refresh_token": refresh_token})

  assert response.status_code == 200 
  assert response.json()["access_token"]

def test_invalid_refresh(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})
  refresh_token = "random string"
  response = test_app.post("/auth/refresh", json = {"refresh_token": refresh_token})

  assert response.status_code == 401

def test_get_email(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})
  token = response.json()["access_token"]
  response = test_app.get("/auth/me", headers =  {"Authorization": f"Bearer {token}"})

  assert response.status_code == 200
  assert response.json() == "test@test.com"