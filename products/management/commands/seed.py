from django.core.management.base import BaseCommand
from django.utils.text import slugify

CATEGORIES = [
    ('Templates', '🎨'), ('UI Kits', '🧩'), ('eBooks', '📚'),
    ('Courses', '🎓'), ('Icons', '✨'), ('Code', '💻'),
    ('Graphics', '🖼️'), ('Fonts', '🔤'),
]

PRODUCTS = [
    dict(name='Minimal Portfolio Template', cat='Templates', price=29, old_price=49, emoji='🎨', badge='hot', tags='nextjs,portfolio', description='A clean Next.js 14 portfolio template.', includes=['Source code', 'Dark mode', 'Blog section']),
    dict(name='E-Commerce UI Kit', cat='UI Kits', price=49, old_price=79, emoji='🛍️', badge='new', tags='figma,ecommerce', description='200+ component Figma design system.', includes=['200+ components', 'Style guide']),
    dict(name='Freelancer Income Bible', cat='eBooks', price=14, old_price=None, emoji='📚', badge='', tags='freelance,income', description='Guide to pricing your freelance services.', includes=['147 page PDF', 'Rate calculator']),
    dict(name='SaaS Landing Page Kit', cat='Templates', price=39, old_price=65, emoji='🚀', badge='', tags='saas,landing', description='High-converting SaaS landing page template.', includes=['8 page layouts', 'HTML + CSS + JS']),
    dict(name='Icon Pack 3200 Icons', cat='Icons', price=19, old_price=35, emoji='✨', badge='hot', tags='icons,svg', description='3200 hand-crafted SVG icons.', includes=['3200 SVG icons', 'Figma file']),
    dict(name='Python Automation Course', cat='Courses', price=59, old_price=129, emoji='🐍', badge='bestseller', tags='python,automation', description='Master Python automation in 40 hours.', includes=['40 hours video', 'Source code']),
    dict(name='Notion Finance Tracker', cat='Templates', price=12, old_price=None, emoji='💰', badge='', tags='notion,finance', description='Personal finance system in Notion.', includes=['Notion template', 'Setup guide']),
    dict(name='Tailwind CSS Components', cat='Code', price=34, old_price=55, emoji='💻', badge='new', tags='tailwind,css', description='80+ production-ready Tailwind components.', includes=['80+ components', 'Dark mode']),
    dict(name='React Dashboard Template', cat='Templates', price=44, old_price=70, emoji='📊', badge='hot', tags='react,dashboard', description='Admin dashboard with React 18 + TypeScript.', includes=['React 18', '15 chart types']),
    dict(name='SEO Masterclass 2025', cat='Courses', price=49, old_price=99, emoji='🔍', badge='', tags='seo,marketing', description='Rank #1 on Google with proven SEO strategies.', includes=['25 hours video', 'Checklist']),
    dict(name='Brand Identity Kit', cat='Graphics', price=69, old_price=110, emoji='🎯', badge='', tags='branding,logo', description='Complete brand identity package.', includes=['50 logo templates', 'Brand guidelines']),
    dict(name='Framer Motion Animations', cat='Code', price=27, old_price=45, emoji='🎬', badge='new', tags='framer,animation', description='50+ Framer Motion animation presets.', includes=['50+ presets', 'TypeScript support']),
]


class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **options):
        from products.models import Category, Product, ProductInclude
        from users.models import User

        self.stdout.write('Seeding categories...')
        cat_map = {}
        for name, emoji in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'emoji': emoji, 'slug': slugify(name)})
            cat_map[name] = cat

        self.stdout.write('Creating seller...')
        seller, created = User.objects.get_or_create(
            email='seller@digitaldrop.com',
            defaults={'first_name': 'Demo', 'last_name': 'Seller', 'role': 'both'}
        )
        if created:
            seller.set_password('password123')
            seller.save()

        self.stdout.write('Creating admin...')
        admin_user, created = User.objects.get_or_create(
            email='admin@digitaldrop.com',
            defaults={'first_name': 'Admin', 'role': 'both', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        self.stdout.write('Seeding products...')
        for p_data in PRODUCTS:
            includes = p_data.pop('includes', [])
            cat_name = p_data.pop('cat')
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={**p_data, 'seller': seller, 'category': cat_map.get(cat_name)}
            )
            if created:
                for i, item in enumerate(includes):
                    ProductInclude.objects.create(product=product, item=item, order=i)
                self.stdout.write(f'  + {product.name}')

        self.stdout.write(self.style.SUCCESS('\nDone! seller@digitaldrop.com / password123'))