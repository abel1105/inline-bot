import json
import os
import time
from datetime import datetime

from modules.request import getHTML, getJSON, postData, postJson

API_ROOT = 'https://inline.app/api/'

WEEKDAY_MAP = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}

is_strict = os.environ['STRICT'] == 'true'
sleep = int(os.environ['SLEEP'])

url = os.environ['INLINE_URL']
if not os.environ['INLINE_URL']:
    url = input('請輸入預定位的網頁：')

group_size = int(os.environ['GROUP_SIZE'])
if not group_size:
    group_size = int(input('訂位人數：'))

desire_date = os.environ['DESIRE_DATE']
desire_time = os.environ['DESIRE_TIME']
desire_weekday = os.environ['DESIRE_WEEKDAY']
if desire_weekday:
    desire_weekday = [int(i) for i in desire_weekday.split(',')]

email = os.environ['EMAIL']
gender = int(os.environ['GENDER'])
name = os.environ['NAME']
phone = os.environ['PHONE']


def printSlot(item):
    print('{}. {} {} {}'.format(item['index'], item['date'], item['weekday_cht'], item['time']))


def printSlots(slots):
    print('============')
    for item in slots:
        printSlot(item)
    print('============')


def getCompanyIdAndBranchId():
    homepage = getHTML(url)
    unique_url = homepage.select('link')[0]['href']
    id_list = unique_url.split('booking/')[1].split('/')
    return id_list[0], id_list[1]


def getAvailableTimeSlots():
    has_slots = False
    last = 0
    while not has_slots:
        if time.time() - last < sleep:
            time.sleep(sleep)
        last = time.time()
        capacities = getJSON(API_ROOT + 'booking-capacitiesV3?companyId=' + company_id + '&branchId=' + branch_id)
        date_list = list(capacities['default'])
        slots = []
        index = 0
        for date in date_list:
            weekday = datetime.fromisoformat(date).weekday()
            weekday_cht = WEEKDAY_MAP[weekday]
            date_data = capacities['default'][date]
            if date_data['status'] == 'open':
                for date_time in date_data['times']:
                    if group_size in date_data['times'][date_time]:
                        # print('{}. {} {} {}'.format(index, date, weekday_cht, time))
                        slots.append({
                            'index': index,
                            'date': date,
                            'weekday_cht': weekday_cht,
                            'weekday': weekday,
                            'time': date_time
                        })
                        index += 1
        if len(slots):
            if is_strict:
                if hasDesireTimeSlot(slots):
                    return slots
                else:
                    print('{} 嚴格模式，目前只有以下位置，會持續檢查'.format(time.strftime("%H:%M:%S")))
                    printSlots(slots)
            else:
                has_slots = True
                return slots
        else:
            print('{} 目前沒有空位'.format(time.strftime("%H:%M:%S")))


def hasDesireTimeSlot(slots):
    for item in slots:
        if desire_date and item['date'] != desire_date:
            continue
        if desire_time and item['time'] != desire_time:
            continue
        if desire_weekday and item['weekday'] not in desire_weekday:
            continue
        return item
    return False


def getDesireTimeSlot(slots):
    item = hasDesireTimeSlot(slots)

    if item:
        print('即將預定：')
        printSlot(item)
        return item

    printSlots(slots)

    index = int(input('沒有合適的條件，請手動選擇欲訂的編號：'))
    return slots[index]


def bookDesireSlot(slot):
    booking_data = {
        'branch': branch_id,
        'company': company_id,
        'date': slot['date'],
        'email': email,
        'gender': gender,
        'groupSize': group_size,
        'kids': 0,
        'language': 'zh-tw',
        'name': name,
        'note': '',
        'numberOfKidChairs': 0,
        'numberOfKidSets': 0,
        'phone': phone,
        'purposes': [],
        'skipPhoneValidation': False,
        'time': slot['time']
    }

    result = postJson(API_ROOT + 'reservations/booking', booking_data)

    book_result = json.loads(result.text)
    print('訂位成功：', book_result['reservationLink'])


company_id, branch_id = getCompanyIdAndBranchId()

time_slots = getAvailableTimeSlots()

desire_slot = getDesireTimeSlot(time_slots)

bookDesireSlot(desire_slot)
