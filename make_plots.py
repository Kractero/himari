import pandas as pd
import plotly.express as px

df = pd.read_csv('files/trades.csv')

pivot = df.pivot_table(
    index='trade_day',
    columns=['season', 'category'],
    values=['total_trades', 'total_price', 'total_buyers', 'total_sellers', 'total_gifts'],
    aggfunc='sum'
).fillna(0)

pivot.columns = [f"{col[0]}_season{col[1]}_{col[2]}" for col in pivot.columns]
pivot = pivot.reset_index()

buyer_cols = [col for col in pivot.columns if 'total_buyers' in col]
seller_cols = [col for col in pivot.columns if 'total_sellers' in col]
trade_cols = [col for col in pivot.columns if 'total_trades' in col]
price_cols = [col for col in pivot.columns if 'total_price' in col]
gift_cols = [col for col in pivot.columns if 'total_gifts' in col]

pivot['total_buyers'] = pivot[buyer_cols].sum(axis=1)
pivot['total_sellers'] = pivot[seller_cols].sum(axis=1)
pivot['total_nations'] = pivot['total_buyers'] + pivot['total_sellers']
pivot['total_trades'] = pivot[trade_cols].sum(axis=1)
pivot['total_price'] = pivot[price_cols].sum(axis=1)
pivot['total_gifts'] = pivot[gift_cols].sum(axis=1)
pivot['total_auctions'] = pivot['total_trades'] - pivot['total_gifts']

pivot['season_1_trades'] = pivot[[col for col in trade_cols if '1' in col]].sum(axis=1)
pivot['season_2_trades'] = pivot[[col for col in trade_cols if '2' in col]].sum(axis=1)
pivot['season_3_trades'] = pivot[[col for col in trade_cols if '3' in col]].sum(axis=1)

pivot['season_1_prices'] = pivot[[col for col in price_cols if '1' in col]].sum(axis=1)
pivot['season_2_prices'] = pivot[[col for col in price_cols if '2' in col]].sum(axis=1)
pivot['season_3_prices'] = pivot[[col for col in price_cols if '3' in col]].sum(axis=1)

pivot['commons'] = pivot[[col for col in trade_cols if '_c' in col]].sum(axis=1)
pivot['uncommons'] = pivot[[col for col in trade_cols if '_u' in col]].sum(axis=1)
pivot['rares'] = pivot[[col for col in trade_cols if '_r' in col]].sum(axis=1)
pivot['ultra-rares'] = pivot[[col for col in trade_cols if '_ur' in col]].sum(axis=1)
pivot['epics'] = pivot[[col for col in trade_cols if '_e' in col]].sum(axis=1)
pivot['legendaries'] = pivot[[col for col in trade_cols if '_l' in col]].sum(axis=1)

pivot['commons_prices'] = pivot[[col for col in price_cols if '_c' in col]].sum(axis=1)
pivot['uncommons_prices'] = pivot[[col for col in price_cols if '_u' in col]].sum(axis=1)
pivot['rares_prices'] = pivot[[col for col in price_cols if '_r' in col]].sum(axis=1)
pivot['ultra-rares_prices'] = pivot[[col for col in price_cols if '_ur' in col]].sum(axis=1)
pivot['epics_prices'] = pivot[[col for col in price_cols if '_e' in col]].sum(axis=1)
pivot['legendaries_prices'] = pivot[[col for col in price_cols if '_l' in col]].sum(axis=1)


# Plot 1: Total trades per day - broken down real trades vs gifts
fig1 = px.area(
    pivot,
    x='trade_day',
    y=['total_auctions', 'total_gifts'],
    title='Total Trades Per Day (Auctions and Gifts)',
    labels={'trade_day': 'Day', 'value': 'Trades'},
    color_discrete_sequence=px.colors.qualitative.Pastel1,
)
fig1.add_scatter(
    x=pivot['trade_day'],
    y=pivot['total_trades'],
    mode='lines',
    name='Total Trades',
    line=dict(color='black', width=1),
)
# fig1.show()
fig1.write_html("files/plot1.html")

# Plot 2: Total volume (price) moved on the market per day
fig2 = px.line(
    pivot,
    x='trade_day',
    y='total_price',
    title='Total Volume (Price) Per Day',
    labels={'trade_day': 'Day', 'total_price': 'Total Volume'},
)
# fig2.show()
fig2.write_html("files/plot2.html")

# Plot 3: Total nations - broken into buyers and sellers
fig3 = px.area(
    pivot,
    x='trade_day',
    y=['total_buyers', 'total_sellers'],
    title='Total Nations Per Day (Buyers and Sellers)',
    labels={'trade_day': 'Day', 'value': 'Count'},
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig3.add_scatter(
    x=pivot['trade_day'],
    y=pivot['total_nations'],
    mode='lines',
    name='Total Nations',
    line=dict(color='black', width=1),
)
# fig3.show()
fig3.write_html("files/plot3.html")

# Plot 4: Total trades per day - broken into seasons
fig4 = px.area(
    pivot,
    x='trade_day',
    y=['season_1_trades', 'season_2_trades', 'season_3_trades'],
    title='Trades Per Day by Season',
    labels={'trade_day': 'Day', 'value': 'Trades'},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig4.add_scatter(
    x=pivot['trade_day'],
    y=pivot['total_trades'],
    mode='lines',
    name='Total Trades',
    line=dict(color='black', width=1),
)
# fig4.show()
fig4.write_html("files/plot4.html")

# Plot 5: Total trades per day - broken into rarities
color_scheme = {
    'commons': '#7e7e7e',         # Common
    'uncommons': '#00aa4c',       # Uncommon
    'rares': '#008ec1',           # Rare
    'ultra-rares': '#ac00e6',     # Ultra Rare
    'epics': '#db9e1c',           # Epic
    'legendaries': 'gold'         # Legendary
}

fig5 = px.area(
    pivot,
    x='trade_day',
    y=['commons', 'uncommons', 'rares', 'ultra-rares', 'epics', 'legendaries'],
    title='Trades Per Day by Category',
    labels={'trade_day': 'Day', 'value': 'Trades'},
    color_discrete_map=color_scheme
)
fig5.add_scatter(
    x=pivot['trade_day'],
    y=pivot['total_trades'],
    mode='lines',
    name='Total Trades',
    line=dict(color='black', width=1),
)
# fig5.show()
fig5.write_html("files/plot5.html")

# Plot 6: Total price per day - broken into seasons
fig6 = px.area(
    pivot,
    x='trade_day',
    y=['season_1_prices', 'season_2_prices', 'season_3_prices'],
    title='Price Per Day by Season',
    labels={'trade_day': 'Day', 'value': 'Price'},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig6.add_scatter(
    x=pivot['trade_day'],
    y=pivot['total_price'],
    mode='lines',
    name='Total Price',
    line=dict(color='black', width=1),
)
# fig6.show()
fig6.write_html("files/plot6.html")

color_scheme = {
    'commons_prices': '#7e7e7e',         # Common
    'uncommons_prices': '#00aa4c',       # Uncommon
    'rares_prices': '#008ec1',           # Rare
    'ultra-rares_prices': '#ac00e6',     # Ultra Rare
    'epics_prices': '#db9e1c',           # Epic
    'legendaries_prices': 'gold'         # Legendary
}

# Plot 7: Total price broken down into rarities
fig7 = px.area(
    pivot,
    x='trade_day',
    y=['commons_prices', 'uncommons_prices', 'rares_prices', 'ultra-rares_prices', 'epics_prices', 'legendaries_prices'],
    title='Price Per Day by Category',
    labels={'trade_day': 'Day', 'value': 'Price'},
    color_discrete_map=color_scheme
)
fig7.add_scatter(
    x=pivot['trade_day'],
    y=pivot['total_price'],
    mode='lines',
    name='Total Price',
    line=dict(color='black', width=1),
)

# fig7.show()
fig7.write_html("files/plot7.html")

print ("Done with plotly generation")