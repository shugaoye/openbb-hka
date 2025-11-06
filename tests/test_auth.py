"""Tests for the authentication system."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    """Test user registration endpoint."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user():
    """Test user login endpoint."""
    # First register a user
    client.post("/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword"
    })
    
    # Then login
    response = client.post("/auth/login", data={
        "username": "testuser2",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_invalid_login():
    """Test login with invalid credentials."""
    response = client.post("/auth/login", data={
        "username": "nonexistentuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_duplicate_registration():
    """Test registration with duplicate username/email."""
    # Register a user
    client.post("/auth/register", json={
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "testpassword"
    })
    
    # Try to register the same username
    response = client.post("/auth/register", json={
        "username": "testuser3",
        "email": "different@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    
    # Try to register the same email
    response = client.post("/auth/register", json={
        "username": "differentuser",
        "email": "test3@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400