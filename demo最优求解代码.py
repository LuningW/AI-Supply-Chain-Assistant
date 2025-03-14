from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Create LP problem
model = LpProblem("Market_Distribution_Optimization", LpMinimize)

# Decision variables
x = {var: LpVariable(var, lowBound=0) for var in [
    "x_p1_w1", "x_p1_w2", "x_p2_w1", "x_p2_w2",
    "x_w1_c1", "x_w1_c2", "x_w1_c3", "x_w1_c4",
    "x_w2_c1", "x_w2_c2", "x_w2_c3"
]}

y = {var: LpVariable(var, cat='Binary') for var in ["y1", "y2", "y3", "y4"]}

d = {
    "d1": 50000 - y["y1"] * 10000,
    "d2": 100000 - y["y2"] * 20000,
    "d3": 50000 - y["y3"] * 10000,
    "d4": 20000 - y["y4"] * 4000
}

# Objective function (minimize total cost)
model += lpSum([
    0*x["x_p1_w1"] + 5*x["x_p1_w2"] + 4*x["x_p2_w1"] + 2*x["x_p2_w2"],
    3*x["x_w1_c1"] + 4*x["x_w1_c2"] + 5*x["x_w1_c3"] + 4*x["x_w1_c4"],
    2*x["x_w2_c1"] + 1*x["x_w2_c2"] + 2*x["x_w2_c3"]
])

# Constraints
model += x["x_p2_w1"] + x["x_p2_w2"] <= 60000  # Factory capacity

model += x["x_p1_w1"] + x["x_p2_w1"] == lpSum([x["x_w1_c1"], x["x_w1_c2"], x["x_w1_c3"], x["x_w1_c4"]])
model += x["x_p1_w2"] + x["x_p2_w2"] == lpSum([x["x_w2_c1"], x["x_w2_c2"], x["x_w2_c3"]])

model += x["x_w1_c1"] + x["x_w2_c1"] == d["d1"]
model += x["x_w1_c2"] + x["x_w2_c2"] == d["d2"]
model += x["x_w1_c3"] + x["x_w2_c3"] == d["d3"]
model += x["x_w1_c4"] == d["d4"]

model += lpSum([y["y1"], y["y2"], y["y3"], y["y4"]]) == 1  # Only one market can be reduced

# Solve the problem
model.solve()

# Print results
print("Optimal Solution:")
for var in x:
    print(f"{var}: {x[var].varValue}")
for var in y:
    print(f"{var}: {y[var].varValue}")
