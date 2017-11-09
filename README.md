# Summary
There are over 15K startup investors globally, the goal of this project is to use machine learning to provide better recommendations on which seed and venture capital investors are most likely to be interested in investing in a startup based on an item-item similarity model (based on an investors past investment data) and a user-user similarity model (based on company's industry and business type).

The recommendation system has been trained on over 139K past startup investment transactions from 1999-2015 from a dataset that was provided by Crunchbase under an educational license.
(The Crunchbase team was terrific, I'd suggest reaching out to them to request access to their dataset.)

This model was able to accurately predict investor-startup matches in cross-validated data at 12.8% (recall) which was a 58% improvement compared to the 8.09% baseline which was calculated by recommending the largest N startup investors.
In addition to higher predictive accuracy, this models return more diverse investor recommendations other than the most well-known investors and therefore is likely to provide useful leads to startups during their fundraising process.


# Methodology
The idea behind this model is that all seed and venture investors are connected either by direct co-investment in a startup or through additional degrees of investment separation.
One of the factors influencing this tightly-connected map is the 'follow-the-leader' investment strategy where investors will heavily weight co-investors when making their investment decision. Co-investors can be a component that de-risks a potential investment especially for smaller to medium sized investors that have less resources to dedicate to extensive due diligence. Therefore, this model looks at your current angel or seed investors and finds who are the most similar investors based on their past investing behavior and recommends the N most similar investors.

If your startup doesn't have any current investors, then the model will natural language processing techniques to take a description of your business, vectorize the key words based on the co-occurence rates of those words in a common web-crawled corpus, and be able to identify similar companies based on cosine differences between the average word vectors of your company descriptions and recommend investors that have also invested in that similar company. The idea behind this recommendation method is to recommend investors that focus on a similar industry or technology application.

# Results
Recall is identified as the most important metric when evaluating these models. Our goal is to help a startup find a potential investor so models that can find a positive match are prioritized, and since the opportunity cost of speaking to additional investors is relatively low, we are less concerned with precision scores.

This item-similarity model was evaluated using a modified k-fold cross-validation approach. For every startup company, we would randomly select 20% of their investors and remove them from the training data set. Our recall was then measured on our models ability to predict the held-out investors. Results were averaged over 5-folds and our recall result was 12.8%. This result was a 58% improvement over the baseline recall of 8.1% which recommended based on the largest investors ranked by number of investments made.

The user-similarity model based on NLP wasn't scored given time constraints and also because the model's recall was expected to be low given the large number of possible investors and the limited signal available in recommending investors based solely on a company's description, especially for popular industry/technology application types. However, the model was still included as I believe there is tangible value in having the additional diverse recommendations that this model provides.

# Future Steps
Future steps include incorporating personnel data for each startup/investor team including where their partners/founders went to school and what was their previous work experience.
I believe this holds the potentially to significantly boost recall given that one of the most important features investors care about is the "quality" of the startup team.
