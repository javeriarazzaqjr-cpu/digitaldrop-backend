from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import BlogPost

User = get_user_model()

POSTS = [
    {
        "title": "5 Tips for Selling Digital Products Online",
        "slug": "5-tips-selling-digital-products",
        "category": "Selling Tips",
        "emoji": "💡",
        "excerpt": "Learn the proven strategies top sellers use to boost their digital product sales.",
        "content": "<p>Selling digital products is one of the best ways to earn passive income online. Here are five tips to help you succeed.</p><h2>1. Know Your Audience</h2><p>Understanding who you're selling to helps you create products that truly solve their problems.</p><h2>2. Price Strategically</h2><p>Research competitor pricing and offer fair value for your product quality.</p><h2>3. Create Eye-Catching Previews</h2><p>Buyers can't touch digital products, so visuals matter a lot.</p><h2>4. Collect Reviews Early</h2><p>Social proof builds trust and increases conversions.</p><h2>5. Keep Improving</h2><p>Update your products regularly based on customer feedback.</p>",
        "read_time": "4 min",
    },
    {
        "title": "How to Price Your UI Kit for Maximum Sales",
        "slug": "pricing-your-ui-kit",
        "category": "Design",
        "emoji": "🎨",
        "excerpt": "Pricing can make or break your UI kit sales. Here's how to find the sweet spot.",
        "content": "<p>Pricing a UI kit correctly is part art, part science. Too high and buyers hesitate; too low and you undervalue your work.</p><h2>Research the Market</h2><p>Browse similar kits to understand the going rate for your niche.</p><h2>Bundle Smartly</h2><p>Offering bundles increases perceived value and average order size.</p><blockquote>Great design sells itself — but the right price seals the deal.</blockquote>",
        "read_time": "3 min",
    },
    {
        "title": "The Rise of AI Tools in Digital Product Creation",
        "slug": "ai-tools-digital-product-creation",
        "category": "Trends",
        "emoji": "🤖",
        "excerpt": "AI is transforming how creators design, write, and package digital products.",
        "content": "<p>From AI-generated artwork to automated copywriting, creators now have powerful new tools at their fingertips.</p><h2>Faster Prototyping</h2><p>AI tools help creators go from idea to finished product in record time.</p><h2>Personalization at Scale</h2><p>AI enables sellers to offer customized variations of their products easily.</p>",
        "read_time": "5 min",
    },
    {
        "title": "Building Your First eBook: A Step-by-Step Guide",
        "slug": "building-your-first-ebook",
        "category": "Guides",
        "emoji": "📚",
        "excerpt": "Everything you need to know to write, design, and publish your first eBook.",
        "content": "<p>Writing an eBook can feel overwhelming, but breaking it into steps makes it manageable.</p><h2>1. Outline Your Content</h2><p>Start with a clear structure before writing.</p><h2>2. Write in Short Sessions</h2><p>Consistency beats marathon writing sessions.</p><h2>3. Design for Readability</h2><p>Use clear fonts, headings, and spacing.</p><h2>4. Export and Sell</h2><p>Convert to PDF and list it on your store.</p>",
        "read_time": "6 min",
    },
    {
        "title": "Why Lifetime Updates Build Customer Loyalty",
        "slug": "lifetime-updates-customer-loyalty",
        "category": "Selling Tips",
        "emoji": "🔄",
        "excerpt": "Offering lifetime updates can set your products apart from the competition.",
        "content": "<p>Customers love knowing a product will keep improving after purchase.</p><h2>Builds Trust</h2><p>Lifetime updates show commitment to quality.</p><h2>Reduces Refunds</h2><p>Buyers are less likely to request refunds if they know fixes are coming.</p>",
        "read_time": "3 min",
    },
    {
        "title": "Top 10 Code Snippets Every Developer Should Sell",
        "slug": "top-code-snippets-to-sell",
        "category": "Code",
        "emoji": "💻",
        "excerpt": "Turn your everyday code solutions into a steady income stream.",
        "content": "<p>Developers often write reusable code that others would happily pay for.</p><h2>Authentication Boilerplates</h2><p>Save buyers hours of setup time.</p><h2>Animation Presets</h2><p>Polished UI animations are always in demand.</p><h2>API Integration Templates</h2><p>Pre-built integrations for popular services sell well.</p>",
        "read_time": "4 min",
    },
]


class Command(BaseCommand):
    help = "Seed blog posts"

    def handle(self, *args, **options):
        author = User.objects.filter(is_staff=True).first() or User.objects.first()
        created = 0
        for post in POSTS:
            obj, was_created = BlogPost.objects.get_or_create(
                slug=post["slug"],
                defaults={
                    "title": post["title"],
                    "category": post["category"],
                    "emoji": post["emoji"],
                    "excerpt": post["excerpt"],
                    "content": post["content"],
                    "author": author,
                    "read_time": post["read_time"],
                    "is_published": True,
                }
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Done! {created} blog posts created."))