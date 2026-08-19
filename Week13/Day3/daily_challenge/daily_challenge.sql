import os
import sqlite3
import zipfile
from pathlib import Path

import pandas as pd
from IPython.display import display

zip_path = Path("/content/Approach to Complex SQLquery Building in Kaggle.zip")

if not zip_path.exists():
    from google.colab import files
    uploaded = files.upload()
    zip_path = Path(next(iter(uploaded.keys())))

db_path = Path("/content/database.sqlite")

with zipfile.ZipFile(zip_path) as z:
    member = next(m.filename for m in z.infolist() if not m.is_dir() and Path(m.filename).name == "database.sqlite")
    with z.open(member) as source, db_path.open("wb") as target:
        target.write(source.read())

connection = sqlite3.connect(db_path)

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        AND name NOT IN ('sysdiagrams')
    ORDER BY name;
    """,
    connection,
)

display(tables)

for table_name in tables["name"]:
    columns = pd.read_sql_query(f"PRAGMA table_info({table_name});", connection)
    print(table_name, list(columns["name"]))

queries = {
    "Query 1": """
SELECT *
FROM Player_Match;
""",
    "Query 2": """
SELECT
    p.Player_Id,
    p.Player_Name AS batsman,
    SUM(bs.Runs_Scored) AS total_runs
FROM Ball_by_Ball AS b
INNER JOIN Batsman_Scored AS bs
    ON b.Match_Id = bs.Match_Id
    AND b.Over_Id = bs.Over_Id
    AND b.Ball_Id = bs.Ball_Id
    AND b.Innings_No = bs.Innings_No
INNER JOIN Player AS p
    ON b.Striker = p.Player_Id
GROUP BY p.Player_Id, p.Player_Name
ORDER BY total_runs DESC, batsman;
""",
    "Query 3": """
WITH innings_scores AS (
    SELECT
        b.Striker AS Player_Id,
        b.Match_Id,
        b.Innings_No,
        SUM(bs.Runs_Scored) AS innings_runs
    FROM Ball_by_Ball AS b
    INNER JOIN Batsman_Scored AS bs
        ON b.Match_Id = bs.Match_Id
        AND b.Over_Id = bs.Over_Id
        AND b.Ball_Id = bs.Ball_Id
        AND b.Innings_No = bs.Innings_No
    GROUP BY b.Striker, b.Match_Id, b.Innings_No
)
SELECT
    p.Player_Id,
    p.Player_Name AS batsman,
    SUM(CASE WHEN i.innings_runs BETWEEN 50 AND 99 THEN 1 ELSE 0 END) AS fifties,
    SUM(CASE WHEN i.innings_runs >= 100 THEN 1 ELSE 0 END) AS hundreds
FROM innings_scores AS i
INNER JOIN Player AS p
    ON i.Player_Id = p.Player_Id
GROUP BY p.Player_Id, p.Player_Name
HAVING fifties > 0 OR hundreds > 0
ORDER BY hundreds DESC, fifties DESC, batsman;
""",
    "Query 4": """
WITH delivery_facts AS (
    SELECT
        b.Match_Id,
        b.Innings_No,
        b.Bowler AS Player_Id,
        COALESCE(bs.Runs_Scored, 0) AS batsman_runs,
        COALESCE(er.Extra_Runs, 0) AS extra_runs,
        et.Extra_Name,
        ot.Out_Name
    FROM Ball_by_Ball AS b
    LEFT JOIN Batsman_Scored AS bs
        ON b.Match_Id = bs.Match_Id
        AND b.Over_Id = bs.Over_Id
        AND b.Ball_Id = bs.Ball_Id
        AND b.Innings_No = bs.Innings_No
    LEFT JOIN Extra_Runs AS er
        ON b.Match_Id = er.Match_Id
        AND b.Over_Id = er.Over_Id
        AND b.Ball_Id = er.Ball_Id
        AND b.Innings_No = er.Innings_No
    LEFT JOIN Extra_Type AS et
        ON er.Extra_Type_Id = et.Extra_Id
    LEFT JOIN Wicket_Taken AS wt
        ON b.Match_Id = wt.Match_Id
        AND b.Over_Id = wt.Over_Id
        AND b.Ball_Id = wt.Ball_Id
        AND b.Innings_No = wt.Innings_No
    LEFT JOIN Out_Type AS ot
        ON wt.Kind_Out = ot.Out_Id
),
bowling_innings AS (
    SELECT
        Player_Id,
        Match_Id,
        Innings_No,
        SUM(batsman_runs + CASE WHEN Extra_Name IN ('wides', 'noballs') THEN extra_runs ELSE 0 END) AS runs_conceded,
        SUM(CASE WHEN Out_Name IS NOT NULL AND Out_Name NOT IN ('run out', 'retired hurt', 'obstructing the field') THEN 1 ELSE 0 END) AS wickets
    FROM delivery_facts
    GROUP BY Player_Id, Match_Id, Innings_No
),
ranked_figures AS (
    SELECT
        Player_Id,
        Match_Id,
        Innings_No,
        runs_conceded,
        wickets,
        ROW_NUMBER() OVER (PARTITION BY Player_Id ORDER BY wickets DESC, runs_conceded ASC, Match_Id ASC) AS figure_rank
    FROM bowling_innings
)
SELECT
    p.Player_Id,
    p.Player_Name AS bowler,
    r.Match_Id,
    r.Innings_No,
    r.wickets,
    r.runs_conceded,
    r.wickets || '/' || r.runs_conceded AS best_bowling_figures
FROM ranked_figures AS r
INNER JOIN Player AS p
    ON r.Player_Id = p.Player_Id
WHERE r.figure_rank = 1
ORDER BY r.wickets DESC, r.runs_conceded ASC, bowler;
""",
    "Query 5": """
WITH player_matches AS (
    SELECT Player_Id, COUNT(DISTINCT Match_Id) AS matches_played
    FROM Player_Match
    GROUP BY Player_Id
),
delivery_facts AS (
    SELECT
        b.Match_Id,
        b.Over_Id,
        b.Ball_Id,
        b.Innings_No,
        b.Striker,
        b.Bowler,
        COALESCE(bs.Runs_Scored, 0) AS batsman_runs,
        COALESCE(er.Extra_Runs, 0) AS extra_runs,
        et.Extra_Name,
        ot.Out_Name,
        wt.Player_Out
    FROM Ball_by_Ball AS b
    LEFT JOIN Batsman_Scored AS bs
        ON b.Match_Id = bs.Match_Id
        AND b.Over_Id = bs.Over_Id
        AND b.Ball_Id = bs.Ball_Id
        AND b.Innings_No = bs.Innings_No
    LEFT JOIN Extra_Runs AS er
        ON b.Match_Id = er.Match_Id
        AND b.Over_Id = er.Over_Id
        AND b.Ball_Id = er.Ball_Id
        AND b.Innings_No = er.Innings_No
    LEFT JOIN Extra_Type AS et
        ON er.Extra_Type_Id = et.Extra_Id
    LEFT JOIN Wicket_Taken AS wt
        ON b.Match_Id = wt.Match_Id
        AND b.Over_Id = wt.Over_Id
        AND b.Ball_Id = wt.Ball_Id
        AND b.Innings_No = wt.Innings_No
    LEFT JOIN Out_Type AS ot
        ON wt.Kind_Out = ot.Out_Id
),
batting_by_player AS (
    SELECT
        Striker AS Player_Id,
        COUNT(DISTINCT Match_Id || '-' || Innings_No) AS batting_innings,
        SUM(batsman_runs) AS runs_scored,
        SUM(CASE WHEN Extra_Name NOT IN ('wides', 'noballs') OR Extra_Name IS NULL THEN 1 ELSE 0 END) AS balls_faced,
        SUM(CASE WHEN batsman_runs = 4 THEN 1 ELSE 0 END) AS fours,
        SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS sixes
    FROM delivery_facts
    GROUP BY Striker
),
batting_dismissals AS (
    SELECT Player_Out AS Player_Id, COUNT(*) AS times_out
    FROM delivery_facts
    WHERE Player_Out IS NOT NULL
        AND Out_Name <> 'retired hurt'
    GROUP BY Player_Out
),
innings_scores AS (
    SELECT
        Striker AS Player_Id,
        Match_Id,
        Innings_No,
        SUM(batsman_runs) AS innings_runs
    FROM delivery_facts
    GROUP BY Striker, Match_Id, Innings_No
),
batting_milestones AS (
    SELECT
        Player_Id,
        MAX(innings_runs) AS highest_score,
        SUM(CASE WHEN innings_runs BETWEEN 50 AND 99 THEN 1 ELSE 0 END) AS fifties,
        SUM(CASE WHEN innings_runs >= 100 THEN 1 ELSE 0 END) AS hundreds
    FROM innings_scores
    GROUP BY Player_Id
),
bowling_by_player AS (
    SELECT
        Bowler AS Player_Id,
        COUNT(DISTINCT Match_Id || '-' || Innings_No) AS bowling_innings,
        SUM(CASE WHEN Extra_Name NOT IN ('wides', 'noballs') OR Extra_Name IS NULL THEN 1 ELSE 0 END) AS balls_bowled,
        SUM(batsman_runs + CASE WHEN Extra_Name IN ('wides', 'noballs') THEN extra_runs ELSE 0 END) AS runs_conceded,
        SUM(CASE WHEN Out_Name IS NOT NULL AND Out_Name NOT IN ('run out', 'retired hurt', 'obstructing the field') THEN 1 ELSE 0 END) AS wickets
    FROM delivery_facts
    GROUP BY Bowler
),
bowling_innings AS (
    SELECT
        Bowler AS Player_Id,
        Match_Id,
        Innings_No,
        SUM(batsman_runs + CASE WHEN Extra_Name IN ('wides', 'noballs') THEN extra_runs ELSE 0 END) AS runs_conceded,
        SUM(CASE WHEN Out_Name IS NOT NULL AND Out_Name NOT IN ('run out', 'retired hurt', 'obstructing the field') THEN 1 ELSE 0 END) AS wickets
    FROM delivery_facts
    GROUP BY Bowler, Match_Id, Innings_No
),
best_bowling AS (
    SELECT
        Player_Id,
        wickets,
        runs_conceded,
        wickets || '/' || runs_conceded AS best_bowling_figures
    FROM (
        SELECT
            Player_Id,
            wickets,
            runs_conceded,
            ROW_NUMBER() OVER (PARTITION BY Player_Id ORDER BY wickets DESC, runs_conceded ASC, Match_Id ASC) AS figure_rank
        FROM bowling_innings
    )
    WHERE figure_rank = 1
)
SELECT
    p.Player_Id,
    p.Player_Name,
    COALESCE(pm.matches_played, 0) AS matches_played,
    COALESCE(bp.batting_innings, 0) AS batting_innings,
    COALESCE(bp.runs_scored, 0) AS runs_scored,
    COALESCE(bp.balls_faced, 0) AS balls_faced,
    ROUND(1.0 * COALESCE(bp.runs_scored, 0) / NULLIF(bd.times_out, 0), 2) AS batting_average,
    ROUND(100.0 * COALESCE(bp.runs_scored, 0) / NULLIF(bp.balls_faced, 0), 2) AS batting_strike_rate,
    COALESCE(bm.highest_score, 0) AS highest_score,
    COALESCE(bm.fifties, 0) AS fifties,
    COALESCE(bm.hundreds, 0) AS hundreds,
    COALESCE(bp.fours, 0) AS fours,
    COALESCE(bp.sixes, 0) AS sixes,
    COALESCE(bowl.bowling_innings, 0) AS bowling_innings,
    COALESCE(bowl.balls_bowled, 0) AS balls_bowled,
    COALESCE(bowl.runs_conceded, 0) AS runs_conceded,
    COALESCE(bowl.wickets, 0) AS wickets,
    ROUND(1.0 * COALESCE(bowl.runs_conceded, 0) / NULLIF(bowl.wickets, 0), 2) AS bowling_average,
    ROUND(6.0 * COALESCE(bowl.runs_conceded, 0) / NULLIF(bowl.balls_bowled, 0), 2) AS economy_rate,
    COALESCE(bb.best_bowling_figures, '0/0') AS best_bowling_figures
FROM Player AS p
LEFT JOIN player_matches AS pm
    ON p.Player_Id = pm.Player_Id
LEFT JOIN batting_by_player AS bp
    ON p.Player_Id = bp.Player_Id
LEFT JOIN batting_dismissals AS bd
    ON p.Player_Id = bd.Player_Id
LEFT JOIN batting_milestones AS bm
    ON p.Player_Id = bm.Player_Id
LEFT JOIN bowling_by_player AS bowl
    ON p.Player_Id = bowl.Player_Id
LEFT JOIN best_bowling AS bb
    ON p.Player_Id = bb.Player_Id
ORDER BY runs_scored DESC, wickets DESC, Player_Name;
"""
}

for title, sql in queries.items():
    print(title)
    display(pd.read_sql_query(sql, connection).head(20))

connection.close()
