r = 0.0535  # Risk-free rate

WE = "251202" #WeeklyExpiry
WE2 = f"20{WE[:2]}-{WE[2:4]}-{WE[4:]}" # YYYY-MM-DD
WE3 = f"{WE[4:6]}-{WE[2:4]}-20{WE[0:2]}" # DD-MM-YYYY

SE = "251209" #SecondWeeklyExpiry
SE2 = f"20{SE[:2]}-{SE[2:4]}-{SE[4:]}" # YYYY-MM-DD
SE3 = f"{SE[4:6]}-{SE[2:4]}-20{SE[0:2]}" # DD-MM-YYYY

ME = "251230" #MonthlyExpiry
ME2 = f"20{ME[:2]}-{ME[2:4]}-{ME[4:]}" #2025-06-26 YYYY-MM-DD
ME3 = f"{ME[4:6]}-{ME[2:4]}-20{ME[0:2]}" #26-06-2025 DD-MM-YYYY

#Colour Codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

#Fyers Usage

FEW = "25D02" #Weekly
FEM = "25DEC" #Monthly