# teachers-directory-app
#### Installation Steps using Docker
- 1.Install Docker (follow https://docs.docker.com/engine/install/)
- 2.from the project directory Run `docker compose up`
- 3.Access website `http://locslhost:8000`

#### Installation Steps with virtual environment
- 1.Install python version 3.x
- 2.Run `cd project_path` replace project path with actual project location
- 3.Run `python3 -m venv venv`
- 4.Run `source venv/bin/activate`
- 5.Run `pip install -r requirements.txt`
- 6.Run `python manage.py migrate`
- 7.Run `python manage.py runserver`
- 8.Access website `http://locslhost:8000`
