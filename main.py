import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Star ratings are given as words in class names like 'star-rating Three'
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
titles, prices, ratings, availability = [], [], [], []

# Loop through first 5 pages
for page in range(1, 6):
    url = base_url.format(page)
    print(f"Scraping Page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]

        raw_price = book.find("p", class_="price_color").text
        clean_price = raw_price.encode('ascii', 'ignore').decode().replace('£', '').strip()

        rating_class = book.find("p", class_="star-rating")["class"][1]
        star_rating = rating_map.get(rating_class, 0)

        in_stock = book.find("p", class_="instock availability").text.strip()

        titles.append(title)
        prices.append(float(clean_price))
        ratings.append(star_rating)
        availability.append(in_stock)

    time.sleep(1)  # polite scraping

# Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price (£)": prices,
    "Rating (1-5)": ratings,
    "Availability": availability
})

# Save to CSV
df.to_csv("enhanced_books_data.csv", index=False)
print("Data saved to 'enhanced_books_data.csv'")

import pandas as pd

pd.set_option('display.max_colwidth', None)  # Show full title text
pd.set_option('display.expand_frame_repr', False)  # Do not wrap rows
pd.set_option('display.width', 1000)  # Set wide enough width

# Analysis
print("\nTop 5 Most Expensive Books:")
print(df.sort_values("Price (£)", ascending=False).head())

print("\nAverage Price:", np.mean(df["Price (£)"]))
print("Average Rating:", np.mean(df["Rating (1-5)"]))

# Visualization
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(df["Price (£)"], bins=10, kde=True, color='skyblue')
plt.title("Book Price Distribution")

plt.subplot(1, 2, 2)
sns.countplot(x="Rating (1-5)", data=df, palette='viridis')
plt.title("Rating Distribution")

plt.tight_layout()
plt.show()
