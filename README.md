# Summary
There are over 15K startup investors globally, the goal of this project was to use machine learning to provide better recommendations on which seed and venture capital investors are most likely to be interested in investing in a startup based on an item-item similarity model (item is the investor) and a user-user similarity model (user is the startup).

The recommendation system has been trained on over 139K past startup investment transactions from 1999-2015 from a dataset that was provided by Crunchbase under an educational license.
(The Crunchbase team was terrific, I'd suggest reaching out to them to request access to their dataset.)

This model was able to accurately predict investor-startup matches in cross-validated data at 12.8% (recall) compared to a 8.09% baseline which was recommending the largest N startup investors.
In addition to higher predictive accuracy, this models return more diverse investor recommendations other than the most well-known investors and therefore is likely to provide useful leads to startups during their fundraising process.


# Methodology
The idea behind this model is that all seed and venture investors are connected either by direct co-investment in a startup or through additional degrees of investment separation.
One of the factors influencing this tightly-connected map is the 'follow-the-leader' investment strategy where investors will heavily weight co-investors when making their investment decision. Co-investors can be a component that de-risks a potential investment especially for smaller to medium sized investors that have less resources to dedicate to extensive due diligence. Therefore, this model looks at your current angel or seed investors and finds who are the most similar investors based on their past investing behavior and recommends the N most similar investors.

If your startup doesn't have any current investors, then the model will natural language processing techniques to take a description of your business, vectorize the key words based on the co-occurence rates of those words in a common web-crawled corpus, and be able to identify similar companies based on cosine differences between the average word vectors of your company descriptions and recommend investors that have also invested in that similar company. The idea behind this recommendation method is to recommend investors that focus on a similar industry or technology application.

# Results
This model was evaluated 
