# This is a pet api project dedicated to internet shop
____

## For start u need:
1. Create virtual environment
   ```python 
    python -m venv env
    ```
2. Activate virtual environment
   ```python 
    Windows: env/Scripts/activate 
    Linux: source env/bin/activate
    ```
3. Install requirements
   ```python 
    pip install -r requirements.txt
    ```
4. Init db
   ```python 
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Filling the database with test data
   ```python 
    python manage.py create_users
    python manage.py create_items
    python manage.py create_reviews
    ```
 6. Run server
   ```python 
    python manage.py runserver
   ```

### U can find docs in /api/v1/docs/ url


