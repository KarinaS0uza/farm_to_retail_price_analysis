import pandas as pd
import plotly.express as px
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title='U.S. Meat Supply Chain Price Analysis',
    layout='wide'
)

# Load data
df = pd.read_csv('meat_price_history.csv')

# Feature engineering: Map Data_Item to SCM stage, meat type, and metric type
stage_map = {
    'Pork gross farm value': 'Farm',
    'Pork net farm value': 'Farm',
    'Pork byproduct value': 'Farm',
    'Choice beef gross farm value': 'Farm',
    'Choice beef net farm value': 'Farm',
    'Choice beef byproduct value': 'Farm',
    'Pork wholesale value': 'Wholesale',
    'Choice beef wholesale value': 'Wholesale',
    'Wholesale broiler composite': 'Wholesale',
    'Pork retail value': 'Retail',
    'Choice beef retail value': 'Retail',
    'All fresh beef retail value': 'Retail',
    'Retail broiler composite': 'Retail',
    'Pork farm to retail price spread': 'Spread',
    'Pork farm to wholesale price spread': 'Spread',
    'Pork Wholesale to retail price spread': 'Spread',
    'Choice beef farm to retail price spread': 'Spread',
    'Choice beef farm to wholesale price spread': 'Spread',
    'Choice beef wholesale to retail price spread': 'Spread',
    'Retail-wholesale spread for broiler composite': 'Spread'
}

meat_map = {
    'Pork byproduct value': 'Pork',
    'Pork gross farm value': 'Pork',
    'Pork net farm value': 'Pork',
    'Pork wholesale value': 'Pork',
    'Pork retail value': 'Pork',
    'Pork farm to retail price spread': 'Pork',
    'Pork farm to wholesale price spread': 'Pork',
    'Pork Wholesale to retail price spread': 'Pork',
    'Choice beef byproduct value': 'Beef',
    'Choice beef gross farm value': 'Beef',
    'Choice beef net farm value': 'Beef',
    'Choice beef wholesale value': 'Beef',
    'Choice beef retail value': 'Beef',
    'Choice beef farm to retail price spread': 'Beef',
    'Choice beef farm to wholesale price spread': 'Beef',
    'Choice beef wholesale to retail price spread': 'Beef',
    'All fresh beef retail value': 'Beef',
    'Wholesale broiler composite': 'Chicken',
    'Retail broiler composite': 'Chicken',
    'Retail-wholesale spread for broiler composite': 'Chicken'
}

metric_map = {
    'Pork byproduct value': 'Byproduct',
    'Choice beef byproduct value': 'Byproduct',
    'Pork gross farm value': 'Value',
    'Pork net farm value': 'Value',
    'Pork wholesale value': 'Value',
    'Pork retail value': 'Value',
    'Choice beef gross farm value': 'Value',
    'Choice beef net farm value': 'Value',
    'Choice beef wholesale value': 'Value',
    'Choice beef retail value': 'Value',
    'All fresh beef retail value': 'Value',
    'Wholesale broiler composite': 'Value',
    'Retail broiler composite': 'Value',
    'Pork farm to retail price spread': 'Spread',
    'Pork farm to wholesale price spread': 'Spread',
    'Pork Wholesale to retail price spread': 'Spread',
    'Choice beef farm to retail price spread': 'Spread',
    'Choice beef farm to wholesale price spread': 'Spread',
    'Choice beef wholesale to retail price spread': 'Spread',
    'Retail-wholesale spread for broiler composite': 'Spread'
}

df['SCM_Stage'] = df['Data_Item'].map(stage_map)
df['Meat_Type'] = df['Data_Item'].map(meat_map)
df['Metric_Type'] = df['Data_Item'].map(metric_map)

# Fix 2025 chickens unit labeling issue
df.loc[
    (df['Meat_Type'] == 'Chicken') &
    (df['Units'] == 'Cents per pound of retail equivalent'),
    'Units'
] = 'Cents per retail pound'

# Clean dataframe
clean_df = df.dropna(subset=['Value']).copy()

def classify_spread(item):
    item = item.lower()
    if 'farm to retail' in item:
        return 'Farm to Retail'
    elif 'farm to wholesale' in item:
        return 'Farm to Wholesale'
    elif 'wholesale to retail' in item or 'retail-wholesale' in item:
        return 'Wholesale to Retail'
    else:
        return 'Other'

clean_df['Spread_Type'] = clean_df['Data_Item'].apply(classify_spread)
spread_df = clean_df[clean_df['Metric_Type'] == 'Spread']

# Color maps
stage_colors = {'Farm': 'blue', 'Wholesale': 'red', 'Retail': 'green'}
spread_colors = {
    'Farm to Retail': 'green',
    'Wholesale to Retail': '#F39C12',
    'Farm to Wholesale': 'red'
}
hist_colors = {
    'Pork': '#7BC8A4',      # soft green
    'Beef': '#F4A6A6',      # soft red/pink
    'Chicken': '#89CFF0'   # soft blue
}

# Header
st.title('U.S. Meat Supply Chain Value Analysis (1970–2025)')
st.write(
    'The dashboards below explore how meat values change across the supply chain '
    'from farm to wholesale to retail for pork, beef, and chicken between 1970 and 2025. '
    'All data were sourced from the U.S. Department of Agriculture (USDA).'
)

st.divider()

# Chart 1: SCM Summary Table
st.header('1. Supply Chain Category Overview')
st.write(
    'This table shows which data categories are available for each meat type '
    'across the four supply chain stages.'
)

scm_summary = pd.DataFrame({
    'SCM Stage': [
        'Stage 1: Farm Production',
        'Stage 1: Farm Production',
        'Stage 1: Farm Production',
        'Stage 2: Wholesale',
        'Stage 3: Retail',
        'Stage 4: Price Spreads',
        'Stage 4: Price Spreads',
        'Stage 4: Price Spreads'
    ],
    'Category': [
        'Gross farm value',
        'Byproduct value',
        'Net farm value',
        'Wholesale value / composite',
        'Retail value / composite',
        'Farm to retail price spread',
        'Farm to wholesale price spread',
        'Wholesale to retail price spread'
    ],
    'Pork': ['✓', '✓', '✓', '✓', '✓', '✓', '✓', '✓'],
    'Choice Beef': ['✓', '✓', '✓', '✓', '✓', '✓', '✓', '✓'],
    'All Fresh Beef': ['—', '—', '—', '—', '✓', '—', '—', '—'],
    'Chicken': ['—', '—', '—', '✓', '✓', '—', '—', '✓']
})

st.dataframe(scm_summary, width='stretch', hide_index=True)

st.caption(
    'Farm, wholesale, and retail values represent the economic value recorded '
    'at each stage of the meat supply chain. Price spreads represent the '
    'difference in value between stages, showing how much value is added as '
    'products move from producers to wholesalers and retailers.'
)

st.divider()

# Chart 2: Value Transmission with dropdown
st.header('2. Value Changes Across the Supply Chain')
st.write(
    'Select a meat type to see how values differ at each stage'
)

meat_choice = st.selectbox(
    'Select meat type:',
    options=['Pork', 'Beef', 'Chicken'],
    key='transmission'
)

if meat_choice == 'Pork':
    values_df = clean_df[
        (clean_df['Meat_Type'] == 'Pork') &
        (clean_df['Metric_Type'] == 'Value')
    ]
    values_df = values_df[
        ~values_df['Data_Item'].isin(['Pork byproduct value', 'Pork gross farm value'])
    ]
elif meat_choice == 'Beef':
    values_df = clean_df[
        (clean_df['Meat_Type'] == 'Beef') &
        (clean_df['Metric_Type'] == 'Value')
    ]
    values_df = values_df[
        ~values_df['Data_Item'].isin([
            'Choice beef byproduct value',
            'Choice beef gross farm value',
            'All fresh beef retail value'
        ])
    ]
else:
    values_df = clean_df[
        (clean_df['Meat_Type'] == 'Chicken') &
        (clean_df['Metric_Type'] == 'Value')
    ]

fig2 = px.line(
    values_df,
    x='Year',
    y='Value',
    color='SCM_Stage',
    title=f'{meat_choice} Value Change Across the Supply Chain',
    labels={'Value': 'Value (cents/lb)', 'SCM_Stage': 'Supply Chain Stage'},
    color_discrete_map=stage_colors
)

# Lock the Supply Chain Stage legend so it can’t be clicked
fig2.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

st.plotly_chart(fig2, use_container_width=True)

if meat_choice == 'Chicken':
    st.caption(
        '⚠️ Note: Farm-level data is not available for chicken. '
        'The vast majority of chickens are produced under vertical integration contracts, '
        'where the wholesaler owns the birds and pays growers a per-unit fee. '
        'Because there is no independent farm market value for chicken, '
        'USDA ERS does not publish a farm value for chickens. '
        'This chart shows wholesale and retail stages only.'
    )

st.divider()

# Chart 3: Price Spreads with dropdown
st.header('3. Supply Chain Price Spreads Over Time')
st.write(
    'Price spreads show the margin added at each stage. '
)

meat_choice_spread = st.selectbox(
    'Select meat type:',
    options=['Pork', 'Beef', 'Chicken'],
    key='spreads'
)

spreads_filtered = spread_df[spread_df['Meat_Type'] == meat_choice_spread]

fig3 = px.line(
    spreads_filtered,
    x='Year',
    y='Value',
    color='Spread_Type',
    title=f'{meat_choice_spread} Supply Chain Price Spreads',
    labels={'Value': 'Spread (cents/lb)', 'Spread_Type': 'Spread Type'},
    color_discrete_map=spread_colors
)

fig3.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

st.plotly_chart(fig3, use_container_width=True)

if meat_choice_spread == 'Chicken':
    st.caption(
        '⚠️ Note: Only the Wholesale-to-Retail spread is available for chicken. '
        'Farm-to-Retail and Farm-to-Wholesale spreads cannot be calculated '
        'because there is no farm-level price series for chickens in the USDA dataset.'
    )

st.divider()

# Chart 4: Value vs Spread comparison
# Chart 4: Value vs Spread comparison
st.header('4. Who Captures the Most Value?')

st.write(
    'This chart compares the net farm value (what farmers receive) '
    'against the farm-to-retail spread (what the marketing chain captures) '
    'for pork and beef over time. A wider spread indicates that a larger '
    'share of value is captured by wholesalers and retailers rather than producers.'
)

wide = clean_df.pivot_table(
    index='Year',
    columns='Data_Item',
    values='Value',
    aggfunc='mean'
).reset_index()

meat_choice_comp = st.selectbox(
    'Select meat type:',
    options=['Pork', 'Beef'],
    key='comparison'
)

if meat_choice_comp == 'Pork':
    farm_col = 'Pork net farm value'
    spread_col = 'Pork farm to retail price spread'
else:
    farm_col = 'Choice beef net farm value'
    spread_col = 'Choice beef farm to retail price spread'

comparison_df = wide[['Year', farm_col, spread_col]].dropna()

comparison_df = comparison_df.melt(
    id_vars='Year',
    value_vars=[farm_col, spread_col],
    var_name='Metric',
    value_name='Value'
)

label_map = {
    farm_col: 'Net Farm Value (farmers receive)',
    spread_col: 'Farm-to-Retail Spread (marketing chain captures)'
}

comparison_df['Metric'] = comparison_df['Metric'].map(label_map)

fig4 = px.line(
    comparison_df,
    x='Year',
    y='Value',
    color='Metric',
    title=f'{meat_choice_comp}: Farm Value vs Marketing Chain Spread (1970–2025)',
    labels={
        'Value': 'Value / Spread (cents/lb)',
        'Year': 'Year'
    },
    color_discrete_map={
        'Net Farm Value (farmers receive)': '#89CFF0',
        'Farm-to-Retail Spread (marketing chain captures)': '#7BC8A4'
    }
)

# Prevent legend toggling
fig4.update_layout(
    legend_itemclick=False,
    legend_itemdoubleclick=False
)

st.plotly_chart(fig4, width='stretch')

if meat_choice_comp == 'Beef':
    st.caption(
        '⚠️ The USDA dataset distinguishes between "Choice Beef" and '
        '"All Fresh Beef" series. This chart uses the Choice Beef farm-to-retail '
        'spread because farm-level and spread data are only available for the '
        'Choice Beef category. "All Fresh Beef" data are available only at the '
        'retail stage.'
    )

st.divider()


# Chart 5: Distribution of Supply Chain Spreads
# Histogram
st.header('5. Distribution of Supply Chain Spreads')

wide = clean_df.pivot_table(
    index='Year',
    columns='Data_Item',
    values='Value',
    aggfunc='mean'
).reset_index()

# Create combined dataframe for histogram
hist_df = pd.DataFrame({
    'Pork': wide['Pork farm to retail price spread'],
    'Beef': wide['Choice beef farm to retail price spread'],
    'Chicken': wide['Retail-wholesale spread for broiler composite']
})

# Convert to long format
hist_long = hist_df.melt(
    var_name='Meat Type',
    value_name='Spread'
)

# Remove missing values
hist_long = hist_long.dropna()

fig = px.histogram(
    hist_long,
    x='Spread',
    color='Meat Type',
    barmode='overlay',
    opacity=0.6,
    title='Distribution of Supply Chain Spreads',
    labels={
        'Spread': 'Spread (cents/lb)',
        'count': 'Number of Years in Range'
    },
    color_discrete_map=hist_colors
)

fig.update_yaxes(title='Number of Years in Range')

st.plotly_chart(fig, width='stretch')

st.caption(
    '⚠️ Chicken data represents the wholesale-to-retail spread only, '
    'because USDA does not publish farm-level chicken value series. '
    'Pork and beef represent farm-to-retail spreads, so comparisons should '
    'be interpreted cautiously.'
)


# Chart 6: Pork Wholesale vs Retail Value Relationship
# Scatter — Pork Wholesale vs Retail value
st.header('6. Wholesale vs Retail Value Relationship')

st.write(
    'This scatterplot shows the relationship between wholesale and retail '
    'values over time for pork and beef. Each point represents a monthly '
    'observation between 1970 and 2025.'
)

# Meat selection
meat_choice_scatter = st.selectbox(
    'Select meat type:',
    options=['Pork', 'Beef'],
    key='scatter'
)

# Select dataset and columns dynamically
if meat_choice_scatter == 'Pork':
    meat_df = clean_df[clean_df['Meat_Type'] == 'Pork']
    wholesale_col = 'Pork wholesale value'
    retail_col = 'Pork retail value'
else:
    meat_df = clean_df[clean_df['Meat_Type'] == 'Beef']
    wholesale_col = 'Choice beef wholesale value'
    retail_col = 'Choice beef retail value'

# Reshape data
meat_wide = meat_df.pivot_table(
    index=['Year', 'Month-number'],
    columns='Data_Item',
    values='Value'
).reset_index()

# Scatterplot
fig = px.scatter(
    meat_wide,
    x=wholesale_col,
    y=retail_col,
    color='Year',
    title=f'{meat_choice_scatter} Wholesale vs Retail Value (1970–2025)',
    labels={
        wholesale_col: 'Wholesale Value (cents/lb)',
        retail_col: 'Retail Value (cents/lb)'
    }
)

st.plotly_chart(fig, width='stretch')

if meat_choice_scatter == 'Beef':
    st.caption(
        '⚠️ This chart uses the USDA Choice Beef series because wholesale '
        'and retail value data are not available for the All Fresh Beef category.'
    )
