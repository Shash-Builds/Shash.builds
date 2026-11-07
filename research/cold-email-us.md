# Cold email to small service businesses: compliance and deliverability notes

Research date: 2026-11-03. Facts are checked against official sources unless marked "unverified" or "folklore." Links are in section 8.

## 1. Checklist

Run this before sending any cold email.

- [ ] The From name and address identify you or your business truthfully.
- [ ] The From domain is one you control and can authenticate (SPF or DKIM, see section 5).
- [ ] The subject line describes what the email actually says. No fake "Re:" or "Fwd:".
- [ ] The email says it is a business offer or advertisement in a plain, easy-to-see line.
- [ ] A valid physical postal address is in the footer. A registered mailbox or PO box is fine.
- [ ] Each email has a clear way to opt out, with a working reply address.
- [ ] You have a process to remove a person from the list the same day. The legal limit is 10 business days.
- [ ] The opt-out option works for at least 30 days after you send.
- [ ] The body is plain text, with at most one link, and no URL shortener.
- [ ] No attachments.
- [ ] The recipient is a real business you checked (a named owner or a business email you found on their site), not a scraped or bought list.
- [ ] The email is personalized with something specific to that business.
- [ ] Today's count is under your planned daily cap (section 6), and the account shows no bounce or spam-warning notices.
- [ ] Your sending log is up to date, so you can show what you sent and when.
- [ ] You have read Google's Acceptable Use Policy (section 3) and accept the risk of a suspension.

## 2. CAN-SPAM in plain words

Source: FTC, "CAN-SPAM Act: A Compliance Guide for Business" (checked 2026-11-03).

**Does it apply to B2B?** Yes. The FTC guide says: "The law makes no exception for business-to-business email." An email to a roofer's business inbox counts.

**What it requires:**

1. **Accurate headers.** From, To, Reply-To, and routing information must be truthful. They must identify the person or business that sent the message.
2. **No misleading subject lines.** The subject must match the content.
3. **Identify ads.** Commercial email must make clear it is an advertisement. The method is flexible, but the disclosure must be easy to notice.
4. **Valid physical postal address.** A current street address, a USPS PO box, or a private mailbox from a commercial mail receiving agency works.
5. **Clear opt-out.** Explain how to stop future marketing email. Give a return address or an easy web option. You may offer topic choices, but one option must stop all marketing from you.
6. **Honor opt-outs within 10 business days.** The opt-out must work for at least 30 days after the send.
7. **No fees or extra steps.** You cannot charge for opting out or ask for more than an email address. You cannot require steps beyond a reply email or one web page visit.
8. **No selling the address** after an opt-out, except to a company that helps you comply.
9. **Responsibility for anyone sending for you.** Hiring someone does not move the duty. The FTC says both the company whose product is promoted and the company that sends the message may be liable.

**Penalties.** The FTC guide says: "Each separate email in violation of the CAN-SPAM Act is subject to penalties of up to $53,088." The guide notes the figure was adjusted for inflation in January 2024. Each email counts separately, so ten bad emails can mean ten penalties. The FTC can also seek redress for consumers.

**Practical note.** CAN-SPAM does not ban cold email. It sets rules for the content and the opt-out. A small sender can follow it with a footer, a postal address, and a working unsubscribe reply.

## 3. Gmail and Google Workspace sending limits, and Gmail's sender rules

### Consumer Gmail (free @gmail.com)

Source: Google, "Gmail sending limits" (support.google.com/mail/answer/22839, checked 2026-11-03).

- More than 500 recipients in one email triggers the limit.
- More than 500 sent emails in one day triggers the limit.
- After you hit the limit, Google says you should be able to send again within 1 to 24 hours.
- The page gives no other numeric limits for free accounts.

### Google Workspace (paid, your own domain)

Source: Google Workspace Help, "Gmail sending limits in Google Workspace" (checked 2026-11-03; the page shows a last-updated date of 2026-10-26).

- Messages per day per user: 2,000 for standard accounts. Trial accounts: 500.
- Recipients per message: 2,000 across To, Cc, and Bcc, with a maximum of 500 external recipients per message.
- Messages sent through SMTP from POP or IMAP clients are capped at 100 recipients. Through the Gmail API, the cap is 500.
- Total recipients per day: 10,000. External recipients per day: 3,000.
- Unique recipients per day: 3,000 total, 2,000 external. The page lists both lines. For cold email, plan around the lower figure of 2,000 unique external recipients per day.
- Limits apply over a rolling 24-hour period. Google says the limits "can change without notice."

**Note for cold email.** At 50 a day you stay far under these caps. For a small sender, the caps are not the real risk. Reputation and policy are.

### Google's acceptable use rule (matters more than the cap)

Source: Google Workspace, Acceptable Use Policy (workspace.google.com/terms/use_policy/, last modified 2026-10-12, checked 2026-11-03).

- You must not use the services "to generate, distribute, publish or facilitate unsolicited mass email, promotions, advertisements, or other solicitations."
- Violation "may result in suspension or termination, or both, of the applicable Services."

**Read this carefully.** One-to-one cold emails to businesses sit in a grey area under this wording. Keep volume low, keep each email personal, and keep opt-outs working. Do not assume a Workspace account is safe from suspension. The consumer Gmail terms were not checked in this research (unverified).

### Gmail's sender rules (2024 onward)

Source: Google Support, "Email sender guidelines" (support.google.com/mail/answer/81126, checked 2026-11-03).

**Rules for all senders (any volume):**

- Set up SPF or DKIM for the sending domain. The page says "SPF or DKIM."
- Use valid reverse DNS (PTR) records for the sending domain or IP.
- Use TLS when transmitting email.
- Keep spam rates below 0.3% in Google Postmaster Tools. Google's stated target is below 0.10%. Avoid reaching 0.30% or higher.
- Format messages to RFC 5322. Each message needs a valid Message-ID. From, To, Subject, and Date appear only once. From has one address.
- Do not impersonate Gmail in the From header.
- Increase volume gradually. Avoid sudden spikes.
- On SMTP error 4.7.28 (quota exceeded), stop sending for at least 10 minutes, then resume with one connection.

**Extra rules for bulk senders (more than 5,000 messages a day to Gmail):**

Google says the extra section applies to senders who "send more than 5,000 messages per day to Gmail accounts." The requirements took effect February 1, 2024.

- SPF, DKIM, and DMARC are all required. DMARC can start at p=none.
- The From domain must align with the SPF or DKIM domain.
- Marketing and subscribed messages must support one-click unsubscribe. Send the header `List-Unsubscribe-Post: List-Unsubscribe=One-Click` and a `List-Unsubscribe` header with an HTTPS URL. Show a visible unsubscribe link in the body too.
- DKIM keys must be 1024 bits or longer. Google recommends 2048 bits if your provider supports it.

**Which rules apply to you:**

- A cold sender at 50 a day is under 5,000. The bulk section does not apply by Google's threshold.
- The all-sender rules still apply from the first email. Spam rate and authentication matter from day one.
- Good practice for a small sender: set up SPF, DKIM, and DMARC anyway, and add the one-click unsubscribe headers. These cost little and help trust. This is a judgment call, not a Google requirement below 5,000 a day.

## 4. Deliverability for a new Gmail or Workspace account

**Warm-up pace.**
- No official Google number for a safe starting volume was found. Unverified.
- Vendor blogs suggest starting at 5 to 10 emails a day, then climbing over 2 to 8 weeks. The vendors disagree. Treat these as folklore.
- Google's own rule is to avoid sudden spikes. A slow ramp follows that rule. The plan in section 6 is an example.

**Why plain text.**
- Plain text with no images, heavy HTML, or tracking pixels is common practice. Google's guidelines do not require it.
- Plain text looks like a personal note. Heavy HTML often looks like a marketing blast.
- Tracking pixels are not needed for cold email. Skip them.

**Links.**
- Use one link at most. Link to a real page on your own domain, such as a demo site.
- Do not use URL shorteners. Filters distrust them because spammers use them. This is folklore, not a Google rule.
- Google says links should be visible and clear, and HTML must not hide text.

**Attachments.**
- Send no attachments. Attachments, especially PDFs and zip files, look like spam in cold email. This is common practice (folklore). Link to the page instead.

**Spam-trigger words.**
- Lists of "spam words" (free, guarantee, urgent, and so on) are folklore.
- No official Google word list was found in the sources checked. Filters weigh sender reputation, authentication, complaints, and engagement far more than single words.
- Avoid all-caps, many exclamation marks, and fake "Re:" subjects. These affect trust, not word lists.

**Personalization.**
- Personalize each email with a real detail: the business name, the town, a specific page on their site, or a review they received. Mass templates with only a name swapped are more likely to be ignored or reported.
- Identical bodies sent in bulk are a common cause of complaints. Each email should read as if it were written for that one business.

**Reply rates.**
- No reliable public reply-rate figure was verified. Unverified.
- Do not plan around a number from a vendor blog. Track your own replies, bounces, and complaints from day one.

## 5. If you use a domain: SPF, DKIM, DMARC

Use your own domain, not a free mail domain. DMARC needs a domain you control. Google's setup pages are linked in section 8.

**Order matters.** Set up SPF and DKIM first. Google says to wait at least 48 hours before enabling DMARC. DNS changes can take up to 48 hours to take effect.

**SPF.**
- Purpose: says which servers may send for your domain.
- Record type: TXT, on the root of the domain (host "@").
- Value if Google Workspace is your only sender: `v=spf1 include:_spf.google.com ~all`
- Google recommends `~all` (soft fail). Use `-all` only if you are sure. A wrong `-all` can block legitimate mail.
- Each domain may have only one SPF record. Put every sender in that one record. An SPF record can have up to 10 include tags.
- Google says no Admin console step is needed for SPF.

**DKIM.**
- Purpose: signs each message so the receiver can check it was not changed.
- Generate the key in the Google Admin console (Apps > Google Workspace > Gmail > Authenticate email).
- Record name: `google._domainkey` (the default selector is "google").
- Record value form: `v=DKIM1; k=rsa; p=<public key from the Admin console>`
- Key length: 2048 bit if your DNS host supports it. Otherwise 1024 bit, the minimum Google lists for Gmail delivery.
- Click "Start authentication" in the Admin console after the record is live.

**DMARC.**
- Purpose: tells receivers what to do when SPF or DKIM fail, and sends you reports.
- Record name: `_dmarc.yourdomain.com` (TXT).
- Starting value from Google's example: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com; pct=100`
- Google's example also includes `adkim=s; aspf=s`. Google advises relaxed alignment, the default, unless you have a spoofing concern.
- Start at `p=none`. Read the reports for a few weeks. Move to `quarantine` or `reject` only after legitimate mail passes.
- Alignment: the From domain must match the domain that passed SPF or DKIM.
- Point `rua` at a dedicated inbox or group. Reports can be high volume.

**Separate sending domain.**
- Many cold senders use a separate domain for outreach, so a problem does not hit the main domain. This is common practice, not a Google rule (unverified as advice).
- That domain needs its own SPF, DKIM, and DMARC records, and its From address must match.

## 6. Safe ramp to 50 a day (example plan)

**This is a conservative example, not a rule from Google.** Google publishes no official ramp. Adjust it based on bounces, complaints, and whether mail lands in the inbox.

| Week | Emails per weekday | Weekday total | Notes |
|---|---|---|---|
| 1 | 5 to 10 | 25 to 50 | Send only to businesses you have checked. Answer any reply the same day. |
| 2 | 10 to 15 | 50 to 75 | Stop for the day if bounces pass about 2% (folklore threshold). |
| 3 | 15 to 25 | 75 to 125 | Check Postmaster Tools if you use a domain. |
| 4 | 25 to 35 | 125 to 175 | Keep the same body style. Vary the personal detail. |
| 5 | 35 to 50 | 175 to 250 | Stop at 50 sent per day, including replies and personal mail. |

Rules that go with the table:

- Count all outgoing mail, not only cold emails. The Gmail and Workspace caps count all sent mail.
- Send in short batches across the day, not one burst.
- If you see a spam warning, a bounce spike, or error 4.7.28, stop for at least 24 hours. Then restart one week back.
- Do not add a new list during a ramp week. Keep the same pace on the same list.
- The example skips weekends for the first month. This is an example choice, not a rule.

## 7. What gets accounts flagged or suspended

**Confirmed by Google sources:**

- **Spam rate at or above 0.3%.** Google says to stay below it in Postmaster Tools and to aim for below 0.10%.
- **Unsolicited mass email or solicitations.** The Workspace policy bars them. Violations may lead to suspension or termination.
- **Quota exceeded (SMTP 4.7.28).** Stop sending for at least 10 minutes.
- **Hitting the daily cap** (500 for consumer Gmail). Sending pauses for 1 to 24 hours.
- **Sudden spikes in volume.** Google says to avoid them.
- **Missing authentication, reverse DNS, or TLS.** Mail can fail or land in spam.

**Common practice, not confirmed by Google (folklore or vendor advice):**

- **High bounce rates.** Bounces from wrong addresses suggest you do not check your list. The 2% figure in section 6 is folklore, unverified.
- **Identical bodies.** The same text sent to many people looks like a blast.
- **Bought or scraped lists.** They hurt reputation and often break the rules above. Use only businesses you have checked.
- **Role addresses** (info@, contact@, sales@, admin@). These are often shared inboxes that can hold spam traps. Prefer a named owner when you can find one (folklore).
- **Spam traps and old addresses.** Effect and frequency unverified.
- **Link shorteners and attachments.** See section 4.
- **Sending to people who asked you to stop.** This breaks CAN-SPAM. Honor opt-outs at once.

## 8. Sources

All links checked 2026-11-03.

Official:

- FTC, "CAN-SPAM Act: A Compliance Guide for Business": https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business (checked 2026-11-03)
- Google Support, "Gmail sending limits" (consumer accounts): https://support.google.com/mail/answer/22839 (checked 2026-11-03)
- Google Workspace Help, "Gmail sending limits in Google Workspace": https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace (checked 2026-11-03)
- Google Support, "Email sender guidelines": https://support.google.com/mail/answer/81126 (checked 2026-11-03)
- Google Workspace, "Acceptable Use Policy": https://workspace.google.com/terms/use_policy/ (checked 2026-11-03)
- Google Workspace Help, "Set up SPF": https://knowledge.workspace.google.com/admin/security/set-up-spf (checked 2026-11-03)
- Google Workspace Help, "Set up DKIM": https://knowledge.workspace.google.com/admin/security/set-up-dkim (checked 2026-11-03)
- Google Workspace Help, "Set up DMARC": https://knowledge.workspace.google.com/admin/security/set-up-dmarc (checked 2026-11-03)

Secondary (vendor pages, used only to show that sources disagree on warm-up numbers; not verified):

- Qualtir, "Gmail daily sending limit": https://qualtir.com/blog/gmail-daily-sending-limit (checked 2026-11-03)
- MailReach, "Gmail sender guidelines (2026 guide)": https://www.mailreach.co/blog/gmail-sender-guidelines (checked 2026-11-03)

Marked "unverified" above because no official source was found: a safe starting volume set by Google, reply-rate figures, the 2% bounce threshold, the effect of spam-trigger words, spam-trap effects, and the consumer Gmail terms for cold email.
