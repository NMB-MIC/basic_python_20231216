import pandas as pd
import matplotlib.pyplot as plt

HOUR_MINUTE_SCALE = 30
production_plan_shifts = {"M": 12*HOUR_MINUTE_SCALE,
                        "N":12*HOUR_MINUTE_SCALE,
                        "MN":24*HOUR_MINUTE_SCALE,
                        "A":7*HOUR_MINUTE_SCALE,
                        "B":7*HOUR_MINUTE_SCALE,
                        "C":7*HOUR_MINUTE_SCALE,
                        "AB":14*HOUR_MINUTE_SCALE,
                        "ABC":24*HOUR_MINUTE_SCALE}

def read_dataset():
    """read raw data from excel file"""
    df_machine_data = pd.read_excel("production_data/machine_data.xlsx")
    df_planing_data = pd.read_excel("production_data/planing_data.xlsx")
    df_ng_data = pd.read_excel("production_data/ng_data.xlsx")
    return df_machine_data,df_planing_data,df_ng_data

def oee_chart(date,machine_no):
    """
    A: Total available time
    B: Run time
    C: Production capacity
    D: Actual production
    E: Product output
    F : Actual good products 
    """
    df_machine_data,df_planing_data,df_ng_data = read_dataset()
    
    # Total available time

    shifts = df_planing_data[(df_planing_data["date"] ==  date) & (df_planing_data["machine_no"] == machine_no)]

    if len(shifts) == 0:
        return "Error: No have data planning"
    else:
        shifts = shifts["shift"].values[0]
        
    A = production_plan_shifts[shifts]

    # Run time
    downtime = df_machine_data[(df_machine_data["date"] == date) & (df_machine_data["machine_no"] == machine_no)]["accum_time(min)"].sum()
    B = A-downtime

    #Production capacity
    C = df_planing_data[(df_planing_data["date"] ==  date ) & (df_planing_data["machine_no"] == machine_no)]["planning(pcs)"].sum()
 
    # Actual production
    D = df_ng_data[(df_ng_data["date"] ==  date ) & (df_ng_data["machine_no"] == machine_no)]["output"].sum()
    if D == 0:
        return "Error: No have data actual production "

    # Product output
    E = D

    # Actual good products
    df_ng_data["finish_goods"] = df_ng_data["output"]-df_ng_data["ng"]
    F = df_ng_data[(df_ng_data["date"] ==  date ) & (df_ng_data["machine_no"] == machine_no)]["finish_goods"].sum()

    if B <= A and D <= C and E == D and F <= E: 
        oee_indicator = {}
        oee_indicator["avialability"] = round(B/A*100,2)
        oee_indicator["perormance_efficiency"] = round(D/C*100,2)
        oee_indicator["quilty_rate"] = round(F/E*100,2)
        oee_indicator["oee"] = round(oee_indicator["avialability"]/100*oee_indicator["perormance_efficiency"]/100*oee_indicator["quilty_rate"]/100*100,2)
        

        # % Total available time
        profits=[100]
        # % Run time
        profits.append(B/A*100)
            # % Production capacity
        profits.append(B/A*100)
            # % Actual production
        profits.append(D/C*profits[2])
            # % Product output
        profits.append(D/C*profits[2])
            # % Actual good products
        profits.append(F/E*profits[4])
    
            # Define a list for losses percentages
        loss=[0]
            # % Time losses
        loss.append(profits[0]-profits[1])
        
        loss.append(profits[1]-profits[2])
        
            # % Speed losses
        loss.append(profits[2]-profits[3])
        
        loss.append(profits[3]-profits[4])
        
            # % Defective units
        loss.append(profits[4]-profits[5])


        ind = [0,1,2,3,4,5]

        fig = plt.figure(figsize=(20,10))
        plt.barh(ind,profits,color='#03C03C')
        plt.barh(ind,loss,left=profits,color='red')
        plt.gca().invert_yaxis()

        plt.yticks([])
        # Add OEE components
        plt.text(0, 0, 'Total Available Time', horizontalalignment='left')
        plt.text(0, 1, 'Run Time', horizontalalignment='left')
        plt.text(profits[1], 1, 'Time Losses', horizontalalignment='left')
        plt.text(0, 2, 'Production Capacity', horizontalalignment='left')
        plt.text(0, 3, 'Actual Production', horizontalalignment='left')
        plt.text(profits[3], 3, 'Speed Losses', horizontalalignment='left')
        plt.text(0, 4, 'Product Output', horizontalalignment='left')
        plt.text(0, 5, 'Actual Good Products', horizontalalignment='left')
        plt.text(profits[5], 5, 'Defective Units', horizontalalignment='left')

        plt.title(f"OEE of MC no:{machine_no} at date:{date}")
        plt.xlabel("Percentage")

        # Plot OEE universal benchmarks
        plt.axvline(85, linestyle='dashed', color='black', label='World Class OEE')
        plt.axvline(60, linestyle='dashdot', color='black', label='Typical OEE')
        plt.axvline(40, linestyle='dotted', color='black', label='Low OEE')
        return fig
        # Errors validation
    if B > A:
        return 'Error. The run time cannot be greater than the total available time.'     
    if D > C:
        return 'Error. The actual production cannot be greater than the production capacity.'       
    if E != D:
        return 'Error. The product output must be equal to actual production.'   
    if F > E:
        return 'Error. The actual good products cannot be greater than the product output.'

#result = oee('21/02/2023','MC01')