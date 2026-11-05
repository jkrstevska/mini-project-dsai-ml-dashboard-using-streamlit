import streamlit as st
import matplotlib.pyplot as plt

from sakila import query

st.set_page_config(page_title="Explore", page_icon="📊", layout="wide")
st.title("📊 Explore the rentals")

# TODO 4: a line chart of the daily rentals of each store in 2005.
#   - rental has rental_date; inventory links each rental (inventory_id) to a store (store_id).
#   - In SQLite, DATE(rental_date) gives the day and STRFTIME('%Y', rental_date) the year.
#   - st.line_chart draws one line per column: pivot the result so that each store is a column.

st.subheader("Daily rentals of each store in 2005")
daily = query(
        """
        SELECT 
            DATE(rental_date) AS day, 
            store_id, 
            COUNT(*) AS rentals
        FROM rental
        JOIN inventory USING (inventory_id)
        WHERE STRFTIME('%Y', rental_date) = '2005'
        GROUP BY day, store_id
        ORDER BY day, store_id
        """
    ).pivot(index="day", columns="store_id", values="rentals")

daily.columns = [f"Store {s}" for s in daily.columns]

st.line_chart(daily)

# TODO 5: a bar chart of the total revenue of each store (payment -> rental -> inventory).

revenue = query(
    """
    SELECT 
        store_id, 
        SUM(amount) AS revenue
    FROM payment p
    JOIN rental r    
        ON p.rental_id = r.rental_id
    JOIN inventory i 
        ON r.inventory_id = i.inventory_id
    GROUP BY store_id
    """
)

st.subheader("Total revenue per store")
st.bar_chart(revenue, x="store_id", y="revenue")

# TODO 6: the top 5 most rented films of each store in 2005, one st.dataframe per store, side by side.

def top_films(store_id):
    return query(
        f"""
        SELECT 
            f.title, 
            COUNT(*) AS rentals
        FROM rental r
        JOIN inventory i 
            ON r.inventory_id = i.inventory_id
        JOIN film f 
            ON i.film_id = f.film_id
        WHERE STRFTIME('%Y', r.rental_date) = '2005'
            AND i.store_id = {store_id}
        GROUP BY f.film_id
        ORDER BY rentals DESC
        LIMIT 5
        """
    )
st.subheader("Top 5 most rented films in 2005")
left, right = st.columns(2)
with left:
    st.markdown("**Store 1**")
    st.dataframe(top_films(1), hide_index=True)
with right:
    st.markdown("**Store 2**")
    st.dataframe(top_films(2), hide_index=True)