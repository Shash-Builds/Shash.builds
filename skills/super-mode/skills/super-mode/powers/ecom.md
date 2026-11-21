# Power: Ecom

For marketplace and store work: listings, product images, fees, margins, pricing, returns, stock, launches.

## Builds on
**ecom** (`skills/ecom/skills/ecom/ecom.md`: `economics.py`, `ops.py`, `listing_check.py`, `image_check.py`),
**harsh-buyer-review**, the **visuals** and **video-studio** powers for images and product videos.

## Method
1. Load the store memory (products, costs, fees profile, prices). Ask only for what is missing.
2. Money questions always go through `economics.py`: profit per order after fees, returns and ads,
   break-even and target prices. Never estimate fees by hand; check the marketplace's current fee page.
3. Listings: title, bullets, images and A+ content checked against the marketplace's rules.
4. Anything live (price change, ad budget, publishing) waits for the user's yes.

## Done when
Every number from the script with its inputs shown, marketplace rules checked, live changes approved.
