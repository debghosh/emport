"""
Alphatic Portfolio Analyzer - ENHANCED VERSION
A comprehensive portfolio analysis platform with advanced features for sophisticated investors

NEW FEATURES:
- Visual enhancements (modern gradient backgrounds, professional typography)
- Educational features (detailed metric explanations with tooltips)
- Market Regime Analysis (5 regime types with historical classification)
- Forward-Looking Risk Analysis (Monte Carlo simulations, VaR, CVaR)
- Enhanced interpretations for every chart
- Complete PyFolio integration
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import pyfolio as pf
from scipy.optimize import minimize
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Alphatic Portfolio Analyzer ✨",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ENHANCED CUSTOM CSS - MODERN GRADIENT THEME
# =============================================================================

st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Gradient Background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Main Header */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .tagline {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    
    /* Sub Headers */
    .sub-header {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Color-Coded Metric Boxes */
    .metric-excellent {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .metric-good {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .metric-fair {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .metric-poor {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Success/Warning/Info Boxes */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: slideInRight 0.5s ease-out;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Interpretation Boxes */
    .interpretation-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        border-left: 5px solid #2196f3;
    }
    
    .interpretation-title {
        font-weight: 600;
        color: #1976d2;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolios' not in st.session_state:
    st.session_state.portfolios = {}
if 'current_portfolio' not in st.session_state:
    st.session_state.current_portfolio = None
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = {}


# =============================================================================
# EDUCATIONAL CONTENT - METRIC EXPLANATIONS
# =============================================================================

METRIC_EXPLANATIONS = {
    'annual_return': {
        'simple': 'Average yearly gain/loss of your investment',
        'detailed': '''
        **Annual Return** is the average yearly percentage gain or loss on your investment.
        
        **Real-World Example:** If your portfolio has a 10% annual return:
        - $100,000 grows to $110,000 in one year
        - Over 10 years, it grows to approximately $259,000 (with compounding)
        
        **What's Normal:**
        - S&P 500 long-term average: ~10% per year
        - Conservative portfolios: 4-6% per year
        - Aggressive growth: 12-15%+ per year
        
        **Important:** Past returns don't guarantee future results!
        ''',
        'thresholds': {
            'excellent': (15, 'Above 15% - Outstanding performance'),
            'good': (10, '10-15% - Very good performance'),
            'fair': (5, '5-10% - Moderate performance'),
            'poor': (0, 'Below 5% - Consider alternatives')
        }
    },
    
    'sharpe_ratio': {
        'simple': 'Risk-adjusted returns - higher is better',
        'detailed': '''
        **Sharpe Ratio** measures how much extra return you get for the extra risk you take.
        
        **Real-World Example:** 
        - Portfolio A: 12% return, Sharpe = 0.5 (volatile)
        - Portfolio B: 10% return, Sharpe = 1.5 (smooth)
        - Portfolio B is better! More consistent returns with less anxiety.
        
        **Professional Benchmarks:**
        - Below 1.0: Not great - too much risk for the return
        - 1.0-2.0: Good to excellent - solid risk-adjusted performance
        - Above 2.0: Outstanding - very rare, often unsustainable
        - Above 3.0: Exceptional - used by top hedge funds
        
        **Why It Matters:** Would you rather have a bumpy 15% return or a smooth 12%? 
        Sharpe Ratio helps you decide.
        ''',
        'thresholds': {
            'excellent': (2.0, 'Above 2.0 - Outstanding risk-adjusted returns'),
            'good': (1.0, '1.0-2.0 - Good risk-adjusted returns'),
            'fair': (0.5, '0.5-1.0 - Acceptable but could be better'),
            'poor': (0, 'Below 0.5 - Poor risk-adjusted returns')
        }
    },
    
    'max_drawdown': {
        'simple': 'Largest peak-to-trough decline',
        'detailed': '''
        **Maximum Drawdown** is the biggest drop from a peak to a trough in your portfolio value.
        
        **Real-World Example:**
        - Your portfolio peaks at $200,000
        - It drops to $150,000 during a market crash
        - Maximum Drawdown = 25% ($50,000 loss)
        - This is the worst pain you experienced
        
        **Can You Handle It?**
        - -10%: Mild correction, happens often
        - -20%: Significant drop, happens every few years
        - -30%: Severe bear market, very painful
        - -40%+: Crisis level, many investors panic sell (DON'T!)
        
        **2008 Crisis Reference:**
        - S&P 500: -56% drawdown
        - Conservative 60/40: -30% drawdown
        - Cash: 0% (but lost to inflation)
        
        **Key Question:** If your portfolio drops by this much, will you sell in panic or stay invested?
        ''',
        'thresholds': {
            'excellent': (-10, 'Above -10% - Very low drawdown'),
            'good': (-20, '-10% to -20% - Moderate drawdown'),
            'fair': (-30, '-20% to -30% - Significant drawdown'),
            'poor': (-40, 'Below -30% - Severe drawdown')
        }
    },
    
    'volatility': {
        'simple': 'How much your portfolio value fluctuates',
        'detailed': '''
        **Volatility (Standard Deviation)** measures how much your portfolio bounces around.
        
        **Real-World Example:**
        - Low volatility (10%): $100K portfolio typically moves $10K up/down yearly
        - Medium volatility (20%): $100K portfolio typically moves $20K up/down yearly
        - High volatility (30%+): $100K portfolio might move $30K+ yearly
        
        **Sleep Well Test:**
        - Below 10%: Very stable, good for retirees
        - 10-15%: Moderate, most can handle this
        - 15-20%: Elevated, need strong stomach
        - Above 20%: High, prepare for wild swings
        
        **Benchmark:**
        - S&P 500: ~15-20% volatility
        - Bonds: ~5-8% volatility
        - Bitcoin: 70-100% volatility (!)
        
        **Important:** Lower volatility = Better sleep at night
        ''',
        'thresholds': {
            'excellent': (10, 'Below 10% - Very low volatility'),
            'good': (15, '10-15% - Moderate volatility'),
            'fair': (20, '15-20% - Elevated volatility'),
            'poor': (25, 'Above 20% - High volatility')
        }
    },
    
    'sortino_ratio': {
        'simple': 'Like Sharpe but only penalizes downside risk',
        'detailed': '''
        **Sortino Ratio** is similar to Sharpe Ratio, but smarter: it only cares about bad volatility (drops), not good volatility (gains).
        
        **Why It's Better Than Sharpe:**
        - Sharpe penalizes you for BOTH ups and downs
        - Sortino only penalizes you for downs
        - Example: A portfolio that goes up 20%, up 25%, up 15% has high Sharpe volatility
        - But that's GOOD volatility! Sortino recognizes this.
        
        **Real-World Comparison:**
        - Portfolio A: Smooth 10% return, Sortino = 1.5
        - Portfolio B: Volatile 12% (mostly up), Sortino = 2.0
        - Portfolio B is better! Higher return AND better downside protection.
        
        **Professional Standards:**
        - Below 1.0: Excessive downside risk
        - 1.0-2.0: Good downside protection
        - Above 2.0: Excellent downside management
        - Above 3.0: Elite downside protection
        
        **Use This When:** You don't mind upside volatility, but you hate losses.
        ''',
        'thresholds': {
            'excellent': (2.0, 'Above 2.0 - Excellent downside protection'),
            'good': (1.0, '1.0-2.0 - Good downside protection'),
            'fair': (0.5, '0.5-1.0 - Moderate downside risk'),
            'poor': (0, 'Below 0.5 - High downside risk')
        }
    },
    
    'calmar_ratio': {
        'simple': 'Return relative to worst drawdown',
        'detailed': '''
        **Calmar Ratio** = Annual Return ÷ Maximum Drawdown
        
        **Real-World Example:**
        - Portfolio A: 12% return, -30% max drawdown → Calmar = 0.4
        - Portfolio B: 10% return, -15% max drawdown → Calmar = 0.67
        - Portfolio B is better! Less risk for similar return.
        
        **What It Means:**
        - A Calmar of 0.5 means you get 0.5% return for every 1% of max drawdown
        - Higher is better - more return for less pain
        
        **Professional Standards:**
        - Below 0.5: High risk for the return
        - 0.5-1.0: Good balance
        - 1.0-2.0: Excellent risk-adjusted returns
        - Above 2.0: Outstanding - rare
        
        **Use Case:** Comparing strategies with different risk profiles.
        ''',
        'thresholds': {
            'excellent': (1.5, 'Above 1.5 - Outstanding return vs drawdown'),
            'good': (0.75, '0.75-1.5 - Good return vs drawdown'),
            'fair': (0.5, '0.5-0.75 - Acceptable'),
            'poor': (0, 'Below 0.5 - High risk for the return')
        }
    },
    
    'alpha': {
        'simple': 'Returns above/below expected (vs benchmark)',
        'detailed': '''
        **Alpha** measures if your portfolio beat the market (benchmark) after accounting for risk.
        
        **Real-World Example:**
        - Benchmark (SPY) returns 10%
        - Your portfolio returns 12% with same risk → Alpha = +2%
        - You added 2% of value through smart selection!
        
        **What Positive Alpha Means:**
        - +2% Alpha = You beat the market by 2% per year
        - Over 10 years, that's 22% more wealth!
        - On $1M, that's an extra $220,000
        
        **Reality Check:**
        - Most professional managers have NEGATIVE alpha (after fees)
        - Getting positive alpha consistently is very hard
        - Even +1% alpha is considered excellent
        
        **Professional Standards:**
        - Positive: You're beating the market - great job!
        - Negative but close to 0: You're matching the market
        - Significantly negative: Consider index funds instead
        
        **Important:** Alpha can be due to skill OR luck. Longer time periods = more reliable.
        ''',
        'thresholds': {
            'excellent': (3, 'Above 3% - Outstanding value added'),
            'good': (1, '1-3% - Good value added'),
            'fair': (-1, '-1% to 1% - Matching benchmark'),
            'poor': (-3, 'Below -1% - Underperforming')
        }
    },
    
    'beta': {
        'simple': 'How much your portfolio moves with the market',
        'detailed': '''
        **Beta** measures how much your portfolio moves compared to the market (benchmark).
        
        **Real-World Example:**
        - Beta = 1.0: Your portfolio moves exactly like the market
          - Market up 10% → Your portfolio up 10%
        - Beta = 1.5: Your portfolio is 50% more volatile
          - Market up 10% → Your portfolio up 15%
          - Market down 10% → Your portfolio down 15%
        - Beta = 0.5: Your portfolio is 50% less volatile
          - Market up 10% → Your portfolio up 5%
          - Market down 10% → Your portfolio down 5%
        
        **What's Right for You?**
        - Beta < 0.8: Conservative, defensive portfolio
        - Beta 0.8-1.2: Similar to market
        - Beta > 1.2: Aggressive, amplified moves
        
        **Life Stage Guide:**
        - Young (20-40): Beta 1.0-1.3 (ride the growth)
        - Mid-career (40-55): Beta 0.8-1.1 (moderate)
        - Near retirement (55-65): Beta 0.6-0.9 (defensive)
        - Retired (65+): Beta 0.5-0.7 (preserve capital)
        
        **Important:** High beta = Higher risk AND higher potential reward
        ''',
        'thresholds': {
            'excellent': (0.8, '0.8-1.2 - Well-balanced market exposure'),
            'good': (0.6, '0.6-0.8 or 1.2-1.4 - Moderate deviation'),
            'fair': (0.5, '0.5-0.6 or 1.4-1.6 - Significant deviation'),
            'poor': (0, 'Below 0.5 or above 1.6 - Extreme deviation')
        }
    },
    
    'win_rate': {
        'simple': 'Percentage of profitable periods',
        'detailed': '''
        **Win Rate** is the percentage of time periods (days, months, etc.) where your portfolio made money.
        
        **Real-World Example:**
        - 65% daily win rate = 65% of days are green (up)
        - 75% monthly win rate = 3 out of 4 months are positive
        
        **Interpretation:**
        - Above 60%: Very consistent, good for confidence
        - 50-60%: Typical for good strategies
        - Below 50%: More losing periods than winning
        
        **Psychology Matters:**
        - Higher win rate = Better emotional experience
        - Lower win rate can still work if wins are bigger than losses
        - Example: 40% win rate but wins average +5% and losses average -1%
        
        **Benchmark:**
        - S&P 500: ~55% daily win rate
        - Good trend-following: 45-50% win rate (but big wins)
        - Mean reversion: 60-70% win rate (but smaller wins)
        
        **Use This To:** Assess if you can emotionally handle the strategy.
        ''',
        'thresholds': {
            'excellent': (65, 'Above 65% - Highly consistent'),
            'good': (55, '55-65% - Good consistency'),
            'fair': (50, '50-55% - Acceptable'),
            'poor': (45, 'Below 50% - More losing than winning periods')
        }
    }
}


def render_metric_explanation(metric_key):
    """
    Render an educational explanation for a metric in an expander
    """
    if metric_key in METRIC_EXPLANATIONS:
        info = METRIC_EXPLANATIONS[metric_key]
        
        with st.expander(f"ℹ️ Learn More About This Metric"):
            st.markdown(f"**Quick Summary:** {info['simple']}")
            st.markdown("---")
            st.markdown(info['detailed'])
            
            if 'thresholds' in info:
                st.markdown("---")
                st.markdown("**📊 How to Interpret:**")
                for level, (threshold, description) in info['thresholds'].items():
                    if level == 'excellent':
                        st.markdown(f"🟢 **Excellent:** {description}")
                    elif level == 'good':
                        st.markdown(f"🟡 **Good:** {description}")
                    elif level == 'fair':
                        st.markdown(f"🟠 **Fair:** {description}")
                    elif level == 'poor':
                        st.markdown(f"🔴 **Poor:** {description}")


def get_metric_color_class(metric_key, value):
    """
    Determine the CSS class for a metric based on its value
    """
    if metric_key not in METRIC_EXPLANATIONS:
        return 'metric-card'
    
    thresholds = METRIC_EXPLANATIONS[metric_key].get('thresholds', {})
    
    # Handle metrics where higher is better
    if metric_key in ['annual_return', 'sharpe_ratio', 'sortino_ratio', 'calmar_ratio', 'alpha', 'win_rate']:
        if value >= thresholds.get('excellent', (float('inf'), ''))[0]:
            return 'metric-excellent'
        elif value >= thresholds.get('good', (float('inf'), ''))[0]:
            return 'metric-good'
        elif value >= thresholds.get('fair', (float('inf'), ''))[0]:
            return 'metric-fair'
        else:
            return 'metric-poor'
    
    # Handle max_drawdown (lower absolute value is better)
    elif metric_key == 'max_drawdown':
        if value >= thresholds.get('excellent', (-float('inf'), ''))[0]:
            return 'metric-excellent'
        elif value >= thresholds.get('good', (-float('inf'), ''))[0]:
            return 'metric-good'
        elif value >= thresholds.get('fair', (-float('inf'), ''))[0]:
            return 'metric-fair'
        else:
            return 'metric-poor'
    
    # Handle volatility (lower is better)
    elif metric_key == 'volatility':
        if value <= thresholds.get('excellent', (float('inf'), ''))[0]:
            return 'metric-excellent'
        elif value <= thresholds.get('good', (float('inf'), ''))[0]:
            return 'metric-good'
        elif value <= thresholds.get('fair', (float('inf'), ''))[0]:
            return 'metric-fair'
        else:
            return 'metric-poor'
    
    # Handle beta (closer to 1.0 is better)
    elif metric_key == 'beta':
        abs_deviation = abs(value - 1.0)
        if abs_deviation <= 0.2:
            return 'metric-excellent'
        elif abs_deviation <= 0.4:
            return 'metric-good'
        elif abs_deviation <= 0.6:
            return 'metric-fair'
        else:
            return 'metric-poor'
    
    return 'metric-card'


# =============================================================================
# DATA FETCHING FUNCTIONS
# =============================================================================

def get_earliest_start_date(tickers):
    """
    Determine the earliest common start date for all tickers
    """
    earliest_dates = []
    
    for ticker in tickers:
        try:
            data = yf.download(ticker, period='max', progress=False, auto_adjust=True)
            if not data.empty:
                earliest_dates.append(data.index[0])
        except Exception as e:
            st.warning(f"Could not fetch history for {ticker}: {str(e)}")
    
    if earliest_dates:
        return max(earliest_dates)
    return None


def download_ticker_data(tickers, start_date, end_date=None):
    """
    Download historical price data for multiple tickers with DIVIDENDS REINVESTED
    
    This function uses auto_adjust=True which automatically adjusts for:
    - Dividends (assumes reinvestment)
    - Stock splits
    - Other corporate actions
    
    This gives you TOTAL RETURN performance, not just price appreciation.
    """
    if end_date is None:
        end_date = datetime.now()
    
    try:
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True  # Automatically adjusts for dividends and splits
        )
        
        if len(tickers) == 1:
            data = pd.DataFrame(data['Close'])
            data.columns = tickers
        else:
            data = data['Close']
        
        return data
    except Exception as e:
        st.error(f"Error downloading data: {str(e)}")
        return None


# =============================================================================
# PORTFOLIO OPTIMIZATION FUNCTIONS
# =============================================================================

def calculate_portfolio_returns(prices, weights):
    """
    Calculate portfolio returns given prices and weights
    """
    returns = prices.pct_change().dropna()
    portfolio_returns = (returns * weights).sum(axis=1)
    
    # Ensure it's a Series with a name for consistency
    if not isinstance(portfolio_returns, pd.Series):
        portfolio_returns = pd.Series(portfolio_returns)
    
    # Give it a default name if it doesn't have one
    if portfolio_returns.name is None:
        portfolio_returns.name = 'returns'
    
    return portfolio_returns


def optimize_portfolio(prices, method='max_sharpe'):
    """
    Optimize portfolio weights
    """
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    num_assets = len(prices.columns)
    
    def portfolio_stats(weights):
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = portfolio_return / portfolio_std
        return portfolio_return, portfolio_std, sharpe_ratio
    
    def neg_sharpe(weights):
        return -portfolio_stats(weights)[2]
    
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]
    
    if method == 'max_sharpe':
        result = minimize(neg_sharpe, initial_guess, method='SLSQP', 
                         bounds=bounds, constraints=constraints)
    
    return result.x if result.success else initial_guess


def calculate_efficient_frontier(prices, num_portfolios=100):
    """
    Calculate efficient frontier for visualization
    """
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    num_assets = len(prices.columns)
    results = np.zeros((3, num_portfolios))
    weights_array = []
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_array.append(weights)
        
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = portfolio_return / portfolio_std
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std
        results[2,i] = sharpe
    
    return results, weights_array


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def calculate_portfolio_metrics(returns, benchmark_returns=None, risk_free_rate=0.02):
    """
    Calculate comprehensive portfolio metrics
    """
    # Ensure returns are a pandas Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    # Basic metrics
    total_return = (1 + returns).prod() - 1
    ann_return = (1 + total_return) ** (252 / len(returns)) - 1
    ann_vol = returns.std() * np.sqrt(252)
    sharpe = (ann_return - risk_free_rate) / ann_vol if ann_vol != 0 else 0
    
    # Downside metrics
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std() * np.sqrt(252)
    sortino = (ann_return - risk_free_rate) / downside_std if downside_std != 0 else 0
    
    # Drawdown
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.expanding().max()
    drawdown = (cum_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Calmar ratio
    calmar = ann_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # Win rate
    win_rate = (returns > 0).sum() / len(returns)
    
    metrics = {
        'Total Return': total_return,
        'Annual Return': ann_return,
        'Annual Volatility': ann_vol,
        'Sharpe Ratio': sharpe,
        'Sortino Ratio': sortino,
        'Max Drawdown': max_drawdown,
        'Calmar Ratio': calmar,
        'Win Rate': win_rate
    }
    
    # Alpha and Beta (if benchmark provided)
    if benchmark_returns is not None:
        if isinstance(benchmark_returns, pd.DataFrame):
            benchmark_returns = benchmark_returns.iloc[:, 0]
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) > 0:
            covariance = aligned_data.cov().iloc[0, 1] * 252
            benchmark_variance = aligned_data['benchmark'].var() * 252
            beta = covariance / benchmark_variance if benchmark_variance != 0 else 1
            
            benchmark_return = (1 + aligned_data['benchmark']).prod() - 1
            benchmark_ann_return = (1 + benchmark_return) ** (252 / len(aligned_data)) - 1
            
            alpha = ann_return - (risk_free_rate + beta * (benchmark_ann_return - risk_free_rate))
            
            metrics['Alpha'] = alpha
            metrics['Beta'] = beta
    
    return metrics


def detect_market_regimes(returns, lookback=60):
    """
    Detect market regimes based on volatility and returns
    
    Regimes:
    1. Bull Market (Low Vol) - Positive returns, low volatility
    2. Bull Market (High Vol) - Positive returns, high volatility  
    3. Sideways/Choppy - Returns near zero, any volatility
    4. Bear Market (Low Vol) - Negative returns, low volatility
    5. Bear Market (High Vol) - Negative returns, high volatility (crisis)
    """
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    # Calculate rolling metrics
    rolling_returns = returns.rolling(lookback).mean() * 252  # Annualized
    rolling_vol = returns.rolling(lookback).std() * np.sqrt(252)  # Annualized
    
    # Calculate percentiles for thresholds
    vol_median = rolling_vol.median()
    return_positive = rolling_returns > 0.02  # Above 2% annualized
    return_negative = rolling_returns < -0.02  # Below -2% annualized
    vol_high = rolling_vol > vol_median
    
    # Classify regimes
    regimes = pd.Series(index=returns.index, dtype='object')
    regimes[:] = 'Sideways/Choppy'  # Default
    
    # Bull markets
    regimes[return_positive & ~vol_high] = 'Bull Market (Low Vol)'
    regimes[return_positive & vol_high] = 'Bull Market (High Vol)'
    
    # Bear markets
    regimes[return_negative & ~vol_high] = 'Bear Market (Low Vol)'
    regimes[return_negative & vol_high] = 'Bear Market (High Vol)'
    
    return regimes


def analyze_regime_performance(returns, regimes):
    """
    Analyze portfolio performance by market regime
    """
    df = pd.DataFrame({'returns': returns, 'regime': regimes})
    
    regime_stats = []
    for regime in df['regime'].unique():
        regime_returns = df[df['regime'] == regime]['returns']
        
        if len(regime_returns) > 0:
            stats = {
                'Regime': regime,
                'Occurrences': len(regime_returns),
                'Avg Daily Return': regime_returns.mean(),
                'Volatility': regime_returns.std() * np.sqrt(252),
                'Best Day': regime_returns.max(),
                'Worst Day': regime_returns.min(),
                'Win Rate': (regime_returns > 0).sum() / len(regime_returns)
            }
            regime_stats.append(stats)
    
    return pd.DataFrame(regime_stats)


def monte_carlo_simulation(returns, days_forward=252, num_simulations=1000):
    """
    Run Monte Carlo simulation for forward-looking risk analysis
    """
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    # Calculate parameters from historical returns
    mean_return = returns.mean()
    std_return = returns.std()
    
    # Run simulations
    last_price = 1.0  # Normalized starting point
    simulations = np.zeros((days_forward, num_simulations))
    
    for i in range(num_simulations):
        daily_returns = np.random.normal(mean_return, std_return, days_forward)
        price_path = last_price * (1 + daily_returns).cumprod()
        simulations[:, i] = price_path
    
    return simulations


def calculate_forward_risk_metrics(returns, confidence_level=0.95):
    """
    Calculate forward-looking risk metrics
    """
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    # Expected return and volatility
    expected_return = returns.mean() * 252
    expected_vol = returns.std() * np.sqrt(252)
    
    # Value at Risk (VaR)
    var_95 = returns.quantile(1 - 0.95)
    var_99 = returns.quantile(1 - 0.99)
    
    # Conditional VaR (CVaR / Expected Shortfall)
    cvar_95 = returns[returns <= var_95].mean()
    cvar_99 = returns[returns <= var_99].mean()
    
    # Probability of daily loss
    prob_loss = (returns < 0).sum() / len(returns)
    
    # Estimated maximum drawdown (based on historical)
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.expanding().max()
    drawdowns = (cum_returns - running_max) / running_max
    estimated_max_dd = drawdowns.min()
    
    return {
        'Expected Annual Return': expected_return,
        'Expected Volatility': expected_vol,
        'VaR (95%)': var_95,
        'VaR (99%)': var_99,
        'CVaR (95%)': cvar_95,
        'CVaR (99%)': cvar_99,
        'Probability of Daily Loss': prob_loss,
        'Estimated Max Drawdown': estimated_max_dd
    }


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def plot_cumulative_returns(returns, title='Cumulative Returns', benchmark_returns=None):
    """
    Plot cumulative returns over time with enhanced styling
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    cum_returns = (1 + returns).cumprod()
    cum_returns.plot(ax=ax, linewidth=2.5, label='Portfolio', color='#667eea')
    
    if benchmark_returns is not None:
        if isinstance(benchmark_returns, pd.DataFrame):
            benchmark_returns = benchmark_returns.iloc[:, 0]
        
        cum_bench = (1 + benchmark_returns).cumprod()
        cum_bench.plot(ax=ax, linewidth=2, label='Benchmark', 
                      color='#ff6b6b', linestyle='--', alpha=0.7)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Return', fontsize=12, fontweight='bold')
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    
    plt.tight_layout()
    return fig


def plot_drawdown(returns, title='Drawdown Over Time'):
    """
    Plot drawdown over time with enhanced styling
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.expanding().max()
    drawdown = (cum_returns - running_max) / running_max
    
    ax.fill_between(drawdown.index, 0, drawdown.values, 
                    color='#dc3545', alpha=0.3, label='Drawdown')
    drawdown.plot(ax=ax, linewidth=2, color='#dc3545')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Drawdown', fontsize=12, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    
    plt.tight_layout()
    return fig


def plot_monthly_returns_heatmap(returns, title='Monthly Returns Heatmap'):
    """
    Plot monthly returns as a heatmap with enhanced styling
    """
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    # Calculate monthly returns
    monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
    
    # Convert to DataFrame with explicit column name
    monthly_returns_df = pd.DataFrame({'returns': monthly_returns})
    monthly_returns_df['Year'] = monthly_returns_df.index.year
    monthly_returns_df['Month'] = monthly_returns_df.index.month
    
    # Pivot the data
    monthly_returns_pivot = monthly_returns_df.pivot(
        index='Year', columns='Month', values='returns'
    )
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_returns_pivot.columns = [month_names[i-1] for i in monthly_returns_pivot.columns]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(monthly_returns_pivot * 100, annot=True, fmt='.1f', 
                cmap='RdYlGn', center=0, ax=ax, cbar_kws={'label': 'Return (%)'})
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Year', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_rolling_metrics(returns, window=60, title='Rolling Metrics'):
    """
    Plot rolling Sharpe and Sortino ratios with enhanced styling
    """
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    rolling_return = returns.rolling(window).mean() * 252
    rolling_vol = returns.rolling(window).std() * np.sqrt(252)
    rolling_sharpe = rolling_return / rolling_vol
    
    downside_returns = returns.copy()
    downside_returns[downside_returns > 0] = 0
    rolling_downside_vol = downside_returns.rolling(window).std() * np.sqrt(252)
    rolling_sortino = rolling_return / rolling_downside_vol
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Sharpe Ratio
    rolling_sharpe.plot(ax=ax1, linewidth=2, color='#667eea', label='Rolling Sharpe')
    ax1.axhline(y=1, color='#28a745', linestyle='--', alpha=0.7, label='Good (1.0)')
    ax1.axhline(y=0, color='#dc3545', linestyle='--', alpha=0.7)
    ax1.set_title(f'Rolling Sharpe Ratio ({window}-day)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Sharpe Ratio', fontsize=11, fontweight='bold')
    ax1.legend(loc='best', frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_facecolor('#f8f9fa')
    
    # Sortino Ratio
    rolling_sortino.plot(ax=ax2, linewidth=2, color='#764ba2', label='Rolling Sortino')
    ax2.axhline(y=1, color='#28a745', linestyle='--', alpha=0.7, label='Good (1.0)')
    ax2.axhline(y=0, color='#dc3545', linestyle='--', alpha=0.7)
    ax2.set_title(f'Rolling Sortino Ratio ({window}-day)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Sortino Ratio', fontsize=11, fontweight='bold')
    ax2.legend(loc='best', frameon=True, shadow=True)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_facecolor('#f8f9fa')
    
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    return fig


def plot_regime_chart(regimes, returns):
    """
    Plot market regime timeline with returns
    """
    # Ensure returns is a Series
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # Color map for regimes
    regime_colors = {
        'Bull Market (Low Vol)': '#28a745',
        'Bull Market (High Vol)': '#17a2b8',
        'Sideways/Choppy': '#ffc107',
        'Bear Market (Low Vol)': '#fd7e14',
        'Bear Market (High Vol)': '#dc3545'
    }
    
    # Plot returns
    cum_returns = (1 + returns).cumprod()
    cum_returns.plot(ax=ax1, linewidth=2, color='#667eea', label='Portfolio Value')
    ax1.set_ylabel('Cumulative Return', fontsize=12, fontweight='bold')
    ax1.set_title('Portfolio Performance Across Market Regimes', 
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='best', frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_facecolor('#f8f9fa')
    
    # Plot regimes as colored background
    for regime, color in regime_colors.items():
        mask = regimes == regime
        if mask.any():
            ax1.fill_between(returns.index, 0, 1, where=mask, 
                            transform=ax1.get_xaxis_transform(),
                            alpha=0.2, color=color, label=regime)
    
    # Create regime timeline
    regime_numeric = pd.Series(index=regimes.index, dtype=float)
    regime_map = {regime: i for i, regime in enumerate(regime_colors.keys())}
    for regime, value in regime_map.items():
        regime_numeric[regimes == regime] = value
    
    ax2.plot(regime_numeric.index, regime_numeric.values, linewidth=0)
    for regime, color in regime_colors.items():
        mask = regimes == regime
        if mask.any():
            ax2.fill_between(regimes.index, 0, 5, where=mask,
                            alpha=0.6, color=color, label=regime)
    
    ax2.set_yticks(range(len(regime_colors)))
    ax2.set_yticklabels(list(regime_colors.keys()))
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Market Regime', fontsize=12, fontweight='bold')
    ax2.set_title('Market Regime Classification', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--', axis='x')
    ax2.set_facecolor('#f8f9fa')
    
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    return fig


def plot_monte_carlo_simulation(simulations, title='Monte Carlo Simulation - 1 Year Forward'):
    """
    Plot Monte Carlo simulation results
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot individual simulations (subset for performance)
    num_to_plot = min(100, simulations.shape[1])
    for i in range(0, num_to_plot):
        ax.plot(simulations[:, i], color='#667eea', alpha=0.1, linewidth=0.5)
    
    # Calculate and plot percentiles
    percentiles = [5, 25, 50, 75, 95]
    percentile_values = np.percentile(simulations, percentiles, axis=1)
    
    colors = ['#dc3545', '#fd7e14', '#28a745', '#17a2b8', '#6c757d']
    labels = ['5th %ile (Worst Case)', '25th %ile', '50th %ile (Median)', 
              '75th %ile', '95th %ile (Best Case)']
    
    for i, (pct, color, label) in enumerate(zip(percentile_values, colors, labels)):
        ax.plot(pct, color=color, linewidth=2.5, label=label, alpha=0.9)
    
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Starting Value')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Trading Days Forward', fontsize=12, fontweight='bold')
    ax.set_ylabel('Portfolio Value (Normalized)', fontsize=12, fontweight='bold')
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    
    plt.tight_layout()
    return fig


def plot_efficient_frontier(results, optimal_weights, portfolio_return, portfolio_std):
    """
    Plot efficient frontier with enhanced styling
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter = ax.scatter(results[1,:], results[0,:], c=results[2,:], 
                        cmap='viridis', marker='o', s=50, alpha=0.6)
    ax.scatter(portfolio_std, portfolio_return, marker='*', color='red', 
              s=500, label='Current Portfolio', edgecolors='black', linewidths=2)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Sharpe Ratio', rotation=270, labelpad=20, fontweight='bold')
    
    ax.set_title('Efficient Frontier', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Volatility (Standard Deviation)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expected Return', fontsize=12, fontweight='bold')
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    
    plt.tight_layout()
    return fig


# =============================================================================
# SIDEBAR - PORTFOLIO BUILDER
# =============================================================================

st.sidebar.markdown("## 📊 Alphatic Portfolio Analyzer ✨")
st.sidebar.markdown("---")

# Portfolio Builder Section
st.sidebar.markdown("### 🔨 Build Portfolio")

# Input for new portfolio name
portfolio_name = st.sidebar.text_input("Portfolio Name", value="My Portfolio")

# Ticker input
ticker_input = st.sidebar.text_area(
    "Enter Tickers (one per line or comma-separated)",
    value="SPY\nQQQ\nAGG",
    height=100
)

# Parse tickers
if ticker_input:
    tickers_list = [t.strip().upper() for t in ticker_input.replace(',', '\n').split('\n') if t.strip()]
else:
    tickers_list = []

# Allocation method
allocation_method = st.sidebar.radio(
    "Allocation Method",
    ["Equal Weight", "Custom Weights", "Optimize (Max Sharpe)"]
)

# Custom weights if selected
custom_weights = {}
if allocation_method == "Custom Weights" and tickers_list:
    st.sidebar.markdown("**Set Custom Weights (must sum to 100%):**")
    for ticker in tickers_list:
        weight = st.sidebar.number_input(
            f"{ticker} %",
            min_value=0.0,
            max_value=100.0,
            value=100.0 / len(tickers_list),
            step=1.0,
            key=f"weight_{ticker}"
        )
        custom_weights[ticker] = weight / 100.0
    
    weight_sum = sum(custom_weights.values())
    if abs(weight_sum - 1.0) > 0.01:
        st.sidebar.warning(f"⚠️ Weights sum to {weight_sum*100:.1f}% (should be 100%)")

# Date range selection
st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Date Range")

date_method = st.sidebar.radio(
    "Start Date Method",
    ["Auto (Earliest Available)", "Custom Date"]
)

if date_method == "Custom Date":
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime(2020, 1, 1)
    )
else:
    start_date = None

end_date = st.sidebar.date_input(
    "End Date",
    value=datetime.now()
)

# Build Portfolio Button
if st.sidebar.button("🚀 Build Portfolio", type="primary"):
    if not tickers_list:
        st.sidebar.error("Please enter at least one ticker!")
    else:
        with st.spinner("Building portfolio..."):
            # Determine start date if auto
            if start_date is None:
                st.info("Determining earliest available start date...")
                auto_start_date = get_earliest_start_date(tickers_list)
                if auto_start_date:
                    start_date = auto_start_date
                    st.success(f"✅ Using earliest start date: {start_date.strftime('%Y-%m-%d')}")
                else:
                    st.error("Could not determine start date. Please use custom date.")
                    st.stop()
            
            # Download data
            prices = download_ticker_data(tickers_list, start_date, end_date)
            
            if prices is not None and not prices.empty:
                # Determine weights
                if allocation_method == "Equal Weight":
                    weights = {ticker: 1/len(tickers_list) for ticker in tickers_list}
                elif allocation_method == "Custom Weights":
                    weights = custom_weights
                else:  # Optimize
                    optimal_weights = optimize_portfolio(prices)
                    weights = {ticker: w for ticker, w in zip(tickers_list, optimal_weights)}
                
                # Calculate portfolio returns
                weights_array = np.array([weights[ticker] for ticker in prices.columns])
                portfolio_returns = calculate_portfolio_returns(prices, weights_array)
                
                # Store in session state
                st.session_state.portfolios[portfolio_name] = {
                    'tickers': tickers_list,
                    'weights': weights,
                    'prices': prices,
                    'returns': portfolio_returns,
                    'start_date': start_date,
                    'end_date': end_date
                }
                st.session_state.current_portfolio = portfolio_name
                
                st.sidebar.success(f"✅ Portfolio '{portfolio_name}' created successfully!")
                st.sidebar.info("📊 Returns include dividends reinvested (Total Return)")
            else:
                st.sidebar.error("Failed to download price data. Please check tickers and dates.")

# Portfolio Management
st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Manage Portfolios")

if st.session_state.portfolios:
    # Select portfolio
    selected_portfolio = st.sidebar.selectbox(
        "Select Portfolio",
        list(st.session_state.portfolios.keys()),
        index=list(st.session_state.portfolios.keys()).index(st.session_state.current_portfolio) 
        if st.session_state.current_portfolio else 0
    )
    st.session_state.current_portfolio = selected_portfolio
    
    # Delete portfolio
    if st.sidebar.button("🗑️ Delete Selected Portfolio"):
        del st.session_state.portfolios[selected_portfolio]
        st.session_state.current_portfolio = list(st.session_state.portfolios.keys())[0] if st.session_state.portfolios else None
        st.sidebar.success("Portfolio deleted!")
        st.rerun()
    
    # Export/Import
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Export/Import")
    
    if st.sidebar.button("📥 Export All Portfolios"):
        export_data = {}
        for name, portfolio in st.session_state.portfolios.items():
            export_data[name] = {
                'tickers': portfolio['tickers'],
                'weights': portfolio['weights'],
                'start_date': portfolio['start_date'].isoformat(),
                'end_date': portfolio['end_date'].isoformat()
            }
        
        json_str = json.dumps(export_data, indent=2)
        st.sidebar.download_button(
            label="Download portfolios.json",
            data=json_str,
            file_name="alphatic_portfolios.json",
            mime="application/json"
        )


# =============================================================================
# MAIN CONTENT AREA
# =============================================================================

# Header
st.markdown('<h1 class="main-header">Alphatic Portfolio Analyzer ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Sophisticated analysis for the educated investor</p>', unsafe_allow_html=True)

# Check if portfolio exists
if not st.session_state.current_portfolio:
    st.markdown("""
        <div class="info-box">
            <h3>👋 Welcome to Alphatic Portfolio Analyzer!</h3>
            <p style="font-size: 1.1rem;">
                Get started by building your first portfolio using the sidebar on the left.
            </p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>📊 Comprehensive portfolio analysis with detailed metrics</li>
                <li>🎯 Portfolio optimization (Maximum Sharpe Ratio)</li>
                <li>📈 PyFolio integration for professional-grade analytics</li>
                <li>🌡️ <strong>NEW:</strong> Market regime analysis across 5 conditions</li>
                <li>🔮 <strong>NEW:</strong> Forward-looking risk analysis with Monte Carlo</li>
                <li>💡 <strong>NEW:</strong> Educational tooltips for every metric</li>
                <li>⚖️ Multi-portfolio and benchmark comparisons</li>
            </ul>
            <p style="margin-top: 1rem; padding: 1rem; background-color: #e3f2fd; border-radius: 8px;">
                <strong>📊 Total Return Analysis:</strong> All performance metrics include dividends 
                reinvested and are adjusted for stock splits. This represents real-world total returns 
                you would achieve with a buy-and-hold strategy.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Get current portfolio
current = st.session_state.portfolios[st.session_state.current_portfolio]
portfolio_returns = current['returns']
prices = current['prices']
weights = current['weights']
tickers = current['tickers']

# Calculate metrics for current portfolio
metrics = calculate_portfolio_metrics(portfolio_returns)

# =============================================================================
# TABS STRUCTURE - 7 TABS
# =============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Overview",
    "📊 Detailed Analysis", 
    "📬 PyFolio Analysis",
    "🌡️ Market Regimes",
    "🔮 Forward Risk",
    "⚖️ Compare Benchmarks",
    "🎯 Optimization"
])

# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================

with tab1:
    st.markdown(f"## Portfolio: {st.session_state.current_portfolio}")
    
    # Total Return Info Box
    st.info("""
        **📊 Total Return Analysis:** All returns shown include dividends reinvested and are adjusted for stock splits. 
        This represents the actual performance you would achieve with a buy-and-hold strategy that reinvests all dividends.
    """)
    
    # Portfolio Composition
    st.markdown("### 📦 Portfolio Composition")
    col1, col2 = st.columns(2)
    
    with col1:
        # Show tickers and weights
        comp_df = pd.DataFrame({
            'Ticker': list(weights.keys()),
            'Weight': [f"{w*100:.2f}%" for w in weights.values()]
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set3(range(len(weights)))
        ax.pie(weights.values(), labels=weights.keys(), autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax.set_title('Portfolio Allocation', fontsize=14, fontweight='bold', pad=20)
        st.pyplot(fig)
    
    # Key Metrics
    st.markdown("---")
    st.markdown("### 🎯 Key Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_class = get_metric_color_class('annual_return', metrics['Annual Return'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Annual Return</h4>
                <h2>{metrics['Annual Return']:.2%}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('annual_return')
    
    with col2:
        metric_class = get_metric_color_class('sharpe_ratio', metrics['Sharpe Ratio'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Sharpe Ratio</h4>
                <h2>{metrics['Sharpe Ratio']:.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('sharpe_ratio')
    
    with col3:
        metric_class = get_metric_color_class('max_drawdown', metrics['Max Drawdown'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Max Drawdown</h4>
                <h2>{metrics['Max Drawdown']:.2%}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('max_drawdown')
    
    with col4:
        metric_class = get_metric_color_class('volatility', metrics['Annual Volatility'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Volatility</h4>
                <h2>{metrics['Annual Volatility']:.2%}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('volatility')
    
    # Additional metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_class = get_metric_color_class('sortino_ratio', metrics['Sortino Ratio'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Sortino Ratio</h4>
                <h2>{metrics['Sortino Ratio']:.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('sortino_ratio')
    
    with col2:
        metric_class = get_metric_color_class('calmar_ratio', metrics['Calmar Ratio'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Calmar Ratio</h4>
                <h2>{metrics['Calmar Ratio']:.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('calmar_ratio')
    
    with col3:
        metric_class = get_metric_color_class('win_rate', metrics['Win Rate'])
        st.markdown(f"""
            <div class="{metric_class}">
                <h4>Win Rate</h4>
                <h2>{metrics['Win Rate']:.2%}</h2>
            </div>
        """, unsafe_allow_html=True)
        render_metric_explanation('win_rate')
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Total Return</h4>
                <h2>{metrics['Total Return']:.2%}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # Performance Chart
    st.markdown("---")
    st.markdown("### 📈 Performance Over Time")
    fig = plot_cumulative_returns(portfolio_returns, f'{st.session_state.current_portfolio} - Cumulative Returns')
    st.pyplot(fig)
    
    # Chart interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 What This Chart Means</div>
            <p><strong>How to Read:</strong> This shows how $1 invested at the start grows over time. 
            A value of 1.5 means your investment grew 50%.</p>
            <p><strong>Look For:</strong> Steady upward trend = good. Sharp drops = drawdowns. 
            Flat periods = your money isn't working for you.</p>
            <p><strong>Action Item:</strong> If the line trends down over 6+ months, consider rebalancing 
            or reviewing your strategy.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Drawdown Chart
    st.markdown("---")
    st.markdown("### 📉 Drawdown Analysis")
    fig = plot_drawdown(portfolio_returns, 'Portfolio Drawdown')
    st.pyplot(fig)
    
    # Drawdown interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 Understanding Drawdowns</div>
            <p><strong>What This Shows:</strong> How much you're "underwater" from your peak value at any point in time.</p>
            <p><strong>Red Flag:</strong> If drawdown exceeds -20%, you're in bear market territory. 
            Don't panic-sell! History shows markets recover.</p>
            <p><strong>Psychology Check:</strong> Look at the deepest drawdown. Can you handle losing that much 
            without selling? If not, consider a less volatile allocation.</p>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: DETAILED ANALYSIS
# =============================================================================

with tab2:
    st.markdown("## 📊 Detailed Analysis")
    
    # Monthly Returns Heatmap
    st.markdown("### 📅 Monthly Returns Heatmap")
    fig = plot_monthly_returns_heatmap(portfolio_returns, 'Monthly Returns (%)')
    st.pyplot(fig)
    
    # Heatmap interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 How to Use This Heatmap</div>
            <p><strong>What This Shows:</strong> Each cell shows the return for that month. 
            Green = gains, Red = losses.</p>
            <p><strong>Patterns to Look For:</strong></p>
            <ul>
                <li>Seasonal trends: Some months consistently better/worse?</li>
                <li>Streaks: 3+ consecutive red months = review needed</li>
                <li>Year comparisons: Are recent years better or worse than historical?</li>
            </ul>
            <p><strong>Red Flags:</strong></p>
            <ul>
                <li>Entire rows of red (bad years - what happened?)</li>
                <li>Consistent December losses (tax-loss harvesting season)</li>
                <li>Recent months all red (time to re-evaluate strategy)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Monthly Income/Gains Table
    st.markdown("---")
    st.markdown("### 💰 Monthly Income Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Calculate dollar gains/losses per month based on portfolio value**")
    
    with col2:
        initial_capital = st.number_input(
            "Initial Portfolio Value ($)", 
            min_value=1000, 
            max_value=100000000, 
            value=100000, 
            step=10000,
            help="Enter your starting portfolio value to see dollar gains/losses"
        )
    
    # Calculate monthly dollar gains
    returns_series = portfolio_returns if isinstance(portfolio_returns, pd.Series) else portfolio_returns.iloc[:, 0]
    monthly_returns = returns_series.resample('M').apply(lambda x: (1 + x).prod() - 1)
    
    # Calculate cumulative value and monthly dollar gains
    cumulative_value = initial_capital
    monthly_data = []
    
    for date, monthly_return in monthly_returns.items():
        month_start_value = cumulative_value
        dollar_gain = month_start_value * monthly_return
        cumulative_value = month_start_value + dollar_gain
        
        monthly_data.append({
            'Date': date.strftime('%Y-%m'),
            'Month': date.strftime('%B'),
            'Year': date.year,
            'Return %': monthly_return * 100,
            'Dollar Gain/Loss': dollar_gain,
            'Portfolio Value': cumulative_value
        })
    
    monthly_df = pd.DataFrame(monthly_data)
    
    # Display options
    view_option = st.radio(
        "View:",
        ["Last 12 Months", "Current Year", "All Time", "By Year"],
        horizontal=True
    )
    
    if view_option == "Last 12 Months":
        display_df = monthly_df.tail(12).copy()
    elif view_option == "Current Year":
        current_year = datetime.now().year
        display_df = monthly_df[monthly_df['Year'] == current_year].copy()
    elif view_option == "By Year":
        selected_year = st.selectbox("Select Year:", sorted(monthly_df['Year'].unique(), reverse=True))
        display_df = monthly_df[monthly_df['Year'] == selected_year].copy()
    else:  # All Time
        display_df = monthly_df.copy()
    
    # Format for display
    display_df['Return %'] = display_df['Return %'].apply(lambda x: f"{x:+.2f}%")
    display_df['Dollar Gain/Loss'] = display_df['Dollar Gain/Loss'].apply(lambda x: f"${x:+,.2f}")
    display_df['Portfolio Value'] = display_df['Portfolio Value'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(
        display_df[['Date', 'Month', 'Return %', 'Dollar Gain/Loss', 'Portfolio Value']],
        use_container_width=True,
        hide_index=True
    )
    
    # Summary statistics
    st.markdown("#### 📊 Income Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_gain = monthly_df['Dollar Gain/Loss'].sum()
    positive_months = (monthly_df['Dollar Gain/Loss'] > 0).sum()
    negative_months = (monthly_df['Dollar Gain/Loss'] < 0).sum()
    avg_monthly_gain = monthly_df['Dollar Gain/Loss'].mean()
    
    with col1:
        st.metric(
            "Total Gain/Loss",
            f"${total_gain:,.2f}",
            f"{((cumulative_value - initial_capital) / initial_capital * 100):+.2f}%"
        )
    
    with col2:
        st.metric(
            "Avg Monthly Gain",
            f"${avg_monthly_gain:,.2f}"
        )
    
    with col3:
        st.metric(
            "Positive Months",
            f"{positive_months}",
            f"{positive_months / len(monthly_df) * 100:.1f}%"
        )
    
    with col4:
        st.metric(
            "Negative Months",
            f"{negative_months}",
            f"{negative_months / len(monthly_df) * 100:.1f}%"
        )
    
    # Tax planning insights
    st.markdown("---")
    st.info("""
        **💡 Tax Planning Tips:**
        - **Short-term gains** (held <1 year): Taxed as ordinary income (10-37%)
        - **Long-term gains** (held >1 year): Lower rates (0%, 15%, or 20%)
        - **Tax-loss harvesting**: Negative months can offset gains if you have other taxable gains
        - **Wash sale rule**: Can't repurchase same security within 30 days when harvesting losses
        - **Consult a CPA**: This is for planning only - not tax advice!
    """)
    
    # Monthly income interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 How to Use Monthly Income Data</div>
            <p><strong>For Retirement Planning:</strong></p>
            <ul>
                <li>Look at average monthly gain - is it enough to live on?</li>
                <li>Check volatility - can you handle the negative months?</li>
                <li>Win rate above 60% = more consistent income</li>
            </ul>
            <p><strong>For Tax Planning:</strong></p>
            <ul>
                <li>December losses? Good time to harvest for tax deduction</li>
                <li>Big gains in one month? Might push you into higher bracket</li>
                <li>Spread gains over multiple years if possible</li>
            </ul>
            <p><strong>For Strategy Evaluation:</strong></p>
            <ul>
                <li>Are monthly gains getting bigger or smaller over time?</li>
                <li>Do gains cluster in certain months (seasonality)?</li>
                <li>Can you emotionally handle the worst months?</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Rolling Metrics
    st.markdown("---")
    st.markdown("### 📈 Rolling Risk-Adjusted Performance")
    window = st.slider("Rolling Window (days)", min_value=20, max_value=252, value=60, step=10)
    fig = plot_rolling_metrics(portfolio_returns, window=window)
    st.pyplot(fig)
    
    # Rolling metrics interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 Understanding Rolling Metrics</div>
            <p><strong>What This Shows:</strong> How your risk-adjusted performance changes over time.</p>
            <p><strong>Sharpe Ratio:</strong> Measures returns vs ALL volatility</p>
            <ul>
                <li>Above 1.0 (green line) = Good risk-adjusted returns</li>
                <li>Consistently above 1.0 = Sustainable strategy</li>
                <li>Dropping toward 0 = Strategy losing effectiveness</li>
            </ul>
            <p><strong>Sortino Ratio:</strong> Measures returns vs DOWNSIDE volatility only</p>
            <ul>
                <li>Higher than Sharpe = Good! Means upside volatility is high</li>
                <li>Much lower than Sharpe = Too many down days</li>
            </ul>
            <p><strong>Action Items:</strong></p>
            <ul>
                <li>If both metrics trend down for 3+ months, consider rebalancing</li>
                <li>Sudden spikes after crashes = good recovery</li>
                <li>Steady improvement = strategy working</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Distribution Analysis
    st.markdown("---")
    st.markdown("### 📊 Returns Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig, ax = plt.subplots(figsize=(10, 6))
        portfolio_returns.hist(bins=50, ax=ax, color='#667eea', alpha=0.7, edgecolor='black')
        ax.axvline(portfolio_returns.mean(), color='#28a745', linestyle='--', 
                   linewidth=2, label=f'Mean: {portfolio_returns.mean():.4f}')
        ax.axvline(portfolio_returns.median(), color='#ffc107', linestyle='--', 
                   linewidth=2, label=f'Median: {portfolio_returns.median():.4f}')
        ax.set_title('Daily Returns Distribution', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Daily Return', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        st.pyplot(fig)
    
    with col2:
        # QQ Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        stats.probplot(portfolio_returns.dropna(), dist="norm", plot=ax)
        ax.set_title('Q-Q Plot (Normal Distribution Test)', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        st.pyplot(fig)
    
    # Distribution interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 What Distribution Analysis Tells You</div>
            <p><strong>Histogram (Left):</strong></p>
            <ul>
                <li>Centered around 0? Good, means positive and negative days balance</li>
                <li>Long left tail (fat negative side)? Portfolio has crash risk</li>
                <li>Long right tail (fat positive side)? Portfolio captures big gains</li>
            </ul>
            <p><strong>Q-Q Plot (Right):</strong></p>
            <ul>
                <li>Points follow red line closely? Returns are "normal" (predictable)</li>
                <li>Points curve away at ends? "Fat tails" = more extreme events than expected</li>
                <li>Lower-left points below line? More severe crashes than normal distribution predicts</li>
            </ul>
            <p><strong>Why It Matters:</strong> Standard risk models assume normal distribution. 
            If your returns aren't normal, you might have more risk than you think!</p>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 3: PYFOLIO COMPREHENSIVE ANALYSIS
# =============================================================================

with tab3:
    st.markdown("## 📬 PyFolio Professional Analysis")
    
    # What is PyFolio section
    st.markdown("""
        <div class="info-box">
            <h3>🎓 What is PyFolio?</h3>
            <p><strong>PyFolio is the institutional-grade analytics library used by hedge funds, 
            asset managers, and professional traders.</strong></p>
            <p><strong>Created by Quantopian</strong> (a professional quant hedge fund platform), 
            PyFolio is the SAME tool used by:</p>
            <ul>
                <li>📊 Hedge fund managers to evaluate their strategies</li>
                <li>💼 Institutional investors to analyze fund performance</li>
                <li>🏦 Asset management firms for client reporting</li>
                <li>📈 Quantitative researchers for strategy validation</li>
            </ul>
            <p><strong>Why is this powerful?</strong> You're getting the EXACT same analytics 
            that professional money managers pay thousands for. This is not "investor-lite" – 
            this is the real deal.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # PyFolio vs Detailed Analysis
    st.markdown("---")
    st.markdown("### 🔬 PyFolio vs. Detailed Analysis Tab")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h4>📊 Detailed Analysis Tab</h4>
                <p><strong>Focus:</strong> Easy-to-understand metrics</p>
                <p><strong>Best For:</strong></p>
                <ul>
                    <li>Quick performance check</li>
                    <li>Understanding basic patterns</li>
                    <li>Educational tooltips</li>
                    <li>Non-expert friendly</li>
                </ul>
                <p><strong>Metrics:</strong> Standard risk/return metrics with explanations</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="border-left: 5px solid #764ba2;">
                <h4>📬 PyFolio Analysis Tab</h4>
                <p><strong>Focus:</strong> Professional validation</p>
                <p><strong>Best For:</strong></p>
                <ul>
                    <li>Comparing to professionals</li>
                    <li>Institutional-grade reporting</li>
                    <li>Deep statistical analysis</li>
                    <li>Due diligence on strategies</li>
                </ul>
                <p><strong>Metrics:</strong> Comprehensive tear sheets used by hedge funds</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 When to Use Each Tab</div>
            <p><strong>Use Detailed Analysis when:</strong></p>
            <ul>
                <li>You want quick, easy-to-understand insights</li>
                <li>You're learning about portfolio metrics</li>
                <li>You need to make a quick decision</li>
                <li>You want clear action items</li>
            </ul>
            <p><strong>Use PyFolio Analysis when:</strong></p>
            <ul>
                <li>You want to validate your strategy like a professional</li>
                <li>You're comparing your performance to fund managers</li>
                <li>You need comprehensive statistics for serious money decisions</li>
                <li>You want to see if your strategy has institutional-quality metrics</li>
                <li>You're presenting performance to sophisticated investors (family office, etc.)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # What PyFolio Adds
    st.markdown("---")
    st.markdown("### 🎯 What PyFolio Adds Beyond Basic Analysis")
    
    st.markdown("""
        <div class="success-box">
            <h4>📊 Unique PyFolio Features:</h4>
            <ol>
                <li><strong>Rolling Beta & Sharpe:</strong> See how your market exposure changes over time</li>
                <li><strong>Rolling Volatility:</strong> Track when your strategy gets risky</li>
                <li><strong>Top Drawdown Periods:</strong> Identify your worst periods with exact dates</li>
                <li><strong>Underwater Plot:</strong> Visualize how long you stayed in drawdown</li>
                <li><strong>Monthly & Annual Returns Table:</strong> Complete historical breakdown</li>
                <li><strong>Distribution Analysis:</strong> Advanced statistical validation</li>
                <li><strong>Worst Drawdown Timing:</strong> Understand when pain happens</li>
            </ol>
            <p style="margin-top: 1rem;"><strong>The Bottom Line:</strong> PyFolio tells you if your 
            strategy would pass institutional due diligence. If hedge funds would invest in your 
            strategy, PyFolio will show it. If they wouldn't, PyFolio will reveal why.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Practical Decision Making Guide
    st.markdown("---")
    st.markdown("### 🎓 How to Use PyFolio for Real Portfolio Decisions")
    
    st.markdown("#### 💼 Real-World Decision Framework")
    
    # Scenario 1
    st.markdown("**Scenario 1: Should I Keep This Strategy?**")
    st.markdown("**Look for:**")
    st.markdown("""
    - **Rolling Sharpe Ratio:** Is it consistently above 0.5? Good sign.
    - **Drawdown Periods:** Do you recover within 6-12 months? Acceptable.
    - **Annual Returns Table:** More green than red years? Keep going.
    """)
    st.markdown("**Red Flags:**")
    st.markdown("""
    - Rolling Sharpe consistently below 0.3 → Strategy isn't working
    - Drawdowns last 2+ years → Too slow to recover
    - More losing years than winning years → Fundamental problem
    """)
    
    # Scenario 2
    st.markdown("**Scenario 2: Is My Strategy Better Than Just Buying SPY?**")
    st.markdown("**Look for:**")
    st.markdown("""
    - **Compare Rolling Sharpe to SPY:** Are you consistently higher? Yes = Worth it.
    - **Check Worst Drawdowns:** Are yours shallower than SPY's -30% to -50%? Good!
    - **Recovery Time:** Do you bounce back faster than SPY? Excellent.
    """)
    st.markdown("**Decision Rule:**")
    st.markdown("""
    - If Rolling Sharpe less than SPY for 2+ years → Just buy SPY (simpler, cheaper)
    - If max drawdown worse than SPY but returns aren't higher → Just buy SPY
    - If you beat SPY on risk-adjusted basis → Keep your strategy!
    """)
    
    # Scenario 3
    st.markdown("**Scenario 3: Can I Handle More Risk?**")
    st.markdown("**Look for:**")
    st.markdown("""
    - **Underwater Plot:** How long were you "underwater" (below peak)?
    - **Top 5 Drawdowns:** Look at duration (days underwater)
    - **Rolling Volatility:** Is it stable or spiky?
    """)
    st.markdown("**Decision Framework:**")
    st.markdown("""
    - If typical drawdown recovery is less than 6 months → You have capacity for more risk
    - If rolling volatility is very stable → Can add more aggressive positions
    - If you're never underwater more than 1 year → Portfolio is quite conservative
    """)
    
    # Scenario 4
    st.markdown("**Scenario 4: Presenting Performance to Financial Advisor**")
    st.markdown("**Your advisor will look at:**")
    st.markdown("""
    - **Cumulative Returns vs Drawdown:** Shows risk-adjusted growth
    - **Rolling Metrics:** Proves consistency, not luck
    - **Worst Drawdown Periods:** Shows you survived crises
    - **Annual Returns Table:** Detailed historical track record
    """)
    st.markdown("**What impresses advisors:**")
    st.markdown("""
    - Positive Sharpe in 2008, 2020, 2022 (crisis years)
    - Consistent rolling Sharpe above 1.0
    - Maximum drawdown less than 25%
    - Fast recovery from drawdowns (under 12 months)
    """)
    
    # Key Metrics to Watch
    st.markdown("---")
    st.markdown("### 📋 PyFolio Metrics Decoder")
    
    with st.expander("📊 Complete Guide to Reading PyFolio Output"):
        st.markdown("""
            <h4>Section 1: Cumulative Returns</h4>
            <ul>
                <li><strong>What it shows:</strong> Portfolio value over time (normalized to start at 1.0)</li>
                <li><strong>Look for:</strong> Steady upward trend with controlled drawdowns</li>
                <li><strong>Red flag:</strong> Long flat periods or severe drops</li>
            </ul>
            
            <h4>Section 2: Rolling Sharpe (6-month)</h4>
            <ul>
                <li><strong>What it shows:</strong> Risk-adjusted returns over time</li>
                <li><strong>Look for:</strong> Line consistently above 0.5, ideally above 1.0</li>
                <li><strong>Red flag:</strong> Frequent dips below 0 (negative risk-adjusted returns)</li>
                <li><strong>Pro tip:</strong> If this trends down over time, your strategy is degrading</li>
            </ul>
            
            <h4>Section 3: Rolling Beta</h4>
            <ul>
                <li><strong>What it shows:</strong> How much your portfolio moves with the market</li>
                <li><strong>Look for:</strong> Stability (beta doesn't swing wildly)</li>
                <li><strong>Interpretation:</strong> 
                    <ul>
                        <li>Beta increasing over time = Taking more market risk</li>
                        <li>Beta decreasing = Becoming more defensive</li>
                        <li>Stable beta = Consistent strategy</li>
                    </ul>
                </li>
            </ul>
            
            <h4>Section 4: Rolling Volatility</h4>
            <ul>
                <li><strong>What it shows:</strong> How much your returns fluctuate</li>
                <li><strong>Look for:</strong> Stable line, spikes during known crisis periods only</li>
                <li><strong>Red flag:</strong> Volatility increasing over time = Strategy becoming riskier</li>
            </ul>
            
            <h4>Section 5: Top 5 Drawdown Periods</h4>
            <ul>
                <li><strong>What it shows:</strong> Your worst losing periods with exact dates</li>
                <li><strong>Look for:</strong> 
                    <ul>
                        <li>Drawdowns aligning with known crises (2008, 2020, 2022) = Expected</li>
                        <li>Recovery time < 12 months = Good resilience</li>
                    </ul>
                </li>
                <li><strong>Red flag:</strong> 
                    <ul>
                        <li>Drawdowns during bull markets = Strategy problem</li>
                        <li>Recovery time > 24 months = Very painful</li>
                    </ul>
                </li>
            </ul>
            
            <h4>Section 6: Underwater Plot</h4>
            <ul>
                <li><strong>What it shows:</strong> How far below your peak you are at any time</li>
                <li><strong>How to read:</strong> 
                    <ul>
                        <li>0% = At new peak (best possible)</li>
                        <li>-20% = 20% below your previous high</li>
                    </ul>
                </li>
                <li><strong>Look for:</strong> Frequent returns to 0% (making new highs)</li>
                <li><strong>Red flag:</strong> Long periods deep underwater = Slow recovery</li>
            </ul>
            
            <h4>Section 7: Monthly Returns (%)</h4>
            <ul>
                <li><strong>What it shows:</strong> Returns for every month, year by year</li>
                <li><strong>Look for:</strong> More green (positive) than red (negative) months</li>
                <li><strong>Pattern analysis:</strong>
                    <ul>
                        <li>Seasonal patterns? Some strategies work better certain times of year</li>
                        <li>Recent years vs early years? Is performance degrading?</li>
                        <li>Consistent bad Decembers? Could be tax-loss harvesting effect</li>
                    </ul>
                </li>
            </ul>
            
            <h4>Section 8: Annual Returns (%)</h4>
            <ul>
                <li><strong>What it shows:</strong> Total return each year</li>
                <li><strong>Look for:</strong> Majority of years positive</li>
                <li><strong>Key benchmark:</strong> 
                    <ul>
                        <li>70%+ winning years = Very good</li>
                        <li>50-70% winning years = Good</li>
                        <li>Below 50% = Questionable</li>
                    </ul>
                </li>
            </ul>
            
            <h4>Section 9: Distribution Analysis</h4>
            <ul>
                <li><strong>What it shows:</strong> Statistical properties of your returns</li>
                <li><strong>Look for:</strong> Relatively normal distribution (bell curve)</li>
                <li><strong>Red flag:</strong> 
                    <ul>
                        <li>Fat left tail = More severe crashes than expected</li>
                        <li>High kurtosis = More extreme events than normal</li>
                    </ul>
                </li>
            </ul>
        """, unsafe_allow_html=True)
    
    # Generate PyFolio Analysis
    st.markdown("---")
    st.markdown("### 📊 Portfolio Report Card")
    st.markdown("""
        **Your portfolio graded against market benchmarks.** Grading is calibrated so the S&P 500 
        earns a solid **B grade** (since SPY beats 80% of professionals long-term). Each metric shows where  you excel and where you need improvement.
        
        **Key:** A = Beating SPY significantly | B = SPY-level (excellent!) | C = Below SPY | D/F = Poor
    """)
    
    # Calculate comprehensive metrics for grading
    def calculate_all_metrics(returns, benchmark_returns=None):
        """Calculate all metrics needed for grading"""
        metrics = calculate_portfolio_metrics(returns, benchmark_returns)
        
        # Add additional metrics for grading
        returns_series = returns if isinstance(returns, pd.Series) else returns.iloc[:, 0]
        
        # Win rate
        win_rate = (returns_series > 0).sum() / len(returns_series)
        
        # Best and worst month
        monthly_returns = returns_series.resample('M').apply(lambda x: (1 + x).prod() - 1)
        best_month = monthly_returns.max() if len(monthly_returns) > 0 else 0
        worst_month = monthly_returns.min() if len(monthly_returns) > 0 else 0
        
        # Recovery time (average days to recover from drawdown)
        cum_returns = (1 + returns_series).cumprod()
        running_max = cum_returns.expanding().max()
        drawdown = (cum_returns - running_max) / running_max
        
        # Find drawdown periods
        in_drawdown = drawdown < 0
        if in_drawdown.any():
            # Calculate average recovery time
            recovery_periods = []
            start_dd = None
            for i, (date, is_dd) in enumerate(in_drawdown.items()):
                if is_dd and start_dd is None:
                    start_dd = date
                elif not is_dd and start_dd is not None:
                    recovery_periods.append((date - start_dd).days)
                    start_dd = None
            avg_recovery_days = np.mean(recovery_periods) if recovery_periods else 0
        else:
            avg_recovery_days = 0
        
        return {
            'Annual Return': metrics['Annual Return'],
            'Sharpe Ratio': metrics['Sharpe Ratio'],
            'Sortino Ratio': metrics['Sortino Ratio'],
            'Max Drawdown': metrics['Max Drawdown'],
            'Volatility': metrics['Annual Volatility'],
            'Calmar Ratio': metrics['Calmar Ratio'],
            'Win Rate': win_rate,
            'Best Month': best_month,
            'Worst Month': worst_month,
            'Alpha': metrics.get('Alpha', 0),
            'Beta': metrics.get('Beta', 1),
            'Avg Recovery Days': avg_recovery_days
        }
    
    def grade_metric(metric_name, value):
        """
        Grade a metric A through F based on REALISTIC market benchmarks
        Calibrated so S&P 500 (SPY) earns a solid B grade
        
        Grading Philosophy:
        - A grade = Beating S&P 500 significantly (top 20% of all strategies)
        - B grade = S&P 500 level (market benchmark - already beats 80% of professionals!)
        - C grade = Below market but positive
        - D grade = Barely positive or slightly negative
        - F grade = Significantly negative or terrible risk-adjusted returns
        
        Returns: (grade, explanation)
        """
        grading_criteria = {
            'Annual Return': {
                'ranges': 'A: >12%, B: 8-12%, C: 4-8%, D: 0-4%, F: <0%',
                'A': (0.12, float('inf')),
                'B': (0.08, 0.12),
                'C': (0.04, 0.08),
                'D': (0.00, 0.04),
                'F': (-float('inf'), 0.00)
            },
            'Sharpe Ratio': {
                'ranges': 'A: >1.0, B: 0.5-1.0, C: 0.2-0.5, D: 0-0.2, F: <0',
                'A': (1.0, float('inf')),
                'B': (0.5, 1.0),
                'C': (0.2, 0.5),
                'D': (0.0, 0.2),
                'F': (-float('inf'), 0.0)
            },
            'Sortino Ratio': {
                'ranges': 'A: >1.5, B: 0.9-1.5, C: 0.5-0.9, D: 0.2-0.5, F: <0.2',
                'A': (1.5, float('inf')),
                'B': (0.9, 1.5),
                'C': (0.5, 0.9),
                'D': (0.2, 0.5),
                'F': (-float('inf'), 0.2)
            },
            'Max Drawdown': {
                'ranges': 'A: >-15%, B: -15% to -25%, C: -25% to -35%, D: -35% to -50%, F: <-50%',
                'A': (-0.15, 0),
                'B': (-0.25, -0.15),
                'C': (-0.35, -0.25),
                'D': (-0.50, -0.35),
                'F': (-float('inf'), -0.50)
            },
            'Volatility': {
                'ranges': 'A: <12%, B: 12-16%, C: 16-20%, D: 20-25%, F: >25%',
                'A': (0, 0.12),
                'B': (0.12, 0.16),
                'C': (0.16, 0.20),
                'D': (0.20, 0.25),
                'F': (0.25, float('inf'))
            },
            'Calmar Ratio': {
                'ranges': 'A: >1.0, B: 0.5-1.0, C: 0.25-0.5, D: 0.1-0.25, F: <0.1',
                'A': (1.0, float('inf')),
                'B': (0.5, 1.0),
                'C': (0.25, 0.5),
                'D': (0.1, 0.25),
                'F': (-float('inf'), 0.1)
            },
            'Win Rate': {
                'ranges': 'A: >60%, B: 55-60%, C: 50-55%, D: 45-50%, F: <45%',
                'A': (0.60, 1.0),
                'B': (0.55, 0.60),
                'C': (0.50, 0.55),
                'D': (0.45, 0.50),
                'F': (0, 0.45)
            },
            'Best Month': {
                'ranges': 'A: >12%, B: 8-12%, C: 4-8%, D: 1-4%, F: <1%',
                'A': (0.12, float('inf')),
                'B': (0.08, 0.12),
                'C': (0.04, 0.08),
                'D': (0.01, 0.04),
                'F': (-float('inf'), 0.01)
            },
            'Worst Month': {
                'ranges': 'A: >-8%, B: -8% to -12%, C: -12% to -16%, D: -16% to -20%, F: <-20%',
                'A': (-0.08, 0),
                'B': (-0.12, -0.08),
                'C': (-0.16, -0.12),
                'D': (-0.20, -0.16),
                'F': (-float('inf'), -0.20)
            },
            'Alpha': {
                'ranges': 'A: >2%, B: 0.5-2%, C: -0.5% to 0.5%, D: -2% to -0.5%, F: <-2%',
                'A': (0.02, float('inf')),
                'B': (0.005, 0.02),
                'C': (-0.005, 0.005),
                'D': (-0.02, -0.005),
                'F': (-float('inf'), -0.02)
            },
            'Beta': {
                'ranges': 'A: 0.85-1.15, B: 0.7-0.85 or 1.15-1.3, C: 0.5-0.7 or 1.3-1.5, D: 0.3-0.5 or 1.5-1.7, F: <0.3 or >1.7',
                'A': [(0.85, 1.15)],
                'B': [(0.7, 0.85), (1.15, 1.3)],
                'C': [(0.5, 0.7), (1.3, 1.5)],
                'D': [(0.3, 0.5), (1.5, 1.7)],
                'F': [(0, 0.3), (1.7, float('inf'))]
            },
            'Avg Recovery Days': {
                'ranges': 'A: <120 days, B: 120-240 days, C: 240-365 days, D: 365-540 days, F: >540 days',
                'A': (0, 120),
                'B': (120, 240),
                'C': (240, 365),
                'D': (365, 540),
                'F': (540, float('inf'))
            }
        }
        
        if metric_name not in grading_criteria:
            return 'N/A', grading_criteria.get(metric_name, {}).get('ranges', 'N/A')
        
        criteria = grading_criteria[metric_name]
        ranges_explanation = criteria['ranges']
        
        # Special handling for Beta (multiple ranges per grade)
        if metric_name == 'Beta':
            for grade in ['A', 'B', 'C', 'D', 'F']:
                for low, high in criteria[grade]:
                    if low <= value < high:
                        return grade, ranges_explanation
            return 'F', ranges_explanation
        
        # Standard handling for other metrics
        for grade in ['A', 'B', 'C', 'D', 'F']:
            low, high = criteria[grade]
            if low <= value < high:
                return grade, ranges_explanation
        
        return 'F', ranges_explanation
    
    def calculate_overall_grade(grades):
        """
        Calculate overall grade with weighting (hedge fund emphasis)
        
        Weighting:
        - Sharpe Ratio: 25% (most important - risk-adjusted return)
        - Alpha: 20% (value added vs benchmark)
        - Max Drawdown: 15% (downside protection)
        - Annual Return: 15% (absolute performance)
        - Sortino Ratio: 10% (downside risk)
        - Calmar Ratio: 5%
        - Volatility: 5%
        - Win Rate: 3%
        - Beta: 2%
        - Others: 5% combined
        """
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'N/A': 2.0}
        
        weights = {
            'Sharpe Ratio': 0.25,
            'Alpha': 0.20,
            'Max Drawdown': 0.15,
            'Annual Return': 0.15,
            'Sortino Ratio': 0.10,
            'Calmar Ratio': 0.05,
            'Volatility': 0.05,
            'Win Rate': 0.03,
            'Beta': 0.02
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for metric, grade in grades.items():
            weight = weights.get(metric, 0.005)  # Small weight for others
            weighted_sum += grade_points.get(grade, 2.0) * weight
            total_weight += weight
        
        gpa = weighted_sum / total_weight if total_weight > 0 else 2.0
        
        # Convert GPA to letter grade
        if gpa >= 3.5:
            return 'A', gpa
        elif gpa >= 2.5:
            return 'B', gpa
        elif gpa >= 1.5:
            return 'C', gpa
        elif gpa >= 0.5:
            return 'D', gpa
        else:
            return 'F', gpa
    
    # Calculate all metrics
    try:
        # Get benchmark for Alpha/Beta if available
        benchmark_returns = None
        try:
            spy_data = download_ticker_data(['SPY'], current['start_date'], current['end_date'])
            if spy_data is not None:
                benchmark_returns = spy_data.pct_change().dropna().iloc[:, 0]
        except:
            pass
        
        all_metrics = calculate_all_metrics(portfolio_returns, benchmark_returns)
        
        # Build grading table
        grading_data = []
        grades_dict = {}
        
        for metric_name, value in all_metrics.items():
            grade, ranges = grade_metric(metric_name, value)
            grades_dict[metric_name] = grade
            
            # Format value based on metric type
            if metric_name in ['Annual Return', 'Volatility', 'Best Month', 'Worst Month', 'Alpha']:
                formatted_value = f"{value:.2%}"
            elif metric_name in ['Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio', 'Beta']:
                formatted_value = f"{value:.2f}"
            elif metric_name == 'Max Drawdown':
                formatted_value = f"{value:.2%}"
            elif metric_name == 'Win Rate':
                formatted_value = f"{value:.1%}"
            elif metric_name == 'Avg Recovery Days':
                formatted_value = f"{value:.0f} days"
            else:
                formatted_value = f"{value:.2f}"
            
            # Color code the grade
            grade_color = {
                'A': '🟢',
                'B': '🟡', 
                'C': '🟠',
                'D': '🔴',
                'F': '⛔'
            }
            
            grading_data.append({
                'Metric': metric_name,
                'Grading Scale': ranges,
                'Your Value': formatted_value,
                'Grade': f"{grade_color.get(grade, '')} {grade}"
            })
        
        # Calculate overall grade
        overall_letter, gpa = calculate_overall_grade(grades_dict)
        
        # Display the table
        grading_df = pd.DataFrame(grading_data)
        
        # Style the dataframe
        st.dataframe(
            grading_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Overall Grade Display
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            grade_color_map = {
                'A': 'success',
                'B': 'info',
                'C': 'warning',
                'D': 'error',
                'F': 'error'
            }
            
            grade_emoji = {
                'A': '🏆',
                'B': '✅',
                'C': '⚠️',
                'D': '❌',
                'F': '⛔'
            }
            
            grade_message = {
                'A': 'Outstanding! You are beating the S&P 500 - doing better than 80%+ of professionals!',
                'B': 'Excellent! S&P 500 level performance (already beats 80% of professionals long-term).',
                'C': 'Below Market. Consider if active management is worth the effort vs. just buying SPY.',
                'D': 'Significantly Below Market. Strategy needs major improvement.',
                'F': 'Poor Performance. Switch to index funds (SPY/VOO) - simpler and better.'
            }
            
            st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; color: white;">
                    <h1 style="margin: 0; font-size: 4rem;">{grade_emoji[overall_letter]}</h1>
                    <h2 style="margin: 0.5rem 0;">Overall Grade: {overall_letter}</h2>
                    <p style="margin: 0; font-size: 1.2rem;">GPA: {gpa:.2f} / 4.0</p>
                    <p style="margin-top: 1rem; font-size: 1.1rem;">{grade_message[overall_letter]}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Grade interpretation
        st.markdown("---")
        st.markdown("#### 📖 Understanding Your Grades")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                **Grade Scale (Calibrated to S&P 500 = B):**
                - 🟢 **A (4.0):** Beating S&P 500 - You're outperforming 80%+ of professionals!
                - 🟡 **B (3.0):** S&P 500 level - Excellent (beats 80% of pros long-term)
                - 🟠 **C (2.0):** Below market - Consider switching to SPY
                - 🔴 **D (1.0):** Significantly below market - Needs major changes
                - ⛔ **F (0.0):** Poor - Just buy SPY/VOO instead
                
                **Remember:** Getting a B means you're doing as well as the best long-term 
                investment! Most active managers fail to achieve this.
            """)
        
        with col2:
            st.markdown("""
                **Overall Grade Weighting (Hedge Fund Standard):**
                - Sharpe Ratio: 25% (Risk-adjusted returns)
                - Alpha: 20% (Value added vs. market)
                - Max Drawdown: 15% (Downside protection)
                - Annual Return: 15% (Absolute performance)
                - Other metrics: 25% (Sortino, Calmar, etc.)
            """)
        
        # Action items based on grade
        st.markdown("---")
        st.markdown("#### 🎯 What Your Grade Means for Action")
        
        if overall_letter == 'A':
            st.success("""
                **Grade A - Outstanding Performance!**
                
                ✅ **What to do:**
                - Document this performance (you're beating professionals!)
                - Maintain current strategy with quarterly rebalancing
                - Consider if you can handle slight increase in risk for potentially higher returns
                - Share this report card with your financial advisor
                
                ⚠️ **Caution:**
                - Don't get overconfident - markets change
                - Ensure you can still handle the max drawdown emotionally
                - Monitor for strategy degradation (check rolling Sharpe)
            """)
        elif overall_letter == 'B':
            st.info("""
                **Grade B - Very Good Performance!**
                
                ✅ **What to do:**
                - You're beating most professionals - well done!
                - Look for specific C or D grades to improve
                - Continue current strategy with confidence
                - Monitor monthly to ensure performance persists
                
                💡 **Improvement Areas:**
                - Check which metrics are C or below
                - Consider minor optimization (Tab 7)
                - Compare to benchmarks (Tab 6) for validation
            """)
        elif overall_letter == 'C':
            st.warning("""
                **Grade C - Acceptable but Room for Improvement**
                
                ⚠️ **What to do:**
                - Review metrics graded D or F - these need attention
                - Compare to simple strategies (60/40, SPY)
                - Consider if complexity is worth the effort
                - Use Tab 7 (Optimization) to explore improvements
                
                🔍 **Key Questions:**
                - Are you beating SPY? If not, why not just buy SPY?
                - Is your Sharpe Ratio > 0.5? If not, too much risk for return
                - Can you emotionally handle the max drawdown?
            """)
        else:  # D or F
            st.error("""
                **Grade D/F - Performance Needs Major Improvement**
                
                🚨 **Immediate Actions:**
                1. **Stop and reassess** - Don't throw good money after bad
                2. **Check Tab 6** - Are you underperforming simple strategies?
                3. **Review Tab 4** - Are you in wrong regime for your strategy?
                4. **Consider alternatives:**
                   - Switch to 60/40 portfolio (simple, proven)
                   - Buy SPY index fund (beats 80% of pros long-term)
                   - Hire a professional advisor
                
                ⚠️ **Reality Check:**
                - If multiple metrics are F, strategy is fundamentally flawed
                - Don't let losses compound - cut losses and restart
                - Sometimes simplest solution (index funds) is best
            """)
        
    except Exception as e:
        st.error(f"Error calculating portfolio grades: {str(e)}")
        st.info("Ensure your portfolio has sufficient data for grading (6+ months recommended)")
    
    # Generate PyFolio Analysis
    st.markdown("---")
    st.markdown("### 📈 Your Professional Tear Sheet")
    
    try:
        # Ensure returns is a Series with datetime index
        returns_series = portfolio_returns.copy()
        if isinstance(returns_series, pd.DataFrame):
            returns_series = returns_series.iloc[:, 0]
        
        with st.spinner("Generating institutional-grade analytics..."):
            fig = pf.create_returns_tear_sheet(returns_series, return_fig=True)
            if fig is not None:
                st.pyplot(fig)
            else:
                st.warning("Could not generate returns tear sheet")
        
        st.markdown("#### 💡 How to Interpret Your Results")
        st.markdown("**Quick Assessment (30 seconds):**")
        st.markdown("""
        1. Look at Annual Returns table → Are most years positive? ✅ or ❌
        2. Check Rolling Sharpe → Is it mostly above 0.5? ✅ or ❌
        3. Review Top 5 Drawdowns → Do you recover within 12 months? ✅ or ❌
        """)
        
        st.success("**If all three are ✅:** You have an institutionally-valid strategy!")
        st.warning("**If any are ❌:** Review the specific section above to understand what needs improvement.")
        
        st.markdown("**Next Steps:**")
        st.markdown("""
        - **If metrics are strong:** Document this analysis! You now have proof 
          your strategy works at a professional level.
        - **If metrics are weak:** Use Tab 7 (Optimization) to explore improvements, 
          or consider a simpler approach (60/40 or SPY).
        - **If metrics are mixed:** Identify the specific weakness (e.g., slow recovery, 
          high volatility) and adjust your allocation accordingly.
        """)
        
        # Professional comparison
        st.markdown("---")
        st.markdown("### 🏆 How Do You Compare to Professionals?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <h4>Hedge Fund Benchmark</h4>
                    <p><strong>Typical Performance:</strong></p>
                    <ul>
                        <li>Annual Return: 8-12%</li>
                        <li>Sharpe Ratio: 0.8-1.5</li>
                        <li>Max Drawdown: -15% to -25%</li>
                        <li>Win Rate: 60-70%</li>
                    </ul>
                    <p style="font-size: 0.9rem; margin-top: 1rem;">
                    <em>If you beat these, you're performing at hedge fund level!</em></p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <h4>Warren Buffett Benchmark</h4>
                    <p><strong>Berkshire Hathaway:</strong></p>
                    <ul>
                        <li>Annual Return: ~20% (historical)</li>
                        <li>Sharpe Ratio: ~0.8</li>
                        <li>Max Drawdown: -50% (2008)</li>
                        <li>Win Rate: ~70%</li>
                    </ul>
                    <p style="font-size: 0.9rem; margin-top: 1rem;">
                    <em>Even Buffett has had severe drawdowns. You're in good company.</em></p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <h4>S&P 500 Benchmark</h4>
                    <p><strong>Index Performance:</strong></p>
                    <ul>
                        <li>Annual Return: ~10%</li>
                        <li>Sharpe Ratio: ~0.5-0.7</li>
                        <li>Max Drawdown: -56% (2008)</li>
                        <li>Win Rate: ~55%</li>
                    </ul>
                    <p style="font-size: 0.9rem; margin-top: 1rem;">
                    <em>If you can't beat this, just buy SPY. That's okay!</em></p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="success-box">
                <h4>🎯 Reality Check</h4>
                <p><strong>Professional investors fail to beat SPY 80-90% of the time over 10+ years.</strong></p>
                <p>If your PyFolio tear sheet shows you beating SPY on a risk-adjusted basis (Sharpe ratio), 
                you're doing better than most professionals. Be proud of that!</p>
                <p><strong>Key Insight:</strong> It's not about having the highest returns. It's about having 
                good risk-adjusted returns that you can stick with through market cycles. PyFolio shows you 
                if your strategy is sustainable long-term.</p>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error generating PyFolio analysis: {str(e)}")
        st.info("Note: PyFolio requires sufficient historical data (typically 6+ months)")
        
        st.markdown("""
            <div class="warning-box">
                <h4>⚠️ Troubleshooting</h4>
                <p>If PyFolio fails to generate:</p>
                <ul>
                    <li>Ensure you have at least 6 months of data</li>
                    <li>Check that your portfolio has daily returns</li>
                    <li>Verify date range includes sufficient trading days</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 4: MARKET REGIMES (NEW!)
# =============================================================================

with tab4:
    st.markdown("## 🌡️ Market Conditions & Regime Analysis")
    st.markdown("""
        <div class="info-box">
            <h4>What Are Market Regimes?</h4>
            <p>Markets behave differently in different conditions. Understanding which "regime" 
            you're in helps you know if your strategy is working as expected.</p>
            <p><strong>The 5 Regimes:</strong></p>
            <ol>
                <li><strong>🟢 Bull Market (Low Vol):</strong> Goldilocks - steady gains, low stress</li>
                <li><strong>🔵 Bull Market (High Vol):</strong> Winning but volatile - gains with anxiety</li>
                <li><strong>🟡 Sideways/Choppy:</strong> Going nowhere - range-bound, frustrating</li>
                <li><strong>🟠 Bear Market (Low Vol):</strong> Slow bleed - gradual decline</li>
                <li><strong>🔴 Bear Market (High Vol):</strong> Crisis mode - crashes and panic</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    # Detect regimes
    with st.spinner("Analyzing market regimes..."):
        regimes = detect_market_regimes(portfolio_returns, lookback=60)
        regime_stats = analyze_regime_performance(portfolio_returns, regimes)
    
    # Current Regime
    st.markdown("---")
    st.markdown("### 🎯 Current Market Regime")
    current_regime = regimes.iloc[-1]
    
    regime_colors = {
        'Bull Market (Low Vol)': '#28a745',
        'Bull Market (High Vol)': '#17a2b8',
        'Sideways/Choppy': '#ffc107',
        'Bear Market (Low Vol)': '#fd7e14',
        'Bear Market (High Vol)': '#dc3545'
    }
    
    regime_descriptions = {
        'Bull Market (Low Vol)': {
            'emoji': '🟢',
            'status': 'Excellent',
            'description': 'Best conditions for investing. Steady gains with low stress. Stay invested!',
            'action': 'Maintain current allocation. Consider adding to positions on minor dips.'
        },
        'Bull Market (High Vol)': {
            'emoji': '🔵',
            'status': 'Good but Volatile',
            'description': 'Making gains but with bumpy ride. Normal during strong growth phases.',
            'action': 'Stay the course. Volatility is creating buying opportunities. Don\'t sell on dips.'
        },
        'Sideways/Choppy': {
            'emoji': '🟡',
            'status': 'Neutral',
            'description': 'Market is range-bound. Frustrating but not dangerous.',
            'action': 'Be patient. Avoid chasing momentum. Good time for rebalancing.'
        },
        'Bear Market (Low Vol)': {
            'emoji': '🟠',
            'status': 'Caution',
            'description': 'Slow grind lower. Early warning sign of potential trouble.',
            'action': 'Review portfolio. Consider raising cash or adding defensive positions.'
        },
        'Bear Market (High Vol)': {
            'emoji': '🔴',
            'status': 'Crisis Mode',
            'description': 'High stress period with significant losses. Historically temporary.',
            'action': 'DO NOT PANIC SELL! Historically the best buying opportunity. Deep breaths.'
        }
    }
    
    regime_info = regime_descriptions[current_regime]
    
    st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid {regime_colors[current_regime]};">
            <h2>{regime_info['emoji']} {current_regime}</h2>
            <h3>Status: {regime_info['status']}</h3>
            <p style="font-size: 1.1rem; margin-top: 1rem;"><strong>What This Means:</strong> 
            {regime_info['description']}</p>
            <p style="font-size: 1.1rem; margin-top: 1rem;"><strong>🎯 Action Item:</strong> 
            {regime_info['action']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Regime Timeline
    st.markdown("---")
    st.markdown("### 📊 Regime Timeline & Performance")
    fig = plot_regime_chart(regimes, portfolio_returns)
    st.pyplot(fig)
    
    # Regime timeline interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 How to Read the Regime Chart</div>
            <p><strong>Top Chart:</strong> Your portfolio value with colored backgrounds showing regimes</p>
            <p><strong>Bottom Chart:</strong> Timeline of regime changes</p>
            <p><strong>Key Insights to Look For:</strong></p>
            <ul>
                <li><strong>Big gains in green zones:</strong> Portfolio is working as designed</li>
                <li><strong>Losses in red zones:</strong> Expected, but how bad compared to benchmark?</li>
                <li><strong>Flat in yellow zones:</strong> Your capital is idle - frustrating but safe</li>
                <li><strong>Quick regime switches:</strong> Market is uncertain, be careful</li>
                <li><strong>Long red zones:</strong> True bear markets - historical best buying opportunity</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Performance by Regime
    st.markdown("---")
    st.markdown("### 📈 Performance by Regime")
    
    # Format the dataframe for display
    regime_stats_display = regime_stats.copy()
    regime_stats_display['Avg Daily Return'] = regime_stats_display['Avg Daily Return'].apply(lambda x: f"{x:.4f}")
    regime_stats_display['Volatility'] = regime_stats_display['Volatility'].apply(lambda x: f"{x:.2%}")
    regime_stats_display['Best Day'] = regime_stats_display['Best Day'].apply(lambda x: f"{x:.2%}")
    regime_stats_display['Worst Day'] = regime_stats_display['Worst Day'].apply(lambda x: f"{x:.2%}")
    regime_stats_display['Win Rate'] = regime_stats_display['Win Rate'].apply(lambda x: f"{x:.2%}")
    
    # Color-code the table
    def color_regime(val):
        color = regime_colors.get(val, '#f8f9fa')
        return f'background-color: {color}; color: white; font-weight: bold'
    
    styled_df = regime_stats_display.style.applymap(
        color_regime, subset=['Regime']
    )
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Regime performance interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 How to Use Regime Performance Data</div>
            <p><strong>What Each Column Means:</strong></p>
            <ul>
                <li><strong>Occurrences:</strong> How many days in each regime</li>
                <li><strong>Avg Daily Return:</strong> Typical daily move in that regime</li>
                <li><strong>Volatility:</strong> Annualized volatility (stress level)</li>
                <li><strong>Best/Worst Day:</strong> Extreme moves to expect</li>
                <li><strong>Win Rate:</strong> % of positive days</li>
            </ul>
            <p><strong>Key Questions to Ask:</strong></p>
            <ul>
                <li>Do you make money in bull markets? (You should!)</li>
                <li>How bad are losses in bear markets vs benchmark?</li>
                <li>Is volatility acceptable in each regime?</li>
                <li>Win rate > 50% in bull markets? Good sign.</li>
                <li>Win rate < 40% in bear markets? Portfolio may need defensive assets.</li>
            </ul>
            <p><strong>🚩 Red Flags:</strong></p>
            <ul>
                <li>Negative returns in Bull Market (Low Vol) - strategy is broken</li>
                <li>Higher losses in Bear Market (High Vol) than benchmark - insufficient protection</li>
                <li>Low win rate across all regimes - strategy is too volatile for you</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 5: FORWARD-LOOKING RISK ANALYSIS (NEW!)
# =============================================================================

with tab5:
    st.markdown("## 🔮 Forward-Looking Risk Analysis")
    st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Important Disclaimer</h4>
            <p><strong>Past performance does not guarantee future results.</strong> 
            This analysis projects future risks based on historical behavior, but markets can change.</p>
            <p>Use these projections as one tool among many for decision-making, not as a crystal ball.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate forward-looking metrics
    with st.spinner("Running forward-looking analysis..."):
        forward_metrics = calculate_forward_risk_metrics(portfolio_returns)
    
    # Expected Metrics
    st.markdown("---")
    st.markdown("### 📊 Expected Performance (Next 12 Months)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        expected_return = forward_metrics['Expected Annual Return']
        color_class = 'metric-excellent' if expected_return > 0.10 else 'metric-good' if expected_return > 0.05 else 'metric-fair'
        st.markdown(f"""
            <div class="{color_class}">
                <h4>Expected Return</h4>
                <h2>{expected_return:.2%}</h2>
                <p style="margin-top: 0.5rem;">Based on historical avg</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        expected_vol = forward_metrics['Expected Volatility']
        color_class = 'metric-excellent' if expected_vol < 0.15 else 'metric-good' if expected_vol < 0.20 else 'metric-fair'
        st.markdown(f"""
            <div class="{color_class}">
                <h4>Expected Volatility</h4>
                <h2>{expected_vol:.2%}</h2>
                <p style="margin-top: 0.5rem;">Expected fluctuation</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        prob_loss = forward_metrics['Probability of Daily Loss']
        color_class = 'metric-excellent' if prob_loss < 0.40 else 'metric-good' if prob_loss < 0.45 else 'metric-fair'
        st.markdown(f"""
            <div class="{color_class}">
                <h4>Daily Loss Probability</h4>
                <h2>{prob_loss:.1%}</h2>
                <p style="margin-top: 0.5rem;">Chance of down day</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        est_max_dd = forward_metrics['Estimated Max Drawdown']
        color_class = 'metric-excellent' if est_max_dd > -0.15 else 'metric-good' if est_max_dd > -0.25 else 'metric-poor'
        st.markdown(f"""
            <div class="{color_class}">
                <h4>Est. Max Drawdown</h4>
                <h2>{est_max_dd:.2%}</h2>
                <p style="margin-top: 0.5rem;">Worst case scenario</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Risk Metrics
    st.markdown("---")
    st.markdown("### 🎯 Value at Risk (VaR) Analysis")
    st.markdown("""
        <div class="info-box">
            <p><strong>Value at Risk (VaR)</strong> answers: "How much could I lose on a bad day?"</p>
            <p><strong>Conditional VaR (CVaR)</strong> answers: "If that bad day happens, how much worse could it get?"</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 95% Confidence Level")
        var_95 = forward_metrics['VaR (95%)']
        cvar_95 = forward_metrics['CVaR (95%)']
        
        st.markdown(f"""
            <div class="metric-card">
                <h4>VaR (95%)</h4>
                <h2>{var_95:.2%}</h2>
                <p style="margin-top: 1rem;">
                <strong>What this means:</strong> On 95% of days, your loss won't be worse than this.
                Or said differently: Only 1 in 20 days (5%) will be worse than this.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card" style="margin-top: 1rem;">
                <h4>CVaR (95%)</h4>
                <h2>{cvar_95:.2%}</h2>
                <p style="margin-top: 1rem;">
                <strong>What this means:</strong> On those 5% worst days, this is the AVERAGE loss.
                This is your "expected bad day" loss.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 99% Confidence Level")
        var_99 = forward_metrics['VaR (99%)']
        cvar_99 = forward_metrics['CVaR (99%)']
        
        st.markdown(f"""
            <div class="metric-card">
                <h4>VaR (99%)</h4>
                <h2>{var_99:.2%}</h2>
                <p style="margin-top: 1rem;">
                <strong>What this means:</strong> On 99% of days, your loss won't be worse than this.
                Only 1 in 100 days (1%) will be worse.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card" style="margin-top: 1rem;">
                <h4>CVaR (99%)</h4>
                <h2>{cvar_99:.2%}</h2>
                <p style="margin-top: 1rem;">
                <strong>What this means:</strong> On those 1% worst days, this is the AVERAGE loss.
                This is your "tail risk" exposure.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # VaR interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 How to Use VaR in Real Life</div>
            <p><strong>Example with $100,000 Portfolio:</strong></p>
            <ul>
                <li>VaR (95%) = -2.5% → On 95% of days, you'll lose less than $2,500</li>
                <li>CVaR (95%) = -3.5% → On the 5% worst days, average loss is $3,500</li>
                <li>VaR (99%) = -4.0% → Only 1% of days lose more than $4,000</li>
                <li>CVaR (99%) = -5.5% → On the very worst 1% of days, average loss is $5,500</li>
            </ul>
            <p><strong>Questions to Ask Yourself:</strong></p>
            <ul>
                <li>Can I emotionally handle the CVaR (95%) loss regularly?</li>
                <li>Can I financially survive the CVaR (99%) loss?</li>
                <li>Do I have enough liquidity to avoid selling at a loss?</li>
            </ul>
            <p><strong>🚩 Red Flags:</strong></p>
            <ul>
                <li>CVaR (95%) > -5%: You'll experience painful days frequently</li>
                <li>CVaR (99%) > -10%: Your worst days are VERY bad</li>
                <li>If these numbers scare you, your portfolio is too aggressive</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Monte Carlo Simulation
    st.markdown("---")
    st.markdown("### 🎲 Monte Carlo Simulation (1 Year Forward)")
    st.markdown("""
        <div class="info-box">
            <p><strong>What is Monte Carlo?</strong> We run 1,000+ possible future scenarios based on your 
            portfolio's historical behavior. This shows the range of possible outcomes.</p>
            <p><strong>How to read:</strong> The fan of lines shows possible paths. The colored lines show 
            key percentiles (5th to 95th). The wider the fan, the more uncertain the future.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Running Monte Carlo simulation (this may take a moment)..."):
        simulations = monte_carlo_simulation(portfolio_returns, days_forward=252, num_simulations=1000)
    
    fig = plot_monte_carlo_simulation(simulations)
    st.pyplot(fig)
    
    # Monte Carlo interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 Understanding Monte Carlo Results</div>
            <p><strong>The Lines Explained:</strong></p>
            <ul>
                <li><strong>Green (50th %ile):</strong> Median outcome - "most likely" path</li>
                <li><strong>Dark Blue (25th & 75th %ile):</strong> "Typical" range of outcomes</li>
                <li><strong>Orange (5th %ile):</strong> Bad luck scenario - 95% chance of doing better</li>
                <li><strong>Gray (95th %ile):</strong> Good luck scenario - 95% chance of doing worse</li>
            </ul>
            <p><strong>What to Look For:</strong></p>
            <ul>
                <li><strong>Wide fan:</strong> High uncertainty, hard to predict</li>
                <li><strong>Narrow fan:</strong> More predictable outcomes</li>
                <li><strong>Most lines above 1.0:</strong> Positive expected returns</li>
                <li><strong>5th %ile below 0.85:</strong> Significant risk of 15%+ loss</li>
            </ul>
            <p><strong>Real-World Use:</strong></p>
            <ul>
                <li>Planning to retire next year? Look at 5th percentile - can you afford that outcome?</li>
                <li>Young investor? Focus on median and 75th percentile - you have time</li>
                <li>Need the money in 1 year? If 25th percentile is below 0.95, you have risk</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Scenario Analysis
    st.markdown("---")
    st.markdown("### 📊 Scenario Analysis (1 Year Forward)")
    
    final_values = simulations[-1, :]
    scenarios = {
        'Best Case (95th %ile)': np.percentile(final_values, 95),
        'Good Case (75th %ile)': np.percentile(final_values, 75),
        'Median Case (50th %ile)': np.percentile(final_values, 50),
        'Bad Case (25th %ile)': np.percentile(final_values, 25),
        'Worst Case (5th %ile)': np.percentile(final_values, 5)
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        scenario_df = pd.DataFrame({
            'Scenario': scenarios.keys(),
            'Portfolio Value': [f"${v:.2f}" for v in scenarios.values()],
            'Return': [f"{(v-1)*100:.1f}%" for v in scenarios.values()]
        })
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h4>Probability Analysis</h4>
                <p style="margin-top: 1rem;">
                    <strong>Make Money:</strong><br>
                    {:.1f}% chance<br><br>
                    <strong>Lose Money:</strong><br>
                    {:.1f}% chance<br><br>
                    <strong>Lose > 10%:</strong><br>
                    {:.1f}% chance
                </p>
            </div>
        """.format(
            (final_values > 1.0).sum() / len(final_values) * 100,
            (final_values < 1.0).sum() / len(final_values) * 100,
            (final_values < 0.9).sum() / len(final_values) * 100
        ), unsafe_allow_html=True)
    
    # Scenario interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 Using Scenarios for Decision-Making</div>
            <p><strong>Example: Planning with $100,000</strong></p>
            <ul>
                <li><strong>Best Case:</strong> Portfolio grows to $115,000 (15% gain) - Happy days!</li>
                <li><strong>Median Case:</strong> Portfolio grows to $107,000 (7% gain) - Acceptable</li>
                <li><strong>Worst Case:</strong> Portfolio drops to $92,000 (8% loss) - Ouch, but survivable?</li>
            </ul>
            <p><strong>Decision Framework:</strong></p>
            <ul>
                <li><strong>Can't afford worst case?</strong> Portfolio is too aggressive. Add bonds/cash.</li>
                <li><strong>Comfortable with worst case?</strong> You're properly positioned.</li>
                <li><strong>Disappointed by median case?</strong> Need more risk for your goals.</li>
            </ul>
            <p><strong>Important Reality Check:</strong></p>
            <ul>
                <li>These scenarios assume historical patterns continue</li>
                <li>Black swan events (2008, COVID) can exceed worst case</li>
                <li>Keep 6-12 months expenses in cash regardless of scenarios</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 6: COMPARE BENCHMARKS
# =============================================================================

with tab6:
    st.markdown("## ⚖️ Compare Against Benchmarks")
    
    # Benchmark selection
    st.markdown("### 📊 Select Benchmarks to Compare")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        compare_spy = st.checkbox("SPY (S&P 500)", value=True)
    with col2:
        compare_6040 = st.checkbox("60/40 Portfolio", value=True)
    with col3:
        compare_agg = st.checkbox("AGG (Bonds)", value=False)
    
    # Download benchmark data
    benchmarks_to_compare = {}
    
    if compare_spy:
        spy_data = download_ticker_data(['SPY'], current['start_date'], current['end_date'])
        if spy_data is not None:
            spy_returns = spy_data.pct_change().dropna()
            benchmarks_to_compare['SPY'] = spy_returns.iloc[:, 0] if isinstance(spy_returns, pd.DataFrame) else spy_returns
    
    if compare_6040:
        # Create 60/40 portfolio
        spy_data = download_ticker_data(['SPY'], current['start_date'], current['end_date'])
        agg_data = download_ticker_data(['AGG'], current['start_date'], current['end_date'])
        
        if spy_data is not None and agg_data is not None:
            combined_data = pd.DataFrame({
                'SPY': spy_data.iloc[:, 0] if isinstance(spy_data, pd.DataFrame) else spy_data,
                'AGG': agg_data.iloc[:, 0] if isinstance(agg_data, pd.DataFrame) else agg_data
            }).dropna()
            
            portfolio_6040 = calculate_portfolio_returns(combined_data, np.array([0.6, 0.4]))
            benchmarks_to_compare['60/40'] = portfolio_6040
    
    if compare_agg:
        agg_data = download_ticker_data(['AGG'], current['start_date'], current['end_date'])
        if agg_data is not None:
            agg_returns = agg_data.pct_change().dropna()
            benchmarks_to_compare['AGG'] = agg_returns.iloc[:, 0] if isinstance(agg_returns, pd.DataFrame) else agg_returns
    
    if not benchmarks_to_compare:
        st.warning("Please select at least one benchmark to compare")
    else:
        # Performance Comparison
        st.markdown("---")
        st.markdown("### 📈 Cumulative Performance Comparison")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Plot portfolio
        cum_returns_portfolio = (1 + portfolio_returns).cumprod()
        cum_returns_portfolio.plot(ax=ax, linewidth=3, label='Your Portfolio', color='#667eea')
        
        # Plot benchmarks
        colors = ['#28a745', '#dc3545', '#ffc107', '#17a2b8']
        for i, (name, returns) in enumerate(benchmarks_to_compare.items()):
            cum_returns_bench = (1 + returns).cumprod()
            cum_returns_bench.plot(ax=ax, linewidth=2, label=name, 
                                  color=colors[i % len(colors)], linestyle='--', alpha=0.8)
        
        ax.set_title('Performance Comparison vs Benchmarks', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cumulative Return', fontsize=12, fontweight='bold')
        ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Performance comparison interpretation
        st.markdown("""
            <div class="interpretation-box">
                <div class="interpretation-title">💡 What This Comparison Tells You</div>
                <p><strong>How to Read:</strong> Your portfolio (bold line) vs benchmarks (dashed lines)</p>
                <p><strong>Key Questions:</strong></p>
                <ul>
                    <li><strong>Are you above or below SPY?</strong> If below, why not just buy SPY? (Lower fees, simpler)</li>
                    <li><strong>Beating SPY but with less volatility?</strong> Excellent! You've improved risk-adjusted returns.</li>
                    <li><strong>Below 60/40?</strong> This is concerning - 60/40 is the "basic" portfolio.</li>
                    <li><strong>Lines diverge then converge?</strong> Different strategies work in different market regimes.</li>
                </ul>
                <p><strong>Reality Check:</strong> Most active managers underperform SPY over 10+ years. 
                If you're not consistently beating SPY, consider just buying it (lower fees, less work).</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics Comparison
        st.markdown("---")
        st.markdown("### 📊 Metrics Comparison")
        
        comparison_data = {
            'Metric': ['Annual Return', 'Volatility', 'Sharpe Ratio', 'Max Drawdown', 'Sortino Ratio', 'Calmar Ratio']
        }
        
        # Add portfolio metrics
        comparison_data['Your Portfolio'] = [
            f"{metrics['Annual Return']:.2%}",
            f"{metrics['Annual Volatility']:.2%}",
            f"{metrics['Sharpe Ratio']:.2f}",
            f"{metrics['Max Drawdown']:.2%}",
            f"{metrics['Sortino Ratio']:.2f}",
            f"{metrics['Calmar Ratio']:.2f}"
        ]
        
        # Add benchmark metrics
        for name, returns in benchmarks_to_compare.items():
            bench_metrics = calculate_portfolio_metrics(returns)
            comparison_data[name] = [
                f"{bench_metrics['Annual Return']:.2%}",
                f"{bench_metrics['Annual Volatility']:.2%}",
                f"{bench_metrics['Sharpe Ratio']:.2f}",
                f"{bench_metrics['Max Drawdown']:.2%}",
                f"{bench_metrics['Sortino Ratio']:.2f}",
                f"{bench_metrics['Calmar Ratio']:.2f}"
            ]
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Metrics comparison interpretation
        st.markdown("""
            <div class="interpretation-box">
                <div class="interpretation-title">💡 How to Compare Metrics</div>
                <p><strong>What to Look For:</strong></p>
                <ul>
                    <li><strong>Higher Annual Return:</strong> You're making more money (good!)</li>
                    <li><strong>Lower Volatility:</strong> Smoother ride than benchmark (good!)</li>
                    <li><strong>Higher Sharpe Ratio:</strong> Better risk-adjusted returns (BEST metric!)</li>
                    <li><strong>Smaller Max Drawdown:</strong> You suffered less in crashes (good!)</li>
                    <li><strong>Higher Sortino & Calmar:</strong> Confirm Sharpe findings (good!)</li>
                </ul>
                <p><strong>Ideal Outcome:</strong></p>
                <ul>
                    <li>Annual Return: Higher than benchmarks ✓</li>
                    <li>Volatility: Lower than benchmarks ✓</li>
                    <li>Sharpe Ratio: Significantly higher ✓</li>
                    <li>Max Drawdown: Smaller absolute value ✓</li>
                </ul>
                <p><strong>🚩 Red Flags:</strong></p>
                <ul>
                    <li>Lower return AND higher volatility = Worst of both worlds</li>
                    <li>Sharpe ratio lower than SPY = You're taking more risk for less return</li>
                    <li>Much worse drawdown = You'll panic-sell during crashes</li>
                </ul>
                <p><strong>Decision Time:</strong> If you're not beating SPY on Sharpe ratio, 
                strongly consider just buying SPY. It's simpler, cheaper, and historically hard to beat.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Rolling Comparison
        st.markdown("---")
        st.markdown("### 📈 Rolling Sharpe Ratio Comparison")
        
        window = 60
        portfolio_rolling_sharpe = (portfolio_returns.rolling(window).mean() * 252) / (portfolio_returns.rolling(window).std() * np.sqrt(252))
        
        fig, ax = plt.subplots(figsize=(14, 8))
        portfolio_rolling_sharpe.plot(ax=ax, linewidth=3, label='Your Portfolio', color='#667eea')
        
        for i, (name, returns) in enumerate(benchmarks_to_compare.items()):
            bench_rolling_sharpe = (returns.rolling(window).mean() * 252) / (returns.rolling(window).std() * np.sqrt(252))
            bench_rolling_sharpe.plot(ax=ax, linewidth=2, label=name,
                                     color=colors[i % len(colors)], linestyle='--', alpha=0.8)
        
        ax.axhline(y=1, color='#28a745', linestyle=':', linewidth=1.5, alpha=0.7, label='Good (1.0)')
        ax.axhline(y=0, color='#dc3545', linestyle=':', linewidth=1.5, alpha=0.7)
        
        ax.set_title(f'Rolling Sharpe Ratio Comparison ({window}-day)', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sharpe Ratio', fontsize=12, fontweight='bold')
        ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Rolling comparison interpretation
        st.markdown("""
            <div class="interpretation-box">
                <div class="interpretation-title">💡 Understanding Rolling Sharpe Comparison</div>
                <p><strong>What This Shows:</strong> Who has better risk-adjusted returns over time</p>
                <p><strong>Key Patterns:</strong></p>
                <ul>
                    <li><strong>Consistently above benchmarks:</strong> Your strategy is working!</li>
                    <li><strong>Occasionally above, often below:</strong> Inconsistent alpha (luck vs skill?)</li>
                    <li><strong>Always below:</strong> Just buy the benchmark instead</li>
                    <li><strong>Divergence in crashes:</strong> Shows which portfolio protects better</li>
                </ul>
                <p><strong>Action Items:</strong></p>
                <ul>
                    <li>If your line is consistently below SPY, switch to SPY</li>
                    <li>If you beat benchmarks in bull markets but lose in bear markets, add defensive assets</li>
                    <li>If you beat in bear markets but lose in bull markets, reduce defensive position</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 7: OPTIMIZATION
# =============================================================================

with tab7:
    st.markdown("## 🎯 Portfolio Optimization")
    st.markdown("""
        <div class="info-box">
            <h4>What is Portfolio Optimization?</h4>
            <p>Find the best allocation of your assets to maximize returns for a given level of risk, 
            or minimize risk for a given level of returns.</p>
            <p><strong>Maximum Sharpe Ratio:</strong> Find the allocation with the best risk-adjusted returns.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Current vs Optimal
    st.markdown("---")
    st.markdown("### 📊 Current vs Optimal Allocation")
    
    # Calculate optimal weights
    with st.spinner("Optimizing portfolio..."):
        optimal_weights = optimize_portfolio(prices, method='max_sharpe')
        optimal_returns = calculate_portfolio_returns(prices, optimal_weights)
        optimal_metrics = calculate_portfolio_metrics(optimal_returns)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Current Allocation")
        current_weights_df = pd.DataFrame({
            'Ticker': list(weights.keys()),
            'Weight': [f"{w*100:.2f}%" for w in weights.values()]
        })
        st.dataframe(current_weights_df, use_container_width=True, hide_index=True)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set3(range(len(weights)))
        ax.pie(weights.values(), labels=weights.keys(), autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax.set_title('Current Allocation', fontsize=14, fontweight='bold', pad=20)
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### Optimal Allocation (Max Sharpe)")
        optimal_weights_dict = {ticker: w for ticker, w in zip(prices.columns, optimal_weights)}
        optimal_weights_df = pd.DataFrame({
            'Ticker': list(optimal_weights_dict.keys()),
            'Weight': [f"{w*100:.2f}%" for w in optimal_weights_dict.values()]
        })
        st.dataframe(optimal_weights_df, use_container_width=True, hide_index=True)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(optimal_weights_dict.values(), labels=optimal_weights_dict.keys(), 
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Optimal Allocation', fontsize=14, fontweight='bold', pad=20)
        st.pyplot(fig)
    
    # Metrics Comparison
    st.markdown("---")
    st.markdown("### 📈 Performance Comparison")
    
    comparison_data = {
        'Metric': ['Annual Return', 'Volatility', 'Sharpe Ratio', 'Max Drawdown', 'Sortino Ratio'],
        'Current Portfolio': [
            f"{metrics['Annual Return']:.2%}",
            f"{metrics['Annual Volatility']:.2%}",
            f"{metrics['Sharpe Ratio']:.2f}",
            f"{metrics['Max Drawdown']:.2%}",
            f"{metrics['Sortino Ratio']:.2f}"
        ],
        'Optimal Portfolio': [
            f"{optimal_metrics['Annual Return']:.2%}",
            f"{optimal_metrics['Annual Volatility']:.2%}",
            f"{optimal_metrics['Sharpe Ratio']:.2f}",
            f"{optimal_metrics['Max Drawdown']:.2%}",
            f"{optimal_metrics['Sortino Ratio']:.2f}"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Optimization interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 Should You Switch to Optimal Allocation?</div>
            <p><strong>What Optimization Does:</strong></p>
            <ul>
                <li>Analyzes historical correlations between assets</li>
                <li>Finds allocation that maximized Sharpe ratio in the PAST</li>
                <li>Assumes future correlations will be similar to historical</li>
            </ul>
            <p><strong>When to Use Optimal Allocation:</strong></p>
            <ul>
                <li>Sharpe ratio significantly higher (0.2+ improvement)</li>
                <li>Similar or better returns with lower volatility</li>
                <li>You believe historical relationships will continue</li>
            </ul>
            <p><strong>⚠️ Important Warnings:</strong></p>
            <ul>
                <li><strong>Over-optimization risk:</strong> "Perfect" historical fit may not work going forward</li>
                <li><strong>Concentration risk:</strong> Optimal allocation often concentrates in few assets</li>
                <li><strong>Turnover costs:</strong> Switching has transaction costs and tax implications</li>
                <li><strong>Rebalancing:</strong> Optimal weights change over time - requires monitoring</li>
            </ul>
            <p><strong>Conservative Approach:</strong></p>
            <ul>
                <li>If optimal Sharpe is only slightly better (< 0.2), stick with current allocation</li>
                <li>If optimal suggests 80%+ in one asset, that's too concentrated - use judgment</li>
                <li>Consider a blend: 70% optimal + 30% equal weight</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Efficient Frontier
    st.markdown("---")
    st.markdown("### 📊 Efficient Frontier")
    
    with st.spinner("Calculating efficient frontier..."):
        results, weights_array = calculate_efficient_frontier(prices, num_portfolios=500)
        
        # Current and optimal portfolio metrics
        current_annual_return = metrics['Annual Return']
        current_annual_vol = metrics['Annual Volatility']
        
        optimal_annual_return = optimal_metrics['Annual Return']
        optimal_annual_vol = optimal_metrics['Annual Volatility']
    
    fig = plot_efficient_frontier(results, optimal_weights, optimal_annual_return, optimal_annual_vol)
    
    # Add current portfolio to plot
    ax = fig.axes[0]
    ax.scatter(current_annual_vol, current_annual_return, marker='o', color='blue',
              s=400, label='Current Portfolio', edgecolors='black', linewidths=2)
    
    # Update legend
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
    
    st.pyplot(fig)
    
    # Efficient frontier interpretation
    st.markdown("""
        <div class="interpretation-box">
            <div class="interpretation-title">💡 Understanding the Efficient Frontier</div>
            <p><strong>What This Chart Shows:</strong></p>
            <ul>
                <li>Each dot = A possible portfolio allocation</li>
                <li>X-axis (Volatility) = Risk</li>
                <li>Y-axis (Return) = Expected Return</li>
                <li>Color = Sharpe Ratio (brighter yellow = better)</li>
            </ul>
            <p><strong>Key Points:</strong></p>
            <ul>
                <li><strong>Blue circle:</strong> Your current portfolio</li>
                <li><strong>Red star:</strong> Optimal portfolio (highest Sharpe)</li>
                <li><strong>Upper edge:</strong> "Efficient frontier" - best return for each risk level</li>
            </ul>
            <p><strong>How to Read Your Position:</strong></p>
            <ul>
                <li><strong>Below and left of red star:</strong> You have lower risk but also lower return</li>
                <li><strong>Above and right of red star:</strong> You have higher risk for the return</li>
                <li><strong>On the frontier:</strong> You're efficient! Can't improve without changing risk</li>
                <li><strong>Below the frontier:</strong> You're inefficient - can get better returns for same risk</li>
            </ul>
            <p><strong>Action Items:</strong></p>
            <ul>
                <li>If you're far below the frontier, consider rebalancing</li>
                <li>If you're on or near the frontier, you're doing well</li>
                <li>Remember: This is based on PAST data - future may differ!</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons
    st.markdown("---")
    st.markdown("### 🎯 Take Action")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Apply Optimal Weights", type="primary"):
            # Update current portfolio with optimal weights
            st.session_state.portfolios[st.session_state.current_portfolio]['weights'] = optimal_weights_dict
            st.session_state.portfolios[st.session_state.current_portfolio]['returns'] = optimal_returns
            st.success("✅ Optimal weights applied! Refresh to see changes in other tabs.")
            st.balloons()
    
    with col2:
        if st.button("💾 Save as New Portfolio"):
            new_name = f"{st.session_state.current_portfolio} (Optimized)"
            st.session_state.portfolios[new_name] = {
                'tickers': tickers,
                'weights': optimal_weights_dict,
                'prices': prices,
                'returns': optimal_returns,
                'start_date': current['start_date'],
                'end_date': current['end_date']
            }
            st.success(f"✅ Saved as '{new_name}'")
    
    with col3:
        # Export optimal weights
        export_weights = pd.DataFrame({
            'Ticker': list(optimal_weights_dict.keys()),
            'Weight': list(optimal_weights_dict.values())
        })
        csv = export_weights.to_csv(index=False)
        st.download_button(
            label="📥 Export Optimal Weights",
            data=csv,
            file_name="optimal_weights.csv",
            mime="text/csv"
        )


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem;">
        <p style="font-size: 1.1rem;">
            <strong>Alphatic Portfolio Analyzer ✨</strong><br>
            Sophisticated analysis for the educated investor
        </p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">
            Built with ❤️ for affluent non-experts who want to understand their investments<br>
            Remember: Past performance does not guarantee future results. Invest responsibly.
        </p>
    </div>
""", unsafe_allow_html=True)