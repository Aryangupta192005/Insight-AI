"""Plotly chart builders for SalesInsight."""
import plotly.express as px

NAVY = "#17324D"
TEAL = "#159A9C"

def monthly_sales_chart(data):
    fig = px.line(data, x="Month", y="Sales", markers=True, title="Monthly Sales Trend")
    fig.update_traces(line_color=TEAL, line_width=3, marker_size=7)
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=55, b=10),
                      xaxis_title="", yaxis_title="Sales (₹)", hovermode="x unified")
    return fig

def category_sales_chart(data):
    fig = px.bar(data, x="Category", y="Sales", title="Sales by Category",
                 color_discrete_sequence=[TEAL], text_auto=".2s")
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=55, b=10),
                      xaxis_title="", yaxis_title="Sales (₹)")
    return fig

def region_sales_chart(data):
    fig = px.bar(data, x="Region", y="Sales", title="Sales by Region",
                 color_discrete_sequence=[NAVY], text_auto=".2s")
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=55, b=10),
                      xaxis_title="", yaxis_title="Sales (₹)")
    return fig
