#install python
 
git clone git@github.com:chalatse/v4.git
cd Backend

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


pip install -r requirements.txt


alembic upgrade head


http://127.0.0.1:8000

#SWAGGER UI
http://127.0.0.1:8000/docs

