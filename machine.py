from fsm import TocMachine


def create_machine():
    machine = TocMachine(
        states=["home", "search", "search_result", "summary", "detail", "valuation_measures","financial_highlights"],
        transitions=[
            {
                "trigger": "advance",
                "source": "home",
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
                "source": "summary",
                "dest": "search_result",
                "conditions": "is_search_result_back_to_summary",
            },
            {
                "trigger": "advance",
                "source": "detail",
                "dest": "valuation_measures",
                "conditions": "is_going_to_valuation_measures",
            },
            {
                "trigger": "advance",
                "source": "detail",
                "dest": "financial_highlights",
                "conditions": "is_going_to_financial_highlights",
            },
            {
                "trigger": "advance",
                "source": ["search", "search_result", "summary", "valuation_measures", "detail", "financial_highlights"],
                "dest": "home",
                "conditions": "is_going_to_home",
            },
        ],
        initial="home",
        auto_transitions=False,
        show_conditions=True,
    )

    return machine
