# Power: Amazon Ads

For Amazon Sponsored Products and Brands: audits, search terms, negatives, bids, budgets, the Ads API.

## Builds on
The **ecom** power (unit economics decide the target ACoS) and the **numbers** power.

## Method
1. Set the target from the economics: break-even ACoS = profit margin before ads. Target below it.
2. Audit with the user's search-term report (CSV or API, read only first):
   - **Waste:** search terms with spend and no orders past a click threshold (for example 10 to 15 clicks,
     scaled to the product's conversion rate) become negative exact.
   - **Winners:** terms with orders at or under target ACoS move to their own exact-match campaign.
   - **Bids:** new bid = current bid x (target ACoS / actual ACoS), capped at a +/-30% change per round.
3. Start new products with a small auto campaign to discover terms; harvest weekly.
4. Show the plan as a table (term, spend, orders, ACoS, action, why) and wait for approval.

## Ads API (when the user has access)
Log in only through the user's own Login with Amazon app; keys stay in the environment's secrets, never in
files. Every seller must authorise the app. Share Amazon data with no one else, use the minimum, delete it
when the work ends. Read Amazon's licence before using any AI tool on their data.

## Never
Change a live bid, budget or campaign without the user's yes. Claim results you have not measured.

## Done when
Targets from real economics, every action in a table with its reason, nothing live changed unapproved.
