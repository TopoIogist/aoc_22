import sys
import os
import networkx as nx
import gurobipy as gp
from gurobipy import GRB

# This is a solution for Advent of Code 2022 day 16 (part 2)
# https://adventofcode.com/2022/day/16

# Gurobi 11.0:
# Total pressure released after 40 time steps with 2 players is 5866.
# real    0m26.583s
# user    1m18.212s
# sys     0m2.690s

# SCIP v8.0.4
# scip -f puzzle16_model_2p_40t.lp
# SCIP Status        : problem is solved [optimal solution found]
# Solving Time (sec) : 75.00
# Solving Nodes      : 1 (total of 3 nodes in 3 runs)
# Primal Bound       : +5.86600000000001e+03 (216 solutions)
# Dual Bound         : +5.86600000000001e+03
# Gap                : 0.00 %

time_steps = 40
players = 2

valves = [{'name': 'AA', 'flow': 0, 'nbs': ['HY', 'UX', 'VQ', 'LW', 'BK'], 'id': 0}, {'name': 'BM', 'flow': 24, 'nbs': ['GH', 'NK', 'YH', 'OH'], 'id': 1}, \
          {'name': 'BY', 'flow': 11, 'nbs': ['SP', 'HS', 'DN', 'KD', 'TK'], 'id': 2}, {'name': 'CJ', 'flow': 21, 'nbs': ['OF', 'YI', 'KD'], 'id': 3}, \
          {'name': 'CQ', 'flow': 18, 'nbs': ['GL', 'XM'], 'id': 4}, {'name': 'EI', 'flow': 17, 'nbs': ['ZX', 'AF'], 'id': 5}, \
          {'name': 'FE', 'flow': 4, 'nbs': ['RU', 'GR', 'YI', 'LG', 'ME'], 'id': 6}, {'name': 'HK', 'flow': 5, 'nbs': ['HT', 'QU', 'TW', 'WV', 'OK'], 'id': 7}, \
          {'name': 'KI', 'flow': 20, 'nbs': ['UW', 'KP'], 'id': 8}, {'name': 'NS', 'flow': 23, 'nbs': ['EU', 'DN'], 'id': 9}, \
          {'name': 'QE', 'flow': 3, 'nbs': ['OU', 'ME', 'UX', 'AX', 'TW'], 'id': 10}, {'name': 'QN', 'flow': 25, 'nbs': ['SD'], 'id': 11}, \
          {'name': 'SK', 'flow': 14, 'nbs': ['GH', 'GA', 'XM'], 'id': 12}, {'name': 'SZ', 'flow': 6, 'nbs': ['WV', 'GA', 'BK', 'KE', 'KN'], 'id': 13}, \
          {'name': 'TN', 'flow': 16, 'nbs': ['UW', 'CG', 'WB'], 'id': 14}, {'name': 'XH', 'flow': 22, 'nbs': ['YS', 'QU', 'UZ', 'DC'], 'id': 15}, \
          {'name': 'AF', 'flow': 0, 'nbs': ['GL', 'EI'], 'id': 16}, \
          {'name': 'AX', 'flow': 0, 'nbs': ['DC', 'QE'], 'id': 17}, {'name': 'BK', 'flow': 0, 'nbs': ['SZ', 'AA'], 'id': 18}, \
          {'name': 'CG', 'flow': 0, 'nbs': ['TN', 'SP'], 'id': 19}, {'name': 'DC', 'flow': 0, 'nbs': ['AX', 'XH'], 'id': 20}, \
          {'name': 'DN', 'flow': 0, 'nbs': ['NS', 'BY'], 'id': 21}, {'name': 'EU', 'flow': 0, 'nbs': ['NS', 'YS'], 'id': 22}, \
          {'name': 'GA', 'flow': 0, 'nbs': ['SK', 'SZ'], 'id': 23}, {'name': 'GH', 'flow': 0, 'nbs': ['BM', 'SK'], 'id': 24}, \
          {'name': 'GL', 'flow': 0, 'nbs': ['AF', 'CQ'], 'id': 25}, {'name': 'GR', 'flow': 0, 'nbs': ['FE', 'OK'], 'id': 26}, \
          {'name': 'HS', 'flow': 0, 'nbs': ['UZ', 'BY'], 'id': 27}, {'name': 'HT', 'flow': 0, 'nbs': ['LW', 'HK'], 'id': 28}, \
          {'name': 'HY', 'flow': 0, 'nbs': ['LG', 'AA'], 'id': 29}, {'name': 'KD', 'flow': 0, 'nbs': ['BY', 'CJ'], 'id': 30}, \
          {'name': 'KE', 'flow': 0, 'nbs': ['OH', 'SZ'], 'id': 31}, {'name': 'KN', 'flow': 0, 'nbs': ['SZ', 'OU'], 'id': 32}, \
          {'name': 'KP', 'flow': 0, 'nbs': ['KI', 'OF'], 'id': 33}, {'name': 'LG', 'flow': 0, 'nbs': ['FE', 'HY'], 'id': 34}, \
          {'name': 'LW', 'flow': 0, 'nbs': ['AA', 'HT'], 'id': 35}, {'name': 'ME', 'flow': 0, 'nbs': ['QE', 'FE'], 'id': 36}, \
          {'name': 'NK', 'flow': 0, 'nbs': ['SD', 'BM'], 'id': 37}, {'name': 'OF', 'flow': 0, 'nbs': ['CJ', 'KP'], 'id': 38}, \
          {'name': 'OH', 'flow': 0, 'nbs': ['BM', 'KE'], 'id': 39}, {'name': 'OK', 'flow': 0, 'nbs': ['HK', 'GR'], 'id': 40}, \
          {'name': 'OU', 'flow': 0, 'nbs': ['KN', 'QE'], 'id': 41}, {'name': 'QU', 'flow': 0, 'nbs': ['HK', 'XH'], 'id': 42}, \
          {'name': 'RU', 'flow': 0, 'nbs': ['TK', 'FE'], 'id': 43}, {'name': 'SD', 'flow': 0, 'nbs': ['NK', 'QN'], 'id': 44}, \
          {'name': 'SP', 'flow': 0, 'nbs': ['BY', 'CG'], 'id': 45}, {'name': 'TK', 'flow': 0, 'nbs': ['BY', 'RU'], 'id': 46}, \
          {'name': 'TW', 'flow': 0, 'nbs': ['HK', 'QE'], 'id': 47}, {'name': 'UW', 'flow': 0, 'nbs': ['KI', 'TN'], 'id': 48}, \
          {'name': 'UX', 'flow': 0, 'nbs': ['AA', 'QE'], 'id': 49}, {'name': 'UZ', 'flow': 0, 'nbs': ['XH', 'HS'], 'id': 50}, \
          {'name': 'VQ', 'flow': 0, 'nbs': ['AA', 'YH'], 'id': 51}, {'name': 'WB', 'flow': 0, 'nbs': ['TN', 'ZX'], 'id': 52}, \
          {'name': 'WV', 'flow': 0, 'nbs': ['SZ', 'HK'], 'id': 53}, {'name': 'XM', 'flow': 0, 'nbs': ['SK', 'CQ'], 'id': 54}, \
          {'name': 'YH', 'flow': 0, 'nbs': ['VQ', 'BM'], 'id': 55}, {'name': 'YI', 'flow': 0, 'nbs': ['FE', 'CJ'], 'id': 56}, \
          {'name': 'YS', 'flow': 0, 'nbs': ['XH', 'EU'], 'id': 57}, {'name': 'ZX', 'flow': 0, 'nbs': ['EI', 'WB'], 'id': 58}]


valve_name_to_id = {}
valuable_valves = []
id_counter = len(valves)
for valve in valves:
   valve_name_to_id[valve['name']] = valve['id']
   if valve['name'] == 'AA' or valve['flow'] != 0:
      valuable_valves.append(valve)

# Create graph from valve data.
G = nx.DiGraph()
for valve in valves:
   G.add_node(valve['name'])
   for neighbor in valve['nbs']:
      G.add_edge(valve['name'], neighbor)

# Calculate shortest paths lengths.
shortest_paths_length = {}
for v1 in valves:
   for v2 in valves:
      path = nx.shortest_path(G, source=v1['name'], target=v2['name'])
      shortest_paths_length[(v1['name'], v2['name'])] = len(path) - 1

# Optimization model
model = gp.Model("Valve Optimization")
# valve_variables[i, t, p] corresponds to valve i being opened by player p after t timesteps.
#valve_variables = model.addVars(len(valuable_valves), time_steps, players, vtype=GRB.BINARY, name="x")
valve_variables = model.addVars(len(valuable_valves), time_steps, players, vtype=GRB.BINARY)
# Assign names to the variables such that the model can be exported.
for i in range(len(valuable_valves)):
    for t in range(time_steps):
        for p in range(players):
            valve_variables[i, t, p].VarName = f"x_{i}_{t}_{p}"

# Players both start at valve AA.
for player in range(players):
    #model.addConstr(valve_variables[valve_name_to_id['AA'], 0, player] >= 1)
    model.addConstr(-valve_variables[valve_name_to_id['AA'], 0, player] <= -1)

# Two valves can only be opened by the same player after t timesteps if they are reachable from each other in t timesteps.
for player in range(players):
   for t in range(time_steps):
      for valve1 in valuable_valves:
         for valve2 in valuable_valves:
            for t2 in range(t, time_steps):
               if valve1['id'] == valve2['id']:
                  continue
               open_penalty = 1 if valve1['name'] != 'AA' else 0
               if t2 - open_penalty - t < shortest_paths_length[(valve1['name'], valve2['name'])]:
                  model.addConstr(valve_variables[valve1['id'], t, player] + valve_variables[valve2['id'], t2, player] <= 1)

# A valve should be opened by at most one player.
pressure_weights = {}
for valve in valuable_valves:
   for t in range(time_steps):
      pressure_weights[(valve['id'], t)] = max(0, (time_steps - t - 1)) * valve['flow']
      for t2 in range(t + 1, time_steps):
         for u1 in range(players):
            for u2 in range(players):
               model.addConstr(valve_variables[valve['id'], t, u1] + valve_variables[valve['id'], t2, u2] <= 1)
for u in range(players):
   for t in range(time_steps):
      model.addConstr(gp.quicksum(valve_variables[i,t,u] for i in range(1,len(valuable_valves))) <= 1)
      for i in range(1,len(valuable_valves)):
         model.addConstr(gp.quicksum(valve_variables[i, t, u] for u in range(players)) <= 1)

# Maximize pressure release.
objective = gp.quicksum(valve_variables[i, t, u] * pressure_weights[(i, t)] 
                        for i in range(len(valuable_valves)) for t in range(time_steps) for u in range(players))
model.setObjective(objective, GRB.MAXIMIZE)

# Optimize and print results.
model_name = f"puzzle16_model_{players}p_{time_steps}t.lp"
model.write(model_name)

model.optimize()
total_pressure = 0
for valve in valuable_valves:
   for t in range(time_steps):
      for u in range(players):
         if valve_variables[valve['id'], t, u].X > 0.1:
            total_pressure += max(0, (time_steps - t - 1)) * valve['flow']

print(f"Total pressure released after {time_steps} time steps with {players} players is {total_pressure}.")