import requests
import re
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib

def _check_in():
    url = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld&client=apple&clientVersion=10.0.4&networkType=wifi&osVersion=14.8.1&uuid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&openudid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&jsonp=jsonp_1645885800574_58482";
    headers  = {"Connection":'keep-alive',
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "Cache-Control": 'no-cache',
                "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
                "accept": "*/*",
                "connection": "Keep-Alive",
                "Accept-Encoding": "gzip,deflate",
                # you only replace pt_key after 30 day and repalace your_pt_key 
                "Cookie": "__jd_ref_cls=JingDou_SceneHome_NewGuidExpo; \
                        mba_muid=1645885780097318205272.81.1645885790055; \
                        mba_sid=81.5;\
                        __jda=122270672.1645885780097318205272.1645885780.1645885780.1645885780.1; \
                        __jdb=122270672.1.1645885780097318205272|1.1645885780; __jdc=122270672; \
                        __jdv=122270672%7Ckong%7Ct_1000170135%7Ctuiguang%7Cnotset%7C1644027879157; \
                        pre_seq=0; \
                        pre_session=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6|143; \
                        unpl=JF8EAKZnNSttWRkDURtVThUWHAgEWw1dH0dXOjMMAFVcTQQAEwZORxR7XlVdXhRKFx9sZhRUX1NIVw4YBCsiEEpcV1ZVC0kVAV9XNVddaEpkBRwAExEZQ1lWW1kMTBcEaWcAUVpeS1c1KwUbGyB7bVFeXAlOFQJobwxkXGhJVQQZBR0UFU1bZBUzCQYXBG1vBl1VXElRAR8FGxUWS1hRWVsISCcBb2cHUm1b%7CV2_ZzNtbRYAFxd9DUNcKRxYB2ILGloRUUYcIVpAAHsbWQZjVBEJclRCFnUUR11nGlgUZgIZXkFcQRRFCEJkexhdB24LFFtEUHMQfQ5GXH0pXAQJbRZeLAcCVEULRmR6KV5VNVYSCkVVRBUiAUEDKRgMBTRREV9KUUNGdlxAByhNWwVvBUIKEVBzJXwJdlR6GF0GZAoUWUdRQCUpUBkCJE0ZWTVcIlxyVnMURUooDytAGlU1Vl9fEgUWFSIPRFN7TlUCMFETDUIEERZ3AEBUKBoIAzRQRlpCX0VFIltBZHopXA%253d%253d; \
                        pt_key=your_pt_key; \
                        pt_pin=jd_IyPtvUHFxSit; \
                        pwdt_id=jd_505bacd333f6b; \
                        sid=1b2c8b7ce820c4188f048e689bf58c8w; \
                        visitkey=36446698972455355"
                }
    response = requests.post(url=url, headers=headers)
    # print(response.text)
    matchs = re.search(r'签到成功|签到失败|今天已签到', response.text, re.DOTALL)
    # print(matchs)
    return matchs.group(0)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def _send_message(form_addr, password, to_addr, smpt_server, matchs):
    # 设置邮件信息
    if matchs == '签到成功' or matchs == '今天已签到':
        msg = MIMEText('JD Douzi automatically signed in successfully.', 'plain', 'utf-8')
    else:
        msg = MIMEText('Your pt_key has expired.', 'plain', 'utf-8')

    # 设置收发邮箱
    msg['From'] = _format_addr('Server <%s>' %form_addr)
    msg['To'] = _format_addr('administrator <%s>' %to_addr)
    msg['Subject'] = Header('Jingdong Douzi automatic sign-in situation', charset='utf-8').encode()

    # 发送邮件
    server = smtplib.SMTP(smpt_server, port=25)
    server.set_debuglevel(1)
    server.login(form_addr, password)
    server.sendmail(form_addr, [to_addr], msg.as_string())
    server.quit()

if __name__=="__main__":
    # 邮箱
    form_addr = 'XXXX@XX.com'
    # 不是邮箱密码,而是开启SMTP服务时的授权码
    password = 'PASSWORD'
    # 收件人的邮箱
    to_addr = 'XXXX@XX.com'
    # qq邮箱的服务器地址
    smpt_server = 'smtp.XX.com'

    matchs = _check_in()
    _send_message(form_addr, password, to_addr, smpt_server, matchs)