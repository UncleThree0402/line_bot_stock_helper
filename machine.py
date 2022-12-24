from fsm import TocMachine


def create_machine():
    machine = TocMachine(
        states=["home", "menu", "search", "search_result", "summary", "detail",
                "valuation_measures", "financial_highlights", "trading_information",
                "stock_chart", "stock_chart_result", "news"],
        transitions=[
            {
                "trigger": "advance",
                "source": "home",
                "dest": "menu",
                "conditions": "is_going_to_menu",
            },
            {
                "trigger": "advance",
                "source": ["search", "search_result", "summary", "valuation_measures", "detail",
                           "financial_highlights", "trading_information", "stock_chart", "news", "home"],
                "dest": "home",
                "conditions": "is_going_to_home",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "search",
                "conditions": "is_going_to_search",
            },
            {
                "trigger": "advance",
                "source": "search",
                "dest": "search_result",
                "conditions": "is_going_to_search_result",
            },
            {
                "trigger": "advance",
                "source": "search_result",
                "dest": "summary",
                "conditions": "is_going_to_summary",
            },
            {
                "trigger": "advance",
                "source": "search_result",
                "dest": "detail",
                "conditions": "is_going_to_detail",
            },
            {
                "trigger": "advance",
                "source": "search_result",
                "dest": "stock_chart",
                "conditions": "is_going_to_stock_chart",
            },
            {
                "trigger": "advance",
                "source": "search_result",
                "dest": "news",
                "conditions": "is_going_to_news",
            },
            {
                "trigger": "advance",
                "source": ["summary", "detail", "stock_chart", "news"],
                "dest": "search_result",
                "conditions": "is_back_to_search_result",
            },
            {
                "trigger": "advance",
                "source": "stock_chart",
                "dest": "stock_chart_result",
                "conditions": "is_going_to_stock_chart_result",
            },
            {
                "trigger": "advance",
                "source": "detail",
                "dest": "valuation_measures",
                "conditions": "is_going_to_valuation_measures",
            }, {
                "trigger": "advance",
                "source": "detail",
                "dest": "trading_information",
                "conditions": "is_going_to_trading_information",
            },
            {
                "trigger": "advance",
                "source": ["financial_highlights", "valuation_measures", "trading_information"],
                "dest": "detail",
                "conditions": "is_back_to_detail",
            },
            {
                "trigger": "advance",
                "source": "detail",
                "dest": "financial_highlights",
                "conditions": "is_going_to_financial_highlights",
            },
            {"trigger": "go_back", "source": "stock_chart_result", "dest": "stock_chart"},
        ],
        initial="home",
        auto_transitions=False,
        show_conditions=True,
    )

    return machine
