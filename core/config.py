import logging

l_logger = logging.getLogger('light_logger')
l_logger.setLevel(logging.INFO)

light_handler = logging.FileHandler('logs/light.log')
light_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
light_handler.setFormatter(formatter)

l_logger.addHandler(light_handler)


w_logger = logging.getLogger('water_logger')
w_logger.setLevel(logging.INFO)

water_handler = logging.FileHandler('logs/water.log')
water_handler.setLevel(logging.INFO)

water_handler.setFormatter(formatter)

w_logger.addHandler(water_handler)


s_logger = logging.getLogger('server_logger')
s_logger.setLevel(logging.INFO)

server_handler = logging.FileHandler('logs/server.log')
server_handler.setLevel(logging.INFO)

server_handler.setFormatter(formatter)

s_logger.addHandler(server_handler)
