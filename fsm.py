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

ssl._create_default_https_context = ssl._create_unverified_context

user_id_buffer = {}
chart_buffer = {}


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_home(self, event):
        text = event.message.text
        return text.lower() == "home"

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"

    def on_enter_menu(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/home.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('Home', FlexMessage))

    def on_enter_home(self, event):
        pass

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

    def is_back_to_search_result(self, event):
        text = event.message.text
        return text.lower() == "back"

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

    def is_back_to_detail(self, event):
        text = event.message.text
        return text.lower() == "back"

    def on_enter_financial_highlights(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/financial_highlights.json', 'r', encoding='utf-8'))
        FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["lastFiscalYearEnd"],
                                             tz=timezone.utc).strftime(
            "%m/%d/%Y UTC")
        FlexMessage["contents"][0]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["mostRecentQuarter"],
                                             tz=timezone.utc).strftime(
            "%m/%d/%Y UTC")

        FlexMessage["contents"][1]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["profitMargins"]:.2%}'
        FlexMessage["contents"][1]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["operatingMargins"]:.2%}'

        FlexMessage["contents"][2]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["returnOnAssets"]:.2%}'
        FlexMessage["contents"][2]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["returnOnEquity"]:.2%}'

        FlexMessage["contents"][3]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["totalRevenue"])
        FlexMessage["contents"][3]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["revenuePerShare"]}'
        FlexMessage["contents"][3]["body"]["contents"][4]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["revenueQuarterlyGrowth"]}'
        FlexMessage["contents"][3]["body"]["contents"][6]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["grossProfits"])
        FlexMessage["contents"][3]["body"]["contents"][8]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["ebitda"])
        FlexMessage["contents"][3]["body"]["contents"][10]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["netIncomeToCommon"])
        FlexMessage["contents"][3]["body"]["contents"][12]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["earningsQuarterlyGrowth"]:.2%}'

        FlexMessage["contents"][4]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["totalCash"])
        FlexMessage["contents"][4]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["totalCashPerShare"]:.2f}'
        FlexMessage["contents"][4]["body"]["contents"][4]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["totalDebt"])
        FlexMessage["contents"][4]["body"]["contents"][6]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["debtToEquity"]:.2f}'
        FlexMessage["contents"][4]["body"]["contents"][8]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["currentRatio"]:.2f}'
        FlexMessage["contents"][4]["body"]["contents"][10]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["bookValue"]:.2f}'

        FlexMessage["contents"][5]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["operatingCashflow"])
        FlexMessage["contents"][5]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["freeCashflow"])

        sent_flex_message(reply_token, FlexSendMessage('Valuation Measures', FlexMessage))

    def is_going_to_trading_information(self, event):
        text = event.message.text
        return text.lower() == "trading information"

    def on_enter_trading_information(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/trading_information.json', 'r', encoding='utf-8'))

        FlexMessage["contents"][0]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["beta"]:.2f}'
        FlexMessage["contents"][0]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["52WeekChange"]:.2%}'
        FlexMessage["contents"][0]["body"]["contents"][4]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["SandP52WeekChange"]:.2%}'
        FlexMessage["contents"][0]["body"]["contents"][6]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["fiftyTwoWeekHigh"]:.2f}'
        FlexMessage["contents"][0]["body"]["contents"][8]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["fiftyTwoWeekLow"]:.2f}'
        FlexMessage["contents"][0]["body"]["contents"][10]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["fiftyDayAverage"]:.2f}'
        FlexMessage["contents"][0]["body"]["contents"][12]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["twoHundredDayAverage"]:.2f}'

        FlexMessage["contents"][1]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["averageVolume"])
        FlexMessage["contents"][1]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["averageVolume10days"])
        FlexMessage["contents"][1]["body"]["contents"][4]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["sharesOutstanding"])
        FlexMessage["contents"][1]["body"]["contents"][6]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["impliedSharesOutstanding"])
        FlexMessage["contents"][1]["body"]["contents"][8]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["floatShares"])
        FlexMessage["contents"][1]["body"]["contents"][10]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["heldPercentInsiders"]:.2%}'
        FlexMessage["contents"][1]["body"]["contents"][12]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["heldPercentInstitutions"]:.2%}'
        FlexMessage["contents"][1]["body"]["contents"][14]["contents"][0]["contents"][1][
            "text"] = TocMachine.format_number(user_id_buffer[event.source.user_id]["sharesShort"])
        FlexMessage["contents"][1]["body"]["contents"][16]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["shortRatio"]:.2f}'
        FlexMessage["contents"][1]["body"]["contents"][18]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["shortPercentOfFloat"]:.2%}'

        FlexMessage["contents"][2]["body"]["contents"][0]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["dividendRate"]:.2f}'
        FlexMessage["contents"][2]["body"]["contents"][2]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["dividendYield"]:.2%}'
        FlexMessage["contents"][2]["body"]["contents"][4]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["trailingAnnualDividendRate"]:.2f}'
        FlexMessage["contents"][2]["body"]["contents"][6]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["trailingAnnualDividendYield"]:.2%}'
        FlexMessage["contents"][2]["body"]["contents"][8]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["fiveYearAvgDividendYield"]:.2f}'
        FlexMessage["contents"][2]["body"]["contents"][10]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["payoutRatio"]:.2%}'
        FlexMessage["contents"][2]["body"]["contents"][12]["contents"][0]["contents"][1][
            "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["lastDividendDate"],
                                             tz=timezone.utc).strftime(
            "%m/%d/%Y UTC")
        FlexMessage["contents"][2]["body"]["contents"][14]["contents"][0]["contents"][1][
            "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["exDividendDate"],
                                             tz=timezone.utc).strftime(
            "%m/%d/%Y UTC")
        FlexMessage["contents"][2]["body"]["contents"][16]["contents"][0]["contents"][1][
            "text"] = f'{user_id_buffer[event.source.user_id]["lastSplitFactor"]}'
        FlexMessage["contents"][2]["body"]["contents"][18]["contents"][0]["contents"][1][
            "text"] = datetime.fromtimestamp(user_id_buffer[event.source.user_id]["lastSplitDate"],
                                             tz=timezone.utc).strftime(
            "%m/%d/%Y UTC")

        sent_flex_message(reply_token, FlexSendMessage('Trading Information Measures', FlexMessage))

    def is_going_to_stock_chart(self, event):
        text = event.message.text
        return text.lower() == "stock chart"

    def on_enter_stock_chart(self, event):
        reply_token = event.reply_token
        FlexMessage = json.load(open('json_file/stock_chart.json', 'r', encoding='utf-8'))
        sent_flex_message(reply_token, FlexSendMessage('Stock Chart', FlexMessage))

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
