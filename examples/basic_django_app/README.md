# Setting up a Basic Django Web Application with an HTML Page

## This guide walks you through setting up a basic Django project, creating a view, connecting a URL, and rendering an HTML page.

1. Install Django

Install Django using pip:
~~~
pip install django
~~~

2. Create a Django Project

Create a new Django project:
~~~

django-admin startproject myproject
cd myproject
~~~

3. Create a Django App

Create a new app within the project:
~~~

python manage.py startapp myapp
~~~

Add the app to the INSTALLED_APPS list in myproject/settings.py:
~~~

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
~~~

4. Create a View

In myapp/views.py, create a view function to render an HTML page:
~~~

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

~~~    

5. Set Up the URL

In myproject/urls.py, include the URL pattern for the new view:
~~~

from django.contrib import admin
from django.urls import path
from myapp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]
~~~

6. Create an HTML Page

Create a directory named templates inside the myapp folder and add an home.html file:


myapp/
├── templates/
│   └── home.html

In home.html, add the following content:
~~~

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <h1>Welcome to My Django App!</h1>
    <p>This is a basic HTML page rendered using Django.</p>
</body>
</html>
~~~

7. Run the Development Server

Apply migrations and start the development server:
~~~

python manage.py migrate
python manage.py runserver
~~~

8. View the Application

Visit http://127.0.0.1:8000/ in your browser to see the "Welcome to My Django App!" message displayed.

Debugging Tips

Check for syntax errors in your urls.py, views.py, or templates.

Ensure all required apps are added to the INSTALLED_APPS list.

Use python manage.py check to identify common configuration issues.

* Conclusion

You now have a working Django project rendering an HTML page! From here, you can expand your app by adding more views, templates, and database functionality.

