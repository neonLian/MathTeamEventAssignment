#from typing import List
import numpy as np

def findBestAssignment(scores: np.array):

    n = len(scores) # number of people to choose from

    # determine what events each person is actually taking (currently only supports 3 events)
    events = np.ones([n,3], dtype=int)*-1
    for i in range(n):
        nextE = 0
        for j in range(6):
            if scores[i][j] > 0:
                events[i][nextE] = j    # events will be zero indexed
                nextE += 1
                if nextE > 3:
                    break

    # dp[n][10][6][6][6][6][6][6]
    dp = np.zeros([n,11,6,6,6,6,6,6]);

    bestScore = 0;
    maxE = [1,1,1,1,1,1]
    for i in range(n):
        print("Processing person " + str(i))
        for ss in range(2**3):
            # Determine which events are included in the current subset
            ev = [0]*6; # Length 6 array indicating 0 or 1 for each event
            curPoints = 0
            for e in range(3):
                if (ss & (1 << e)):
                    ev[events[i][e]] = 1
                    curPoints += scores[i][events[i][e]]
            # Base case
            if i == 0:
                dp[i][1][ev[0]][ev[1]][ev[2]][ev[3]][ev[4]][ev[5]] = curPoints
            # Main transition
            # Sorry to any programmers who are hurt in their soul from seeing 9 nested for loops
            else:
                # Efficiency note: limit ranges to maximum reached value

                for p in range(min(i, 10)):
                    for e1 in range(maxE[0]):
                        for e2 in range(maxE[1]):
                            for e3 in range(maxE[2]):
                                for e4 in range(maxE[3]):
                                    for e5 in range(maxE[4]):
                                        for e6 in range(maxE[5]):

                                            invalidEvents = False
                                            for e in [e1+ev[0],e2+ev[1],e3+ev[2],e4+ev[3],e5+ev[4],e6+ev[5]]:
                                                if e > 5:
                                                    invalidEvents = True
                                                    break;
                                            if invalidEvents:
                                                break;

                                            newPts = dp[i-1][p][e1][e2][e3][e4][e5][e6] + curPoints;

                                            dp[i][p+1][e1+ev[0]][e2+ev[1]][e3+ev[2]][e4+ev[3]][e5+ev[4]][e6+ev[5]] = \
                                                max(newPts,
                                                    dp[i-1][p+1][e1+ev[0]][e2+ev[1]][e3+ev[2]][e4+ev[3]][e5+ev[4]][e6+ev[5]],
                                                    dp[i-1][ p ][e1+ev[0]][e2+ev[1]][e3+ev[2]][e4+ev[3]][e5+ev[4]][e6+ev[5]]);
                                            if newPts > bestScore:
                                                bestScore = newPts;
                                                print(str(maxE) + " " + str(e6))
                                                print(f"{i}[{p}]{ev} --> {e1+ev[0]}/{e2+ev[1]}/{e3+ev[2]}/{e4+ev[3]}/{e5+ev[4]}/{e6+ev[5]} --> {newPts}");

            if ss == 0b111:
                for j in range(6):
                    maxE[j] = min(6, maxE[j]+ev[j])

    return {'best_score': bestScore, 'best_team': []}
