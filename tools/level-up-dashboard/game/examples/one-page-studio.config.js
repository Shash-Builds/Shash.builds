// Example config: a one-page website studio (the setup shash.builds uses), with personal
// targets removed. Paste over the CONFIG block in level-up-game.html, then change the numbers.
const CONFIG = {
  title: "Level-Up",
  roleModel: "The Role Model",
  startDate: "",
  totalDays: 365,
  timezone: "America/New_York",
  currency: { symbol: "$", locale: "en-US" },
  money: { goal: 10000, byDay: 90, unitPrice: 400, unitName: "sites", mathTitle: "The $10k math",
           mathText: "$10k in 90 days is about 25 sites at $400 (or 18 sites plus 100 skill sales). That is about 2 clients a week, which takes about 50 DMs a day at a 1 to 2% close rate." },
  miniBoss: { title: "First $1,200", day: 14, target: 1200, product: "site", note: "Three one-page sites in two weeks." },
  contentLabel: "daily post",
  products: [["site", "One-page site", 400], ["care", "Care plan", 49], ["pro", "Skill Pro pack", 29], ["course", "Course", 0], ["other", "Other", 0]],
  channels: ["Cold email", "Instagram DM", "LinkedIn DM", "Upwork", "Contra", "Fiverr", "Skill marketplace", "Gumroad/Payhip", "YouTube", "Referral", "Other"],
  marketplaces: ["Upwork", "Contra", "Fiverr"],
  coldChannels: ["Cold email", "Instagram DM", "LinkedIn DM"],
  platforms: ["Instagram", "LinkedIn", "YouTube", "X", "Other"],
  followers: [["ig", "Instagram"], ["li", "LinkedIn"], ["yt", "YouTube"], ["x", "X"]],
  counters: [
    ["dms", "Cold DMs/emails", 1, 10], ["followups", "Follow-ups", 1], ["mkt", "Marketplace tries", 1],
    ["replies", "Replies (DM/email)", 1], ["mkt_replies", "Marketplace replies", 1], ["booked", "Calls booked", 1],
    ["held", "Calls held", 1], ["testimonials", "Video testimonials", 1], ["product_min", "Product work (min)", 15], ["hours", "Hours worked", 0.5]
  ],
  quests: [
    { k: "dms", label: "50 cold DMs/emails", target: 50, xp: "1 XP each" },
    { k: "followups", label: "10 follow-ups", target: 10, xp: "1 XP each" },
    { k: "mkt", label: "5 marketplace tries", target: 5, xp: "1 XP each" },
    { k: "posts", label: "1 content post", target: 1, xp: "10 XP" },
    { k: "product_min", label: "30 min product work", target: 30, xp: "5 XP" },
    { k: "logged", label: "Log numbers before bed", target: 1, xp: "5 XP" }
  ],
  xp: { perCounter: { dms: 1, followups: 1, mkt: 1, booked: 25, testimonials: 50 },
        thresholds: [{ key: "product_min", min: 30, xp: 5 }], post: 10, sale: 100, logged: 5, streakDays: 7, streakMult: 2 },
  funnel: [["Contacts", ["dms", "mkt"]], ["Replies", ["replies", "mkt_replies"]], ["Calls booked", ["booked"]], ["Calls held", ["held"]], ["Sales", "sales"]],
  levels: [
    { name: "Broke and Building", goal: "Site live, offer set, skill listing up", day: 7, needs: [{ metric: "flags", flags: [["site", "Site live"], ["offer", "Offer set"], ["listing", "Skill listing up"]] }] },
    { name: "Afloat", goal: "First sale of anything", day: 30, boss: true, needs: [{ metric: "sales", target: 1 }] },
    { name: "Proof", goal: "3 paying clients and 3 video testimonials", day: 50, needs: [{ metric: "productSales", product: "site", target: 3 }, { metric: "counter", key: "testimonials", target: 3 }] },
    { name: "Momentum", goal: "$3k earned in total", day: 65, needs: [{ metric: "total", target: 3000 }] },
    { name: "First 10K", goal: "$10k earned in total", day: 90, boss: true, needs: [{ metric: "total", target: 10000 }] },
    { name: "Machine", goal: "$10k in a single month", day: 180, needs: [{ metric: "bestMonth", target: 10000 }] },
    { name: "Recurring", goal: "30 care-plan clients in the last 31 days", day: 210, needs: [{ metric: "productSales", product: "care", target: 30, withinDays: 31 }] },
    { name: "Leverage", goal: "First helper doing outreach", day: 240, needs: [{ metric: "flags", flags: [["helper", "Helper doing outreach"]] }] },
    { name: "Audience", goal: "50k followers across platforms", day: 300, needs: [{ metric: "followers", target: 50000 }] },
    { name: "Scale", goal: "$50k in a single month", day: 330, needs: [{ metric: "bestMonth", target: 50000 }] },
    { name: "{roleModel}", goal: "$30k month and 100k followers", day: 365, boss: true, needs: [{ metric: "bestMonth", target: 30000 }, { metric: "followers", target: 100000 }] }
  ]
};
