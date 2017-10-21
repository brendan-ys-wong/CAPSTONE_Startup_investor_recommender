# Summary
This repository is a current work-in-progress, please excuse the mess.

This project will build a recommender system to recommend to start-ups
which investors are likely to be interested in investing in their next
round of financing.


# Exploratory Data Analysis
Statistics from exploring the data set

_Funding types_
- venture: 24,264
    - A: 11,663
    - B: 7,197
    - C: 3,753
    - D: 1,685
    - E: 641
    - F: 228
    - G: ?
    - H: ?
- seed: 17,116
    - A: 85
    - B: 6
    - C: 3
- undisclosed: 3,810
- angel: 2,508
    - A: 13
    - B: 1
- debt_financing: 1,328
- private_equity: 1,260
- grant: 922
- convertible_note: 766
- equity_crowd_funding: 255
- non_equity_assistance: 122
- post_ipo_equity: 90
- secondary_market: 73
- post_ipo_debt: ?
- product_crowdfunding: ?

_Investors by seed count_
- At least 1: 30,189
- At least 2: 12,104
- At least 3: 7,954
- At least 4: 6,074
- At least 5: 5,306
- At least 6: 4,316
- At least 7: 3,797
- At least 8: 3,390
- At least 10: 2828
- At least 15: 1,968
- At least 20: 1,501
- At least 25: 1,208
- At least 50: 558
- At least 100: 209
- At least 150: 117
- At least 200: 75
- At least 250: 57
- At least 300: 44
- At least 350: 32
- At least 400: 22
- At least 500: 12
- At least 600: 11
- At least 700: 9
- At least 800: 6

_Unique funding rounds by year_
- 2015: 24,741
- 2014: 28,340
- 2013: 23,992
- 2012: 18,064
- 2011: 14,067
- 2010: 10,278
- 2009: 7,428
- 2008: 8,442
- 2007: 9,478
- 2006: 6,438
- 2005: 5,206
- 2004: 3,414
- 2003: 2,690
- 2002: 1,760
- 2001: 1,991
- 2000: 1,252
- 1999: 753

# Fundraising results

_Based on seed investor size_
Average rate of companies receiving multiple rounds of financing based on seed investor size
- (0,10):     0.59 | 22,815
- (11,50):    0.65 | 20,268
- (51,200):   0.68 | 18,097
- (201,400):  0.73 | 7,364
- (401,700):  0.71 | 3,547
- (700,1050): 0.55 | 4,928


# Potential Risks
- Unbalanced classes (more multiple financing round companies than not approx 60/40)
- Data leakage due to time-series nature of dataset

# Current Findings


# Reading Notes:
_GRAPH THEORY TOPICS_
- Informal Networks
- Amplification / Feedback loops
- Middle-class networkers
- Adjacency-list {A: {B:2, D:5, E:5}}
- Snowball sampling
- Centrality
    - Degree Centrality: Celebrities
    - Closeness Centrality: Gossip Mongers
    - Betweenness Centrality: Boundary spanners
    - Eigenvector centrality: Gray cardinals
- Subcomponents: Most active network
- Ego Networks: Reach of information
    - Clustering coefficient: Mutual trust within ego network
- Forbidden triads: Arbitrage opportunities/structural holes
- Hierarchical Clustering   
    - graph distance
    - similarity
- Affiliation networks
