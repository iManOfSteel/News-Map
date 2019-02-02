import json
import urllib.request
import sys
import time
import pandas

#ids = [int(sys.argv[1])]

#ids = [30453222, 32182751, 34274730, 29721010, 12973535, 27126289, 39699882, 104083518, 23967044, 140865189, 3551694, 62621848, 89368740, 27566010, 117782125, 37094684, 27585111, 41682535, 67100441, 89458252, 95388014, 35929536, 29725575, 89507937, 38590870, 55471849, 29606802, 56786071, 134920716, 60460495, 7865622, 47908301, 54385637]
#ids = [30453222]
ids = [2786108, 29380417, 19003088, 39560954, 113818503, 39560083, 168019671, 29492720, 43346024, 42594637, 42535075, 42329155, 35068738, 55342106, 23558538, 41393439, 42943762, 41830487, 54576025, 61485111, 42413977, 42564785, 5608669, 43044144, 4730335, 66415024, 34461379, 24684922, 157227477, 49796420, 107816149, 34763916, 60543844, 1205247, 33412153, 33993930, 23951627, 42329298, 16308781, 71991592, 107493817, 29378821, 38801259, 124728567, 32608222, 30488458, 137330177, 139776120, 43737658, 42286071, 39560963, 23702661]

for public_id in ids:
    #public_id = int(sys.argv[1])
    print(public_id)

    number_of_news = 52 * 100
    url = 'https://api.vk.com/api.php?v=5.92&oauth=1&method=wall.get&access_token=21879b7121879b7121879b71e821eff3832218721879b717dd3b072e11a6bb90613e277&count=100'
    url += '&owner_id=-' + str(public_id)

    output_long = open('public' + str(public_id) + '.csv', 'w')
    output_short = open('public' + str(public_id) + '_short.csv', 'w')
    for i in range(number_of_news // 100):
        response = urllib.request.urlopen(url + '&offset=' + str(i * 100))
        data = json.loads(response.read().decode('utf-8'))
        #print(url + '&offset=' + str(i * 100))
        for item in data['response']['items']:
            output_long.write('№%:№%:'.join([item['text'].replace('\n', ' '),\
                                            str(pandas.to_datetime(item['date'] + 3 * 60 * 60, unit='s')),\
                                            str(public_id)]))
            output_long.write('\n')

            idx = item['text'].find('\n')
            output_short.write('№%:№%:'.join([item['text'][:idx if idx != -1 else len(item['text'])],\
                                             str(pandas.to_datetime(item['date'] + 3 * 60 * 60, unit='s')),\
                                             str(public_id)]))
            output_short.write('\n')
