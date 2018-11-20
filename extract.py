# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import unicodedata

from numpy.distutils import line_endings
from scipy.constants import year

import roman
import re


class Document():
    dict_id = {}

    def __init__(self, id):
        self.id = id
        self.myid = None
        if self.id not in self.dict_id:
            self.dict_id[self.id] = len(self.dict_id) + 1

        self.myid = self.dict_id[self.id]
        self.name = ''
        self.document_number = ''
        self.issue_date = ''
        self.effect_date = ''
        self.issue_place = ''
        self.type = ''
        self.signer = ''
        self.scope = ''
        self.speciality = ''
        self.field = ''
        self.effect = ''
        self.pursuant = []
        self.proposed = ''
        self.article = []
        self.clause = []
        self.file = []
        self.van_ban_duoc_huong_dan = []
        self.van_ban_hien_thoi = []
        self.van_ban_huong_dan = []
        self.van_ban_het_hieu_luc = []
        self.van_ban_can_cu = []
        self.van_ban_quy_dinh_het_hieu_luc = []
        self.van_ban_bi_het_hieu_luc_mot_phan = []
        self.van_ban_dan_chieu = []
        self.van_ban_quy_dinh_het_hieu_luc_mot_phan = []
        self.van_ban_bi_dinh_chi = []
        self.van_ban_lien_quan_khac = []
        self.van_ban_dinh_chi = []
        self.van_ban_bi_dinh_chi_mot_phan = []
        self.van_ban_dinh_chi_mot_phan = []
        self.van_ban_duoc_bo_sung = []
        self.van_ban_bo_sung = []
        self.van_ban_duoc_sua_doi = []
        self.van_ban_sua_doi = []
        self.json = {}
        self.crawl_text()
        self.vb_lien_quan = []
        self.nam_van_ban = []

    def crawl_text(self):
        try:
            r = requests.get('http://vbpl.vn/tw/Pages/vbpq-toanvan.aspx?dvid=13&ItemID=' + self.id)

        except requests.exceptions.ConnectionError:
            with open('log/debug.log', 'a') as f:
                f.write('content: ' + self.id + '\n')
            return

        if not r.url.startswith('http://vbpl.vn/tw/Pages/vbpq-toanvan.aspx?dvid=13&ItemID='):
            with open('log/debug.log', 'a') as f:
                f.write('content: ' + self.id + '\n')

        text = BeautifulSoup(r.content, 'lxml')
        contents = text.select('.toanvancontent p')
        contents_size = len(contents)
        index = 0
        num_article = 0
        is_article = False
        is_clause = False
        num_clause = 0
        tmp_clause = []
        sub_clause = ''
        while index < contents_size:
            line = contents[index]
            line.text.strip()
            line_cleaned = line.text.strip()
            linee = ''.join(line_cleaned).encode('utf8')
            vblq = []
            if line_cleaned.startswith(u"Căn cứ"):
                self.pursuant.append(line_cleaned)
                tmp = ''.join(line_cleaned)

                searchObj1 = re.search(ur'(.*)Căn cứ (.*?) ngày.*', tmp, re.MULTILINE|re.IGNORECASE|re.UNICODE)
                searchObj2 = re.search(ur'(.*)Căn cứ (.*?) năm.*', tmp, re.MULTILINE|re.IGNORECASE|re.UNICODE)
                # searchObj3 = re.search()
                year = re.search('[0-9][0-9][0-9][0-9]', tmp, re.I|re.M|re.U)
                if(searchObj1):
                    print searchObj1.group(2)
                    if(year):
                        print year.group()
                    else:
                        print 'none_year'
                    temp =searchObj1.group(2)
                    # temp = unicodedata.normalize('NFKD', temp).encode('ascii', 'ignore')
                    # print temp
                    # vblq.append(temp)

                    # print type(searchObj.group(2))
                    # print searchObj.group(3)
                    # self.vb_lien_quan.append(''.join(searchObj.group(2)))
                    # self.vb_lien_quan.append(searchObj.group(2))
                elif(searchObj2):
                    print searchObj2.group(2)
                    if (year):
                        print year.group()
                    temp = searchObj2.group(2)
                    # temp = unicodedata.normalize('NFKD', temp).encode('ascii', 'ignore')
                    print temp
                    vblq.append(temp)

                # else:
                    # print 'noooooo'
                # self.pursuant = self.pursuant.encode('utf8')
                # [x.encode('utf-8') for x in self.pursuant]
                # print self.pursuant

            index += 1
        self.vb_lien_quan = vblq
        # print vblq
        str1 = ''.join(self.pursuant)
        str1 = str1.encode('utf8')
        # print str1

        # tmp_clause.append(sub_clause)
        # self.clause.append(tmp_clause)
        # if not self.article:
        #     sub_clause = ''
        #     for line in contents:
        #         if not line.text.strip().startswith(u'Căn cứ') and not line.text.strip().startswith(u'Theo đề nghị'):
        #             sub_clause = sub_clause + line.text.strip() + '\n'
        #     self.clause.append([sub_clause])
        #     self.article.append(self.name)


    def build_json(self):
        json_article = []
        for i, art in enumerate(self.article):
            json_article.append({str(i+1): {"tieu_de": art, "cac_khoan": self.clause[i]}})

        self.json = {
            "0": {"ma_so_van_ban": self.myid},
            "1": {"so_hieu": self.document_number},
            "2": {"ten_van_ban": self.name},
            "3": {"loai_van_ban": self.type},
            "4": {"noi_ban_hanh": self.issue_place},
            "5": {"nguoi_ky": self.signer},
            "6": {"ngay_ban_hanh": self.issue_date},
            "7": {"ngay_hieu_luc": self.effect_date},
            "8": {"file": {"link": self.file, "path": ""}},
            "9": {"can_cu": self.pursuant},
            "10": {"ben_de_nghi": self.proposed},
            "11": {"nganh": self.speciality},
            "12": {"linh_vuc": self.field},
            "13": {"pham_vi": self.scope},
            "14": {"cac_dieu": json_article},
            "15": {"hieu_luc": self.effect},
            "16": {"van_ban_lien_quan":
                       {"van_ban_duoc_huong_dan": self.van_ban_duoc_huong_dan,
                        "van_ban_hien_thoi": self.van_ban_hien_thoi,
                        "van_ban_huong_dan": self.van_ban_huong_dan,
                        "van_ban_het_hieu_luc": self.van_ban_het_hieu_luc,
                        "van_ban_can_cu": self.van_ban_can_cu,
                        "van_ban_quy_dinh_het_hieu_luc": self.van_ban_quy_dinh_het_hieu_luc,
                        "van_ban_bi_het_hieu_luc_mot_phan": self.van_ban_bi_het_hieu_luc_mot_phan,
                        "van_ban_dan_chieu": self.van_ban_dan_chieu,
                        "van_ban_quy_dinh_het_hieu_luc_mot_phan": self.van_ban_quy_dinh_het_hieu_luc_mot_phan,
                        "van_ban_bi_dinh_chi": self.van_ban_bi_dinh_chi,
                        "van_ban_lien_quan_khac": self.van_ban_lien_quan_khac,
                        "van_ban_dinh_chi": self.van_ban_dinh_chi,
                        "van_ban_bi_dinh_chi_mot_phan": self.van_ban_bi_dinh_chi_mot_phan,
                        "van_ban_dinh_chi_mot_phan": self.van_ban_dinh_chi_mot_phan,
                        "van_ban_duoc_bo_sung": self.van_ban_duoc_bo_sung,
                        "van_ban_bo_sung": self.van_ban_bo_sung,
                        "van_ban_duoc_sua_doi": self.van_ban_duoc_sua_doi,
                        "van_ban_sua_doi": self.van_ban_sua_doi
                        }
                   }
        }
        # print(json.dumps(d.json))
        # print self.id
        print self.json
        str111 = ''.join(self.json)
        str111 = str111.encode('utf8')
        print str111
        #
        # with open('/home/chiendb/data/vbpl/' + str(self.myid) + '.json', 'w+', encoding='utf8') as f:
        #     json.dump(self.json, f, ensure_ascii=False)
d = Document('27573')
# d = Document('126904')
# d = Document('70821')
