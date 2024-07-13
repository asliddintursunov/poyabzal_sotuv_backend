from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
from models import Products

def products_dict(products_arr):
    products = []
    for product in products_arr:
        shoe = {
            "name": product.product_name,
            "size": product.product_size,
            "color": product.product_color,
            "sold_price": product.product_sold_price,
            "get_price": product.product_get_price,
            "sold_time": product.product_sold_time,
        }
        products.append(shoe)
    
    return products

def monthly_stats_dict(products_arr):
    savdo = 0
    foyda = 0
    chiqim = 0
    soft_foyda = 0
    
    for product in products_arr:
        savdo += product.product_sold_price
        foyda += product.product_sold_price - product.product_get_price
        
    data = {
        "savdo": savdo,
        "foyda": foyda
    }
    return data


def get_month_range(start_date, end_date):
    start_year, start_month = map(int, start_date.split('/'))
    end_year, end_month = map(int, end_date.split('/'))
    
    start = datetime(start_year, start_month, 1)
    end = datetime(end_year, end_month, 1)
    
    current = start
    result = []
    
    while current <= end:
        result.append(current.strftime('%Y/%m'))
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)
    
    return result



def stats_graph_dict(date_str, id):
    year_months = {
        "01": "yanvar",
        "02": "fevral",
        "03": "mart",
        "04": "aprel",
        "05": "may",
        "06": "iyun",
        "07": "iyul",
        "08": "avgust",
        "09": "sentyabr",
        "10": "oktyabr",
        "11": "noyabr",
        "12": "dekabr",
    }
    curr_year = int(date_str.split("-")[0])
    curr_month = int(date_str.split("-")[1])

    start_year = 0
    end_year = 0
    start_month = 0
    end_month = 0
    
    if curr_month == 1:
        start_year = curr_year - 1
        end_year = curr_year - 1
        start_month = 7
        end_month = 12
    elif curr_month <= 6 and curr_month >= 2:
        start_year = curr_year - 1
        end_year = curr_year
        start_month = curr_month + 6
        end_month = curr_month - 1
    elif curr_month >= 7 and curr_month <= 12:
        start_year = curr_year    
        end_year = curr_year
        start_month = curr_month - 6
        end_month = curr_month - 1
    
    start_date = f"{start_year}/{start_month}"
    end_date = f"{end_year}/{end_month}"
    
    months = get_month_range(start_date=start_date, end_date=end_date)
    
    result = []
    
    for date_str in months:
        date_str = date_str.replace("/", "-")
        date = datetime.strptime(date_str, "%Y-%m")
        
        start_date = date.replace(day=1)
        next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_date = next_month - timedelta(days=1)
        
        sold_products = Products.query.filter(
            Products.product_sold_time >= start_date, 
            Products.product_sold_time <= end_date, 
            Products.seller_id == id
        ).all()
        stats = monthly_stats_dict(sold_products)
        
        yr = date_str.split("/")[0]
        mnh = date_str.split("/")[1]
        stats.update({"date": f"{yr}-{year_months.get(mnh)}"})
        
        result.append(stats)

    return result