"""The home page. Run the whole app from the your-code folder:

    streamlit run Home.py
"""

import streamlit as st

from sakila import query       # query("SELECT ...") returns a DataFrame, cached

st.set_page_config(page_title="Sakila DVD Rentals", page_icon="🎬", layout="wide")

# TODO 1: a title (st.title) and an image of your choice (st.image, with a URL or a file).
st.title("Sakila DVD Rentals")
st.image("https://i.pinimg.com/736x/0a/9a/fe/0a9afe87dce550f3b5979d47745d3d19.jpg", caption="Welcome to Sakila DVD Rentals")

# TODO 2: one sentence for the store managers: what this dashboard is for.
st.write("This dashboard provides insights into the Sakila DVD rental business, including film inventory, customer activity, and revenue trends.")

# TODO 3: four st.metric numbers in four st.columns: the number of films, customers and rentals,
#         and the total revenue (the sum of payment.amount). One SQL query can return all four.
films, customers, rentals, revenue = query("""
    SELECT
        (SELECT COUNT(*) FROM film) AS films,
        (SELECT COUNT(*) FROM customer) AS customers,
        (SELECT COUNT(*) FROM rental) AS rentals,
        (SELECT SUM(amount) FROM payment) AS revenue
""").iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Films", f"{int(films):,}")
col2.metric("Customers", f"{int(customers):,}")
col3.metric("Rentals", f"{int(rentals):,}")
col4.metric("Revenue", f"${revenue:,.2f}")