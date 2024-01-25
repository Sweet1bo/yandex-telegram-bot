import math
import re
import sys
import json

from database.models.Driver import Driver
from database.models.Park import Park
from database.models.YandexSession import YandexSession
from repositories.DriverRepository import DriverRepository
from services.CarService import CarService
from services.DriverService import DriverService
from services.Api.YandexApiService import YandexApiService

cookie = 'yandexuid=2810398611635584074; yuidss=2810398611635584074; ymex=1950944074.yrts.1635584074#1950944074.yrtsi.1635584074; _ym_uid=1635634819248571806; is_gdpr=0; mda=0; is_gdpr_b=COaIGBC3TygC; my=YwA=; gdpr=0; i=hyg6we+f8ox1+40LTDxJx8FfnU4Q2SzdO2hdXbrarHYvU/SM0LU7WqFJN6OSoFavyGDPsRdZLmNx5v2o91G6CZYlfb0=; yandex_gid=43; yabs-frequency=/5/00010000001FcuTX/1Z49MUz5j7V_HFp___-2OK5jXW000FX48sFWZwpsQiPf_4GWsN29jnIpaatyH400/; sMLIIeQQeFnYt=1; Session_id=3:1643882260.5.0.1636200303510:t0XoWQ:a.1.2:1|444449288.0.2|1558561845.7681143.2.2:7681143|3:247547.461178.TAJZ8alRJL4K6_C6IK2bt4wfVpY; sessionid2=3:1643882260.5.0.1636200303510:t0XoWQ:a.1.2:1|444449288.0.2|1558561845.7681143.2.2:7681143|3:247547.461178.TAJZ8alRJL4K6_C6IK2bt4wfVpY; yp=1646333360.ygu.1#1651968256.szm.1%3A1920x1080%3A1920x937#1959242260.udn.cDpkcmRpc3Bvb2w%3D#1667813070.p_sw.1636277070#1643830002.nwcst.1643745000_43_1#1646333359.spcs.l#1646420843.csc.2#1644408076.dq.1#1959241446.multib.1; L=VktYeWRXZEZaYEJRQVdAW10CWFpbR3p9UCoiDAoJFSU+.1643882260.14877.376857.b990fea02651d4f8d5383ddbaa8c21dd; yandex_login=drdispool; park_id=612aadb1ef0d455d9682a77603524039; _yasc=DZ7ryxxAhStSOdno2nmnmgjtQqGb/uPfhR9tie9QakIL139iyA0efQ==; computer=1; y360w.xpnd.444449288=0; instruction=1'
yandex_api = YandexApiService(cookie, '81b8e0f16d5144938d1c7b6cf77cc27e')
car_service = CarService(cookie, '612aadb1ef0d455d9682a77603524039')

# driver = yandex.get_driver(json.dumps({'driver_id': 'bec4457b38fbdb7b133ee1b03c4129d3'}))
# car_id = driver['driver']['car']['id']
#
# print(yandex.get_driver_car(json.dumps({'car_id': car_id})))

car_id = 'd99821bdbfc4505697441a005ec101b7'
#print(car_service.add_child_seat(car_id))

driver = DriverRepository.get_driver_by_id(1)
print(DriverRepository.get_driver_by_id(1))

drivers = Driver.where({'car_id': '', 'driver_id': '9006b7dd1dd1416a847f44b9b31345a3', 'park_id': 2}).get()
print(len(drivers))