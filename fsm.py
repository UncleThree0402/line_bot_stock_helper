from transitions.extensions import GraphMachine
import json
from utils import send_text_message, sent_flex_message
from linebot.models import FlexSendMessage, ImageSendMessage
import yfinance as yf
from datetime import datetime
from datetime import timezone
import pandas as pd
import mplfinance as mpf
from imgurpython import ImgurClient
from GoogleNews import GoogleNews
import ssl
from finvizfinance.screener.overview import Overview
from finvizfinance.news import News

ssl._create_default_https_context = ssl._create_unverified_context

user_id_buffer = {}
chart_buffer = {}


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"

    def on_enter_menu(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/menu.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('Menu', FlexMessage))

    def is_going_to_search(self, event):
        text = event.message.text
        return text.lower() == "search"

    def on_enter_search(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/search.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('Search', FlexMessage))

    def is_going_to_top5(self, event):
        text = event.message.text
        return text.lower() == "top5"

    def on_enter_top5(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/top5.json', 'r', encoding='utf-8'))
            foverview = Overview()
            foverview.set_filter(signal="Top Gainers")
            df = foverview.screener_view(select_page=1)
            df_list = df.values.tolist()

            for i in range(5):
                FlexMessage["body"]["contents"][1]["contents"][i]["contents"][0]["text"] = f'{df_list[i][0]}'
                FlexMessage["body"]["contents"][1]["contents"][i]["contents"][1]["text"] = f'{df_list[i][7]:.2f}'
                FlexMessage["body"]["contents"][1]["contents"][i]["contents"][2]["text"] = f'{df_list[i][8]:.2%}'
                FlexMessage["body"]["contents"][1]["contents"][i]["contents"][3]["action"]["text"] = f'{df_list[i][0]}'

            foverview = Overview()
            foverview.set_filter(signal="Top Losers")
            df = foverview.screener_view(select_page=1)
            df_list = df.values.tolist()

            for i in range(5):
                FlexMessage["body"]["contents"][3]["contents"][i]["contents"][0]["text"] = f'{df_list[i][0]}'
                FlexMessage["body"]["contents"][3]["contents"][i]["contents"][1]["text"] = f'{df_list[i][7]:.2f}'
                FlexMessage["body"]["contents"][3]["contents"][i]["contents"][2]["text"] = f'{df_list[i][8]:.2%}'
                FlexMessage["body"]["contents"][3]["contents"][i]["contents"][3]["action"]["text"] = f'{df_list[i][0]}'

            sent_flex_message(reply_token, FlexSendMessage('Search', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_top5news(self, event):
        text = event.message.text
        return text.lower() == "top5news"

    def on_enter_top5news(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/top5news.json', 'r', encoding='utf-8'))
            fnews = News()
            all_news = fnews.get_news()
            all_news = list(all_news.values())
            all_news = all_news[0].values.tolist()

            for i in range(5):
                FlexMessage["contents"][i]["body"]["contents"][0]["contents"][0][
                    "text"] = all_news[i][1]
                FlexMessage["contents"][i]["body"]["contents"][0]["contents"][1]["contents"][1][
                    "text"] = all_news[i][2]
                FlexMessage["contents"][i]["body"]["contents"][0]["contents"][2]["contents"][1][
                    "text"] = all_news[i][3]
                FlexMessage["contents"][i]["body"]["contents"][0]["contents"][2]["contents"][1][
                    "action"]["uri"] = all_news[i][3]

            sent_flex_message(reply_token, FlexSendMessage('Search', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_introduction(self, event):
        text = event.message.text
        return text.lower() == "introduction"

    def on_enter_introduction(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/introduction.json', 'r', encoding='utf-8'))
            sent_flex_message(reply_token, FlexSendMessage('Introduction', FlexMessage))
        except:
            self.go_to_error(event)

    def on_enter_error(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/error.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('ERROR', FlexMessage))

    def is_going_to_show_fsm(self, event):
        text = event.message.text
        return text.lower() == "show fsm"

    def on_enter_show_fsm(self, event):
        reply_token = event.reply_token
        sent_flex_message(reply_token, ImageSendMessage(original_content_url="https://i.imgur.com/GCW5dXs.png",
                                                        preview_image_url="https://i.imgur.com/GCW5dXs.png"))
        self.go_menu(event)


    def is_going_to_search_result(self, event):
        user_id_buffer[event.source.user_id] = yf.Ticker(event.message.text.lower()).info
        return True

    def on_enter_search_result(self, event):
        reply_token = event.reply_token
        try:
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
            try:
                FlexMessage["body"]["contents"][8]["contents"][2]["contents"][1]['text'] = TocMachine.format_number(
                    user_id_buffer[event.source.user_id]["marketCap"])
            except:
                FlexMessage["body"]["contents"][8]["contents"][2]["contents"][1]['text'] = "N/A"

            sent_flex_message(reply_token, FlexSendMessage('Search Result', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_summary(self, event):
        text = event.message.text
        return text.lower() == "summary"

    def on_enter_summary(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/summary.json', 'r', encoding='utf-8'))
            FlexMessage["body"]["contents"][0]["contents"][0]["text"] = user_id_buffer[event.source.user_id][
                "longBusinessSummary"]
            sent_flex_message(reply_token, FlexSendMessage('Summary', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_detail(self, event):
        text = event.message.text
        return text.lower() == "detail"

    def on_enter_detail(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/detail.json', 'r', encoding='utf-8'))
            sent_flex_message(reply_token, FlexSendMessage('Summary', FlexMessage))
        except:
            self.go_to_error(event)

    def is_back_to_search_result(self, event):
        text = event.message.text
        return text.lower() == "back"

    def on_enter_home(self, event):
        user_id_buffer.pop(event.source.user_id)

    def is_going_to_valuation_measures(self, event):
        text = event.message.text
        return text.lower() == "valuation measures"

    def on_enter_valuation_measures(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/valuation_measures.json', 'r', encoding='utf-8'))
            try:
                FlexMessage["body"]["contents"][0]["contents"][0]["contents"][1]["text"] = TocMachine.format_number(
                    user_id_buffer[event.source.user_id]["marketCap"])
            except:
                FlexMessage["body"]["contents"][0]["contents"][0]["contents"][1]["text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][0]["contents"][2]["contents"][1]["text"] = TocMachine.format_number(
                    user_id_buffer[event.source.user_id]["enterpriseValue"])
            except:
                FlexMessage["body"]["contents"][0]["contents"][2]["contents"][1]["text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["trailingPE"]:.3f}'
                print(f'{user_id_buffer[event.source.user_id]["trailingPE"]:.3f}')
            except:
                FlexMessage["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][2]["contents"][2]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["forwardPE"]:.3f}'
            except:
                FlexMessage["body"]["contents"][2]["contents"][2]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["priceToSalesTrailing12Months"]:.3f}'
            except:
                FlexMessage["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][4]["contents"][2]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["priceToBook"]:.3f}'
            except:
                FlexMessage["body"]["contents"][4]["contents"][2]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["pegRatio"]:.3f}'
            except:
                FlexMessage["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["enterpriseToRevenue"]:.3f}'
            except:
                FlexMessage["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["enterpriseToEbitda"]:.3f}'
            except:
                FlexMessage["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            sent_flex_message(reply_token, FlexSendMessage('Valuation Measures', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_financial_highlights(self, event):
        text = event.message.text
        return text.lower() == "financial highlights"

    def is_back_to_detail(self, event):
        text = event.message.text
        return text.lower() == "back"

    def on_enter_financial_highlights(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/financial_highlights.json', 'r', encoding='utf-8'))

            try:
                FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["lastFiscalYearEnd"],
                                                     tz=timezone.utc).strftime(
                    "%m/%d/%Y UTC")
            except:
                FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["mostRecentQuarter"],
                                                     tz=timezone.utc).strftime(
                    "%m/%d/%Y UTC")
            except:
                FlexMessage["contents"][0]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["profitMargins"]:.2%}'
            except:
                FlexMessage["contents"][1]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["operatingMargins"]:.2%}'
            except:
                FlexMessage["contents"][1]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["returnOnAssets"]:.2%}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["returnOnEquity"]:.2%}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["totalRevenue"])
            except:
                FlexMessage["contents"][3]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["revenuePerShare"]}'
            except:
                FlexMessage["contents"][3]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["revenueQuarterlyGrowth"]}'
            except:
                FlexMessage["contents"][3]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["grossProfits"])
            except:
                FlexMessage["contents"][3]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["ebitda"])
            except:
                FlexMessage["contents"][3]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["netIncomeToCommon"])
            except:
                FlexMessage["contents"][3]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][3]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["earningsQuarterlyGrowth"]:.2%}'
            except:
                FlexMessage["contents"][3]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][4]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["totalCash"])
            except:
                FlexMessage["contents"][4]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][4]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["totalCashPerShare"]:.2f}'
            except:
                FlexMessage["contents"][4]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][4]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["totalDebt"])
            except:
                FlexMessage["contents"][4]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][4]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["debtToEquity"]:.2f}'
            except:
                FlexMessage["contents"][4]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][4]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["currentRatio"]:.2f}'
            except:
                FlexMessage["contents"][4]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][4]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["bookValue"]:.2f}'
            except:
                FlexMessage["contents"][4]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][5]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["operatingCashflow"])
            except:
                FlexMessage["contents"][5]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][5]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["freeCashflow"])
            except:
                FlexMessage["contents"][5]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            sent_flex_message(reply_token, FlexSendMessage('Valuation Measures', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_trading_information(self, event):
        text = event.message.text
        return text.lower() == "trading information"

    def on_enter_trading_information(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/trading_information.json', 'r', encoding='utf-8'))

            try:
                FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["beta"]:.2f}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["52WeekChange"]:.2%}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["SandP52WeekChange"]:.2%}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["fiftyTwoWeekHigh"]:.2f}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["fiftyTwoWeekLow"]:.2f}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["fiftyDayAverage"]:.2f}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][0]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["twoHundredDayAverage"]:.2f}'
            except:
                FlexMessage["contents"][0]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["averageVolume"])
            except:
                FlexMessage["contents"][1]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["averageVolume10days"])
            except:
                FlexMessage["contents"][1]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["sharesOutstanding"])
            except:
                FlexMessage["contents"][1]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["impliedSharesOutstanding"])
            except:
                FlexMessage["contents"][1]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["floatShares"])
            except:
                FlexMessage["contents"][1]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["heldPercentInsiders"]:.2%}'
            except:
                FlexMessage["contents"][1]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["heldPercentInstitutions"]:.2%}'
            except:
                FlexMessage["contents"][1]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][14]["contents"][0]["contents"][1][
                    "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["sharesShort"])
            except:
                FlexMessage["contents"][1]["body"]["contents"][14]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][16]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["shortRatio"]:.2f}'
            except:
                FlexMessage["contents"][1]["body"]["contents"][16]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][1]["body"]["contents"][18]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["shortPercentOfFloat"]:.2%}'
            except:
                FlexMessage["contents"][1]["body"]["contents"][18]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["dividendRate"]:.2f}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["dividendYield"]:.2%}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][2]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["trailingAnnualDividendRate"]:.2f}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][4]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["trailingAnnualDividendYield"]:.2%}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][6]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["fiveYearAvgDividendYield"]:.2f}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][8]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["payoutRatio"]:.2%}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][10]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["lastDividendDate"],
                                                     tz=timezone.utc).strftime(
                    "%m/%d/%Y UTC")
            except:
                FlexMessage["contents"][2]["body"]["contents"][12]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][14]["contents"][0]["contents"][1][
                    "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["exDividendDate"],
                                                     tz=timezone.utc).strftime(
                    "%m/%d/%Y UTC")
            except:
                FlexMessage["contents"][2]["body"]["contents"][14]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][16]["contents"][0]["contents"][1][
                    "text"] = f'{user_id_buffer[event.source.user_id]["lastSplitFactor"]}'
            except:
                FlexMessage["contents"][2]["body"]["contents"][16]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            try:
                FlexMessage["contents"][2]["body"]["contents"][18]["contents"][0]["contents"][1][
                    "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["lastSplitDate"],
                                                     tz=timezone.utc).strftime(
                    "%m/%d/%Y UTC")
            except:
                FlexMessage["contents"][2]["body"]["contents"][18]["contents"][0]["contents"][1][
                    "text"] = "N/A"

            sent_flex_message(reply_token, FlexSendMessage('Trading Information Measures', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_stock_chart(self, event):
        text = event.message.text
        return text.lower() == "stock chart"

    def on_enter_stock_chart(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/stock_chart.json', 'r', encoding='utf-8'))
            sent_flex_message(reply_token, FlexSendMessage('Stock Chart', FlexMessage))
        except:
            self.go_to_error(event)

    def is_going_to_stock_chart_result(self, event):
        chart_buffer[event.source.user_id] = event.message.text.lower()
        return True

    def on_enter_stock_chart_result(self, event):
        reply_token = event.reply_token
        tsm = yf.Ticker(user_id_buffer[event.source.user_id]["symbol"])
        if chart_buffer[event.source.user_id] == "1m":
            hist = tsm.history(period="1d", interval="1m")
        elif chart_buffer[event.source.user_id] == "5m":
            hist = tsm.history(period="5d", interval="5m")
        elif chart_buffer[event.source.user_id] == "30m":
            hist = tsm.history(period="1mo", interval="30m")
        elif chart_buffer[event.source.user_id] == "1h":
            hist = tsm.history(period="3mo", interval="1h")
        elif chart_buffer[event.source.user_id] == "1d":
            hist = tsm.history(period="6mo", interval="1d")
        elif chart_buffer[event.source.user_id] == "1wk":
            hist = tsm.history(period="2y", interval="1wk")
        elif chart_buffer[event.source.user_id] == "1mo":
            hist = tsm.history(period="5y", interval="1mo")
        elif chart_buffer[event.source.user_id] == "3mo":
            hist = tsm.history(period="10y", interval="3mo")
        else:
            hist = tsm.history(period="max", interval="3mo")

        fig = mpf.figure(figsize=(15, 15))
        mpf.plot(hist, type='line', style='yahoo', savefig="test.png", volume=True)
        client = ImgurClient("c065cb2b1511ce8", "61bff6f736bf57807987df100e32b7e32f991e71")
        upload_image = client.upload_from_path("test.png")
        sent_flex_message(reply_token, ImageSendMessage(original_content_url=upload_image["link"],
                                                        preview_image_url=upload_image["link"]))
        self.go_back()


    def is_going_to_news(self, event):
        text = event.message.text
        return text.lower() == "news"

    def on_enter_news(self, event):
        try:
            reply_token = event.reply_token
            FlexMessage = json.load(open('json_file/news.json', 'r', encoding='utf-8'))
            news = GoogleNews(period='7d')
            news.search(user_id_buffer[event.source.user_id]["symbol"])
            result = news.result()

            idx = 0
            for res in result:
                FlexMessage["contents"][idx]["body"]["contents"][0]["contents"][0]["contents"][1][
                    "text"] = res["title"]
                FlexMessage["contents"][idx]["body"]["contents"][0]["contents"][2]["contents"][1][
                    "text"] = res["desc"]
                FlexMessage["contents"][idx]["body"]["contents"][0]["contents"][4]["contents"][1][
                    "text"] = res["link"]
                FlexMessage["contents"][idx]["body"]["contents"][0]["contents"][4]["contents"][1][
                    "action"]["uri"] = res["link"]

                if idx == 4:
                    break
                else:
                    idx += 1

            sent_flex_message(reply_token, FlexSendMessage('Stock Chart', FlexMessage))
        except:
            self.go_to_error(event)

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
