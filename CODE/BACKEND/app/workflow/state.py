from typing import Any, TypedDict


class InvestmentState(TypedDict, total=False):
    user_id: int
    goal: dict
    financial_profile: dict
    risk_answers: dict
    risk_category: str | None
    risk_profile: dict
    market_symbol: str
    market_data: dict
    financial_analysis: dict
    goal_analysis: dict
    candidate_portfolio: dict
    scenarios: dict
    validation_result: dict
    final_response: dict
    error: str
