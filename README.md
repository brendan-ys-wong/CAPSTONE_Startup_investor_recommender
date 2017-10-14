# Objectives

- Based on which investor invested in earlier financing rounds (e.g. angel, A), can we predict the probability of securing future financing?

- As an investor, what is the optimal network structure for investing in startups?
- For start-ups, did the investor's network significantly impact the liklihood of success?

# Exploratory Data Analysis

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
    - B: 
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

# Prediction: Can investors predict future funding rounds?

_Steps:_
- Company list with series A funding
- Target column with value 0 to X depending on how many future rounds
- Feature matrix all investors that invest past series A as columns. 1's or 0's. (angel, series-a, series-b, series-c+, 'private-equity', 'post-ipo')
- Holdout 30% of data
