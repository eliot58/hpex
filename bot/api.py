import aiohttp
from datetime import datetime


base_url = "http://127.0.0.1:8000"

async def get_texts():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/text/") as response:
            return await response.json()     
        

async def get_agent_by_id(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/agent/?id={id}") as response:
            return await response.json()
        
async def get_agent_by_code(code):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/agent/?code={code}") as response:
            return await response.json()
        
async def get_client(code):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/client/?code={code}") as response:
            return await response.json()
        

async def create_agent(id, full_name, date_of_birth, city, transport, username, phone, code, qr_code):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        if qr_code:
            data.add_field('qr_code', open(qr_code, 'rb'))

        input_date = datetime.strptime(date_of_birth, '%d.%m.%Y')

        output_date_str = input_date.strftime('%Y-%m-%d')

        data.add_field("csrfmiddlewaretoken", "Ogq0qpO5itPQteWTuCMNMjK4du9S7ZvTGjJ3RPkmqXXzNtBfxm3aEd165vQGRtjT")
        data.add_field('fullName', full_name)
        data.add_field('tg_id', str(id))
        data.add_field('date_of_birth', output_date_str)
        data.add_field('city', city)
        data.add_field('transport', transport)
        data.add_field('username', username if username else phone)
        data.add_field('phone', phone)
        data.add_field('code', code)

        async with session.post(f"{base_url}/agent/", data=data) as response:
            return await response.json()

        

async def create_client(user_id, full_name, code, city, phone):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('fullName', full_name)
        data.add_field('user', str(user_id))
        data.add_field('city', city)
        data.add_field('phone', phone)
        data.add_field('code', code)

        async with session.post(f"{base_url}/client/", data=data) as response:
            return await response.json()
        

async def create_track(table):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file', open(table, 'rb'))

        async with session.post(f"{base_url}/track/", data=data) as response:
            return await response.json()
        

async def create_ransom(table):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file', open(table, 'rb'))
        async with session.post(f"{base_url}/ransom/", data=data) as response:
            return await response.json()