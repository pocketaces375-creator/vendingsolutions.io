"""Traffic pages for vendingsolutions.io: one page per city we serve, one per venue type, guides that answer what
venue owners search for, and a page for customers who scan the QR sticker on a machine.
Each page has its own real content (no copy-paste doorway pages), internal links, and schema.org data.
Edit the lists below and push; build.py renders them."""

CITIES = [
    {"name": "Fort Lauderdale", "county": "Broward",
     "intro": "From the bars on Las Olas Boulevard to Himmarshee Village and the beach strip along A1A, Fort Lauderdale nights run late. That's exactly when a customer runs out of vape and walks out to find a store.",
     "spots": "Las Olas Boulevard, Himmarshee Village, the A1A beachfront, Flagler Village"},
    {"name": "Miami", "county": "Miami-Dade",
     "intro": "Brickell lounges, Wynwood bars and Little Havana spots stay busy well past midnight. A smart machine on the wall keeps customers inside your venue instead of out looking for a corner store.",
     "spots": "Brickell, Wynwood, Downtown, Little Havana"},
    {"name": "Hollywood", "county": "Broward",
     "intro": "Between the Hollywood Broadwalk and the bars around Young Circle and Hollywood Boulevard, venues here serve locals and tourists every night of the week.",
     "spots": "the Broadwalk, Young Circle, Downtown Hollywood Boulevard"},
    {"name": "Pompano Beach", "county": "Broward",
     "intro": "Pompano's beachfront and Atlantic Boulevard bars are growing fast. Adding a free machine is an easy way to give regulars one more reason to stay.",
     "spots": "Atlantic Boulevard, the Pompano Beach pier area, Old Pompano"},
    {"name": "Boca Raton", "county": "Palm Beach",
     "intro": "Mizner Park and downtown Boca draw an upscale crowd that expects convenience. A clean, wall-mounted touchscreen machine fits right in.",
     "spots": "Mizner Park, Downtown Boca, Federal Highway"},
    {"name": "West Palm Beach", "county": "Palm Beach",
     "intro": "Clematis Street and the Rosemary Square area are West Palm's nightlife core. Venues there get busy crowds who don't want to leave mid-night.",
     "spots": "Clematis Street, Rosemary Square, Northwood Village"},
    {"name": "Wilton Manors", "county": "Broward",
     "intro": "Wilton Drive is one of South Florida's busiest bar strips. A machine that's always stocked and always supported is a small upgrade customers notice.",
     "spots": "Wilton Drive and the surrounding bars and lounges"},
    {"name": "Delray Beach", "county": "Palm Beach",
     "intro": "Atlantic Avenue in Delray is packed every weekend. Bars and lounges there can add a revenue stream without adding staff or inventory.",
     "spots": "Atlantic Avenue, Pineapple Grove, the beachfront"},
]

VENUES = [
    {"slug": "bars-and-pubs", "name": "Bars & pubs",
     "why": "Your regulars stay for another round instead of leaving to buy a vape. Bartenders never have to handle nicotine sales, ID checks or refunds.",
     "points": ["No inventory behind the bar", "Age verification built into the machine", "Customers get help 24/7 from our support line, not your staff"]},
    {"slug": "nightclubs-and-lounges", "name": "Nightclubs & lounges",
     "why": "Late-night crowds who leave to find a store often don't come back. A machine inside keeps them in the building, and the touchscreen can promote your events and bottle specials.",
     "points": ["Touchscreen ads for your events", "Card and phone payments, fast checkout", "Stock reported every minute, so it's full on your busiest night"]},
    {"slug": "hookah-and-cigar-lounges", "name": "Hookah & cigar lounges",
     "why": "Your customers already enjoy nicotine products. Offering vapes on the way out adds sales without taking up counter space or staff time.",
     "points": ["Wall-mounted, 30 × 30 inches", "We stock what your customers ask for", "Zero cost to you"]},
    {"slug": "hotels-and-resorts", "name": "Hotels & resorts",
     "why": "Guests who vape ask the front desk where to buy one. A discreet machine near the bar or lobby answers that question and earns you revenue.",
     "points": ["Discreet, modern design", "Age verification always on", "We handle permits, installation and service"]},
    {"slug": "bowling-and-entertainment-centers", "name": "Bowling & entertainment centers",
     "why": "Adults on a night out stay longer when they don't have to leave the building. Built-in age verification keeps sales 21+ even where families visit during the day.",
     "points": ["Built-in age verification", "Placed in adult areas like the bar", "Fully managed and serviced"]},
    {"slug": "event-and-concert-venues", "name": "Event & concert venues",
     "why": "Big crowds, long nights, and no way to leave and come back. A machine meets demand on site and adds a revenue line to every event.",
     "points": ["Handles rushes with quick card checkout", "Restocked before your big nights", "Revenue share with nothing to manage"]},
]

GUIDES = [
    {"slug": "are-vape-vending-machines-legal-in-florida", "title": "Are vape vending machines legal in Florida?",
     "desc": "What Florida bars and venues need to know about nicotine vending: the 21+ age limit, age verification, permits, and who handles them.",
     "body": """<p>Yes, nicotine vending is allowed in Florida when it's done the right way. The key rules every venue owner should know:</p>
<ul><li><b>21 and over only.</b> Selling nicotine products to anyone under 21 is against Florida law.</li>
<li><b>Age checks.</b> Our machines have built-in age verification, which stays on in any venue that doesn't check ID at the door.</li>
<li><b>Permits.</b> Selling nicotine products requires the right state permit (in Florida, through the Department of Business and Professional Regulation). We take care of permits for every machine we place, at no cost to the venue.</li>
<li><b>Placement.</b> Machines go in adult areas of your venue, such as the bar.</li></ul>
<p>Rules change, and local ordinances can add their own. We keep up with them so you don't have to. If you have a question about your location, <a href="/schedule-free-consult/">ask us during a free consultation</a>.</p>
<p class="muted">This page is general information, not legal advice.</p>"""},
    {"slug": "how-a-vape-vending-machine-makes-money-for-your-bar", "title": "How a vape vending machine makes money for your bar",
     "desc": "Where the revenue comes from, what affects it, and why there's no cost or risk for the venue.",
     "body": """<p>A smart vape vending machine earns your venue money in two ways: a share of every sale, and the customers it keeps inside instead of sending them out to a store.</p>
<h2>What affects how much it earns</h2>
<ul><li><b>Foot traffic and hours.</b> Late-night venues with steady crowds sell the most.</li>
<li><b>Placement.</b> Near the bar or the exit to the smoking area works best.</li>
<li><b>Selection.</b> We stock what your customers actually buy, and adjust using the machine's sales data.</li>
<li><b>Always stocked.</b> The machine reports stock every minute, so it's restocked before it runs out.</li></ul>
<h2>Why there's no risk</h2>
<p>You don't buy the machine, the stock or the permits, and you don't spend staff time on it. We install, stock and service it for free, and you get a share of the revenue. <a href="/services/">See how it works</a>.</p>"""},
    {"slug": "why-customers-stay-longer", "title": "Why customers stay longer when they don't have to leave for a vape",
     "desc": "The hidden cost of customers leaving mid-night, and how an on-site machine keeps them (and their tab) in your venue.",
     "body": """<p>About 1 in 7 adults vape. When one runs out mid-night, they leave to find a store, and many don't come back. That's a closed tab, an empty seat and a friend group that moves on.</p>
<p>A machine on your wall fixes that. Customers buy inside and use it outside or later, and they stay. Many of our partners don't allow vaping indoors at all. The machine still keeps people from leaving.</p>
<p>The touchscreen also works for you: it plays your own promos for events, specials and menu items between sales.</p>
<p><a href="/schedule-free-consult/">Get a free machine for your venue</a>.</p>"""},
    {"slug": "how-age-verification-works-in-vending-machines", "title": "How age verification works in our vending machines",
     "desc": "How smart vape vending machines keep sales 21+, and what that means for your venue.",
     "body": """<p>Every machine we place has built-in age verification. In venues that don't check ID at the door, it stays on for every sale, so only customers 21 and over can buy.</p>
<p>That means your staff never has to card someone at the machine, and you're never on the hook for an underage sale. We take this seriously: it's both the law and the right thing to do.</p>
<p>Have questions about how it works at your venue? <a href="/schedule-free-consult/">Talk to us</a>.</p>"""},
]
