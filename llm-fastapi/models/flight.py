from sqlalchemy import create_engine,text
from datetime import datetime
import urllib.parse
from core.config import config

db_host = "192.168.110.175"
db_port = "3306"
db_user = "root"
db_password = "root@JDkj!123"
db_name = "jdkj_bean_ai"

pwd = urllib.parse.quote(config.DB_PASSWORD)

DATABASE_URL=f"mysql+pymysql://{config.DB_USER}:{pwd}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
engine=create_engine(DATABASE_URL,echo=True)

def get_flights(departure_city=None, arrival_city=None, departure_date=None):
    if departure_date:
        try:
            departure_date = datetime.strptime(departure_date, '%Y年%m月%d日').strftime('%Y-%m-%d')
        except ValueError:
            return {"content": "无效的日期格式，请使用 YYYY年MM月DD日 格式"}

    query = "SELECT * FROM ass_flights WHERE status = 'Scheduled'"
    params = {}
    if departure_city:
        query += " AND departure_city = :departure_city"
        params['departure_city'] = departure_city

    if arrival_city:
        query += " AND arrival_city = :arrival_city"
        params['arrival_city'] = arrival_city

    if departure_date:
        query += " AND departure_date = :departure_date"
        params['departure_date'] = departure_date


    with engine.connect() as connection:
        result=connection.execute(text(query),params)
        flights=result.fetchall()
        if not flights:
            return {"content": "未找到该用户的预订航班"}

        # 将结果转换为字典格式，便于模型处理

        if len(flights) == 1:
            # 如果只有一个航班信息，返回单个字典
            flight = flights[0]
            return {
                "flight_id": flight.id,
                "flight_number": flight.flight_number,
                "departure_city": flight.departure_city,
                "arrival_city": flight.arrival_city,
                "departure_date": flight.departure_date.strftime('%Y-%m-%d'),
                "status": flight.status,
                "created_at": flight.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            # 如果有多个航班信息，将每个航班转换为字典并以键值对的方式组织起来
            flight_dict = {
                f"flight_{index + 1}": {
                    "flight_id": flight.id,
                    "flight_number": flight.flight_number,
                    "departure_city": flight.departure_city,
                    "arrival_city": flight.arrival_city,
                    "departure_date": flight.departure_date.strftime('%Y-%m-%d'),
                    "status": flight.status,
                    "created_at": flight.created_at.strftime('%Y-%m-%d %H:%M:%S')
                } for index, flight in enumerate(flights)
            }
            return flight_dict




def cancel_flights(flight_id,flights):
    update_query = text("""
                UPDATE ass_flights
                SET status = 'Cancelled'
                WHERE id = :flight_id AND status = 'Scheduled';
            """)


    with engine.connect() as connection:

        # 取消航班
        result=connection.execute(update_query, {"flight_id": flight_id})
        if result.rowcount>0:

            connection.commit()
            return {"status": "successfully cancel", "message": flights}
        else:
            return {"content": "未找到匹配的航班记录，可能已取消或ID不正确"}



def cancel_flight_by_details(departure_city, arrival_city, departure_date):


    # 使用 get_flights() 来获取符合条件的航班
    flights = get_flights(departure_city=departure_city, arrival_city=arrival_city,
                               departure_date=departure_date)

    if "content" in flights:
        return flights  # 返回查询失败的信息

    # 假设只有一个航班符合条件，或者只取消第一个匹配的航班
    if "flight_id" in flights:
        flight_id = flights['flight_id']
        result=cancel_flights(flight_id,flights)
        return result

    return {"content": "找到多个符合条件的航班，请提供更多信息以唯一确定航班"}




