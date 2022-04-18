# Inline bot

## Install

Install package

```bash
cd inline-bot
pipenv install
```

Put your personal cookie into `.env`

```bash
cp .env.example .env
```


### Run

```bash
pipenv run python inline.py
```


### ENV

#### example

```dotenv
INLINE_URL=https://inline.app/booking/-M4Mo8Y0HRth76gEAC0B:inline-live-1/-M4Mo8rzzOHzEDFpHkad
DESIRE_DATE=2022-04-20
# 0: Mon, 1: Tue, 2: Wed, 3: Thu, 4: Fri, 5: Sat, 6: Sun
# support format: '5,6'
DESIRE_WEEKDAY=5,6
DESIRE_TIME=12:00
# strict
STRICT=true
SLEEP=1
GROUP_SIZE=2
# gender 0=male 1=female
GENDER=0
NAME=李白
PHONE=+886912345678
EMAIL=XXXXX@gmail.com
```

#### desire condition

`DESIRE_DATE`: optional, the date you want to book

`DESIRE_WEEKDAY`: optional, the weekday you want to book (0: Mon, 1: Tue, 2: Wed, 3: Thu, 4: Fri, 5: Sat, 6: Sun)

`DESIRE_TIME`: optional, the time you want to book

For example:
1. If you want to book weekend afternoon, you can set `DESIRE_WEEKDAY=5,6` `DESIRE_TIME=12:00`
2. If you want to book particular evening, you can set `DESIRE_DATE=2022-10-10` `DESIRE_TIME=18:00`


#### strict mode

When you set `STRICT=true` which means we will keep scanning seats until it matches on your desire condition.


