import requests
from PIL import Image
from io import BytesIO
#harry585858
#request query(보안문자) fake 번호 이미지?
#post sugang.dongguk.edu/d/l/loginCheck?fake=
#txtUserID txtPwd secNo 입력한보안문자
#POST sugang.dongguk.edu/d/s/del?fake=(fake 번호) 삭제 params: CM015.110@DS034101@CSC4011@01 형태
#post sugang.dongguk.edu/d/s/add?fake=(fake 번호) 추가 params: CM015.110@DS034101@CSC4011@01 형태
#1737774763142
url = 'https://sugang.dongguk.edu/'
fake = 173777 #보안문자 이미지 번호
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Connection": "keep-alive"  # Keep-Alive 헤더 추가
}
cookies = {

}
session = requests.Session()
def add(inp):
    data = {
        'params':'CM015.110@DS034101'+inp,
        'pWaitDiv':'T'
    }
    response = session.post(url+'d/s/add?fake='+str(fake), data=data, headers=headers)
    print(response.status_code)

def delete(inp):
    data = {
        'params':'CM015.110@DS034101'+inp,
        'pWaitDiv':'T'
    }
    response = session.post(url+'d/s/del?fake='+str(fake), data=data, headers=headers)
    print(response.status_code)

def login(id,pw, secNo):
    data = {
        'txtUserID':id,
        'txtPwd':pw,
        'secNo':secNo
    }
    response = session.post(url+'d/l/loginCheck?fake='+str(fake), data=data, headers=headers)
    return response.text

def start():
    while True:
        select = input('신청/취소/끝 1/2/3')
        if select == 1:
            subject = input('과목@분반 형식 입력 : ')
            if subject.find('@') != -1:
                add(subject)
            else:
                print('다시 입력')
        elif select == 2:
            subject = input('과목@분반 형식 입력 : ')
            if subject.find('@') != -1:
                delete(subject)
            else:
                print('다시 입력')
        elif select == 3:
            return


response = session.get(url,headers=headers)
response1 = session.post(url+'p/l/loginPage', headers=headers)
if response.status_code == 200:
    inp = input('로그인 하시겠습니까? Y/N : ')
    if inp == 'Y' or inp == 'y':
        id = input('id 입력 : ')
        pw = input('pw 입력 : ')
        fake = response.text.find('src="/static/js/fn-appinfo.min.js?v=')
        fakeend = response.text.find('" type="text/javascript"></script>')
        if fake == -1 or fakeend == -1:
            print("fake 번호를 찾을 수 없습니다.")
        else:
            fake = response.text[fake+36:fakeend]
            response = session.get(url+'d/l/mcrImg?fake='+fake)
            print(fake)
            if response.status_code == 200:
            # 이미지 데이터를 BytesIO로 변환하여 PIL에서 처리 가능하도록 함
                img = Image.open(BytesIO(response.content))
                img.show()
            secNo = input('보안문자 입력 : ')
            if login(id,pw,secNo).find('OK') != -1:
                print('로그인 성공')
                start()
            else:
                print('로그인 실패')
else:
    print('사이트 접속 불가')