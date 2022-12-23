from transitions.extensions import GraphMachine
import json
from utils import send_text_message, sent_flex_message
from linebot.models import FlexSendMessage
import yfinance as yf
from datetime import datetime


user_id_buffer = {}


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_search(self, event):
        text = event.message.text
        return text.lower() == "search"

    def on_enter_search(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/search.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('Search', FlexMessage))

    def is_going_to_search_result(self, event):
        user_id_buffer[event.source.user_id] = yf.Ticker(event.message.text.lower()).info
        return True

    def on_enter_search_result(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/serach_result.json', 'r', encoding='utf-8'))

        FlexMessage["hero"]["url"] = user_id_buffer[event.source.user_id]["logo_url"]

        FlexMessage["body"]["contents"][0]["contents"][0]["text"] = user_id_buffer[event.source.user_id]["symbol"]

        FlexMessage["body"]["contents"][2]["contents"][0]["contents"][1][
            'text'] = f'{user_id_buffer[event.source.user_id]["ask"]:.2f} x {user_id_buffer[event.source.user_id]["askSize"]}'
        FlexMessage["body"]["contents"][2]["contents"][2]["contents"][1][
            'text'] = f'{user_id_buffer[event.source.user_id]["bid"]:.2f} x {user_id_buffer[event.source.user_id]["bidSize"]}'

        FlexMessage["body"]["contents"][4]["contents"][0]["contents"][1][
            'text'] = f'{user_id_buffer[event.source.user_id]["previousClose"]:.2f}'
        FlexMessage["body"]["contents"][4]["contents"][2]["contents"][1][
            'text'] = f'{user_id_buffer[event.source.user_id]["open"]:.2f}'

        FlexMessage["body"]["contents"][6]["contents"][0]["contents"][1][
            'text'] = f'{user_id_buffer[event.source.user_id]["dayLow"]:.2f} - {user_id_buffer[event.source.user_id]["dayHigh"]:.2f}'
        FlexMessage["body"]["contents"][6]["contents"][2]["contents"][1][
            'text'] = f'{user_id_buffer[event.source.user_id]["fiftyTwoWeekLow"]:.2f} - {user_id_buffer[event.source.user_id]["fiftyTwoWeekHigh"]:.2f}'

        FlexMessage["body"]["contents"][8]["contents"][0]["contents"][1]['text'] = TocMachine.format_number(
            user_id_buffer[event.source.user_id]["volume"])
        FlexMessage["body"]["contents"][8]["contents"][2]["contents"][1]['text'] = TocMachine.format_number(
            user_id_buffer[event.source.user_id]["marketCap"])

        sent_flex_message(reply_token, FlexSendMessage('Search Result', FlexMessage))

    def is_going_to_summary(self, event):
        text = event.message.text
        return text.lower() == "summary"

    def on_enter_summary(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/summary.json', 'r', encoding='utf-8'))
        FlexMessage["body"]["contents"][0]["contents"][0]["text"] = user_id_buffer[event.source.user_id][
            "longBusinessSummary"]
        sent_flex_message(reply_token, FlexSendMessage('Summary', FlexMessage))

    def is_going_to_detail(self, event):
        text = event.message.text
        return text.lower() == "detail"

    def on_enter_detail(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/detail.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('Summary', FlexMessage))

    def is_search_result_back_to_summary(self, event):
        text = event.message.text
        return text.lower() == "back"

    def is_going_to_home(self, event):
        text = event.message.text
        return text.lower() == "home"

    def on_enter_home(self, event):
        user_id_buffer.pop(event.source.user_id)

    def is_going_to_valuation_measures(self, event):
        text = event.message.text
        return text.lower() == "valuation measures"

    def on_enter_valuation_measures(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/valuation_measures.json', 'r', encoding='utf-8'))
        FlexMessage["body"]["contents"][0]["contents"][0]["contents"][1]["text"] = TocMachine.format_number(
            user_id_buffer[event.source.user_id]["marketCap"])
        FlexMessage["body"]["contents"][0]["contents"][2]["contents"][1]["text"] = TocMachine.format_number(
            user_id_buffer[event.source.user_id]["enterpriseValue"])

        FlexMessage["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["trailingPE"]:.3f}'
        FlexMessage["body"]["contents"][2]["contents"][2]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["forwardPE"]:.3f}'

        FlexMessage["body"]["contents"][4]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["priceToSalesTrailing12Months"]:.3f}'
        FlexMessage["body"]["contents"][4]["contents"][2]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["priceToBook"]:.3f}'

        FlexMessage["body"]["contents"][6]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["pegRatio"]:.3f}'

        FlexMessage["body"]["contents"][8]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["enterpriseToRevenue"]:.3f}'

        FlexMessage["body"]["contents"][10]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["enterpriseToEbitda"]:.3f}'

        sent_flex_message(reply_token, FlexSendMessage('Valuation Measures', FlexMessage))

    def is_going_to_financial_highlights(self, event):
        text = event.message.text
        return text.lower() == "financial highlights"

    def on_enter_financial_highlights(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/financial_highlights.json', 'r', encoding='utf-8'))
        FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["enterpriseToEbitda"]:.3f}'

        sent_flex_message(reply_token, FlexSendMessage('Valuation Measures', FlexMessage))

    @staticmethod
    def safe_num(num):
        if isinstance(num, str):
            num = float(num)
        return float('{:.3g}'.format(abs(num)))

    @staticmethod
    def format_number(num):
        num = TocMachine.safe_num(num)
        sign = ''

        metric = {'T': 1000000000000, 'B': 1000000000, 'M': 1000000, 'K': 1000, '': 1}

        for index in metric:
            num_check = num / metric[index]

            if (num_check >= 1):
                num = num_check
                sign = index
                break

        return f"{str(num).rstrip('0').rstrip('.')}{sign}"
