#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed under Apache License v2
# https://github.com/Salamdev/Quran-CommonPhrases

import mysql.connector
from tqdm import tqdm
from difflib import SequenceMatcher
import sqlite3
import apsw
from shutil import move

#####################

minimumMatchingWords = 3
maximumMatchingWords = 100  # 100 for unlimited
surahRangeToExtractSimilars = [1, 114]  # Surah Range (1 - 114) To Extract Similars From Whole Quran
mysqlconfig = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'quran'
}

#####################


def matchingsubstrings(_a, _b):
    r = {
        "isSame": False,
        "matchingBlocks": None,
        "ratio": 0.0
    }
    seqmatch = SequenceMatcher(None, _a, _b, False)
    if (len(_a) and len(_b)) > minimumMatchingWords:
        blocks = seqmatch.get_matching_blocks()
        r["matchingBlocks"] = [dict(i._asdict()) for i in blocks]
    else:
        r["matchingBlocks"] = []
    r["ratio"] = seqmatch.ratio()
    if r["ratio"] == 1.0:
        r["isSame"] = True
    else:
        r["isSame"] = False
    return r


def insert():
    for i in matchingblocks:
        lite_insertcur.execute(
            """INSERT INTO result
            (a_surah, a_ayah, a_text, b_surah, b_ayah, b_text, issame, ratio, matchingblock,a_place,b_place,length)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (surah, ayah, a[0],
             target_surah,
             target_ayah, b[0], result["isSame"], result["ratio"],
             i['text'], i['coordinate']['a']+1, i['coordinate']['b']+1, i['coordinate']['size']))
    lite_conn.commit()


ayah_conn = target_conn = mysql.connector.connect(**mysqlconfig)
ayah_cursor = ayah_conn.cursor(buffered=True)
target_cursor = target_conn.cursor(buffered=True)
apsw_conn = apsw.Connection(':memory:')
lite_conn = sqlite3.connect(str(apsw_conn))
lite_tablecur = lite_insertcur = lite_selectcur = lite_selectcur2 = lite_conn.cursor()
ayah_count = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135, 112, 78,
              118,64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29,
              18,45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56,
              40,31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8,
              3,9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]
lite_tablecur.execute(
    """create table if not exists result(id integer primary key autoincrement,a_ayah int,a_surah int,a_text text,b_ayah int,b_surah int,
    b_text text,issame boolean,matchingblock text,a_place int,b_place int,length int,ratio float)""")
lite_conn.commit()
for surah in range(surahRangeToExtractSimilars[0], surahRangeToExtractSimilars[1] + 1):
    for ayah in range(1, ayah_count[surah - 1] + 1):
        ayah_cursor.execute(
            "SELECT text FROM quran.quran_text where sura=" + str(surah) + " and aya=" + str(ayah) + ";")
        a = ayah_cursor.fetchone()
        a_words = a[0].split()
        pb = tqdm(ascii=True, desc="surah " + str(surah) + " | ayah " + str(ayah) + " ", unit=' target_surah',
                  total=114)
        for target_surah in range(1, 115):
            for target_ayah in range(1, ayah_count[target_surah - 1] + 1):
                if surah != target_surah or (surah == target_surah and ayah != target_ayah):
                    target_cursor.execute(
                        "SELECT text FROM quran.quran_text where sura=" + str(target_surah) + " and aya=" + str(
                            target_ayah) + ";")
                    b = target_cursor.fetchone()
                    result = matchingsubstrings(a_words, b[0].split())
                    matchingblocks = [
                        {
                            "text": ' '.join(a_words[i["a"]:i["a"] + i["size"]]),
                            "coordinate": i
                        }
                        for i in result["matchingBlocks"] if maximumMatchingWords >= i["size"] >= minimumMatchingWords]
                    if len(matchingblocks) > 0:
                        insert()
            pb.update(1)
        pb.close()

conn = apsw.Connection('result.db')
with conn.backup("main", apsw_conn, "main") as backup:
    while not backup.done:
        backup.step(100)
move(str(apsw_conn), 'result.db')
