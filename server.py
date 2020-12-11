from flask import (
    Flask,
    request,
    make_response,
    Response,
    stream_with_context
)
import os
import requests
import telebot
from telebot import types
import threading
from config import *
from DbHandler import DbHandler
from security import *
import tg_client

server = Flask(__name__)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/d")
def serve_file():
    file_hash = request.args.get('id', default=0, type=str)
    link = db.select('links', 'hash = \'{hash}\''. format(hash=file_hash))

    if (link is False or len(link) == 0):
        return "File not found"
    else:
        link = link[0]

    stream = stream_with_context(tg_client.get_file_stream(link['message_id']))
    return Response(stream,
                    headers={
                        'Content-Type': 'application/octet-stream',
                        'Content-Length': link['file_size'],
                        'Content-Disposition': 'attachment; filename="{file_name}"'.format(file_name=link['file_name'])
                    })


@server.route("/")
def webhook():
    webhook = bot.get_webhook_info()
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + "/bot")
    return "!", 200


if (POLLING):
    bot.remove_webhook()
    thread = threading.Thread(target=bot.polling)
    thread.daemon = True
    thread.start()


server.run(host="0.0.0.0", port=5000)
