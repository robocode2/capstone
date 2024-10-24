from datetime import datetime, timedelta, timezone
import scrapy
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import fahrenheit_to_celsius, inch_to_mm, load_locations
import json

class MeteoblueSpider(scrapy.Spider):
    name = "MeteoBlue"
    locations = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("MeteoBlue")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url')
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
        current_date = datetime.now(timezone.utc)

        
        rows = response.css('table.forecast-table tr')
        
        columns = [[] for _ in range(14)]

        for row in rows[1:5] + rows[13:14]:  # rows 2-5 and row 14 are irrelevant
            data = row.css('td::text').getall()
            if data:
                for i in range(14):
                    columns[i].append(data[i].strip() if i < len(data) else '')

        weather_conditions = [[] for _ in range(14)]
        for row in rows:
            imgs = row.xpath('td/img')
            for i, img in enumerate(imgs):
                title = img.xpath('@title').get()
                weather_conditions[i].append(title.strip() if title else '')

        precipitation_data_str = response.xpath('//*[@id="canvas_14_days_forecast_precipitations"]/@data-precipitation').get()

        try:
            precipitation_data = json.loads(precipitation_data_str) if precipitation_data_str else [None] * 14
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse precipitation data: {precipitation_data_str}")
            precipitation_data = [None] * 14


        temp_unit = response.css('.h1.current-temp::text').re_first(r'°[CF]')
        for i in range(14):
            temp_high = columns[i][2].replace('°', '') if len(columns[i]) > 2 else None
            temp_low = columns[i][3].replace('°', '') if len(columns[i]) > 3 else None
            precipitation_amount=precipitation_data[i] if i < len(precipitation_data) else None

            if temp_unit == '°F':
                temp_high = fahrenheit_to_celsius(temp_high)
                temp_low = fahrenheit_to_celsius(temp_low)
                precipitation_amount= inch_to_mm(float(precipitation_amount))

                
            item = DayForecastItem(
                country=country,
                state=state,
                city=city,
                weather_condition=weather_conditions[i][0] if i < len(weather_conditions) else None,                
                temp_high=temp_high,
                temp_low=temp_low,
                precipitation_chance=columns[i][4].replace('%', '') if len(columns[i]) > 4 else None,
                precipitation_amount=float(precipitation_amount),
                wind_speed=None,
                humidity= None,
                source='MeteoBlue',
                collection_date= current_date,
                forecasted_day= current_date + timedelta(days=i)
            )
            yield item

        
