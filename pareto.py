import pypyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def pareto_chart(mc_no):
    """query data from sql then return pareto chart """
    cnxn = pypyodbc.connect("Driver= {SQL Server};"
                            "Server=192.168.1.102\SQLEXPRESS;"
                            "Database=test;"
                            "uid=sa;pwd=sa@admin")
    df = pd.read_sql_query(f"SELECT  [defect],[pcs],[mc_no] FROM [test].[dbo].[ng_defect] where [mc_no] ='{mc_no}' ",cnxn)
    if len(df)== 0:
        return None
    df = df.sort_values(by='pcs', ascending=False)
    df["cum_percentage"] = round((df["pcs"]).cumsum()/df["pcs"].sum()*100,2)
    
    x = df['defect']
    y = df['pcs']
    y2 = df['cum_percentage']

    fig,ax =plt.subplots(figsize=(22,10))

    ax.bar(x,y)
    ax.set_title(f"Pareto chart {mc_no}")
    ax.set_xlabel("defect Error")
    ax.set_ylabel("pcs")

    ax2 = ax.twinx()
    ax2.plot(x,y2,color="red",marker="D",ms=7)
    ax2.axhline(80,color="orange",linestyle="dashed")
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel("Cumulative Percentage")
    #plt.show()
    return fig