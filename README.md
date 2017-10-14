# Objectives

- Can we predict if you'll get further rounds of financing based on size of your seed investor?

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


# Prediction: Can investors predict future funding rounds?

_Steps:_
- Company list with series A funding
- Target column with value 0 to X depending on how many future rounds
- Feature matrix all investors that invest past series A as columns. 1's or 0's. (angel, series-a, series-b, series-c+, 'private-equity', 'post-ipo')
- Holdout 30% of data
