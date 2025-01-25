import requests
from PIL import Image
from io import BytesIO
#request query(보안문자) fake 번호 이미지?
#post sugang.dongguk.edu/d/l/loginCheck?fake=
#txtUserID txtPwd secNo 입력한보안문자
#POST sugang.dongguk.edu/d/s/del?fake=(fake 번호) 삭제 params: CM015.110@DS034101@CSC4011@01 형태
#post sugang.dongguk.edu/d/s/add?fake=(fake 번호) 추가 params: CM015.110@DS034101@CSC4011@01 형태
#1737774763142 51191
url = 'https://sugang.dongguk.edu/'
fake = 1737774763142 #보안문자 이미지 번호
def add(inp):
    data = {
        'params':'CM015.110@DS034101'+inp,
        'pWaitDiv':'T'
    }
    response = requests.post(url+'d/s/add?fake='+str(fake), json=data)
    print(response.status_code)

def delete(inp):
    data = {
        'params':'CM015.110@DS034101'+inp,
        'pWaitDiv':'T'
    }
    response = requests.post(url+'d/s/del?fake='+str(fake), json=data)
    print(response.status_code)
def login(id,pw, secNo):
    data = {
        'txtUserID':id,
        'txtPwd':pw,
        'secNo':secNo
    }
    response = requests.post(url+'d/l/loginCheck?fake='+str(fake), json=data)
    print(response.status_code)
    print(response.text)


response = requests.post(url+'p/l/loginPage')
if response.status_code == 200:
    inp = input('로그인 하시겠습니까? Y/N : ')
    if inp == 'Y' or inp == 'y':
        id = input('id 입력 : ')
        pw = input('pw 입력 : ')
        print(response.text)
        fake = response.text.find('src="/static/js/fn-appinfo.min.js?v=')
        fakeend = response.text.find('" type="text/javascript"></script>')
        if fake == -1 or fakeend == -1:
            print("fake 번호를 찾을 수 없습니다.")
        else:
            fake = response.text[fake+36:fakeend]
            response = requests.get(url+'d/l/mcrImg?fake='+fake)
            if response.status_code == 200:
            # 이미지 데이터를 BytesIO로 변환하여 PIL에서 처리 가능하도록 함
                img = Image.open(BytesIO(response.content))
                img.show()
            secNo = input('보안문자 입력 : ')
            login(id,pw,secNo)
else:
    print('사이트 접속 불가')