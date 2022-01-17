import requests , json , time
from datetime import datetime
from os import path , stat
from colorama import init , Fore
import aiocron , asyncio , pytz , argparse
init()
RED = Fore.RED
YLW = Fore.YELLOW
BLU = Fore.BLUE
GRN = Fore.GREEN
RES = Fore.RESET
# ================================================ #
Main_Url = "https://www.instagram.com/"
Login_Url = "accounts/login/ajax/"
session = requests.session()
timeNum = 0
TimerFun_Bool = False
# ================================================ #


def Login():

    UserName = input(f'\n{GRN}Enter Your Instagram Username {BLU}:{RES} ')
    PassWord = input(f'{GRN}Enter Your Instagram Account Password {BLU}:{RES} \n')
    print(f"{RED}[============================]{RES}")
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    session.headers.update({'Referer': Main_Url})
    Base_Requests = session.get(Main_Url)
    session.headers.update({'X-CSRFToken':Base_Requests.cookies['csrftoken']})
    Login_Requests = session.post(f"{Main_Url}{Login_Url}", data={'enc_password': "#PWD_INSTAGRAM_BROWSER:0:{}:{}".format(int(datetime.now().timestamp()),PassWord) ,'username':UserName,} , allow_redirects=True)
    session.headers.update({'X-CSRFToken':Login_Requests.cookies['csrftoken']})
    with open('cookies.txt', 'w+') as file:
        json.dump(session.cookies.get_dict(), file)
    with open('headers.txt', 'w+') as file:
        json.dump(session.headers, file)

    if Login_Requests.json()['authenticated']:
        print(f"{GRN}Logged in{RES}")
    else:
        print(f"{RED}Login Failed\n")
        Login()


def Subsidiary():
    with open('cookies.txt', 'r') as file:
        session.cookies.update(json.load(file))
    with open('headers.txt', 'r') as file:
        session.headers = json.load(file)

@aiocron.crontab('*/1 * * * *')
async def BioTimer():
    if TimerFun_Bool == True:
        ir=pytz.timezone("Asia/Tehran")
        biography = f"""⏰Time : {datetime.now(ir).strftime("%H:%M")}
📅Date : {datetime.now(ir).strftime("%Y/%d/%m")}"""
        data = session.get("https://www.instagram.com/accounts/edit/?__a=1")
        main = data.json()['form_data']
        first_name = main['first_name']
        email = main['email']
        username = main['username']
        phone_number = main['phone_number']
        external_url = main['external_url']
        chaining_enabled = main['chaining_enabled']
        data = session.post("https://www.instagram.com/accounts/edit/" , data={
            "first_name":first_name,
            "email":email,
            "username":username,
            "phone_number":phone_number,
            "biography":biography,
            "external_url":external_url,
            "chaining_enabled":chaining_enabled})
        if data.json()['status'] == "ok":
            print(f"{GRN}successful")
        else:
            print(f"{RED}Unsuccessful")
    
def chenger(biography):
    data = session.get("https://www.instagram.com/accounts/edit/?__a=1")
    main = data.json()['form_data']
    first_name = main['first_name']
    email = main['email']
    username = main['username']
    phone_number = main['phone_number']
    external_url = main['external_url']
    chaining_enabled = main['chaining_enabled']
    data = session.post("https://www.instagram.com/accounts/edit/" , data={
        "first_name":first_name,
        "email":email,
        "username":username,
        "phone_number":phone_number,
        "biography":biography,
        "external_url":external_url,
        "chaining_enabled":chaining_enabled})
    if data.json()['status'] == "ok":
        print(f"{GRN}successful")
    else:
        print(f"{RED}Unsuccessful")


# ================================================ #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the exploit you want faster with me :) ")
    parser.add_argument("--btimer", help="See the latest exploits",action="store_true")
    parser.add_argument("--btext", help="See the tool version",action="store_true")
    parser.add_argument('-t','--time', help='Search by tag')

    
    args = parser.parse_args()


    if args.time:
        try:
            timeNum += int(args.time)
        except:
            print("Error")

    if args.btimer == True and args.btext == True:
        print("Error")
    elif args.btimer == False and args.btext == False:
        print("Error")
    else:
        if args.btimer == True:
            if args.time:
                print("Error")
            else:
                if(path.exists("cookies.txt") == True ) and (stat("cookies.txt").st_size > 0) and (path.exists("headers.txt") == True) and (stat("headers.txt").st_size > 0):
                    Subsidiary()
                else:
                    Login()
                TimerFun_Bool = True
                asyncio.get_event_loop().run_forever()

        if args.btext == True:
            while(True):
                with open("bio_text.txt","r") as file:
                    bioText = file.read().splitlines()
                for TxT in bioText:
                    if(path.exists("cookies.txt") == True ) and (stat("cookies.txt").st_size > 0) and (path.exists("headers.txt") == True) and (stat("headers.txt").st_size > 0):
                        Subsidiary()
                        chenger(TxT)
                    else:
                        Login()
                        chenger(TxT)
                    time.sleep(timeNum)
    
