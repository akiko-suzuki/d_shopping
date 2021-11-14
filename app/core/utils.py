from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string

TAX = 10


def calc_price_tax(price):
    """ 税込金額に計算して返す
    :param price: 税抜き金額
    :return: 税込の金額を返す
    """
    calc_price = int((1 + (TAX / 100)) * price)
    return calc_price


def send_mail(request, subject, message_txt, context, to_list, bcc=None):
    """ メールを送信する

    :param request:
    :param subject: 件名
    :param message_txt: 使用するtxtファイルのパス
    :param context: txtファイルに渡したいもの（context={}）
    :param to_list: 宛先のリスト
    :param bcc:
    :return:
    """
    message = render_to_string(message_txt, context, request)
    email_message = EmailMessage(
        subject=subject,  # 件名
        body=message,  # 本文
        from_email=settings.DEFAULT_FROM_EMAIL,  # 送信者
        to=to_list,  # 宛先（リスト）
        bcc=bcc
    )
    try:
        email_message.send()
        return True
    except BadHeaderError:
        HttpResponse('無効なヘッダが検出されました。')
        return False
