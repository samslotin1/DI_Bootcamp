# Superstore data blending dashboard

## Data sources and blend keys

The packaged Tableau workbook contains three separate sources from the supplied Sample Superstore workbook:

- **Orders** is the primary source for sales, profit, category, region, and order counts.
- **Returns** blends to Orders on **Order ID** for the returned-order numerator.
- **People** blends to Orders on **Region** to assign each regional sales total to its manager.

## Tableau calculation for return rate

Set **Orders** as the primary source and activate the **Order ID** link to Returns. In the Return rate by category worksheet, create these calculated fields:

```
Returned orders = COUNTD(IF [Returns].[Returned] = 'Yes' THEN [Returns].[Order ID] END)
Return rate = [Returned orders] / COUNTD([Orders].[Order ID])
```

Format `Return rate` as a percentage. For the regional-manager view, activate the **Region** link from Orders to People and use `ATTR([People].[Person])` as the manager label.

## Key findings

- Total sales are **$2,297,201** and total profit is **$286,397**.
- **West** leads sales at **$725,458**.
- **Technology** has the highest returned-order rate at **8.0%**.
- **Copiers** produces the highest sub-category profit at **$55,618**.
