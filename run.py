import json
import os
import random
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
from lxml import etree
# from IP import headers
from tqdm import tqdm
from datetime import datetime, timedelta
import urllib3, re, time, logging, match


time_turn = {}
time_mon = ['12', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
current_time = datetime.now()
local_time = current_time.strftime("%Y/%m/%d")
formatted_time = current_time.strftime("%Y/%m/%d").split('/')

# def time_format(time):
#     match time:
#         case "1":
#             return "12"

for id, i in enumerate(time_mon):
    time_turn[f"0{str(id + 1)}"] = i


def get_yesterday():
    today = datetime.now()
    yesterday = str((today - timedelta(days=1)).strftime("%Y/%m/%d")).split(" ")[0]
    # print(yesterday)
    return yesterday


def compare_with_yesterday(date_str):
    yesterday = get_yesterday()
    date_format = "%Y/%m/%d"
    yesterday = datetime.strptime(yesterday, date_format)
    datetime_date = datetime.strptime(date_str, date_format)

    return datetime_date == yesterday



class Douyin:
    def __init__(self):
        # self.SeemFlower = "https://www.douyin.com/hashtag/7342703537991714879"
        self.SeemFlower = "https://www.douyin.com/aweme/v1/web/challenge/aweme/"
        # self.huitun_url = "https://dy.huitun.com/app/index.html#/app/anchor/anchor_list/anchor_detail?id=94475040756&keyword=CFM%E6%9D%8E%E7%99%BD%20%E7%99%BD%E7%BB%99%E5%A4%A9%E6%89%8D&tabKey=live_record"
        self.headers_douyin = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            'Cookie': "douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; ttwid=1%7CoaKBJdOngaSdkaoRhpDlp94I7ABKDVPpcV-f-iyPBrw%7C1698992130%7C1ef592bbfd7688d22857aa38b072b03a7ff3d841a6f8c5bbdb17ab02e1017b6f; d_ticket=7c4c8ea877cf2fd1f88b8c633272368117323; LOGIN_STATUS=1; store-region=cn-gd; store-region-src=uid; my_rd=2; __live_version__=%221.1.1.5721%22; live_use_vvc=%22false%22; csrf_session_id=def309a22d5ba191e1ab08ae175ba167; passport_csrf_token=237477354b89d83cc9f393cc9cd31774; passport_csrf_token_default=237477354b89d83cc9f393cc9cd31774; bd_ticket_guard_client_web_domain=2; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; passport_assist_user=CkEqRkeohZaEQZcKBDx3oe5VtM1q3jSZjafa_Jyz5EzTyjTngmv2XrIkThngjguUey4B4_GNVqCcbLWzOXD-v3sMThpKCjwGsJYin6EtAyHR2zHNPBfpYjqTzM92aCV9tZUMYN6sirTQ84ZXlGe2BgSps8jZtfoR8MPb8pa24WiWV_QQprPLDRiJr9ZUIAEiAQNOBhOd; n_mh=bN8K4Fz-o5PcExr4ZW22ZekQw9_IqxP4NTSwLseA1IM; sso_auth_status=f967f02a1e5842942e3d5fd4be4d0f78; sso_auth_status_ss=f967f02a1e5842942e3d5fd4be4d0f78; sso_uid_tt=9419018aa2029c9eded6cf2866d37d24; sso_uid_tt_ss=9419018aa2029c9eded6cf2866d37d24; toutiao_sso_user=6c014c724a7c5c56b197651763553ebe; toutiao_sso_user_ss=6c014c724a7c5c56b197651763553ebe; sid_ucp_sso_v1=1.0.0-KDVhYWY3OGFkODkxMmQxODliOGIyYThjMjQ1ZjBiYmNjMDRmZTBlN2UKHwidlsDcmoy3AxDSjqyvBhjvMSAMMOjz6pgGOAJA8QcaAmxxIiA2YzAxNGM3MjRhN2M1YzU2YjE5NzY1MTc2MzU1M2ViZQ; ssid_ucp_sso_v1=1.0.0-KDVhYWY3OGFkODkxMmQxODliOGIyYThjMjQ1ZjBiYmNjMDRmZTBlN2UKHwidlsDcmoy3AxDSjqyvBhjvMSAMMOjz6pgGOAJA8QcaAmxxIiA2YzAxNGM3MjRhN2M1YzU2YjE5NzY1MTc2MzU1M2ViZQ; passport_auth_status=44b75d6db28462e48e3c77ff90cfa075%2Cf902ec89fb2b0060279593fb6364e135; passport_auth_status_ss=44b75d6db28462e48e3c77ff90cfa075%2Cf902ec89fb2b0060279593fb6364e135; uid_tt=f5a813b4b00f326cc26b3cfca3fddcd5; uid_tt_ss=f5a813b4b00f326cc26b3cfca3fddcd5; sid_tt=7478899e208dbda4965a2f7efa5781c5; sessionid=7478899e208dbda4965a2f7efa5781c5; sessionid_ss=7478899e208dbda4965a2f7efa5781c5; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=32c5b74c49067d5abf25b8300ead3280; __security_server_data_status=1; sid_guard=7478899e208dbda4965a2f7efa5781c5%7C1709901653%7C5184000%7CTue%2C+07-May-2024+12%3A40%3A53+GMT; sid_ucp_v1=1.0.0-KGYyYTdjYWM5OGE2MDUzMTYxYzZhNmFlMGZkNmRjOGU5NzBhMjBkODkKGwidlsDcmoy3AxDVjqyvBhjvMSAMOAJA8QdIBBoCaGwiIDc0Nzg4OTllMjA4ZGJkYTQ5NjVhMmY3ZWZhNTc4MWM1; ssid_ucp_v1=1.0.0-KGYyYTdjYWM5OGE2MDUzMTYxYzZhNmFlMGZkNmRjOGU5NzBhMjBkODkKGwidlsDcmoy3AxDVjqyvBhjvMSAMOAJA8QdIBBoCaGwiIDc0Nzg4OTllMjA4ZGJkYTQ5NjVhMmY3ZWZhNTc4MWM1; publish_badge_show_info=%220%2C0%2C0%2C1709901652246%22; pwa2=%220%7C0%7C3%7C0%22; passport_fe_beating_status=true; download_guide=%223%2F20240308%2F1%22; dy_swidth=1707; dy_sheight=1067; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.6%7D; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; strategyABtestKey=%221710088215.328%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; SEARCH_RESULT_LIST_TYPE=%22single%22; __ac_signature=_02B4Z6wo00f012mOjLAAAIDAwvZnyZEI4i9progAAL-ZqX8Ftal8dn6vXv9gtZFfjplemXyVOJd5V9HZXIAB6I21A4L56Cl6IsYwIoxsZmqlvNryXfvhHNXJ8mkELOvSI9qNiDClNDRQFmZtfb; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQVVpV0NYMWovQnpxUUdIQVUzUkYvMk1iU2xrNUxvcERFdEh0SThCT202YXpZREovOWlPMEZjeFFNbGVFc2JsbzZDM2JWV01wS3dHbnl6a3ZHNGlBcGs9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA57y5xvj41STKvKOQv9rm7BV4ov4y7q8oSKNTp0rHFkSSim-BPVD3KKrOzvD6jIfm%2F1710172800000%2F0%2F0%2F1710132629018%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA57y5xvj41STKvKOQv9rm7BV4ov4y7q8oSKNTp0rHFkSSim-BPVD3KKrOzvD6jIfm%2F1710172800000%2F0%2F0%2F1710133229019%22; tt_scid=0JStIf6N55SQrYLbPpcaq4VfHQfQg3mX6D85DFrCGxQ1idRiNDKiuMMpTJSITGoNb9eb; odin_tt=52a28d11495bf3b983724265073ed7d7322821d81c9b12cfe1943b0cd44915359e9260312d9c5e08ce0befae51f5d07adf9d59ff8d3c416700b10d4eb12c93de; msToken=tHtzCi6C8fk_TCOLbKC3fmrI5tekoQTCsmnFt0ke90nO9rbpUzvkwDy8hOz-V7lHOZTgeQfOlYPYjFf1YsdHw6ZOTztYQpZPaJEaMbTCtCpns6r9my8Zj5Tail56-3-H; msToken=QrB7JuBlGxoYxLTHULwRARSmRiAhAFZUdow0ciOBCRtMecFFdypcARxmCAg45HLlQ28Nx_8UBbmlIwAqj6qHkgfhCChUloVY1g3kDQteTZFMGaGiqjVqNGxqCH0kdIt0; IsDouyinActive=false",
        }

        self.params = {
            "webid": 7297115571598427684,
        }
        self.msToken = "KFKtLeHzRI-pmMQLaFW0JSuKdwzQadX9gesYla0SRRsHVsiWX9gyt_cbyznz6s4KysGL5U9JD19xOdVayM-2DajhRwyoJIHXZIF04X1rgh980LoC6q1h1OB_N_XSEiGC"

    def get_ms_token(self, randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def FindSoup(self):
        for i in tqdm(range(1), desc="数据爬取", unit="条"):
            res = rq.get(self.SeemFlower, headers=self.headers_douyin, params=self.params)

            if re.match(r'^2\d{2}$', str(res.status_code)):
                print("接入成功！")
            else:
                print(f"响应码：{res.status_code}，\n接入失败！")
                break

            Soup = bs(res.text, 'lxml')
            print(Soup)

            Title_seemnum = Soup.find('span', class_="yvQVx0SM")
            print(Title_seemnum.text)

            Topic = Soup.find('div', class_="tY125K59 KRhadFw3").find('h1', class_="pofH9bi9")

            print(Topic)


class HuiTun:

    def __init__(self):
        self.date_val = []
        self.date = None
        logging.basicConfig(level=logging.INFO)
        self.member = ["白鲨嘉尔（尊师阿肯）", "CF西西妹妹", "CF白鲨柠夏", "CF白鲨乔艺", "白鲨肖奇伦(世界冠军）", 'cf.solo（世界冠军）', 'CF可为', '鲨鱼biu', 'CFM战舞', '李白白']
        self.uuid = {"白鲨嘉尔（尊师阿肯）": "93799493572",
                     "CF西西妹妹": "2826191940619754",
                     "CF白鲨柠夏": "52632783749",
                     "CF白鲨乔艺": "4163208336904988",
                     "白鲨肖奇伦(世界冠军）": "2950694835061771",
                     "cf.solo（世界冠军）": "78294392283",
                     "CF可为": "65625395958",
                     "鲨鱼biu": "6600022542",
                     "CFM战舞": "70208951769",
                     "李白白": "94475040756", }
        self.room = {}
        self.startLive = []
        self.roomId = []
        self.file_list = []
        self.csv_list = []
        self.date_dict = {}
        # self.huitun_rooms = f"https://dyapi.huitun.com/live/v2/record?_t=1710149400712&from=1&time=&has=&keyword=&mod=DESC&sort=&start={formatted_time[0]}-{time_turn[formatted_time[1]]}-{formatted_time[2]}&end={formatted_time[0]}-{formatted_time[1]}-{formatted_time[2]}&filterMap=&uid={self.uuid['李白白']}&example="

        # self.huitun_url = f"https://dyapi.huitun.com/live/roomInfo?_t=1710163257869&roomId=7344723571312659250&uid={self.uuid['李白白']}&example=false"

        self.headers_huitun = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
            'Cookie': "__root_domain_v=.huitun.com; _qddaz=QD.565509897799709; SESSION=Yzk0NDcwNTQtZTNmYS00YjdkLWI3YzYtNTgyMDczZWI3MGMz",
        }

    def huitun_room(self):
        for name in tqdm(self.member, desc="直播房间列表", unit="unit"):
            time.sleep(random.randint(5, 10))
            res = rq.get(f"https://dyapi.huitun.com/live/v2/record?_t=1710149400712&from=1&time=&has=&keyword=&mod=DESC&sort=&start={formatted_time[0]}-{time_turn[formatted_time[1]]}-{formatted_time[2]}&end={formatted_time[0]}-{formatted_time[1]}-{formatted_time[2]}&filterMap=&uid={self.uuid[name]}&example=", headers=self.headers_huitun)

            if re.match(r'^2\d{2}$', str(res.status_code)):
                print('\n')
                logging.info("房间号接入成功！")

                if not os.path.exists('./rooms/'):
                    os.makedirs('./rooms/')

                with open(f'./rooms/{name}_room.json', 'w', encoding='utf-8') as file:
                    json.dump(res.json(), file, ensure_ascii=False, indent=4)

            else:
                logging.error(f"响应码：{res.status_code}，接入失败！")
                break



    def roomZip(self):
        for name in self.member:
            self.roomId.clear()
            self.startLive.clear()
            try:
                with open(f'./rooms/{name}_room.json', 'r', encoding="utf-8") as file:
                    self.json_data = json.load(file)
            except Exception as f:
                logging.error(f'错误信息1：{f}')
                return 0

            if self.json_data['message'] == "账号已在别处登录，继续使用请重新登录！":
                logging.error("\n账号已在别处登录，继续使用请重新登录！\n")
                break

            # try:
            for i in self.json_data['data']:
                self.roomId.append(i['roomId'])
                data = (i['startLive'].split(" "))[0]
                self.date_val.clear()
                self.date_val = ((i['startLive'].split(" "))[1]).split(':')
                self.date = f"{self.date_val[0]}_{self.date_val[1]}"
                if name in self.date_dict:
                    self.date_dict[name].append(self.date)
                else:
                    self.date_dict[name] = [self.date]
                self.startLive.append(data)

            # except Exception as f:
            #     logging.error(f'错误信息2：{f}')
            #     pass

            # print(f'李白白：roomId, {self.roomId}, \nstartLive, {self.startLive}')

            # room = dict(zip(self.startLive, self.roomId))
            room = {}

            for date, value in zip(self.startLive, self.roomId):
                if date in room:
                    room[date].append(value)
                else:
                    room[date] = [value]
            # print(room)

            for day in tqdm(list(set(self.startLive)), desc="数据爬取", unit="条"):
                result = compare_with_yesterday(day)
                # print(self.date_dict[name][id])

                if result:
                    for id, times in enumerate(room[day]):
                        self.huitun_url = f"https://dyapi.huitun.com/live/roomInfo?_t=1710163257869&roomId={times}&uid={self.uuid[name]}&example=false"
                        if not os.path.exists(f'./members/{name}'):
                            os.makedirs(f'./members/{name}')
                        res = rq.get(self.huitun_url, headers=self.headers_huitun)

                        if re.match(r'^2\d{2}$', str(res.status_code)):
                            logging.info(f"{name}直播信息接入成功！")

                            # day_list = day.split('/')
                            # day_new = f"{day}"


                            with open(f'./members/{name}/{id}.json', 'w', encoding='utf-8') as file:
                                json.dump(res.json(), file, ensure_ascii=False, indent=4)

                            time.sleep(random.randint(5, 10))

                        else:
                            logging.error(f"响应码：{res.status_code}，接入失败！")
                            break




                else:
                    logging.warning(f"{name}昨日“{get_yesterday()}”与“{day}”不匹配，拒绝爬取。")


    def extract_json(self):
        # if self.json_data['message'] == "账号已在别处登录，继续使用请重新登录！":
        #     logging.error("\n账号已在别处登录，继续使用请重新登录！\n")
        #     return 0

        for name in self.member:
            self.file_list.clear()

            for root, dirs, files in os.walk(f'./members/{name}/'):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    self.file_list.append(file_path)

            for file in self.file_list:
                with open(file, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)

                # try:
                item = json_data['data']
                name = item["nickName"]
                startLiveTime = item["startLiveTime"]
                endLiveTime = item["endLiveTime"]
                liveDuration = item["liveDuration"]
                avgOnline = item["avgOnline"]
                maxUserNum = item["maxUserNum"]
                watchTimes = item["watchTimes"]
                title = item["title"]
                linetime = f"{startLiveTime}\n~\n{endLiveTime}"
                self.csv_list.append([name, linetime, liveDuration, avgOnline, maxUserNum, watchTimes, title])
            # print(self.csv_list)



            # except Exception as f:
            #     logging.error(f'错误信息3：{f}')
            #     pass
        # print(self.csv_list)
        self.write_csv(self.csv_list)

    def write_csv(self, all):
        df = pd.DataFrame(all)
        df.to_csv('./members.csv', index=False, header=['主播名称', '开播时间', '直播时长', '直播平均在线人数', '直播在线人数峰值', '观看总人次', '直播标题'], mode="w+")
        print('写入成功!')


if __name__ == '__main__':
    topic = HuiTun()
    topic.huitun_room()
    topic.roomZip()
    topic.extract_json()
