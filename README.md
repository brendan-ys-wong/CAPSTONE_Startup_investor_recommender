# Summary
There are over 15K startup investors globally, the goal of this project is to use machine learning to provide better recommendations on which seed and venture capital investors are most likely to be interested in investing in a startup based on an item-item similarity model (based on an investors past investment data) and a user-user similarity model (based on company's industry and business type).

The recommendation system has been trained on over 139K past startup investment transactions from 1999-2015 from a dataset that was provided by Crunchbase under an educational license.
(The Crunchbase team was terrific, I'd suggest reaching out to them to request access to their dataset.)

This model was able to accurately predict investor-startup matches in cross-validated data at 12.8% (recall) which was a 58% improvement compared to the 8.09% baseline which was calculated by recommending the largest N startup investors.
In addition to higher predictive accuracy, this models return more diverse investor recommendations other than the most well-known investors and therefore is likely to provide useful leads to startups during their fundraising process.


# Methodology
EDA: Plotted a network graph where investors and startups were individual nodes and investments were directional edges connecting the various nodes. I identified the most influential nodes based on a new centrality measure that combined eigenvector centrality (proxy for how influential a node is) and closeness centrality (proxy for the nodes access to information across the ecosystem). I found that this new centrality measure held a strong positive correlation to the percentage of an investors investments that ultimately received multiple rounds of financing. This finding led to the key insight that there is a signal in the investment data whereby investment decisions are at least partially driven by relationships between investors. This led to the approach of creating a recommendation system that could predict investors to startups.

Model: Combined two different models, a item similarity model base on the interaction data of investors investing in startup companies and a user similarity model which used natural language processing to vectorize company descriptions to identify similar companies. Recommendations were either made on the basis of who current seed or venture investors were and finding the N most similar investors, or finding investors that invested in similar companies based on the company descriptions.

Cross-validation: Utilized a modified k-fold cross-validation with 5 folds, where 20% of investors for all start-up companies were moved into a test set and model was evaluated based on the ability to accurately predict those held out matches.


# Results
Recall is identified as the most important metric when evaluating these models. Our goal is to help a startup find a potential investor so models that can find a positive match are prioritized, and since the opportunity cost of speaking to additional investors is relatively low, we are less concerned with precision scores.

The model's cross-validated results were averaged over 5-folds and our recall result was 12.8%. This result was a 58% improvement over the baseline recall of 8.1% which recommended based on the largest investors ranked by number of investments made.

The user-similarity model based on NLP wasn't scored given time constraints and also because the model's recall was expected to be low given the large number of possible investors and the limited signal available in recommending investors based solely on a company's description, especially for popular industry/technology application types. However, the model was still included as I believe there is tangible value in having the additional diverse recommendations that this model provides.

# Future Steps
Future steps include incorporating personnel data for each startup/investor team including where their partners/founders went to school and what was their previous work experience.
I believe this holds the potentially to significantly boost recall given that one of the most important features investors care about is the "quality" of the startup team.
