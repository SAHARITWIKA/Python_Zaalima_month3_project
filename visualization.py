import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from db import fetch_transactions

def plot_summary(user_id):
    data = fetch_transactions(user_id)
    df = pd.DataFrame(data, columns=["id","user_id","type","category","amount","date"])

    if df.empty:
        return "No data available to visualize."

    # Bar chart
    plt.figure(figsize=(8,5))
    sns.barplot(x="category", y="amount", hue="type", data=df, estimator=sum)
    plt.title("Expenses & Income by Category")
    plt.show()

    # Pie chart for expenses
    expense_df = df[df['type']=="Expense"]
    if not expense_df.empty:
        plt.figure(figsize=(6,6))
        expense_df.groupby("category")["amount"].sum().plot.pie(autopct="%1.1f%%")
        plt.title("Expense Breakdown")
        plt.show()

    return "Visualization complete."
