from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post
from django.core.files import File
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Populate blog with sample posts and images'

    def handle(self, *args, **options):
        # Create a default user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@cybershield.com', 'is_staff': True, 'is_superuser': True}
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            self.stdout.write('Admin user already exists')

        # Create sample posts
        posts_data = [
            {
                'title': 'Introduction to Cybersecurity',
                'content': 'Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These cyberattacks are usually aimed at accessing, changing, or destroying sensitive information, extorting money from users, or interrupting normal business processes.\n\nKey aspects of cybersecurity include:\n• Network security\n• Application security\n• Information security\n• Operational security\n• Disaster recovery and business continuity\n• User education\n\nIn today\'s interconnected world, cybersecurity has become more important than ever. Organizations and individuals must take proactive measures to protect their digital assets.',
                'image': 'images/shield.jpg'
            },
            {
                'title': 'Understanding Phishing Attacks',
                'content': 'Phishing is a cyber attack technique where attackers masquerade as trustworthy sources to obtain sensitive information from victims. It\'s one of the most common types of cyber attacks.\n\nPhishing attacks typically involve:\n• Deceptive emails that appear to come from legitimate sources\n• Fake websites designed to look like real ones\n• Urgent requests for personal or financial information\n• Malicious links that download malware\n\nTo protect yourself from phishing:\n1. Verify sender email addresses carefully\n2. Look for secure connections (HTTPS)\n3. Never click on suspicious links\n4. Use email authentication tools\n5. Keep software updated\n6. Enable two-factor authentication',
                'image': 'images/phishing.jpg'
            },
            {
                'title': 'Digital Forensics Investigation Process',
                'content': 'Digital forensics is the process of discovering and interpreting electronic data. The goal is to preserve, recover, and analyze digital evidence to support an investigation.\n\nThe digital forensics process typically includes:\n\n1. Identification - Recognizing potential digital evidence\n2. Collection - Properly acquiring data without alteration\n3. Preservation - Protecting evidence from modification\n4. Analysis - Examining data to find relevant information\n5. Documentation - Recording all findings and procedures\n6. Presentation - Presenting evidence in a legal manner\n\nDigital forensics is crucial in criminal investigations, corporate espionage cases, and incident response. Proper procedure is essential to ensure evidence admissibility in court.',
                'image': 'images/azamat-e-FP_N_InBPdg-unsplash.jpg'
            },
            {
                'title': 'Best Practices for Password Security',
                'content': 'Strong passwords are your first line of defense against unauthorized access. According to security experts, passwords should follow these best practices:\n\nPassword Requirements:\n• Minimum 12 characters long\n• Mix of uppercase and lowercase letters\n• Inclusion of numbers and special characters\n• Avoid common words or patterns\n• Unique for each account\n\nPassword Management:\n1. Use a password manager to store passwords securely\n2. Enable multi-factor authentication (MFA)\n3. Change passwords regularly\n4. Never share passwords\n5. Don\'t use personal information\n6. Avoid password reuse across sites\n\nRemember: A strong password policy can prevent 80% of security breaches according to recent studies.',
                'image': 'images/bermix-studio-bCrM2e1M0a4-unsplash.jpg'
            },
            {
                'title': 'Malware Types and Detection',
                'content': 'Malware is malicious software designed to harm or exploit your computer system. There are many types of malware, each with different behaviors and impacts.\n\nCommon Malware Types:\n• Viruses - Attach to legitimate programs\n• Worms - Self-propagating without user interaction\n• Trojans - Disguised as legitimate software\n• Ransomware - Encrypts files and demands payment\n• Spyware - Monitors user activity\n• Adware - Displays unwanted advertisements\n• Rootkits - Provides administrative access\n\nDetection Methods:\n1. Use reliable antivirus software\n2. Keep operating system updated\n3. Enable firewalls\n4. Use email filtering\n5. Regular security scans\n6. Monitor system performance\n\nIf malware is detected, disconnect from the internet immediately and run a full system scan.',
                'image': 'images/le-vu-vSlCNmZdjHQ-unsplash.jpg'
            },
        ]

        for post_data in posts_data:
            title = post_data['title']
            
            # Check if post already exists
            if Post.objects.filter(title=title).exists():
                self.stdout.write(f'Post "{title}" already exists')
                continue
            
            # Create the post
            post = Post(
                title=title,
                content=post_data['content'],
                author=user,
            )
            
            # Add image if it exists
            image_path = post_data.get('image')
            if image_path:
                full_path = Path('/workspaces/Python-Assignment') / image_path
                if full_path.exists():
                    with open(full_path, 'rb') as f:
                        post.image.save(
                            os.path.basename(image_path),
                            File(f),
                            save=False
                        )
                    post.save()
                    self.stdout.write(self.style.SUCCESS(f'Created post "{title}" with image'))
                else:
                    post.save()
                    self.stdout.write(self.style.WARNING(f'Created post "{title}" without image (image not found)'))
            else:
                post.save()
                self.stdout.write(self.style.SUCCESS(f'Created post "{title}"'))

        self.stdout.write(self.style.SUCCESS('Blog population complete!'))
