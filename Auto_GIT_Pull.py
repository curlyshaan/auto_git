import subprocess
import re
import win32api
import win32com.client as win32
import win32net
import sys


def get_email():
    user_info = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 2)
    full_name = user_info["full_name"]
    full_name = full_name.replace(',', ' ')
    full_name = full_name.lower().strip()
    full_name = re.findall(r'\s*([^\s]+)', full_name)[:2]
    email = full_name[1] + "." + full_name[0] + "@cigna.com"
    return email


def send_email(subj, msg):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = get_email()
    mail.Subject = subj
    mail.Body = msg
    mail.Send()


def run(*args):
    return subprocess.check_call(['git'] + list(args))


def pull(arg1):
    try:
        try:
            run("add", ".")
            run("commit", "-m", "committing before bat file")
            run("checkout", arg1)
            run("pull")
            send_email("GIT Pull Success", "Git pull today was a success.")
        except subprocess.CalledProcessError as e:
            run("checkout", arg1)
            run("pull")
            send_email("GIT Pull Success", "Git pull today was a success.")

    except subprocess.CalledProcessError as e:
        send_email("GIT Pull Error", "Error While Pulling GIT. Please check for errors!")


def main(argv):
    if len(argv) == 1:
        arg1 = "master"
    else:
        arg1 = argv[1]

    pull(arg1)


main(sys.argv)
