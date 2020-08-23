@Echo Off
Set "repo_path=%~1"
Set "py_file_path=%~2"
Set "branch=%~3"

If Not Defined repo_path (
    REM Set your default REPO Path
    Set "repo_path=C:\GIT\Analysis\360-analysis"
    REM Set your Python File Path
    Set "py_file_path=C:\GIT\Analysis\360-analysis\NJ\WIP-Sai\Auto_Git_Project\Python_Files
    REM Set your default Branch
    Set "branch=master"
)
Echo %repo_path%
Echo %py_file_path%

CD /D "%repo_path%"
python %py_file_path%\Auto_Git_Push.py %branch%
