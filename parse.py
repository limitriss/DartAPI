import requests
import time
import json

# Case 1. 최근 보고서 (3개월 이내)
# get_recent_report()
# Case 2. 
#
#

api_auth = None
with open('auth.txt', 'r') as f:
    api_auth = f.readline()


class DartAPI:
    """
    시작일 최소 : 19990101
    """
    auth = api_auth
    recent_request = None
    TERM = 2

    @staticmethod
    def url():
        """
        공통 url
        """
        MAX_COUNT_PER_PAGE = 100    # 한페이지 최대 100개


        url = 'http://dart.fss.or.kr/api/search.json?' \
              'auth=%s' \
              '&start_dt=%s' \
              '&page_set=%s' \
              '&page_no=%s' \
              % (DartAPI.auth,
                 START_DATE,  # 시작일 최소 : 19990101
                 MAX_COUNT_PER_PAGE,  
                 page_no)



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
    def get_recent_report(START_DATE, page_no=1):
        """
        request 요청에 제한이 있어
        request 요청 사이에 기타작업(가공, DB) 가능하도록 제너레이터
        :param START_DATE: 최근 3개월로 지정해야함
        :yield: 보고서리스트 (최대 100개) (제너레이터)
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

    @staticmethod
    def get_recent_report_by_type(START_DATE=19990101, page_no=1, 
                                    dsp_tp_list=None, 
                                    bsn_tp_list=None):
        """
        request 요청에 제한이 있어
        request 요청 사이에 기타작업(가공, DB) 가능하도록 제너레이터
        :param START_DATE: 최근 3개월로 지정해야함
        :yield: 보고서리스트 (최대 100개) (제너레이터)
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

        if dsp_tp_list:
            for dsp_tp in dsp_tp_list:
                url += ('&dsp_tp=' + dsp_tp) 

        if bsn_tp_list:
            for bsn_tp in bsn_tp_list:
                url += ('&bsn_tp=' + bsn_tp) 

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
    for data in DartAPI.get_recent_report(20180101):
        print(data)
