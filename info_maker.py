#test 모듈
#단체 대화방에서 대화의 정도를 분석하도록 한다.
#카톡 데이터의 구조 : 0000년 0월 00일 오전 00:00, 000 : ~~~~

from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class talk_data_type:
    num : int
    talk_date :date
    name: str
    talk_type : str # 0:메세지 1:이모티콘 2:사진 3:동영상 4:도배 5:웃음
    msg : str


def talk_data_making() :

    repeat_msg_num = 5  #talk 세부 설정 세팅

    talk_address = input()
    f = open(talk_address,'r',encoding='UTF8') #인코딩을 변환해주지않으면 오류가 생긴다

    maked_data = list()

    while True:
        line = f.readline()
        line = '2020년 8월 30일 오전 12:43, 회원님 : 까먹엇노'
        if not line : break

        data_ing = talk_data_type


        if line.index(',')>=23 or line.index(',') == None :
            pass #정상대화가 아닌 날짜변경로그거나 저장한 날짜등을 표시하는 경우 카운팅하지않고 넘긴다

        else :
            #날짜데이터를 추출해낸다
            y_n = line.index('년')
            m_n = line.index('월')
            d_n = line.index('일')
            data_ing.talk_date = date(int(line[y_n-4:y_n]),int(line[m_n-2:m_n]),
                                     int(line[d_n-3:d_n]))

            #이름데이터 추출
            data_ing.name =

