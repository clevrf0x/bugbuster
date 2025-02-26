from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List, Optional

router = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={404: {"description": "Not found"}},
)

# Dummy data for users (with realistic sensitive information)
DUMMY_USERS = [
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "+91-9876543210",
        "address": "123, MG Road, Bangalore, Karnataka",
        "aadhaar": "1234-5678-9012",
        "pan": "ABCDE1234F",
        "account_number": "1234567890",
        "balance": 50000.0,
        "transactions": [
            {"id": 1, "type": "credit", "amount": 10000.0, "description": "Salary"},
            {"id": 2, "type": "debit", "amount": 5000.0, "description": "Rent"},
        ],
        "loans": [
            {"id": 1, "amount": 200000.0, "status": "approved"},
            {"id": 2, "amount": 50000.0, "status": "pending"},
        ],
        "password": "alice123",  # Weak password for demonstration
        "role": "customer"
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "phone": "+91-9876543211",
        "address": "456, Connaught Place, New Delhi",
        "aadhaar": "9876-5432-1098",
        "pan": "XYZAB5678G",
        "account_number": "0987654321",
        "balance": 100000.0,
        "transactions": [
            {"id": 1, "type": "credit", "amount": 20000.0, "description": "Freelance Payment"},
            {"id": 2, "type": "debit", "amount": 10000.0, "description": "Groceries"},
        ],
        "loans": [
            {"id": 1, "amount": 100000.0, "status": "approved"},
        ],
        "password": "bob123",  # Weak password for demonstration
        "role": "customer"
    }
]

# Helper function to find a user by ID
def get_user_by_id(user_id: int):
    return next((user for user in DUMMY_USERS if user["id"] == user_id), None)

# Endpoint to get user profile (vulnerable to IDOR)
@router.get("/users/profile")
async def get_user_profile(user_id: int = Query(..., description="The ID of the user to retrieve")):
    user = get_user_by_id(user_id)
    if user:
        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "address": user["address"],
            "account_number": user["account_number"],
            "balance": user["balance"]
        }
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to get user transactions (vulnerable to IDOR)
@router.get("/users/transactions")
async def get_user_transactions(user_id: int = Query(..., description="The ID of the user to retrieve")):
    user = get_user_by_id(user_id)
    if user:
        return user["transactions"]
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to get user loans (vulnerable to IDOR)
@router.get("/users/loans")
async def get_user_loans(user_id: int = Query(..., description="The ID of the user to retrieve")):
    user = get_user_by_id(user_id)
    if user:
        return user["loans"]
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to login (vulnerable to broken authentication)
@router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    user = next((user for user in DUMMY_USERS if user["email"] == email and user["password"] == password), None)
    if user:
        return {"message": "Login successful", "user_id": user["id"]}
    raise HTTPException(status_code=401, detail="Invalid email or password")

# Endpoint to apply for a loan (vulnerable to mass assignment)
@router.post("/loans/apply")
async def apply_for_loan(user_id: int = Body(...), loan_details: dict = Body(...)):
    user = get_user_by_id(user_id)
    if user:
        loan_id = len(user["loans"]) + 1
        loan_details["id"] = loan_id
        loan_details["status"] = "pending"
        user["loans"].append(loan_details)
        return {"message": "Loan application submitted successfully", "loan_id": loan_id}
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to reset password (vulnerable to brute-force attacks)
@router.post("/reset-password")
async def reset_password(email: str = Body(...)):
    user = next((user for user in DUMMY_USERS if user["email"] == email), None)
    if user:
        return {"message": "Password reset link sent to your email"}
    raise HTTPException(status_code=404, detail="User not found")
