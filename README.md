# JWKS Server

## Overview
This project aims to enhance the security of a JWKS server by implementing SQLite to store private keys, safeguarding against SQL injection vulnerabilities. By utilizing a serverless database, the project ensures that private keys are persistently stored and securely accessed, reinforcing the server's resilience in authentication processes.

## Requirements
- Python 3.8+
- Flask
- cryptography
- PyJWT
- pytest
- requests
- coverage

## Setup
1. Run the server:
    ```bash
    python3 main.py
    ```

2. Run the Gradebot
    ```bash
    ./gradebot project2
    ```

3. Run the coverage
    ```bash
    coverage run
    coverage report
    ```
