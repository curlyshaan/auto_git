import subprocess
import re
import win32api
import sys
import win32com.client as win32
import win32net


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


def push(arg1):
    try:
        try:
            run("checkout", arg1)
            run("add", ".")
            run("commit", "-m", "commit via bat file")
            run("push", "-u", "origin", arg1)
            success = True
            send_email("GIT Push Success", "Successfully committed all updates.")
        except subprocess.CalledProcessError as e:
            run("commit", "-a")
            run("push", "-u", "origin", arg1)
            success = "OK"
            send_email("GIT Push Success!!", "Successfully committed all updates.")
    except subprocess.CalledProcessError as e:
        success = False
        send_email("GIT Push Error", "Error While Committing Code. Please check for errors!")
    print(success)


def main(argv):
    if len(argv) == 1:
        arg1 = "master"
    else:
        arg1 = argv[1]

    push(arg1)


main(sys.argv)
