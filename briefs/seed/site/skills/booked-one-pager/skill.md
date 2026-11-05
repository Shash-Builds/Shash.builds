---
name: booked-one-pager
description: Build a one-page website for a service business (coach, dentist, gym, salon, realtor, lawyer, contractor and so on) whose only job is to get the visitor to book a call or appointment. Use when someone asks for a landing page, a one-page site, a small business website, or a portfolio that should "get more bookings". Produces one self-contained HTML file that works on a phone, loads fast and has almost no text.
---

# Booked one-pager

A visitor gives a small business site about five seconds. In that time they need to know three things: what you do, that you're good, and how to book. Everything on the page serves one of those three. Everything else gets cut.

Made by Shashwat Jain (web designer). Free to use, change and share.

## 1. Ask five questions first

Don't start designing until you know:

1. What does the business do, in one sentence a customer would say?
2. Who is the customer, and what are they worried about before booking?
3. What is the one action? (Book a call, book an appointment, get a quote, claim a free class.)
4. Where does that action go? (Calendly link, booking tool, phone, WhatsApp, email.)
5. What proof exists? (Photos of the owner or the work, real reviews, numbers that are true.)

If the person can't answer 5, the page leans harder on photos and the owner's face.

## 2. The page, top to bottom

Six blocks. Most pages need all six and nothing more.

1. **Hero.** The owner's photo or the best photo of the work, a headline of six words or fewer that names the result, one button. Put three true facts beside it (price, speed, location or hours).
2. **A strip of who it's for.** The kinds of customers or services, as single words.
3. **Proof.** Pictures, not paragraphs: before and after, the work, the space, the team. Three to six images.
4. **How it works.** Three steps, three to five words each.
5. **Price or offer.** One number, big, with four short points under it.
6. **Contact.** A big "Let's talk." and the booking button, plus one or two backup ways to reach them.

## 3. Words

- Aim for under 80 words on the whole page, buttons included.
- The headline names what the customer gets ("Websites that get you booked", "Get stronger with coaches who know your name"), not what the business is.
- Buttons say exactly what happens: "Book a 15-min call", "Claim your free week".
- No dashes as punctuation, no "not X but Y", no stock phrases ("seamless", "elevate", "unlock", "in today's world"). Read it out loud. If it sounds like an ad, rewrite it like the owner talking.
- Only true numbers. If there are no reviews yet, leave reviews out.

## 4. Design

- One bold idea, everything around it quiet. Good bold ideas: a giant word behind the owner's photo, one strong brand colour on the whole hero, oversized numbers.
- Two fonts: a characterful display face for headlines, a plain one for everything else. Pick ones that fit the business (a law firm and a gym should not share a font).
- Three or four colours, all set as CSS variables at the top. Check text contrast.
- Big tap targets (44px or more). The booking button is visible without scrolling on a phone.
- Keep motion small: one entrance animation in the hero, gentle hover lifts. Respect reduced motion.

## 5. Build

- One HTML file. CSS and JS inline. Images compressed (WebP, under 150 KB each) and embedded or placed next to the file.
- Mobile first. Check at 390px and 1440px wide, and make sure nothing scrolls sideways.
- Wire the booking: a single constant at the top of the script holds the Calendly (or other) link, and every booking button uses it.
- Add a title, a meta description, Open Graph tags, and JSON-LD (`LocalBusiness` or `ProfessionalService`, with the offer and price) so search engines and AI assistants can describe the business correctly.

## 6. Before you hand it over

- Read every word once more. Can anything go?
- Tap every button on a phone. Does each one do what its label says?
- Is the owner's face or real work visible in the first screen?
- Does the page load in under two seconds on mobile data?

If all four are yes, ship it.
