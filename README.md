# Basketball League Site

### Django

1. Create a virtual environment:

```
python3 -m venv env
```

2. Activate the virtual environment:

```
. env/bin/activate
```

3. Install the python requirements:

```
pip install -r requirements.txt
```

4. Create database

```
./manage migrate
```

5. Initialise site data

```
./manage init_site_users

./manage init_league
```

6. start the server

```
./manage runserver
```

9. browse to http://localhost:8000/admin/

```
username: admin
pasword: password
```



### React App

1. cd bblsite-frontend

2. npm install

3. npm start

4. browse to http://localhost:3000

```
username: admin@bbl.com
password password
```