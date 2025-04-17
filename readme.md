# SETUP
1. Install Flask using this command in the CLI:
* Windows: `pip install flask`
* MacOs: `pip3 install flask`

2. Install the SQLAlchemy ORM for Flask using this command in the CLI:
* Windows: `pip install Flask Flask-SQLAlchemy`
* MacOd: `pip3 install Flask Flask-SQLAlchemy`

    We will be using in memory database for now so we dont actually need to setup a server right now.

3. In order to run the application from your IDE you will need to be in the projects parent directory. Meaning you will need to be int the `CIT260` folder from your CLI using this command to run the application:
* Windows: `python -m BLL.app`
* MacOs: `python3 -m BLL.app`

# Create a New Branch, Pushing, and PRs
This is very important so that you don't accidently modify the main branch without approval from everyone. Make sure to have Git installed on your machine. Here are the steps to create your own branch, pushing and creating PR's:
1. Create your own branch using this command `git checkout -b <new-branch-name>
`
2. Add your work to the commit by running `git add <fileName>` or add all files with `git add .`
3. Then commit the files by running `git commit -m "<add desciptive message here>"`
4. Then run this command to push to the repository `git push -u origin <new-branch-name>
`. This command only needs to be ran once when you create a new branch. 
* If you have already ran that command you can just run `git push` and that will push to your branch. But make sure you are actually in YOUR REPOSITORY.

5. Next go to the GitHub repo and create a PULL REQUEST targeting to merge into the main branch.

# Using the Base.css file
For consistency across all webpages I've created a `base.css` file that will add a
header, footer, CSS style to the body, containers, and buttons that are meant to 
match the style of the real CSN homepage. (This can all be changed as we progress,
but for now, this will add consistency across all pages.)

## Steps to Implement

1. Ensure that your HTML file has both of the following links in the `<head>` block:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/[YOUR HTML FILE NAME HERE]') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
```
2. Ensure that your `app.py` has the `static_folder` listed:
```python
app = Flask(__name__, template_folder="../presentation/templates", static_folder="../presentation/static")
```
3. Ensure you have the header block added to your HTML file:
```html
<header>
    <nav>
        <div class="logo">
            <img src="{{ url_for('static', filename='images/logo_0_0.webp') }}" alt="Logo">
            Exam Registration
        </div>
        <ul class="navbar">
            <li><a href="{{ url_for('home') }}">Home</a></li>
            <li><a href="{{ url_for('login') }}">Login</a></li>
            <li><a href="{{ url_for('signup') }}">Sign Up</a></li>
        </ul>
    </nav>
</header>
```
4. Ensure you have the footer block added to your HTML file:
```html
<footer>
    <p>&copy; 2025 Exam Registration. All rights reserved. | 
        <a href="https://github.com/blingo77/CIT_260_Proj" target="_blank">GitHub Repository</a>
    </p>
</footer>
```
5. Using Predefined CSS Styles
To use a predefined CSS style in one of your blocks, include `class="logo"` in your
block tags such as:
```html
<div class="logo">Content here</div>
```
This class will match the `.logo` style within the `base.css` file.