#!/usr/bin/env python3
import os, re, subprocess, sys
from datetime import datetime, timezone, timedelta

COURSE_NAMES = {
    "104.634": "Analysis",
    "184.686": "Datenbanksysteme",
    "185.A92": "Einführung in die Programmierung 2",
    "280.A69": "Daten- und Informatikrecht",
}
MESZ = timezone(timedelta(hours=2))
NOW = datetime.now(timezone.utc)
CUTOFF = NOW + timedelta(days=14)
KEYWORDS = ["abgabe","hochladen","assignment","fällig","upload","einreichen"]

userid = os.environ.get("TUWEL_USERID", "")
token  = os.environ.get("TUWEL_TOKEN", "")

if not userid or not token:
    print("ERROR: TUWEL_USERID or TUWEL_TOKEN environment variables not set.")
    sys.exit(1)

url = f"https://tuwel.tuwien.ac.at/calendar/export_execute.php?userid={userid}&authtoken={token}&preset_what=all&preset_time=monthnow"
result = subprocess.run(["curl","-sf",url],capture_output=True,text=True)
raw_data = result.stdout
if not raw_data:
    print(f"ERROR: Empty response from TUWEL. curl stderr: {result.stderr}")
    sys.exit(1)

raw = re.sub(r"\r?\n[ \t]","",raw_data)
events = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", raw, re.DOTALL)

def gf(ev,k):
    m=re.search(rf"^{k}[;:](.+)",ev,re.MULTILINE|re.IGNORECASE)
    return m.group(1).strip() if m else ""

course_map={}
for ev in events:
    cat=gf(ev,"CATEGORIES"); s=gf(ev,"SUMMARY")
    m=re.match(r"[\d.]+\s+(.+?)\s*\([A-Z]{2}",s)
    if m and cat and cat not in course_map: course_map[cat]=m.group(1).strip().rstrip(",\\")
    elif "AlgoDat" in cat and cat not in course_map:
        m2=re.match(r"[\d.]+\s+(.+?)\s*\(",s)
        if m2: course_map[cat]=m2.group(1).strip()

def course(cat):
    if cat in course_map: return course_map[cat]
    c=re.sub(r"-\d{4}S$","",cat); c=re.sub(r"^\d+[\d.]*-?","",c).strip("-")
    return COURSE_NAMES.get(c or cat, c or cat)

def clean(s):
    s=s.replace("\\,",",").replace("\\n"," ")
    return re.sub(r"^[\d.]+\s+.+?\s*\([^)]+\)\s*\d{4}S\s*/\s*","",s).strip()

def tuntil(diff):
    h=diff.total_seconds()/3600
    return f"{int(h)}h {int((h%1)*60)}min" if h<24 else f"{int(h//24)}d {int(h%24)}h"

def parse_dt(s):
    s=s.strip()
    if s.endswith("Z"): return datetime.strptime(s,"%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    if "T" in s: return datetime.strptime(s,"%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
    return datetime.strptime(s,"%Y%m%d").replace(tzinfo=timezone.utc)

results=[]
for ev in events:
    s=gf(ev,"SUMMARY"); cat=gf(ev,"CATEGORIES")
    raw_dt=gf(ev,"DUE") or gf(ev,"DTSTART")
    if not raw_dt: continue
    try: dt=parse_dt(raw_dt)
    except: continue
    if not (NOW<=dt<=CUTOFF): continue
    if not any(k in s.lower() for k in KEYWORDS): continue
    results.append((dt,s,cat))

results.sort(key=lambda x:x[0])

os.system("clear")

if not results:
    print("Keine Abgaben in den nächsten 14 Tagen.")
else:
    print("TUWEL Abgaben – nächste 14 Tage:\n")
    for i,(dt,s,cat) in enumerate(results,1):
        dm=dt.astimezone(MESZ); diff=dt-NOW
        print(f"  {i}. {clean(s)}")
        print(f"     Kurs:    {course(cat)}")
        print(f"     Fällig:  {dm.strftime('%d.%m.%Y %H:%M')} MESZ")
        print(f"     In:      {tuntil(diff)}")
        print()


