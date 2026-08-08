# python_sandbox

## nhl_microservice
Using Python 3.14.6

Steps for setup or run step 3 to activate virtual environment when a new command prompt is opened:
1. From the nhl_microservice folder run: `python -m venv venv`
2. Then run: `.\venv\Scripts\activate`
3. Install packages: `pip install fastapi uvicorn httpx beautifulsoup4 sqlalchemy aiosqlite`
4. Run the app: `uvicorn main:app --reload`
5. Swagger page is here: `http://localhost:8000/docs`
