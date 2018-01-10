import requests
import time
import json

# Case 1. 최근 보고서 (3개월 이내)
# get_recent_report()
# Case 2. 


api_auth = None
with open('auth.txt', 'r') as f:
    api_auth = f.readline()


DEFAULT_QUERY = {
'auth': api_auth,
'page_no': 1,
'start_dt': 19990101,   # 시작일 최소 : 19990101
'page_set': 100         # 한페이지 최대 100개
}


class DartAPI:
    """
    시작일 최소 : 19990101
    """
    recent_request = None
    TERM = 2


    @staticmethod
    def url(query=DEFAULT_QUERY):
        """
        query: dict
            dsp_tp, bsn_tp: list
        """
        url = 'http://dart.fss.or.kr/api/search.json?'
        
        for query_type in query.keys():
            if query_type == 'dsp_tp':
                for dsp_tp in query[query_type]:
                    url += ('&dsp_tp=' + dsp_tp)
            elif query_type == 'bsn_tp':
                for bsn_tp in query[query_type]:
                    url += ('&bsn_tp=' + bsn_tp) 
            else:
                url += ('&%s=%s' % (query_type, query[query_type]))
        return url

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
        query = DEFAULT_QUERY
        query['start_dt'] = START_DATE
        query['page_no'] = page_no
        url = DartAPI.url(query)

        while not DartAPI.can_request():
            time.sleep(0.1)
        r = requests.get(url)
        DartAPI.recent_request = time.time()
        data = json.loads(r.content.decode('utf8'))

        err_code = data['err_code']
        err_msg = data['err_msg']
        page_no = data['page_no']
        total_page = data['total_page']
        if err_code != '000':
            raise ValueError(err_msg, url)

        print('page %s/%s' % (page_no, total_page))
        yield data['list']

        page_no += 1
        while page_no <= total_page:
            query['page_no'] = page_no
            url = DartAPI.url(query)

            while not DartAPI.can_request():
                time.sleep(0.1)
            r = requests.get(url)
            DartAPI.recent_request = time.time()
            data = json.loads(r.content.decode('utf8'))

            err_code = data['err_code']
            err_msg = data['err_msg']
            page_no = data['page_no']
            if err_code != '000':
                raise ValueError(err_msg, url)

            print('page %s/%s' % (page_no, total_page))
            page_no += 1
            yield data['list']

    @staticmethod
    def get_recent_report_by_type(START_DATE, page_no=1, 
        dsp_tp_list=None, 
        bsn_tp_list=None):
        """
        request 요청에 제한이 있어
        request 요청 사이에 기타작업(가공, DB) 가능하도록 제너레이터
        :param START_DATE: 최근 3개월로 지정해야함
        :yield: 보고서리스트 (최대 100개) (제너레이터)
        """
        query = DEFAULT_QUERY
        query['start_dt'] = START_DATE
        query['page_no'] = page_no

        if dsp_tp_list:
            query['dsp_tp'] = dsp_tp_list
        if bsn_tp_list:
            query['bsn_tp'] = bsn_tp_list

        url = DartAPI.url(query)

        while not DartAPI.can_request():
            time.sleep(0.1)
        r = requests.get(url)
        DartAPI.recent_request = time.time()
        data = json.loads(r.content.decode('utf8'))

        err_code = data['err_code']
        err_msg = data['err_msg']
        page_no = data['page_no']
        total_page = data['total_page']
        if err_code != '000':
            raise ValueError(err_msg, url)

        print('page %s/%s' % (page_no, total_page))
        yield data['list']

        page_no += 1
        while page_no <= total_page:
            query['page_no'] = page_no
            url = DartAPI.url(query)

            while not DartAPI.can_request():
                time.sleep(0.1)
            r = requests.get(url)
            DartAPI.recent_request = time.time()
            data = json.loads(r.content.decode('utf8'))

            err_code = data['err_code']
            err_msg = data['err_msg']
            page_no = data['page_no']
            if err_code != '000':
                raise ValueError(err_msg, url)

            print('page %s/%s' % (page_no, total_page))
            page_no += 1
            yield data['list']


if __name__ == '__main__':
    for data in DartAPI.get_recent_report(20180101):
        print(data)

    for data in DartAPI.get_recent_report_by_type(20180101,
                                                    dsp_tp_list=['A'],
                                                    bsn_tp_list=['B003']):
        print(data)
