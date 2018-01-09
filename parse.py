import requests
import time
import json

# Case 1.

auth_file = open('auth.txt', 'r')


class DartAPI:
    auth = auth_file.readline()
    recent_request = None
    TERM = 2

    @staticmethod
    def can_request():
        if DartAPI.recent_request is None:
            return True
        else:
            if time.time() - DartAPI.recent_request > DartAPI.TERM:
                return True
            else:
                return False

    @staticmethod
    def get_recent_report_code(START_DATE, page_no=1):
        """
        START_DATE 만 지정
        최근 3개월로 지정해야함
        :param START_DATE:
        :return: 보고서리스트 (최대 100개) (제너레이터)
        """
        url = 'http://dart.fss.or.kr/api/search.json?' \
              'auth=%s' \
              '&start_dt=%s' \
              '&page_set=%s' \
              '&page_no=%s' \
              % (DartAPI.auth,
                 START_DATE,  # 시작일 최소 : 19990101
                 100,  # 한페이지 최대 100개
                 page_no)

        r = requests.get(url)
        DartAPI.recent_request = time.time()
        content = r.content
        data = json.loads(content.decode('utf8'))

        err_code = data['err_code']
        err_msg = data['err_msg']
        page_no = data['page_no']
        total_page = data['total_page']

        if err_code != '000':
            raise ValueError(err_msg)

        print('page %s/%s' % (page_no, total_page))
        yield data['list']

        page_no += 1
        while page_no <= total_page:
            url = 'http://dart.fss.or.kr/api/search.json?' \
                  'auth=%s' \
                  '&start_dt=%s' \
                  '&page_set=%s' \
                  '&page_no=%s' % \
                  (DartAPI.auth,
                   START_DATE,  # 시작일 최소 : 19990101
                   100,  # 한페이지 최대 100개
                   page_no)

            while not DartAPI.can_request():
                time.sleep(0.5)
            r = requests.get(url)
            DartAPI.recent_request = time.time()
            content = r.content
            data = json.loads(content.decode('utf8'))
            print('page %s/%s' % (page_no, total_page))
            page_no += 1
            yield data['list']


if __name__ == '__main__':
    for data in DartAPI.get_recent_report_code(20180101):
        print(data)
