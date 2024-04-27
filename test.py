import os
import sqlite3

import requests
import base64

# print(requests.get("http://127.0.0.1:5000/api/categories/1").json())
database = sqlite3.connect("db/base.sqlite")

# for id, image_name in database.cursor().execute("SELECT id, image_name FROM desk"):
#     data = open(f"static/img/{image_name}.png", "rb").read()
#     database.cursor().execute(f"UPDATE desk SET binary = '{str(base64.b64encode(data))[2:-1]}' WHERE id = {id}")
# for id, image_name in database.cursor().execute("SELECT id, image_name FROM thread"):
#     data = open(f"static/img/{image_name}.png", "rb").read()
#     database.cursor().execute(f"UPDATE thread SET binary = '{str(base64.b64encode(data))[2:-1]}' WHERE id = {id}")
# database.commit()
#
# 1 / 0

for name, image_name in (
        ("Разработка программного обеспечения", "development"),
        ("Игры", "games"),
        ("Мультфильмы", "cartoons"),
        ("CGI 3D", "cgi3d"),
        ("Аниме", "anime"),
        ("Музыка", "music"),
        ("CGI 2D", "cgi2d"),
        ("Сериалы", "series"),
):
    database.cursor().execute(f"INSERT INTO desk(name, image_name) VALUES('{name}', '{image_name}')")
for desk_id, name, image_name in (
        (1, "Python", "python"),
        (1, "Unreal Engine", "unrealengine"),
        (2, "Undertale", "undertale"),
        (2, "Bendy and The Ink Machine", "bendy"),
        (3, "Стар против сил зла", "star"),
        (3, "Гравити Фолз", "gravityfalls"),
        (4, "Blender", "blender"),
        (4, "Mixer", "mixer"),
        (5, "В лес, где мерцают светлячки", "totheforest"),
        (5, "Унесенные призраками", "spiritedaway"),
        (6, "Инди-ру", "ruindie"),
        (6, "Электронная", "electronic"),
        (7, "Inkscape", "inkscape"),
        (7, "Krita", "krita"),
        (8, "Нетфликс", "netflix"),
        (8, "Дисней+", "disneyplus"),
):
    database.cursor().execute(f"INSERT INTO thread(desk_id, name, image_name) "
                              f"VALUES({desk_id}, '{name}', '{image_name}')")

for name, surname, email, password in (
        ("Мастер-пользователь", "", "master@gmail.com", "scrypt:32768:8:1$Q7G5uCDD5jLIN4Cy$3a00963d3333af39053f11fb5af"
                                                        "f8ce54367273ff879271471c539db99c87064b7fb40e46abaac44ccd386555"
                                                        "f886a0a659caa1ad5a41f90e9bb88a8a3d3484a"),
        ("Неизвестные", "", "unknown@gmail.com", "")
):
    database.cursor().execute(f"INSERT INTO user(name, surname, email, hashed_password) "
                              f"VALUES('{name}', '{surname}', '{email}', '{password}')")

for desk_id, thread_id, root, writer, text, number in (
        (1, 1, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (1, 2, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (2, 3, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (2, 4, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (3, 5, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (3, 6, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (4, 7, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (4, 8, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (5, 9, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (5, 10, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (6, 11, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (6, 12, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (7, 13, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (7, 14, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (8, 15, "NULL", 1, "Начинайте задавать вопросы здесь!", 1),
        (8, 16, "NULL", 1, "Начинайте задавать вопросы здесь!", 1)
):
    database.cursor().execute(f"INSERT INTO message(desk, thread, root, writer, text, number) "
                              f"VALUES({desk_id}, {thread_id}, {root}, {writer}, '{text}', {number})")

database.commit()
database.close()
