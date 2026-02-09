"""
☕ The Coffee Shop Survival Simulator (2026 Edition)
Commercial Grade • Premium Financial Analysis Tool
Based on Q1/2026 US Market Research
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF
import base64

# ============================================================================
# COLOR PALETTE
# ============================================================================
COLORS = {
    'primary': '#1A3C40',
    'accent': '#C38D56',
    'teal': '#4A9B9B',
    'navy': '#2C3E50',
    'terracotta': '#C97B63',
    'gold': '#D4A855',
    'sage': '#87A889',
    'background': '#F9F9F7',
    'sidebar': '#F8F9FA',
    'card': '#FFFFFF',
    'text': '#1A3C40',
    'muted': '#6C757D',
    'border': '#DEE2E6',
    'success': '#2D6A4F',
    'warning': '#D4A855',
    'error': '#C97B63'
}

# ============================================================================
# DATA BREAKDOWNS (FOR PDF EXPORT)
# ============================================================================
RENOVATION_BREAKDOWN = [
    ("Design & Permits (Architect/MEP/Fire)", 22000),
    ("Demolition & Site Prep", 10000),
    ("Plumbing (Floor Drains/Grease Trap)", 45000),
    ("Electrical (Panel/Circuits/LED)", 35000),
    ("Flooring, Walls & Ceiling", 30000),
    ("Millwork & Custom Bar Build", 28000),
]

EQUIPMENT_BREAKDOWN = [
    ("Espresso Machine (2-3 Group)", 24000),
    ("Grinders (2 Espresso + 1 Bulk)", 8000),
    ("Water Filtration + Ice Machine", 9000),
    ("Refrigeration (Under-counter/Walk-in)", 15000),
    ("Oven, Blender & Prep Equipment", 12000),
    ("Commercial Dishwasher", 8000),
    ("POS System & Technology", 10000),
]

# Help text for trust signals
HELP_TEXT = "Based on our exclusive Q1/2026 Coffee Market Research (US Region). Updated quarterly."

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Coffee Shop Survival Simulator 2026",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PASSWORD PROTECTION (Persistent via Query Params)
# ============================================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    
    # Check if already authenticated via query params
    query_params = st.query_params
    if query_params.get("auth") == "verified":
        return True
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "save150k":
            st.session_state["password_correct"] = True
            # Set query param to persist across refreshes
            st.query_params["auth"] = "verified"
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <h1 style="color: #1A3C40; font-size: 2.5rem;">☕ Coffee Shop Survival Simulator</h1>
            <p style="color: #6C757D; font-size: 1.1rem;">2026 Commercial Edition</p>
            <hr style="border: none; height: 2px; background: linear-gradient(90deg, transparent, #C38D56, transparent); margin: 2rem auto; max-width: 300px;">
            <p style="color: #1A3C40; font-weight: 600; margin-bottom: 0.5rem;">🔐 Enter Access Code</p>
            <p style="color: #6C757D; font-size: 0.85rem;">This tool saves you up to <strong style="color: #00A86B;">$150,000</strong> in consulting fees.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Access Code", type="password", on_change=password_entered, key="password",
                placeholder="Enter your access code...",
                label_visibility="collapsed"
            )
            st.caption("💡 Hint: What amount does this tool save you?")
        return False
    
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem;">
            <h1 style="color: #1A3C40; font-size: 2.5rem;">☕ Coffee Shop Survival Simulator</h1>
            <p style="color: #6C757D; font-size: 1.1rem;">2026 Commercial Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Access Code", type="password", on_change=password_entered, key="password",
                placeholder="Enter your access code...",
                label_visibility="collapsed"
            )
            st.error("❌ Incorrect access code. Please try again.")
            st.caption("💡 Hint: save + the amount this tool saves you (in thousands)")
        return False
    
    else:
        # Password correct - set query param for persistence
        st.query_params["auth"] = "verified"
        return True

if not check_password():
    st.stop()

# ============================================================================
# CSS STYLING
# ============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {COLORS['background']};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .block-container {{
        padding: 1.5rem 1rem !important;
        max-width: 900px !important;
    }}
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background: {COLORS['sidebar']} !important;
        border-right: 1px solid {COLORS['border']};
    }}
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] h1, h2, h3 {{
        color: {COLORS['text']} !important;
        font-weight: 600 !important;
    }}
    
    section[data-testid="stSidebar"] label {{
        color: {COLORS['text']} !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    section[data-testid="stSidebar"] .stNumberInput > div > div > input {{
        background: {COLORS['card']} !important;
        border: 2px solid {COLORS['border']} !important;
        border-radius: 8px !important;
        color: {COLORS['text']} !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }}
    
    section[data-testid="stSidebar"] .stNumberInput > div > div > input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 3px rgba(26, 60, 64, 0.15) !important;
    }}
    
    section[data-testid="stSidebar"] .stExpander {{
        background: {COLORS['card']} !important;
        border: 2px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Main expander header (collapsed state) - improved visibility */
    section[data-testid="stSidebar"] .stExpander > details > summary {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #2D5A5A 100%) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
    }}
    
    section[data-testid="stSidebar"] .stExpander > details > summary p {{
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }}
    
    section[data-testid="stSidebar"] .stExpander > details > summary svg {{
        color: white !important;
    }}
    
    /* When expanded - lighter background */
    section[data-testid="stSidebar"] .stExpander > details[open] > summary {{
        background: {COLORS['primary']} !important;
        border-radius: 8px 8px 0 0 !important;
    }}
    
    /* Enhanced visibility for nested expanders */
    section[data-testid="stSidebar"] .stExpander .stExpander {{
        background: #E8F4F4 !important;
        border: 2px solid {COLORS['primary']} !important;
    }}
    
    section[data-testid="stSidebar"] .stExpander .stExpander > details > summary {{
        background: #E8F4F4 !important;
    }}
    
    section[data-testid="stSidebar"] .stExpander .stExpander > details > summary p {{
        color: {COLORS['primary']} !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
    }}
    
    section[data-testid="stSidebar"] .stExpander .stExpander > details > summary svg {{
        color: {COLORS['primary']} !important;
    }}
    
    /* Nested expander styling */
    .breakdown-expander {{
        background: rgba(26, 60, 64, 0.03);
        border-radius: 8px;
        padding: 0.5rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }}
    
    /* HEADER */
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #2D5A5A 100%);
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(26, 60, 64, 0.15);
        flex-wrap: wrap;
        gap: 1rem;
    }}
    
    .header-text h1 {{
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .header-text p {{
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
        margin: 0.25rem 0 0 0;
    }}
    
    /* METRIC CARDS */
    .metric-card {{
        background: {COLORS['card']};
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid {COLORS['border']};
        margin-bottom: 0.75rem;
    }}
    
    .metric-label {{
        color: {COLORS['muted']};
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }}
    
    .metric-value {{
        color: {COLORS['primary']};
        font-size: 1.75rem;
        font-weight: 700;
        line-height: 1.2;
    }}
    
    .metric-value.gold {{ color: {COLORS['accent']}; }}
    .metric-value.success {{ color: {COLORS['success']}; }}
    .metric-value.error {{ color: {COLORS['error']}; }}
    
    .metric-delta {{ font-size: 0.8rem; margin-top: 0.35rem; font-weight: 500; }}
    .metric-delta.positive {{ color: {COLORS['success']}; }}
    .metric-delta.negative {{ color: {COLORS['error']}; }}
    
    .ai-insight {{
        font-size: 0.85rem;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        display: inline-block;
        font-weight: 600;
    }}
    
    .ai-insight.excellent {{ background: rgba(45,106,79,0.15); color: #1B5E3F; border: 1px solid #2D6A4F; }}
    .ai-insight.good {{ background: rgba(74,155,155,0.15); color: #2B7A78; border: 1px solid #4A9B9B; }}
    .ai-insight.warning {{ background: rgba(212,168,85,0.2); color: #8B6914; border: 1px solid #D4A855; }}
    .ai-insight.danger {{ background: rgba(201,123,99,0.15); color: #A84832; border: 1px solid #C97B63; }}
    
    .section-header {{
        color: {COLORS['primary']};
        font-size: 1.1rem;
        font-weight: 700;
        margin: 1.75rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid {COLORS['accent']};
        display: inline-block;
    }}
    
    .alert {{
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 0.75rem 0;
    }}
    
    .alert-success {{
        background: linear-gradient(135deg, rgba(45,106,79,0.12) 0%, rgba(45,106,79,0.05) 100%);
        border-left: 5px solid {COLORS['success']};
    }}
    
    .alert-warning {{
        background: linear-gradient(135deg, rgba(212,168,85,0.15) 0%, rgba(212,168,85,0.05) 100%);
        border-left: 5px solid {COLORS['warning']};
    }}
    
    .alert-error {{
        background: linear-gradient(135deg, rgba(201,123,99,0.12) 0%, rgba(201,123,99,0.05) 100%);
        border-left: 5px solid {COLORS['error']};
    }}
    
    .alert-title {{ font-weight: 700; font-size: 1rem; margin-bottom: 0.4rem; color: {COLORS['primary']}; }}
    .alert-text {{ font-size: 0.9rem; color: {COLORS['text']}; line-height: 1.5; }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    hr {{ border: none; height: 1px; background: {COLORS['border']}; margin: 1.5rem 0; }}
    
    @media (max-width: 768px) {{
        .header-container {{ flex-direction: column; text-align: center; }}
        .metric-value {{ font-size: 1.5rem; }}
        .block-container {{ padding: 1rem 0.5rem !important; }}
        .ai-insight {{ font-size: 0.8rem; padding: 0.4rem 0.6rem; }}
        .alert-title {{ font-size: 0.95rem; }}
        .alert-text {{ font-size: 0.85rem; }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PDF GENERATION (INCLUDES FULL BREAKDOWNS)
# ============================================================================
class BusinessPlanPDF(FPDF):
    def header(self):
        # Header with colored background
        self.set_fill_color(26, 60, 64)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.set_y(8)
        self.cell(0, 10, 'Coffee Shop Business Plan 2026', ln=True, align='C')
        self.ln(15)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Coffee Shop Survival Simulator - Commercial Edition | Q1/2026 Data', align='C')
    
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(26, 60, 64)
        self.set_fill_color(249, 249, 247)
        self.cell(0, 8, f'  {title}', ln=True, fill=True)
        self.ln(2)
    
    def key_metric(self, label, value, status=""):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(108, 117, 125)
        self.cell(60, 6, label, ln=False)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(26, 60, 64)
        self.cell(50, 6, str(value), ln=False)
        if status:
            if "OK" in status or "Healthy" in status:
                self.set_text_color(45, 106, 79)
            elif "DANGER" in status or "High" in status:
                self.set_text_color(201, 123, 99)
            else:
                self.set_text_color(212, 168, 85)
            self.set_font('Helvetica', 'I', 9)
            self.cell(0, 6, status, ln=True)
        else:
            self.ln()

def create_pdf(data):
    pdf = BusinessPlanPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ==================== PAGE 1: EXECUTIVE SUMMARY ====================
    pdf.section_title("EXECUTIVE SUMMARY")
    
    runway_text = "Infinite" if data['runway'] > 999 else f"{data['runway']:.1f} months"
    payback_text = "N/A" if data['payback'] > 999 else f"{data['payback']:.1f} months"
    profit_status = "Profitable" if data['profit'] >= 0 else "Loss"
    
    pdf.key_metric("Monthly Revenue:", f"${data['revenue']:,.0f}")
    pdf.key_metric("Monthly Expenses:", f"${data['expenses']:,.0f}")
    pdf.key_metric("Net Profit/Loss:", f"${data['profit']:,.0f}", f"({data['margin']:.1f}% margin) - {profit_status}")
    pdf.key_metric("Cash Runway:", runway_text)
    pdf.key_metric("Payback Period:", payback_text)
    pdf.ln(5)
    
    # ==================== INPUT PARAMETERS ====================
    pdf.section_title("INPUT PARAMETERS - CAPITAL & INVESTMENT")
    pdf.key_metric("Total Capital:", f"${data['total_capital']:,.0f}")
    pdf.key_metric("Renovation Budget:", f"${data['renovation']:,.0f}")
    pdf.key_metric("Equipment Budget:", f"${data['equipment']:,.0f}")
    pdf.key_metric("Operating Cash:", f"${data['remaining_cash']:,.0f}", 
                   "OK" if data['remaining_cash'] >= 0 else "SHORTFALL!")
    pdf.ln(3)
    
    pdf.section_title("INPUT PARAMETERS - LOCATION & REAL ESTATE")
    pdf.key_metric("Shop Size:", f"{data['sqft']:,} sqft")
    pdf.key_metric("Base Rent:", f"${data['base_rent']:.2f}/sqft/year")
    pdf.key_metric("NNN Charges:", f"${data['nnn']:.2f}/sqft/year")
    pdf.key_metric("Monthly Rent Total:", f"${data['monthly_rent']:,.0f}")
    pdf.key_metric("Utilities:", f"${data['utilities']:,.0f}/month")
    pdf.ln(3)
    
    pdf.section_title("INPUT PARAMETERS - STAFFING")
    pdf.key_metric("Number of Employees:", f"{data['employees']}")
    pdf.key_metric("Hours/Employee/Day:", f"{data['hours_per_day']:.1f}")
    pdf.key_metric("Hourly Wage:", f"${data['hourly_wage']:.2f}")
    pdf.key_metric("Labor Burden:", f"{data['labor_burden']:.0f}%")
    pdf.key_metric("Monthly Labor Cost:", f"${data['monthly_labor']:,.0f}")
    pdf.ln(3)
    
    pdf.section_title("INPUT PARAMETERS - COST OF GOODS SOLD")
    pdf.key_metric("Milk Price:", f"${data['milk_price']:.2f}/gallon")
    pdf.key_metric("Coffee Beans:", f"${data['bean_price']:.2f}/lb")
    pdf.key_metric("Packaging:", f"${data['packaging']:.2f}/cup")
    pdf.key_metric("Unit Cost per Cup:", f"${data['unit_cost']:.2f}")
    pdf.key_metric("Monthly COGS:", f"${data['monthly_cogs']:,.0f}")
    pdf.ln(3)
    
    pdf.section_title("INPUT PARAMETERS - SALES PROJECTIONS")
    pdf.key_metric("Average Price/Cup:", f"${data['avg_price']:.2f}")
    pdf.key_metric("Cups Sold/Day:", f"{data['cups_per_day']}")
    pdf.key_metric("Operating Days/Month:", f"{data['operating_days']}")
    pdf.key_metric("Monthly Cups Sold:", f"{data['monthly_cups']:,}")
    pdf.ln(5)
    
    # ==================== PAGE 2: CAPEX BREAKDOWN ====================
    pdf.add_page()
    
    pdf.section_title(f"RENOVATION INVESTMENT: ${data['renovation']:,.0f}")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    for item, cost in RENOVATION_BREAKDOWN:
        pdf.cell(120, 6, f"  - {item}", ln=False)
        pdf.cell(0, 6, f"${cost:,.0f}", ln=True)
    total_reno = sum(c for _, c in RENOVATION_BREAKDOWN)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(108, 117, 125)
    pdf.cell(0, 6, f"  Standard total: ${total_reno:,.0f} | Your budget: ${data['renovation']:,.0f}", ln=True)
    pdf.ln(5)
    
    pdf.section_title(f"EQUIPMENT INVESTMENT: ${data['equipment']:,.0f}")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    for item, cost in EQUIPMENT_BREAKDOWN:
        pdf.cell(120, 6, f"  - {item}", ln=False)
        pdf.cell(0, 6, f"${cost:,.0f}", ln=True)
    total_equip = sum(c for _, c in EQUIPMENT_BREAKDOWN)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(108, 117, 125)
    pdf.cell(0, 6, f"  Standard total: ${total_equip:,.0f} | Your budget: ${data['equipment']:,.0f}", ln=True)
    pdf.ln(8)
    
    # ==================== RISK ANALYSIS ====================
    pdf.section_title("RISK ANALYSIS")
    
    rent_status = "[DANGER: >15%]" if data['rent_r'] > 15 else "[WARNING: >10%]" if data['rent_r'] >= 10 else "[OK: Healthy]"
    labor_status = "[DANGER: >35%]" if data['labor_r'] > 35 else "[OK: Controlled]"
    cogs_status = "[WARNING: >30%]" if data['cogs_r'] > 30 else "[OK: Good]"
    
    pdf.key_metric("Rent Ratio:", f"{data['rent_r']:.1f}% of Revenue", rent_status)
    pdf.key_metric("Labor Ratio:", f"{data['labor_r']:.1f}% of Revenue", labor_status)
    pdf.key_metric("COGS Ratio:", f"{data['cogs_r']:.1f}% of Revenue", cogs_status)
    pdf.ln(8)
    
    # ==================== BREAK-EVEN ANALYSIS ====================
    pdf.section_title("BREAK-EVEN ANALYSIS")
    
    # Calculate break-even
    if data['avg_price'] > data['unit_cost']:
        fixed_costs = data['monthly_labor'] + data['monthly_rent'] + data['utilities']
        be_cups_monthly = fixed_costs / (data['avg_price'] - data['unit_cost'])
        be_cups_daily = be_cups_monthly / data['operating_days']
        cups_surplus = data['cups_per_day'] - be_cups_daily
        
        pdf.key_metric("Fixed Costs/Month:", f"${fixed_costs:,.0f}")
        pdf.key_metric("Contribution Margin/Cup:", f"${data['avg_price'] - data['unit_cost']:.2f}")
        pdf.key_metric("Break-even Point:", f"{be_cups_daily:.0f} cups/day ({be_cups_monthly:,.0f}/month)")
        pdf.key_metric("Your Projection:", f"{data['cups_per_day']} cups/day", 
                       f"+{cups_surplus:.0f} above BE" if cups_surplus > 0 else f"{cups_surplus:.0f} below BE!")
        
        if data['profit'] > 0:
            payback_mo = (data['renovation'] + data['equipment']) / data['profit']
            pdf.key_metric("Payback Period:", f"{payback_mo:.1f} months ({payback_mo/12:.1f} years)")
    else:
        pdf.key_metric("Status:", "INVALID - Price below unit cost!", "[CRITICAL]")
    pdf.ln(8)
    
    # ==================== FINANCIAL SUMMARY TABLE ====================
    pdf.section_title("MONTHLY PROFIT & LOSS STATEMENT")
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(26, 60, 64)
    
    # Revenue
    pdf.cell(100, 6, "  REVENUE", ln=False)
    pdf.cell(0, 6, f"${data['revenue']:,.0f}", ln=True, align='R')
    
    # Expenses
    pdf.set_text_color(80, 80, 80)
    pdf.cell(100, 6, "    (-) Cost of Goods Sold", ln=False)
    pdf.cell(0, 6, f"${data['monthly_cogs']:,.0f}", ln=True, align='R')
    
    pdf.cell(100, 6, "    (-) Labor", ln=False)
    pdf.cell(0, 6, f"${data['monthly_labor']:,.0f}", ln=True, align='R')
    
    pdf.cell(100, 6, "    (-) Rent", ln=False)
    pdf.cell(0, 6, f"${data['monthly_rent']:,.0f}", ln=True, align='R')
    
    pdf.cell(100, 6, "    (-) Utilities", ln=False)
    pdf.cell(0, 6, f"${data['utilities']:,.0f}", ln=True, align='R')
    
    # Total Expenses
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(26, 60, 64)
    pdf.cell(100, 6, "  TOTAL EXPENSES", ln=False)
    pdf.cell(0, 6, f"${data['expenses']:,.0f}", ln=True, align='R')
    
    # Profit line
    pdf.ln(2)
    pdf.set_draw_color(26, 60, 64)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    
    profit_color = (45, 106, 79) if data['profit'] >= 0 else (201, 123, 99)
    pdf.set_text_color(*profit_color)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(100, 8, "  NET PROFIT/LOSS", ln=False)
    pdf.cell(0, 8, f"${data['profit']:,.0f}", ln=True, align='R')
    
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(100, 6, "  Net Margin", ln=False)
    pdf.cell(0, 6, f"{data['margin']:.1f}%", ln=True, align='R')
    
    # ==================== FOOTER NOTE ====================
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, 'This report was generated by Coffee Shop Survival Simulator 2026.', ln=True)
    pdf.cell(0, 5, 'All default values are based on Q1/2026 US Coffee Market Research.', ln=True)
    pdf.cell(0, 5, 'For investment purposes only. Consult a financial advisor before making decisions.', ln=True)
    
    return pdf.output()

# ============================================================================
# DEFAULTS
# ============================================================================
D = {
    'cap': 350000, 'reno': 185000, 'equip': 85000,
    'milk': 4.48, 'oat': 5.20, 'bean': 14.50, 'pkg': 0.17,
    'wage': 15.0, 'burden': 0.18, 'rent': 45.0, 'nnn': 12.0, 'util': 1200,
    'sqft': 800, 'staff': 3, 'hrs': 8.0, 'price': 5.50, 'cups': 120, 'days': 30
}

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="header-container">
    <div class="header-text">
        <h1>☕ Coffee Shop Survival Simulator</h1>
        <p>2026 Edition • Commercial Financial Projections</p>
    </div>
</div>
""", unsafe_allow_html=True)

# CSS to highlight sidebar toggle button and add label
st.markdown("""
<style>
    /* Highlight and animate the sidebar toggle button */
    [data-testid="collapsedControl"] {
        background: linear-gradient(135deg, #1A3C40 0%, #2D5A5A 100%) !important;
        border-radius: 8px !important;
        animation: pulseGlow 2s ease-in-out infinite !important;
    }
    
    [data-testid="collapsedControl"] svg {
        color: white !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            box-shadow: 0 0 5px #1A3C40, 0 0 10px #1A3C40; 
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 15px #C38D56, 0 0 25px #C38D56; 
            transform: scale(1.05);
        }
    }
    
    /* Add label next to toggle button */
    [data-testid="collapsedControl"]::after {
        content: "← Configure Your Scenario";
        position: absolute;
        left: 50px;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(135deg, #1A3C40 0%, #2D5A5A 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(26, 60, 64, 0.3);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CLEAN WITH NESTED EXPANDERS
# ============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # ===== CAPITAL & INVESTMENT =====
    with st.expander("💰 Capital & Investment", expanded=True):
        cap = st.number_input("Total Available Capital ($)", 10000, 2000000, D['cap'], 10000, help=HELP_TEXT)
        
        reno = st.number_input("Renovation Budget ($)", 0, 500000, D['reno'], 5000, help=HELP_TEXT)
        
        # NESTED EXPANDER FOR RENOVATION BREAKDOWN
        with st.expander("📋 View Renovation Breakdown", expanded=False):
            st.markdown("**Standard Build Cost Allocation:**")
            for item, cost in RENOVATION_BREAKDOWN:
                st.markdown(f"- {item}: **${cost:,}**")
            st.caption("💡 Tip: Save up to 40% with Second Generation space.")
        
        equip = st.number_input("Equipment Budget ($)", 0, 300000, D['equip'], 5000, help=HELP_TEXT)
        
        # NESTED EXPANDER FOR EQUIPMENT BREAKDOWN
        with st.expander("📋 View Equipment List", expanded=False):
            st.markdown("**Standard Equipment Package:**")
            for item, cost in EQUIPMENT_BREAKDOWN:
                st.markdown(f"- {item}: **${cost:,}**")
            st.caption("💡 Tip: Save 30-50% buying used equipment.")
        
        cash = cap - reno - equip
        if cash >= 0:
            st.success(f"✅ Operating Cash: **${cash:,.0f}**")
        else:
            st.error(f"❌ Shortfall: **${abs(cash):,.0f}**")
    
    # ===== LOCATION (COLLAPSED) =====
    with st.expander("🏪 Location & Real Estate", expanded=False):
        sqft = st.number_input("Shop Size (sqft)", 200, 5000, D['sqft'], 50, help=HELP_TEXT)
        rent = st.number_input("Base Rent ($/sqft/year)", 10.0, 200.0, D['rent'], 1.0, help=HELP_TEXT)
        nnn = st.number_input("NNN Charges ($/sqft/year)", 0.0, 50.0, D['nnn'], 0.5, help=HELP_TEXT)
        util = st.number_input("Utilities ($/month)", 500, 5000, D['util'], 100, help=HELP_TEXT)
    
    # ===== STAFFING (COLLAPSED) =====
    with st.expander("👥 Staffing & Labor", expanded=False):
        staff = st.number_input("Number of Employees", 1, 20, D['staff'], help=HELP_TEXT)
        hrs = st.number_input("Hours per Employee per Day", 4.0, 12.0, D['hrs'], 0.5, help=HELP_TEXT)
        wage = st.number_input("Hourly Wage ($)", 10.0, 30.0, D['wage'], 0.5, help=HELP_TEXT)
        burden = st.number_input("Labor Burden (%)", 0.0, 40.0, D['burden']*100, 1.0, help="Taxes, insurance, benefits. " + HELP_TEXT) / 100
    
    # ===== COGS (COLLAPSED) =====
    with st.expander("☕ Cost of Goods Sold", expanded=False):
        milk = st.number_input("Whole Milk ($/gallon)", 2.0, 10.0, D['milk'], 0.1, help=HELP_TEXT)
        oat = st.number_input("Oat Milk ($/carton)", 2.0, 12.0, D['oat'], 0.1, help=HELP_TEXT)
        bean = st.number_input("Coffee Beans ($/lb)", 8.0, 30.0, D['bean'], 0.5, help=HELP_TEXT)
        pkg = st.number_input("Packaging ($/cup)", 0.05, 0.50, D['pkg'], 0.01, help=HELP_TEXT)
        mtype = st.radio("Primary Milk Type", ["Dairy", "Oat"], horizontal=True)
        milk_p = milk if mtype == "Dairy" else oat
    
    # ===== SALES (COLLAPSED) =====
    with st.expander("📈 Sales Projections", expanded=False):
        price = st.number_input("Average Price per Cup ($)", 3.0, 12.0, D['price'], 0.25, help=HELP_TEXT)
        cups = st.number_input("Cups Sold per Day", 20, 500, D['cups'], 10, help=HELP_TEXT)
        days = st.number_input("Operating Days per Month", 20, 31, D['days'], help=HELP_TEXT)

# ============================================================================
# CALCULATIONS
# ============================================================================
bean_c = (bean / 453) * 20 * 1.1
milk_c = (milk_p / 128) * 10 * 1.1
unit = bean_c + milk_c + pkg

mo_cups = cups * days
rev = mo_cups * price
cogs = mo_cups * unit
labor = staff * hrs * days * wage * (1 + burden)
rent_b = (sqft * rent) / 12
rent_n = (sqft * nnn) / 12
rent_t = rent_b + rent_n
exp = cogs + labor + rent_t + util
profit = rev - exp

rent_r = (rent_t / rev * 100) if rev > 0 else 0
labor_r = (labor / rev * 100) if rev > 0 else 0
cogs_r = (cogs / rev * 100) if rev > 0 else 0
margin = (profit / rev * 100) if rev > 0 else 0

if profit < 0 and cash > 0:
    burn, runway = abs(profit), cash / abs(profit)
else:
    burn, runway = 0, float('inf') if profit >= 0 else 0

payback = (reno + equip) / profit if profit > 0 else float('inf')

# ============================================================================
# EXPORT PDF BUTTON (Simplified - No Charts)
# ============================================================================

pdf_data = {
    # Executive Summary
    'revenue': rev, 'expenses': exp, 'profit': profit, 'margin': margin,
    'runway': runway if runway < 1000 else 9999, 'payback': payback if payback < 1000 else 9999,
    
    # Capital & Investment
    'total_capital': cap, 'renovation': reno, 'equipment': equip, 'remaining_cash': cash,
    
    # Location
    'sqft': sqft, 'base_rent': rent, 'nnn': nnn, 'utilities': util, 'monthly_rent': rent_t,
    
    # Staffing
    'employees': staff, 'hours_per_day': hrs, 'hourly_wage': wage, 
    'labor_burden': burden * 100, 'monthly_labor': labor,
    
    # COGS
    'milk_price': milk_p, 'bean_price': bean, 'packaging': pkg,
    'unit_cost': unit, 'monthly_cogs': cogs,
    
    # Sales
    'avg_price': price, 'cups_per_day': cups, 'operating_days': days, 'monthly_cups': mo_cups,
    
    # Risk Ratios
    'rent_r': rent_r, 'labor_r': labor_r, 'cogs_r': cogs_r
}

col_exp1, col_exp2 = st.columns([3, 1])
with col_exp2:
    if st.button("📥 Export PDF", type="primary", use_container_width=True):
        pdf_bytes = create_pdf(pdf_data)
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="Coffee_Shop_Business_Plan_2026.pdf">📄 Click to Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ Business Plan PDF generated successfully!")

# ============================================================================
# HELPERS
# ============================================================================
def get_insight(margin):
    if margin >= 20:
        return '<span class="ai-insight excellent">✨ Excellent! Investment ready.</span>'
    elif margin >= 10:
        return '<span class="ai-insight good">👍 Good fundamentals.</span>'
    elif margin >= 5:
        return '<span class="ai-insight warning">⚠️ Thin margins. Review costs.</span>'
    else:
        return '<span class="ai-insight danger">🚨 High Risk. Review COGS.</span>'

def metric(label, value, delta=None, delta_type="", value_class="", insight=None):
    delta_html = f'<div class="metric-delta {delta_type}">{delta}</div>' if delta else ""
    insight_html = insight if insight else ""
    return f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value {value_class}">{value}</div>{delta_html}{insight_html}</div>'

def alert(atype, title, text):
    return f'<div class="alert alert-{atype}"><div class="alert-title">{title}</div><div class="alert-text">{text}</div></div>'

# ============================================================================
# SURVIVAL STATUS
# ============================================================================
st.markdown('<div class="section-header">⚡ Survival Analysis</div>', unsafe_allow_html=True)

if cash < 0:
    st.markdown(alert("error", "💥 BANKRUPT BEFORE LAUNCH", 
        f"You need ${abs(cash):,.0f} more capital to cover initial investment."), unsafe_allow_html=True)
elif profit < 0:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(metric("Cash Reserve", f"${cash:,.0f}", f"-${burn:,.0f}/mo", "negative"), unsafe_allow_html=True)
    with c2:
        rt = f"{runway:.1f} months" if runway < 100 else "∞"
        insight = '<span class="ai-insight danger">🚨 Critical runway!</span>' if runway <= 6 else ""
        st.markdown(metric("Runway", rt, "Until zero cash", "negative", "error", insight), unsafe_allow_html=True)
    
    if 0 < runway < 50:
        x = np.arange(0, int(min(runway + 4, 24)))
        y = [max(0, cash - burn * i) for i in x]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=COLORS['terracotta'], width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(201,123,99,0.12)'))
        fig.add_hline(y=0, line_dash="dot", line_color='#1A3C40', line_width=2)
        fig.update_layout(
            title=dict(text=f"💸 Cash Runway: {runway:.1f} months", font=dict(size=16, color='#1A3C40', family='Arial Black')),
            xaxis=dict(
                title=dict(text="Months", font=dict(size=14, color='#1A3C40', family='Arial')),
                showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False,
                tickfont=dict(size=13, color='#1A3C40', family='Arial'),
                fixedrange=True
            ),
            yaxis=dict(
                title=dict(text="Cash ($)", font=dict(size=14, color='#1A3C40', family='Arial')),
                showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False,
                tickfont=dict(size=13, color='#1A3C40', family='Arial'),
                fixedrange=True
            ),
            height=380, template="plotly_white", margin=dict(l=20, r=20, t=60, b=50),
            plot_bgcolor='rgba(255,255,255,0.95)', paper_bgcolor='rgba(0,0,0,0)',
            dragmode=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(alert("error", "🔥 BURNING CASH", f"Losing ${burn:,.0f}/month. {runway:.1f} months until zero cash."), unsafe_allow_html=True)
else:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(metric("Cash Reserve", f"${cash:,.0f}", f"+${profit:,.0f}/mo", "positive"), unsafe_allow_html=True)
    with c2:
        pb = f"{int(payback//12)}y {int(payback%12)}m" if payback < 120 else "N/A"
        st.markdown(metric("Payback Period", pb, f"${reno+equip:,.0f} CapEx", "", "gold"), unsafe_allow_html=True)
    st.markdown(alert("success", "✅ SUSTAINABLE MODEL", f"Net profit ${profit:,.0f}/month. Runway: Infinite."), unsafe_allow_html=True)

st.divider()

# ============================================================================
# FINANCIAL DASHBOARD
# ============================================================================
st.markdown('<div class="section-header">📊 Financial Dashboard</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown(metric("Monthly Revenue", f"${rev:,.0f}", f"{mo_cups:,} cups sold"), unsafe_allow_html=True)
with c2:
    st.markdown(metric("Monthly Expenses", f"${exp:,.0f}", f"{(exp/rev*100):.0f}% of revenue" if rev > 0 else ""), unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    val_class = "success" if profit >= 0 else "error"
    insight = get_insight(margin)
    st.markdown(metric("Net Profit", f"${profit:,.0f}", f"{margin:.1f}% margin", 
        "positive" if profit >= 0 else "negative", val_class, insight), unsafe_allow_html=True)
with c4:
    unit_insight = '<span class="ai-insight good">👍 Healthy unit economics</span>' if (price - unit) / price > 0.65 else ""
    st.markdown(metric("Unit Economics", f"${unit:.2f}/cup", f"${price - unit:.2f} gross margin", "", "gold", unit_insight), unsafe_allow_html=True)

st.divider()

# ============================================================================
# RISK ANALYSIS
# ============================================================================
st.markdown('<div class="section-header">⚠️ Risk Indicators</div>', unsafe_allow_html=True)

if rent_r > 15:
    st.markdown(alert("error", f"🏠 Rent Ratio: {rent_r:.1f}%", "DANGER - You're working for the landlord. Target: <15%"), unsafe_allow_html=True)
elif rent_r >= 10:
    st.markdown(alert("warning", f"🏠 Rent Ratio: {rent_r:.1f}%", "Elevated. Ideal target: <10%"), unsafe_allow_html=True)
else:
    st.markdown(alert("success", f"🏠 Rent Ratio: {rent_r:.1f}%", "Healthy occupancy cost"), unsafe_allow_html=True)

if labor_r > 35:
    st.markdown(alert("error", f"👥 Labor Ratio: {labor_r:.1f}%", "Too high. Reduce hours or headcount. Target: <35%"), unsafe_allow_html=True)
else:
    st.markdown(alert("success", f"👥 Labor Ratio: {labor_r:.1f}%", "Labor costs controlled"), unsafe_allow_html=True)

if cogs_r > 30:
    st.markdown(alert("warning", f"☕ COGS Ratio: {cogs_r:.1f}%", "High. Negotiate better supplier pricing. Target: <30%"), unsafe_allow_html=True)
else:
    st.markdown(alert("success", f"☕ COGS Ratio: {cogs_r:.1f}%", "Good cost control"), unsafe_allow_html=True)

st.divider()

# ============================================================================
# DONUT CHART - Commercial Quality
# ============================================================================
st.markdown('<div class="section-header">📈 Cost Structure</div>', unsafe_allow_html=True)

labels = ['COGS', 'Labor', 'Base Rent', 'NNN', 'Utilities']
values = [cogs, labor, rent_b, rent_n, util]
# Brighter, vibrant commercial colors
colors_chart = ['#00A86B', '#E63946', '#1E90FF', '#9B59B6', '#F39C12']

fig_donut = go.Figure(data=[go.Pie(
    labels=labels, values=values, hole=0.55,
    marker=dict(colors=colors_chart, line=dict(color='white', width=3)),
    textinfo='percent+label', textposition='outside',
    textfont=dict(size=12, family='Arial', color='#1A3C40'),
    hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
    pull=[0.02, 0.02, 0.02, 0.02, 0.02]
)])

fig_donut.add_annotation(
    text=f"<b>${exp:,.0f}</b><br><span style='font-size:12px;color:#6C757D'>Total/Month</span>",
    x=0.5, y=0.5, font=dict(size=24, color='#1A3C40', family='Arial Black'), showarrow=False
)

fig_donut.update_layout(
    height=450, showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5, 
                font=dict(size=12, family='Arial')),
    margin=dict(l=30, r=30, t=30, b=70), 
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_donut, use_container_width=True)

# ============================================================================
# BREAK-EVEN & PAYBACK ANALYSIS
# ============================================================================
st.markdown('<div class="section-header">📊 Break-even & Payback Analysis</div>', unsafe_allow_html=True)

if price > unit:
    fixed = labor + rent_t + util
    be_cups_month = fixed / (price - unit)
    be_cups_day = be_cups_month / days
    
    # Surplus/Deficit calculation
    cups_surplus = cups - be_cups_day
    profit_per_cup = price - unit
    
    # Display metrics in cards
    col_be1, col_be2 = st.columns(2)
    
    with col_be1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">☕ BREAK-EVEN POINT</div>
            <div class="metric-value">{be_cups_day:.0f} cups/day</div>
            <div class="metric-delta">or {be_cups_month:,.0f} cups/month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_be2:
        if cups_surplus > 0:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📈 YOUR PROJECTION</div>
                <div class="metric-value success">{cups} cups/day</div>
                <div class="metric-delta positive">+{cups_surplus:.0f} cups above break-even ✓</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📉 YOUR PROJECTION</div>
                <div class="metric-value error">{cups} cups/day</div>
                <div class="metric-delta negative">{cups_surplus:.0f} cups below break-even ✗</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Payback Period with Date
    col_pb1, col_pb2 = st.columns(2)
    
    with col_pb1:
        if profit > 0:
            payback_months = (reno + equip) / profit
            payback_years = int(payback_months // 12)
            payback_mo = int(payback_months % 12)
            
            from datetime import datetime, timedelta
            today = datetime.now()
            payback_date = today + timedelta(days=payback_months * 30)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⏰ PAYBACK PERIOD</div>
                <div class="metric-value gold">{payback_years}y {payback_mo}m</div>
                <div class="metric-delta">({payback_months:.1f} months total)</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⏰ PAYBACK PERIOD</div>
                <div class="metric-value error">N/A</div>
                <div class="metric-delta negative">Not profitable - cannot payback</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_pb2:
        if profit > 0:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📅 TIME TO PAYBACK</div>
                <div class="metric-value gold">In {payback_months:.0f} months</div>
                <div class="metric-delta">Based on ${profit:,.0f}/month profit</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📅 TIME TO PAYBACK</div>
                <div class="metric-value error">Never</div>
                <div class="metric-delta negative">Losing ${abs(profit):,.0f}/month</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Summary Alert
    if profit > 0:
        monthly_profit_per_cup = profit / mo_cups
        st.markdown(alert("success", "✅ PROFITABLE MODEL", 
            f"You're selling {cups_surplus:.0f} cups/day above break-even. Each cup contributes ${profit_per_cup:.2f} to cover fixed costs. "
            f"Total monthly profit: ${profit:,.0f}. CapEx of ${reno+equip:,.0f} will be recovered in {payback_years}y {payback_mo}m ({payback_months:.0f} months)."), 
            unsafe_allow_html=True)
    else:
        cups_needed_extra = abs(cups_surplus)
        st.markdown(alert("error", "❌ NOT PROFITABLE", 
            f"You need to sell {cups_needed_extra:.0f} more cups/day to break even. "
            f"Current loss: ${abs(profit):,.0f}/month. Consider: increasing price, reducing costs, or boosting sales."), 
            unsafe_allow_html=True)
    
    # Break-even Chart (always visible) - Commercial quality
    x = np.linspace(0, cups * 1.5, 50)
    rev_l = x * price * days
    cost_l = (x * unit * days) + fixed
    
    fig_be = go.Figure()
    # Brighter, vibrant colors
    fig_be.add_trace(go.Scatter(x=x, y=rev_l, name='Revenue', 
        line=dict(color='#00A86B', width=4),
        fill='tozeroy', fillcolor='rgba(0, 168, 107, 0.08)'))
    fig_be.add_trace(go.Scatter(x=x, y=cost_l, name='Total Cost', 
        line=dict(color='#E63946', width=4)))
    
    # Break-even label at top
    fig_be.add_vline(x=be_cups_day, line_dash="dash", line_color='#D4A855', line_width=2,
        annotation_text=f"☕ Break-even: {be_cups_day:.0f}/day", 
        annotation_position="top left",
        annotation_font=dict(size=12, color='#D4A855', family='Arial'))
    
    fig_be.update_layout(
        title=dict(text="📈 Revenue vs Cost by Daily Sales Volume", font=dict(size=16, color=COLORS['primary'], family='Arial Black')),
        xaxis=dict(
            title=dict(text="Cups/Day", font=dict(size=14, color='#1A3C40', family='Arial')),
            showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False,
            tickfont=dict(size=13, color='#1A3C40', family='Arial'),
            fixedrange=True  # Disable zoom on x-axis
        ),
        yaxis=dict(
            title=dict(text="$/Month", font=dict(size=14, color='#1A3C40', family='Arial')),
            showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False,
            tickfont=dict(size=13, color='#1A3C40', family='Arial'),
            fixedrange=True  # Disable zoom on y-axis
        ),
        height=420, template="plotly_white", 
        legend=dict(orientation="h", y=1.12, font=dict(size=13, color='#1A3C40', family='Arial')),
        margin=dict(l=20, r=20, t=70, b=50), 
        plot_bgcolor='rgba(255,255,255,0.95)', paper_bgcolor='rgba(0,0,0,0)',
        dragmode=False  # Completely disable drag/zoom
    )
    st.plotly_chart(fig_be, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False})
else:
    st.warning("⚠️ Price is below unit cost - cannot calculate break-even point. Raise your price!")

# ============================================================================
# DETAILED BREAKDOWN (always visible)
# ============================================================================
st.markdown('<div class="section-header">📋 Full Financial Breakdown</div>', unsafe_allow_html=True)

col_fin1, col_fin2 = st.columns(2)

with col_fin1:
    st.markdown(f"""
<div class="metric-card">
<div class="metric-label">💰 REVENUE</div>
<div style="font-size:0.95rem; color:#2C3E50;">
${rev:,.0f}/month<br>
<span style="color:#6C757D;">{mo_cups:,} cups @ ${price:.2f} avg</span>
</div>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
<div class="metric-card">
<div class="metric-label">☕ UNIT COST: ${unit:.2f}/cup</div>
<div style="font-size:0.9rem; color:#2C3E50;">
• Coffee beans: ${bean_c:.3f}<br>
• Milk: ${milk_c:.3f}<br>
• Packaging: ${pkg:.3f}
</div>
</div>
    """, unsafe_allow_html=True)

with col_fin2:
    st.markdown(f"""
<div class="metric-card">
<div class="metric-label">📊 EXPENSES: ${exp:,.0f}/mo</div>
<div style="font-size:0.9rem; color:#2C3E50;">
• COGS: ${cogs:,.0f} ({cogs_r:.1f}%)<br>
• Labor: ${labor:,.0f} ({labor_r:.1f}%)<br>
• Base Rent: ${rent_b:,.0f}<br>
• NNN: ${rent_n:,.0f}<br>
• Utilities: ${util:,.0f}
</div>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
<div class="metric-card">
<div class="metric-label">🏗️ CAPEX: ${reno+equip:,.0f}</div>
<div style="font-size:0.9rem; color:#2C3E50;">
• Renovation: ${reno:,.0f}<br>
• Equipment: ${equip:,.0f}<br>
• <strong>Cash Reserve: ${cash:,.0f}</strong>
</div>
</div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown(f'<div style="text-align:center;color:{COLORS["muted"]};font-size:0.8rem;padding:1rem 0;">☕ Coffee Shop Survival Simulator 2026 • Commercial Edition • Q1/2026 US Market Data</div>', unsafe_allow_html=True)
