import os
import webbrowser
import pandas as pd
import plotly.express as px

# reading data
df = pd.read_excel("data/youtube_data.xlsx")
df["published_at"] = pd.to_datetime(df["published_at"])
print("Rows aur columns:", df.shape)

os.makedirs("charts", exist_ok=True)

# Chart 1: Top 10 videos by views
top = df.nlargest(10, "views")
fig1 = px.bar(top, x="views", y="title", orientation="h",
              title="Top 10 Videos by Views")
fig1.update_layout(yaxis={"categoryorder": "total ascending"})

# Chart 2: views with time
fig2 = px.line(df.sort_values("published_at"), x="published_at", y="views",
               hover_name="title", title="Views Over Time")

# Chart 3: Likes vs Views
fig3 = px.scatter(df, x="views", y="likes", size="comments",
                  hover_name="title", title="Likes vs Views")

# Chart 4: Views distribution
fig4 = px.histogram(df, x="views", nbins=30, title="Views Distribution")

# Chart 5: according  to Uploading day average views
df["weekday"] = df["published_at"].dt.day_name()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = df.groupby("weekday")["views"].mean().reindex(order).reset_index()
fig5 = px.bar(wd, x="weekday", y="views", title="Average Views by Upload Day")

figs = [fig1, fig2, fig3, fig4, fig5]

# ---------- 3. Sab charts ko ek HTML page mein jodo ----------
parts = []
for i, fig in enumerate(figs):
    parts.append(
        fig.to_html(
            full_html=False,                              # sirf chart ka tukra, poora page nahi
            include_plotlyjs="cdn" if i == 0 else False,  # Plotly ki JS sirf ek baar load ho
        )
    )

charts_html = "\n".join(f'<div class="card">{p}</div>' for p in parts)

page = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>YouTube Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f2f2f2; margin: 0; padding: 20px; }}
    h1 {{ text-align: center; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
    .card {{ background: white; border-radius: 10px; padding: 10px; }}
  </style>
</head>
<body>
  <h1>YouTube Data Dashboard</h1>
  <div class="grid">
    {charts_html}
  </div>
</body>
</html>"""

# ---------- 4. Save karo aur browser mein kholo ----------
with open("charts/dashboard.html", "w", encoding="utf-8") as f:
    f.write(page)

webbrowser.open("file://" + os.path.abspath("charts/dashboard.html"))
print("Dashboard ban gaya: charts/dashboard.html")
