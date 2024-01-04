# queries/query/__init__.py
from .assets_liabilities_ import assets_liability_query
from .cash_flow_query_ import cash_flow_query
from .debt_management_query_ import debt_management_query
from .liquidity_query_ import liquidity_query
from .market_valuation_query_ import market_valuation_query
from .operational_efficiency_query_ import operational_efficiency_query
from .profitability_query_ import profitability_query

ASSET_LIABILITIES = assets_liability_query
CASH_FLOW = cash_flow_query
DEBT_MANAGEMENT = debt_management_query
LIQUIDITY = liquidity_query
MARKET_VALUATION = market_valuation_query
PROFITABILITY = profitability_query
OPERATIONAL_EFFICIENCY = operational_efficiency_query
QUERY_FILES = {
    "Assets Liabilities": "apps/queries/assets_liabilities.sql",
    "Cash Flow": "apps/queries/cash_flow_query.sql",
    "Debt Management": "apps/queries/debt_management_query.sql",
    "Liquidity": "apps/queries/liquidity_query.sql",
    "Market Valuation": "apps/queries/market_valuation_query.sql",
    "Operational Efficiency": "apps/queries/operational_efficiency_query.sql",
    "Profitability": "apps/queries/profitability_query.sql"
}

__all__ = [
    'ASSET_LIABILITIES',
    'CASH_FLOW',
    'DEBT_MANAGEMENT',
    'LIQUIDITY',
    'MARKET_VALUATION',
    'OPERATIONAL_EFFICIENCY',
    'PROFITABILITY',
    'QUERY_FILES'
]


