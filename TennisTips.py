#!/usr/bin/python

import re
import urllib2, urllib
import os, sys
from bs4 import BeautifulSoup
import csv
import sqlite3

db = sqlite3.connect(':memory:')

def init_db(cur):
    cur.execute('''CREATE TABLE tennisBet (
        Tournament TEXT,
		h2h_bet TEXT,
		Latest_Odd REAL,
        Num_Bets INTEGER,
        Coins REAL,
		H1_Bet_Rating INTEGER,
		H2_Bet_Rating INTEGER,
		diff INTEGER)''')

def populate_db(cur, tennisTxt1,tennisTxt2,tennisTxt3,tennisTxt4,tennisTxt5,tennisTxt6,tennisTxt7,tennisTxt8):
	cur.execute('''
		INSERT INTO tennisBet VALUES (?,?,?,?,?,?,?,?)''', 
		(tennisTxt1,tennisTxt2,+tennisTxt3,tennisTxt4,tennisTxt5,tennisTxt6,tennisTxt7,tennisTxt8))
		
cur = db.cursor()
init_db(cur)



##Connect to https://matchstat.com/tennis/betting-tips
#fileObj = open('table_tennis_tips',"w")
usock = urllib.urlopen("https://matchstat.com/tennis/betting-tips")
lines=usock.read()
usock.close()
fileObj = open('tennis_table.txt',"w")
fileObj.write(lines)
fileObj.close()
line_count=0

with open("tennis_table.txt", "r") as in_file:
    buf = in_file.readlines()

with open("tennis_table.txt", "w") as out_file:
    for line in buf:
        if "<tbody>" in line:
            line = line + "<tr>\n"
        if "</tr>" in line:
            line = line + "<tr>\n"
        out_file.write(line)

in_file.close()
out_file.close()


fileObj = open('tennis_table.txt',"r")

html_ = fileObj.read()
html=re.sub('&nbsp;','_',html_)
soup = BeautifulSoup(html)

data = []
table = soup.find('table', attrs={'class':'table draw-table'})
table_body = table.find('tbody')
rows = soup.table.tbody.findAll('tr')

for row in rows:

	tennisTxt2=row.findAll(href=re.compile("tennis/tournaments"))
	tennisTxt3=row.findAll(href=re.compile("tennis/h2h-odds-bets"))
	tennisTxt4=row.findAll(title=re.compile("Latest odds from"))
	tennisTxt5=row.findAll(href=re.compile("tennis/betting-odds-tips"))
	
	try:
		cols = row.find_all('td')
		print ""
		print "##############################################################################"
		print ""
		print "Tournament: " + tennisTxt2[0].text
		print "h2h bet: " + tennisTxt3[0].text
		print "Latest Odd: " + tennisTxt4[0].text.strip()
		print "Num. Bets: " + tennisTxt5[0].text
		print "Coins: " + cols[4].text
		print "H1 Bet Rating: " + cols[5].text.strip()
		print "H2 Bet Rating: " + cols[6].text.strip()
	except IndexError:
		break

	populate_db(cur,tennisTxt2[0].text,tennisTxt3[0].text,float(tennisTxt4[0].text.strip()),int(tennisTxt5[0].text),float(cols[4].text),int(cols[5].text.strip()),int(cols[6].text.strip()),abs(int(cols[5].text.strip())-int(cols[6].text.strip())))
	db.commit()

for row in cur.execute('SELECT * FROM tennisBet'):
	print row
print "******************"
for row in cur.execute('SELECT * FROM tennisBet ORDER BY Coins DESC LIMIT 1'):
	print row
print "******************"
for row in cur.execute('SELECT * FROM tennisBet ORDER BY Num_Bets DESC LIMIT 1'):
	print row
print "******************"
for row in cur.execute('SELECT * FROM tennisBet ORDER BY diff DESC LIMIT 1'):
	print row

	
sys.exit()
