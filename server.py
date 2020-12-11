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



server.run(host="0.0.0.0", port=5000)
