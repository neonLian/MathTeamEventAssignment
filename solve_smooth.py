from typing import List
import numpy as np

def ss3_to_arr6(ss: int, events, i) -> List[int]:
    ev = [0]*6; # Length 6 array indicating 0 or 1 for each event
    for e in range(3):
        if (ss & (1 << e)):
            ev[events[i][e]] = 1
    return ev

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
    prev = np.zeros([n,11,6,6,6,6,6,6,2]) # added Y/N, event (3) ss

    bestScore = 0;
    bestScoreIndex = [0]*8;
    maxE = [1,1,1,1,1,1]
    for i in range(n):
        print("Processing person " + str(i))
        for ss in range(2**3):

            # Determine which events are included in the current subset
            ev = ss3_to_arr6(ss, events, i); # Length 6 array indicating 0 or 1 for each event
            curPoints = 0
            for e in range(6):
                if ev[e]:
                    curPoints += scores[i][e]

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

                                            baseEventIndex = (e1, e2, e3, e4, e5, e6);
                                            eventIndexWithAdded = (e1+ev[0],e2+ev[1],e3+ev[2],e4+ev[3],e5+ev[4],e6+ev[5]);

                                            # Check if this event subset would cause more than 5 ppl in an event
                                            invalidEvents = False
                                            for e in eventIndexWithAdded:
                                                if e > 5:
                                                    invalidEvents = True
                                                    break;
                                            if invalidEvents:
                                                break;

                                            newPts = dp[i-1][p][baseEventIndex] + curPoints;

                                            curDPStatePts = dp[i-1][p+1][eventIndexWithAdded];
                                            lastDPStatePts = dp[i-1][ p ][eventIndexWithAdded];

                                            bestDPStatePts = max(newPts, curDPStatePts, lastDPStatePts);
                                            dp[i][p+1][eventIndexWithAdded] = bestDPStatePts;

                                            # Traceback to identify which people were added and with what events
                                            """
                                            if bestDPStatePts == newPts:
                                                prev[i][p+1][eventIndexWithAdded] = [1, ss]
                                            elif bestDPStatePts == curDPStatePts:
                                                pass
                                            elif bestDPStatePts == lastDPStatePts:
                                                prev[i][p+1][eventIndexWithAdded] = [0, 0]
                                            """
                                            
                                            if newPts > bestScore:
                                                bestScore = newPts;
                                                print(f"{i}[{p}]{ev} --> {str.join('/', [str(x) for x in eventIndexWithAdded] )} --> {newPts}");

            if ss == 0b111:
                for j in range(6):
                    maxE[j] = min(6, maxE[j]+ev[j])

    return {'best_score': bestScore, 'best_team': []}
