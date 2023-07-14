import time, json, base64, random, string, logging, random,json, gevent.monkey
from mylib import *
from Ggrequest import *
import xml.etree.ElementTree as ET
from locust import *
from locust.env import Environment

gevent.monkey.patch_all()

jsonstr = '{"cid": "cid_BzanIxIY", "req_id": "req_OssjLsTY", "cnt_id": "cnt_CmpgXijc", "lang": "ja-JP", "nw_id": "hw_nRWEXUCl", "pub_id": "pub_RQBbzrAB", "more_info": false, "ad_units": [{"no": 1, "hrc": "hrc_FTdCiVYc", "code": "z_v_r_b_2", "dy_id": 5, "sizes": [{"w": 300, "h": 250}]}, {"no": 2, "hrc": "hrc_YBaLEncJ", "code": "z_a_c_2", "dy_id": 8, "sizes": [{"w": 900, "h": 112}]}, {"no": 3, "hrc": "hrc_bsJZrNVa", "code": "shorts", "dy_id": 5, "sizes": [{"w": 200, "h": 800}]}, {"no": 4, "hrc": "hrc_UthSHBPw", "code": "shorts", "dy_id": 6, "sizes": [{"w": 200, "h": 800}]}]}'

class Single_GetOneV2(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(5, 10)
    probability = 0.6
    @task
    def get_onev2(self):
            with self.client.get(url="/getonev2", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang()}, catch_response=True, name="Single_GetOneV2") as resp:
                code = resp.status_code
                if code == 200:
                    json_data = json.loads(resp.text)
                    if json_data["data"]["is_404"] == True:
                        resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
                    else:
                        xml = base64.b64decode(json_data["data"]["xml"])
                        self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
            

class Single_Post_GetGGV2(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(5, 10)
    @task
    def get_ggv2(self):
        json_body = generate_random_ggrequest_body()
        resp = self.client.post(url="http://loadtest.dev.ganjing.world/v1/cdkapi/getggv2", json = json_body, name="Single_Post_GetGGV2")
        if resp.status_code == 200:
            json_var = resp.json()

class GetOneV2_With_Callback(HttpUser):
    host = "https://loadtest.dev.ganjing.world/v1/cdkapi"
    wait_time = between(5, 10)
    @task
    def get_onev2(self):
        probability = 0.6
        with self.client.get(url="/getonev2", params={"cid":random_text(), "cnt_id":random_text(), "req_id":random_text(), "lang":random_lang()}, name="Single_GetOneV2",catch_response=True) as resp:
            code = resp.status_code
            if code == 200:
                json_data = json.loads(resp.text)
                if json_data["data"]["is_404"] == False:
                    xml = base64.b64decode(json_data["data"]["xml"])
                    self.Impression = ET.fromstring(xml).findall(".//Impression")[1].text
                    self.Skip = ET.fromstring(xml).findall(".//*[@event='skip']")[1].text
                    self.Progress = ET.fromstring(xml).findall(".//*[@event='progress']")[1].text
                    self.FirstQuartile = ET.fromstring(xml).findall(".//*[@event='firstQuartile']")[1].text
                    self.Midpoint = ET.fromstring(xml).findall(".//*[@event='midpoint']")[1].text
                    self.ThirdQuartile = ET.fromstring(xml).findall(".//*[@event='thirdQuartile']")[1].text
                    self.Complete = ET.fromstring(xml).findall(".//*[@event='complete']")[1].text
                    self.ClickTracking = ET.fromstring(xml).findall(".//ClickTracking")[0].text
                    if(decision(probability)):
                        self.client.get(url=self.Impression, name="Impression")
                        if(decision(probability)):
                            self.client.get(url=self.Skip, name="Skip")
                            if(decision(probability)):
                                self.client.get(url=self.Progress, name="Progress")
                                if(decision(probability)):
                                    self.client.get(url=self.FirstQuartile, name="FirstQuartile")
                                    if(decision(probability)):
                                        self.client.get(url=self.Midpoint, name="Midpoint")
                                        if(decision(probability)):
                                            self.client.get(url=self.ThirdQuartile, name="ThirdQuartile")
                                            if(decision(probability)):
                                                self.client.get(url=self.Complete, name="ThirdQuartile")
                                                if(decision(probability)):
                                                    self.client.get(url=self.Complete, name="Complete")
                                                    self.client.get(url=self.ClickTracking, name="ClickTracking")
                else:
                    resp.failure("is_404: True. NoAdsReason: " + json_data["data"]["no_ad_reason"])
 


if __name__ == "__main__":
    my_env = Environment(user_classes=[Single_GetOneV2])
    Single_GetOneV2(my_env).run()
