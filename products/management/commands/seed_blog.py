from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import BlogPost

User = get_user_model()

POSTS = [
    {
        "title": "How to Create a Professional Portfolio Website",
        "slug": "create-professional-portfolio-website",
        "category": "Tutorials",
        "emoji": "🖥️",
        "image_url": "https://picsum.photos/seed/portfolio-site/800/450",
        "excerpt": "A step-by-step guide to building a portfolio website that actually gets you hired.",
        "read_time": "7 min",
        "content": """
<p>Your portfolio website is often the first impression a potential client or employer has of your work. Getting it right can be the difference between landing a great project and getting overlooked. In this guide, we'll walk through everything you need to build a portfolio that stands out.</p>

<h2>1. Start With Your Best Work</h2>
<p>Resist the urge to show everything you've ever made. Choose 4-8 projects that best represent the kind of work you want to be hired for. Quality over quantity wins every time — a portfolio with three outstanding projects beats one with fifteen mediocre ones.</p>

<h2>2. Tell the Story Behind Each Project</h2>
<p>Don't just show a finished image. Walk visitors through your process: the problem you were solving, the constraints you faced, the decisions you made, and the results. This context turns a pretty picture into proof that you can think.</p>

<h2>3. Keep the Design Simple</h2>
<p>Your portfolio is there to showcase your work, not compete with it. Use plenty of white space, a clean type system, and let your projects breathe. A cluttered layout distracts from the very thing you're trying to highlight.</p>

<h2>4. Make Contact Effortless</h2>
<p>If someone is impressed by your work, don't make them hunt for a way to reach you. A clear "Get in Touch" button, visible email address, and links to your social profiles should be just a click away from every page.</p>

<h2>5. Optimize for Speed and Mobile</h2>
<p>Large unoptimized images are the most common reason portfolio sites feel slow. Compress your images, use modern formats like WebP, and always test how your site looks and performs on a phone — many visitors will view it there first.</p>

<blockquote>A portfolio isn't a gallery — it's a sales page for your skills.</blockquote>

<h2>Need a Head Start?</h2>
<p>If you'd rather not build from scratch, browse our marketplace for ready-made portfolio templates that you can customize with your own work in an afternoon.</p>
""",
    },
    {
        "title": "10 Best Portfolio Website Templates in 2026",
        "slug": "best-portfolio-templates-2026",
        "category": "Product Roundups",
        "emoji": "🏆",
        "image_url": "https://picsum.photos/seed/portfolio-templates/800/450",
        "excerpt": "We tested dozens of templates so you don't have to — here are this year's standouts.",
        "read_time": "6 min",
        "content": """
<p>Choosing the right portfolio template can save you weeks of design and development work. We reviewed dozens of templates available on DigitalDrop and picked out the ones that consistently impress both clients and recruiters.</p>

<h2>What We Looked For</h2>
<p>Every template on this list was evaluated for clean code, mobile responsiveness, ease of customization, and modern visual design. We also prioritized templates that load quickly and are easy to update without touching much code.</p>

<h2>Top Picks by Category</h2>
<p><strong>For Designers:</strong> Look for templates with large image grids, smooth hover transitions, and minimal text — your visuals should do the talking.</p>
<p><strong>For Developers:</strong> Templates with project case-study layouts, tech-stack tags, and GitHub/live-demo links work best.</p>
<p><strong>For Writers and Marketers:</strong> A clean blog-style layout with featured articles and a strong "About" section tends to perform well.</p>

<h2>Customization Tips</h2>
<p>Whatever template you choose, swap out the placeholder fonts and colors for ones that reflect your personal brand. Small changes — like a custom accent color or a unique header treatment — go a long way in making a template feel like "yours."</p>

<h2>Where to Find Them</h2>
<p>All of the templates referenced in this roundup are available in our Templates and Code categories. Filter by "Best Rated" to see what other buyers loved most.</p>
""",
    },
    {
        "title": "How to Start Selling Digital Products Online",
        "slug": "start-selling-digital-products-online",
        "category": "Industry Tips",
        "emoji": "💼",
        "image_url": "https://picsum.photos/seed/sell-digital-products/800/450",
        "excerpt": "Everything you need to know to turn your skills into a digital product business.",
        "read_time": "8 min",
        "content": """
<p>Selling digital products is one of the most accessible ways to build an online income. Unlike physical goods, there's no inventory, no shipping, and your products can be sold an unlimited number of times. Here's how to get started the right way.</p>

<h2>Step 1: Pick Something You Already Know How to Make</h2>
<p>Your first product doesn't need to be revolutionary — it just needs to solve a real problem for a specific group of people. Templates, presets, guides, and toolkits related to your existing skills are the easiest starting point.</p>

<h2>Step 2: Validate Before You Build</h2>
<p>Before spending weeks on a polished product, create a simple version and see if anyone is interested. Share it in communities related to your niche, or pre-sell it to a small group at a discount in exchange for feedback.</p>

<h2>Step 3: Package It Properly</h2>
<p>Buyers judge digital products by how they're presented. Clear previews, a well-written description, and a list of exactly what's included (file formats, license terms, support) all increase trust and conversions.</p>

<h2>Step 4: Choose the Right Marketplace</h2>
<p>Marketplaces like DigitalDrop handle payments, hosting, and discovery for you — letting you focus on creating. Listing your product here gives you instant access to buyers actively searching for what you make.</p>

<h2>Step 5: Promote Consistently</h2>
<p>Even great products need visibility. Share behind-the-scenes content, post updates when you improve your product, and ask happy customers for reviews — they're some of your best marketing.</p>

<h2>Step 6: Reinvest in Your Next Product</h2>
<p>Once your first product gains traction, use what you learned — about your audience, pricing, and what sells — to create your next one. Many successful sellers build small families of related products that customers buy together.</p>

<blockquote>The best time to start is before you feel ready.</blockquote>
""",
    },
    {
        "title": "New Features Added to DigitalDrop",
        "slug": "new-features-added-to-digitaldrop",
        "category": "Marketplace News",
        "emoji": "🚀",
        "image_url": "https://picsum.photos/seed/digitaldrop-news/800/450",
        "excerpt": "Here's what's new on the platform this month, including a smoother checkout experience.",
        "read_time": "3 min",
        "content": """
<p>We've been hard at work improving DigitalDrop based on feedback from both buyers and sellers. Here's a roundup of what's new.</p>

<h2>Faster, Secure Checkout</h2>
<p>Checkout now processes payments more smoothly with improved card validation and clearer error messages, so fewer purchases get interrupted.</p>

<h2>Improved Seller Dashboard</h2>
<p>Sellers can now see a clearer breakdown of revenue, recent orders, and product performance — all from a single overview page.</p>

<h2>Wishlist Improvements</h2>
<p>Saving products for later is now faster and syncs instantly across your account, so your wishlist is always up to date no matter where you browse from.</p>

<h2>What's Coming Next</h2>
<p>We're working on more discovery features to help great products get discovered faster, plus deeper analytics for sellers. Stay tuned!</p>
""",
    },
    {
        "title": "Free Event Planner Template",
        "slug": "free-event-planner-template",
        "category": "Free Resources",
        "emoji": "🎁",
        "image_url": "https://picsum.photos/seed/event-planner-template/800/450",
        "excerpt": "Download our free event planning template to keep every detail of your next event on track.",
        "read_time": "2 min",
        "content": """
<p>Planning an event — whether it's a wedding, conference, or birthday party — comes with a hundred small details that are easy to lose track of. That's why we put together a free event planner template to help.</p>

<h2>What's Inside</h2>
<p>The template includes a guest list tracker, a budget breakdown, a vendor contact sheet, and a day-of timeline so nothing falls through the cracks.</p>

<h2>Who It's For</h2>
<p>Whether you're planning your own event or managing them for clients, this template gives you a simple, organized starting point you can customize to fit any occasion.</p>

<h2>Want More?</h2>
<p>If you love this free template, check out our premium Eventify planning tools in the marketplace — they include digital RSVP tracking, budget visualizations, and vendor management features.</p>
""",
    },
    {
        "title": "How to Build a Mobile App with Ionic",
        "slug": "build-mobile-app-with-ionic",
        "category": "Tutorials",
        "emoji": "📱",
        "image_url": "https://picsum.photos/seed/ionic-mobile-app/800/450",
        "excerpt": "A beginner-friendly walkthrough of building your first cross-platform app with Ionic and Angular.",
        "read_time": "9 min",
        "content": """
<p>Ionic makes it possible to build apps for iOS, Android, and the web from a single codebase using familiar web technologies. Here's how to get started.</p>

<h2>1. Set Up Your Environment</h2>
<p>Install Node.js, then install the Ionic CLI globally. From there, you can generate a new project with a single command and choose from starter templates for tabs, sidebar menus, or blank layouts.</p>

<h2>2. Understand the Project Structure</h2>
<p>An Ionic + Angular project is organized into pages, components, and services. Pages represent full screens, components are reusable UI pieces, and services handle data and API calls.</p>

<h2>3. Build Your First Page</h2>
<p>Start simple — a home page with a list of items is a great way to learn how Ionic's UI components work, including cards, lists, and buttons that automatically adapt to each platform's design language.</p>

<h2>4. Connect to a Backend</h2>
<p>Most real apps need data from a server. Using Angular's HTTP client, you can fetch data from a REST API and display it in your pages, handling loading and error states gracefully.</p>

<h2>5. Test on Real Devices</h2>
<p>While the browser is great for development, always test on real iOS and Android devices before launch — touch interactions, keyboard behavior, and performance can differ significantly.</p>

<h2>6. Prepare for the App Stores</h2>
<p>Once your app is ready, Ionic's tooling helps you build native binaries for the App Store and Google Play, including handling icons, splash screens, and permissions.</p>

<blockquote>Ship a small version first — you can always add features after real users start using it.</blockquote>
""",
    },
    {
        "title": "Common Mistakes New Designers Make",
        "slug": "common-mistakes-new-designers-make",
        "category": "Industry Tips",
        "emoji": "⚠️",
        "image_url": "https://picsum.photos/seed/designer-mistakes/800/450",
        "excerpt": "Avoid these common pitfalls and level up your design work faster.",
        "read_time": "5 min",
        "content": """
<p>Every designer makes mistakes when starting out — but recognizing them early can save you years of frustration. Here are some of the most common ones.</p>

<h2>Using Too Many Fonts</h2>
<p>Sticking to one or two type families with a clear hierarchy almost always looks more professional than mixing several different styles.</p>

<h2>Ignoring Spacing and Alignment</h2>
<p>Consistent spacing and alignment is one of the fastest ways to make a design look polished — and one of the easiest things to overlook.</p>

<h2>Designing Without Real Content</h2>
<p>Lorem ipsum text can hide layout problems that only appear once real content — with varying lengths — is added. Whenever possible, design with real or realistic content from the start.</p>

<h2>Skipping Feedback</h2>
<p>It's tempting to perfect a design alone before showing anyone, but early feedback — even on rough drafts — helps catch issues before you've invested too much time in the wrong direction.</p>

<h2>Not Designing for Mobile First</h2>
<p>Designing for large screens first often leads to cramped, awkward mobile layouts. Starting with mobile constraints forces simpler, more focused designs that scale up gracefully.</p>

<blockquote>Good design is rarely about adding more — it's about removing what doesn't serve the user.</blockquote>
""",
    },
    {
        "title": "Top Selling Products This Month",
        "slug": "top-selling-products-this-month",
        "category": "Marketplace News",
        "emoji": "📈",
        "image_url": "https://picsum.photos/seed/top-selling-products/800/450",
        "excerpt": "See which products buyers couldn't stop downloading this month.",
        "read_time": "3 min",
        "content": """
<p>Every month, certain products rise to the top of our charts. Here's a look at the categories and trends driving sales right now.</p>

<h2>Code & Automation Tools Are Booming</h2>
<p>With more creators automating repetitive tasks, ready-made scripts, animation presets, and integration templates have seen strong growth.</p>

<h2>Courses Continue to Perform Well</h2>
<p>Buyers are increasingly looking for structured, practical courses they can complete in a weekend — short, focused content is outperforming longer bundles.</p>

<h2>UI Kits Remain a Staple</h2>
<p>Design teams continue to rely on high-quality UI kits to speed up their workflow, especially kits that include both light and dark mode variants.</p>

<h2>What This Means for Sellers</h2>
<p>If you're creating new products, consider focused, practical tools that solve one problem really well — that's exactly what's resonating with buyers this month.</p>
""",
    },
]


class Command(BaseCommand):
    help = "Seed blog posts with detailed content and images"

    def handle(self, *args, **options):
        author = User.objects.filter(is_staff=True).first() or User.objects.first()
        created = 0
        updated = 0
        for post in POSTS:
            obj, was_created = BlogPost.objects.update_or_create(
                slug=post["slug"],
                defaults={
                    "title": post["title"],
                    "category": post["category"],
                    "emoji": post["emoji"],
                    "image_url": post["image_url"],
                    "excerpt": post["excerpt"],
                    "content": post["content"],
                    "author": author,
                    "read_time": post["read_time"],
                    "is_published": True,
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Done! {created} created, {updated} updated."))