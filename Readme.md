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