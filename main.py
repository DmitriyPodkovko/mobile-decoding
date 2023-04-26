import csv
import json
from sys import exit
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import parse
from phonenumbers import geocoder
from phonenumbers import timezone
from phonenumbers import carrier


def ru_num(phone):
    # if phone[0:1] == "+" and phone[2:3] == "9":
    if phone[0:1] == "7" and phone[1:2] == "9":
        # num_one = phone[2:5]
        num_one = phone[1:4]
        # two_num = phone[5:]
        two_num = phone[4:]
        return csv_read(num_one, two_num, phone)
    # elif phone[0:1] == "7" and phone[1:2] == "7":
    #     print(f'{phone};Unknown region')
    #     return f'{phone};Unknown region\n'
    # elif phone[0:1] == "8" and phone[1:2] == "9":
    #     num_one = phone[1:4]
    #     two_num = phone[4:]
    #     csv_read(num_one, two_num, phone)
    else:
        print(f'{phone};Unknown region')
        return f'{phone};Unknown region\n'
        # phnum_parse(phone)


def csv_read(zone, number, phone):
    with open('zone.json', 'r', encoding='utf-8') as f:
        zone_t = json.load(f)
    with open("DEF-9xx.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            if i != 0:
                if line[0].split(";")[0] == zone and \
                        [k for k in range(int(line[0].split(";")[1]),
                                          int(line[0].split(";")[2]))
                         if int(number) == k]:
                    prov = line[0].split(";")[4]
                    region = line[0].split(";")[5].strip()
                    try:
                        for z in zone_t:
                            if region in z:
                                time_zone = z[region]
                        print(f'{phone};{region};{time_zone};{prov}')
                        return f'{phone};{region};{time_zone};{prov}\n'
                    except KeyError:
                        print(f'\n[+] Number information: {phone}:\n    '
                              f'- Provider (ОпСоС): {prov}\n    '
                              f'- Region: {region}')
                        return (f'\n[+] Number information: {phone}:\n    '
                                f'- Provider (ОпСоС): {prov}\n    '
                                f'- Region: {region}')


def phnum_parse(phone):
    try:
        ph_parse = parse(phone)
    except NumberParseException:
        print('[-] Wrong region')
        return
    ph_timezone = timezone.time_zones_for_number(ph_parse)
    ph_region = geocoder.description_for_number(ph_parse, 'ru')
    ph_prov = carrier.name_for_number(ph_parse, 'ru')
    if ph_prov == "":
        ph_prov = "Uncnown"
    elif ph_region == "":
        ph_region = "Uncnown"
    elif ph_timezone[0] == "":
        print(f'\n[+] Number information: {phone}:\n    '
              f'- Provider (ОпСоС): {ph_prov}\n    '
              f'- Region: {ph_region}\n    - Timezone: Uncnown')
        return
    print(f'\n[+] Number information: {phone}:\n    '
          f'- Provider (ОпСоС): {ph_prov}\n    '
          f'- Region: {ph_region}\n    - Timezone: {ph_timezone[0]}')


def main():
    with open("example_result.txt", 'w', encoding='utf-8-sig') as outfile, \
            open("example.txt", 'r', encoding='utf-8') as infile:
        for line in infile:
            phone = line.replace("-", "").replace("(", "") \
                        .replace(")", "").replace(" ", "") \
                        .replace("\n", "")
            if phone[0:1] == "7":
                outfile.write(ru_num(phone))
            else:
                exit('END!!!')
                # phnum_parse(phone)

        # print('\n* INFORMATION ABOUT THE PHONE NUMBER. REGION, OPERATOR AND TIME ZONE *\n')
        # phone = input('Enter number >>> ').replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        # if phone[0:1] == "7":
        # if phone[1:2] == "7":
        #     russia_num(phone)
        # else:
        #     # phnum_parse(phone)
        #     # elif phone[0:1] == "8":
        #     #     russia_num(phone)
        #     # else:
        #     phnum_parse(phone)


if __name__ == "__main__":
    main()
