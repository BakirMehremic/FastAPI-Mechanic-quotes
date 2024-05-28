This project is built using FastAPI, bcrypt for password hashing, SQLAlchemy ORM connected to a 
SQLite database so it's easier to get running on a different PC, it uses JWT Authentification as
recommended in FastAPI docs, pydantic for request modeling etc.
It is structured in a mostly standard way apart from the route logic being in the crud package.

The point of this API is that users can send requests to mechanics regarding their car and a description
of the problem and the mechanic answers with a quote containing the amount to fix and description,
the user can then accept or decline this quote, or delete the request altogether.
Admins can have permission set to all or partial which determine if they can only view all data 
or delete it from the db. To see all the functionality see the screenshots or routes in app/routes.

You can get the api running by:
1. Cloning the repo
2. cd to the location, pythom -m venv venv
3. venv/scripts/activate
4. pip install -r requirements.txt
5. cd app
6. uvicorn main:app --reload
