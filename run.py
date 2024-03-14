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
import urllib3, re, time, logging, match, shutil


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
            'Cookie': "",
        }

        self.params = {
            "webid": 7297115571598427684,
        }
        self.msToken = ""

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

        if os.path.exists('./members/'):
            shutil.rmtree('./members/')

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
