import traceback

from repositories.YandexSessionRepository import YandexSessionRepository
from services.DriverService import DriverService

sessions = YandexSessionRepository.all()

for session in sessions:
    try:
        print('Обновляем водителей ' + session.park.name)
        driverService = DriverService(session.session, session.park.park_id, '')
        driverService.load_drivers_to_db(session.park.id)
    except Exception as e:
        traceback.print_exc()