from heyoo import WhatsApp
# messenger = WhatsApp('EAAJVc3j40G8BAO30KsKwZBRDifNf7I9mxfyOIy7GISIEjoF7QZCBJfPexPHGL3eRoOUvLiWInTrmMh32ZBt2GE8IJqWjMZABNSZCf0TFR3y9BBNBH1y0x1rbLNLPHslznC9ZAyZChSWKJaPcUFuzQ2Mmvm3ZAdMOOd4CwIjFMfw7IdmSaQLb5qZAZBWTyfPWuzkbvSzGwKmsLYvgZDZD',  phone_number_id='110829038490956')
# messenger.send_message('Your message ', '923462901820')
import os
import json
from heyoo import WhatsApp
from os import environ
from flask import Flask, request, make_response
from os import environ
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import logging
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://wslnapfcxanodr:a7264b32be99407001919e87affb1e06e86a4f8a844daa4eb722678aed8d4cfe@ec2-54-163-34-107.compute-1.amazonaws.com:5432/dfb4pqic2dqauj'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql+postgres://hfajwxasfwdoos:e0b6d820210e1f674fbf7ccd02a88e30009b435291c3de994365d886721f0176@ec2-3-209-39-2.compute-1.amazonaws.com:5432/d89giqj71hltdv'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db=SQLAlchemy(app)
# app = Flask(__name__)
#
# class Sender(db.Model):
#     __tablename__ = "sender"
#     id = db.Column(db.Integer, primary_key=True)
# #     # email = db.Column(db.String(120), unique=True)
#     sender_response = db.Column(db.JSON)
    # sender_name = db. Column(db.String(100), nullable = False)
    # sender_message = db.Column(db.String(1000), nullable = False)
    # sender_message_type = db.Column(db.String(1000), nullable=False)
    # sender_number = db.Column(db.String(1000), nullable=False)
    # latitude = db.Column(db.Float, index=False, unique=False)
    # longitude = db.Column(db.Float, index=False, unique=False)

    # def __init__(self, sender_response):
    #     self.sender_response = sender_response
    #     # self.sender_name = sender_name
    #     # self.sender_message = sender_message
    #     # self.sender_number = sender_number
    #     # self.latitude = latitude
    #     # self.longitude = longitude
    #     # self.sender_message_type = sender_message_type
    #
    #
#     def __repr__(self):
#         return '<E-mail %r>' % self.sender_response
messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as# #WhatsApp(token = "inpust accesstoken", phone_number_id="input phone number id") #messages are not recieved without this pattern
# #
# #
VERIFY_TOKEN = 'umer' #application secret here
#
# #to be tested in prod environment
# messenger = WhatsApp(os.getenv("heroku whatsapp token"),phone_number_id='105582068896304')
# # VERIFY_TOKEN = "heroku whatsapp token"
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.route("/webhook", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            logging.info("Verified webhook")
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        logging.error("Webhook Verification failed")
        return "Invalid verification token"

    # Handle Webhook Subscriptions
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    # pet = Sender(sender_response=data)
    # db.session.add(pet)
    # db.session.commit()
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        print(new_message)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            # pet = Sender(sender_name=name, sender_number=mobile)
            # db.session.add(pet)
            # db.session.commit()

            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message = messenger.get_message(data)
                logging.info("Message: %s", message,'mobile',mobile,'name',name)
                # pet = Sender(sender_name=name, sender_number=mobile, sender_message_type=type,sender_message=message)

                # messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_response = messenger.get_interactive_response(data)
                print('message_response',message_response)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                print('intractive_type',intractive_type,'message_id',message_id,'message_text',message_text,'mobile',mobile,'name',name)
                # logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_location = messenger.get_location(data)
                print('message_location',message_location)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                # pet = Sender(sender_name=name, sender_number=mobile, sender_message_type=type, sender_message=message)
                print('message_latitude',message_latitude,'message_longitude',message_longitude,'mobile',mobile,'name',name)
                # logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                image = messenger.get_image(data)
                print(image)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                print(f"image_url {image_url}")
                # logging.info(f"{mobile} image_url {image_url}")
                image_filename = messenger.download_media(image_url, mime_type)
                print('image_filename',image_filename,'mobile',mobile,'name',name)
                # print(f"{mobile} sent image {image_filename}")
                # logging.info('image_filename',image_filename)


            elif message_type == "video":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                print(f"{mobile} video_url {video_url}")
                # logging.info(f"{mobile} video_url {video_url}")
                video_filename = messenger.download_media(video_url, mime_type)
                print('video_filename', video_filename,'mobile',mobile,'name',namee)
                # print(f"{mobile} sent video {video_filename}")
                # logging.info('video_filename', video_filename)

            elif message_type == "audio":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                print(f" audio_url {audio_url}")
                # logging.info(f"{mobile} audio_url {audio_url}")
                audio_filename = messenger.download_media(audio_url, mime_type)
                print('audio_filename', audio_filename,'mobile',mobile,'name',name)
                # print(f" sent audio {audio_filename}")
                # logging.info('audio_filename', audio_filename)

            elif message_type == "file":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                file = messenger.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                print(f" file_url {file_url}")
                # logging.info(f"{mobile} file_url {file_url}")
                file_filename = messenger.download_media(file_url, mime_type)
                print('file_filename', file_filename,'mobile',mobile,'name',name)
                # print(f"{mobile} sent file {file_filename}")
                # logging.info('file_filename', file_filename)
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
