#!/usr/bin/env python3
"""
Content Processor for LinkedIn and Resume Analysis
Handles LinkedIn profile parsing, resume attribute extraction, and user content organization
"""

import os
import re
import uuid
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import PyPDF2
from dataclasses import asdict
import time
from dotenv import load_dotenv

# LinkedIn scraping imports
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from database_manager import (
    DatabaseManager, LinkedInAttribute, ResumeAttribute, 
    ConversationContext
)


class LinkedInProcessor:
    """Dynamic LinkedIn profile processor using real-time scraping"""
    
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
        # Load environment variables from .env file
        load_dotenv()
        self.linkedin_email = os.getenv('LINKEDIN_EMAIL')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD')
        
        if self.linkedin_email and self.linkedin_password:
            print("✅ LinkedIn credentials loaded from .env file")
        else:
            print("⚠️  No LinkedIn credentials found in .env file")
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome WebDriver with automatic driver management"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Automatically install and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Stealth settings to avoid detection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.implicitly_wait(10)
            
            print("✅ Chrome WebDriver setup successful")
            return driver
            
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            print("💡 Trying alternative configurations...")
            
            # Try fallback configuration
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.implicitly_wait(5)
                
                print("✅ Chrome WebDriver setup with fallback configuration")
                return driver
                
            except Exception as fallback_error:
                print(f"❌ Fallback driver setup also failed: {fallback_error}")
                raise Exception("Unable to setup Chrome WebDriver. Please check your Chrome installation.")
    
    def parse_linkedin_url(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Parse LinkedIn profile information using dynamic scraping
        """
        max_retries = 2
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"🔍 Scraping LinkedIn profile: {linkedin_url} (Attempt {retry_count + 1}/{max_retries})")
                
                # Ensure URL format is correct
                if not linkedin_url.startswith('http'):
                    linkedin_url = f"https://{linkedin_url}"
                
                # Setup driver
                self.driver = self._setup_driver()
                
                # Add delay to avoid rate limiting
                time.sleep(2)
                
                # Attempt to login if credentials are available
                if not self.is_logged_in and self.linkedin_email and self.linkedin_password:
                    self._attempt_login()
                
                # Scrape the profile with timeout
                try:
                    person = Person(linkedin_url, driver=self.driver, scrape=True, close_on_complete=False)
                    
                    # Validate that we got actual data
                    if not person or not hasattr(person, 'name') or not person.name:
                        if not self.is_logged_in:
                            print("⚠️  Profile scraping failed - LinkedIn authentication may be required")
                            print("💡 Add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to your .env file for better results")
                        raise ValueError("Failed to scrape profile data - profile may be private or requires authentication")
                    
                    # Extract basic profile information
                    linkedin_data = {
                        'profile_url': linkedin_url,
                        'headline': self._safe_extract(person.job_title, 'Professional'),
                        'summary': self._clean_text(self._safe_extract(person.about, 'Experienced professional')),
                        'location': self._safe_extract(person.location, 'Location not specified'),
                        'industry': self._extract_industry_from_headline(person.job_title) if person.job_title else 'Technology',
                        'connections_count': 'N/A',  # Not easily accessible
                        'posts_count': 'N/A',
                        'articles_count': 'N/A',
                        'endorsements': 'N/A',
                        'recommendations': 'N/A',
                        'activity_keywords': self._extract_activity_keywords(person)
                    }
                    
                    print(f"✅ Successfully scraped LinkedIn profile for: {person.name}")
                    return linkedin_data
                    
                except TimeoutException:
                    print(f"⏰ Timeout while scraping profile (attempt {retry_count + 1})")
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(5)  # Wait before retry
                        continue
                    
            except Exception as e:
                print(f"❌ Error scraping LinkedIn profile (attempt {retry_count + 1}): {e}")
                retry_count += 1
                
                if retry_count < max_retries:
                    print(f"🔄 Retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                
            finally:
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
        
        print("⚠️  All scraping attempts failed. Using fallback profile data.")
        return self._get_fallback_linkedin_data(linkedin_url)
    
    def _attempt_login(self):
        """Attempt to login to LinkedIn if credentials are provided"""
        try:
            print("🔐 Attempting LinkedIn authentication...")
            actions.login(self.driver, self.linkedin_email, self.linkedin_password)
            self.is_logged_in = True
            print("✅ LinkedIn authentication successful")
            time.sleep(3)  # Wait after login
        except Exception as e:
            print(f"❌ LinkedIn authentication failed: {e}")
            print("💡 Continuing without authentication - limited data may be available")
            self.is_logged_in = False
    
    def _safe_extract(self, value: Any, default: str) -> str:
        """Safely extract value with fallback"""
        try:
            return str(value) if value and str(value).strip() else default
        except:
            return default
    
    def _extract_industry_from_headline(self, headline: str) -> str:
        """Extract industry from job headline"""
        if not headline:
            return "Technology"
            
        headline_lower = headline.lower()
        
        # Industry keywords mapping
        industry_keywords = {
            'Technology': ['engineer', 'developer', 'software', 'ai', 'ml', 'data', 'tech', 'programming'],
            'Finance': ['finance', 'investment', 'trading', 'banking', 'capital', 'analyst'],
            'Healthcare': ['healthcare', 'medical', 'health', 'doctor', 'nurse', 'clinical'],
            'Education': ['education', 'teacher', 'professor', 'academic', 'research'],
            'Marketing': ['marketing', 'sales', 'advertising', 'brand', 'growth'],
            'Consulting': ['consultant', 'consulting', 'advisory', 'strategy'],
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in headline_lower for keyword in keywords):
                return industry
        
        return "Technology"  # Default
    
    def _extract_activity_keywords(self, person) -> str:
        """Extract activity keywords from profile content"""
        keywords = []
        
        # Extract from job title
        if person.job_title:
            keywords.extend(self._extract_tech_keywords(person.job_title))
        
        # Extract from about section
        if person.about:
            keywords.extend(self._extract_tech_keywords(person.about))
        
        # Extract from experiences
        for exp in person.experiences:
            if exp.description:
                keywords.extend(self._extract_tech_keywords(exp.description))
        
        # Remove duplicates and return top keywords
        unique_keywords = list(set(keywords))
        return ', '.join(unique_keywords[:10])
    
    def _extract_tech_keywords(self, text: str) -> List[str]:
        """Extract technical keywords from text"""
        if not text:
            return []
            
        tech_keywords = [
            'Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust', 'TypeScript',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
            'Machine Learning', 'AI', 'Data Science', 'Analytics',
            'SQL', 'NoSQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'API', 'REST', 'GraphQL', 'Microservices',
            'Leadership', 'Management', 'Strategy', 'Product'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in tech_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _clean_text(self, text: str) -> str:
        """Clean and truncate text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Truncate if too long
        if len(cleaned) > 500:
            cleaned = cleaned[:500] + "..."
        
        return cleaned
    
    def extract_work_experience_from_profile(self, linkedin_url: str) -> List[Dict[str, Any]]:
        """Extract work experience data from LinkedIn profile using dynamic scraping"""
        try:
            print(f"🔍 Extracting work experience from: {linkedin_url}")
            
            # Ensure URL format is correct
            if not linkedin_url.startswith('http'):
                linkedin_url = f"https://{linkedin_url}"
            
            # Setup driver
            self.driver = self._setup_driver()
            
            # Scrape the profile
            person = Person(linkedin_url, driver=self.driver, scrape=True, close_on_complete=False)
            
            work_experiences = []
            
            # Extract work experience from scraped data
            for exp in person.experiences:
                try:
                    # Parse dates
                    start_date, end_date = self._parse_experience_dates(exp.from_date, exp.to_date)
                    
                    work_experience = {
                        'title': self._clean_text(exp.position_title) if exp.position_title else 'Professional',
                        'company': self._clean_text(exp.institution_name) if exp.institution_name else 'Company',
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': self._clean_text(exp.description) if exp.description else 'Professional experience',
                        'location': self._clean_text(exp.location) if exp.location else 'Location not specified'
                    }
                    
                    work_experiences.append(work_experience)
                    
                except Exception as exp_error:
                    print(f"⚠️  Error processing experience: {exp_error}")
                    continue
            
            print(f"✅ Extracted {len(work_experiences)} work experiences")
            return work_experiences
            
        except Exception as e:
            print(f"❌ Error extracting work experience: {e}")
            if "not logged in" in str(e).lower() or "authentication" in str(e).lower():
                print("💡 Work experience extraction requires LinkedIn authentication")
                print("💡 Add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to your .env file")
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def extract_education_from_profile(self, linkedin_url: str) -> List[Dict[str, Any]]:
        """Extract education data from LinkedIn profile using dynamic scraping"""
        try:
            print(f"🔍 Extracting education from: {linkedin_url}")
            
            # Ensure URL format is correct
            if not linkedin_url.startswith('http'):
                linkedin_url = f"https://{linkedin_url}"
            
            # Setup driver
            self.driver = self._setup_driver()
            
            # Scrape the profile
            person = Person(linkedin_url, driver=self.driver, scrape=True, close_on_complete=False)
            
            education_records = []
            
            # Extract education from scraped data
            for edu in person.educations:
                try:
                    # Parse dates
                    start_year, graduation_year = self._parse_education_dates(edu.from_date, edu.to_date)
                    
                    # Extract degree and field information
                    degree_info = self._parse_degree_info(edu.degree)
                    
                    education_record = {
                        'degree': degree_info['degree'],
                        'field': degree_info['field'],
                        'institution': self._clean_text(edu.institution_name) if edu.institution_name else 'Institution',
                        'graduation_year': graduation_year,
                        'start_year': start_year,
                        'gpa': self._extract_gpa(edu.description) if edu.description else '',
                        'honors': self._extract_honors(edu.description) if edu.description else ''
                    }
                    
                    education_records.append(education_record)
                    
                except Exception as edu_error:
                    print(f"⚠️  Error processing education: {edu_error}")
                    continue
            
            print(f"✅ Extracted {len(education_records)} education records")
            return education_records
            
        except Exception as e:
            print(f"❌ Error extracting education: {e}")
            if "not logged in" in str(e).lower() or "authentication" in str(e).lower():
                print("💡 Education extraction requires LinkedIn authentication")
                print("💡 Add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to your .env file")
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def _parse_experience_dates(self, from_date: str, to_date: str) -> Tuple[str, Optional[str]]:
        """Parse experience dates from LinkedIn format"""
        try:
            start_date = self._parse_date_string(from_date) if from_date else 'Unknown'
            end_date = self._parse_date_string(to_date) if to_date and to_date.lower() != 'present' else None
            return start_date, end_date
        except:
            return 'Unknown', None
    
    def _parse_education_dates(self, from_date: str, to_date: str) -> Tuple[str, str]:
        """Parse education dates from LinkedIn format"""
        try:
            start_year = self._extract_year(from_date) if from_date else 'Unknown'
            graduation_year = self._extract_year(to_date) if to_date else 'Unknown'
            return start_year, graduation_year
        except:
            return 'Unknown', 'Unknown'
    
    def _parse_date_string(self, date_str: str) -> str:
        """Parse date string to standard format (YYYY-MM)"""
        if not date_str:
            return 'Unknown'
        
        # Try to extract year and month
        year_match = re.search(r'(\d{4})', date_str)
        if year_match:
            year = year_match.group(1)
            # Try to find month
            month_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', date_str, re.IGNORECASE)
            if month_match:
                month_map = {
                    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                }
                month = month_map.get(month_match.group(1).lower(), '01')
                return f"{year}-{month}"
            return year
        
        return date_str
    
    def _extract_year(self, date_str: str) -> str:
        """Extract year from date string"""
        if not date_str:
            return 'Unknown'
        
        year_match = re.search(r'(\d{4})', date_str)
        return year_match.group(1) if year_match else date_str
    
    def _parse_degree_info(self, degree_str: str) -> Dict[str, str]:
        """Parse degree string to extract degree and field"""
        if not degree_str:
            return {'degree': 'Degree', 'field': 'Field of Study'}
        
        # Common degree patterns
        degree_patterns = [
            r'(Bachelor.*?Engineering|Bachelor.*?Science|Bachelor.*?Arts|Bachelor.*?Business)',
            r'(Master.*?Science|Master.*?Engineering|Master.*?Business|Master.*?Arts)',
            r'(PhD|Doctor.*?Philosophy|Doctorate)',
            r'(Associate|Diploma|Certificate)'
        ]
        
        degree = degree_str
        field = 'General Studies'
        
        # Extract degree type
        for pattern in degree_patterns:
            match = re.search(pattern, degree_str, re.IGNORECASE)
            if match:
                degree = match.group(1)
                break
        
        # Extract field (usually after "in" or at the end)
        field_match = re.search(r'in\s+(.+)', degree_str, re.IGNORECASE)
        if field_match:
            field = field_match.group(1).strip()
        else:
            # Try to extract field from common patterns
            if 'computer' in degree_str.lower() or 'software' in degree_str.lower():
                field = 'Computer Science'
            elif 'engineering' in degree_str.lower():
                field = 'Engineering'
            elif 'business' in degree_str.lower():
                field = 'Business'
            elif 'data' in degree_str.lower():
                field = 'Data Science'
        
        return {'degree': degree, 'field': field}
    
    def _extract_gpa(self, description: str) -> str:
        """Extract GPA from education description"""
        if not description:
            return ''
        
        # Look for GPA patterns
        gpa_patterns = [
            r'GPA[:\s]*(\d+\.\d+)',
            r'(\d+\.\d+)[/\s]*GPA',
            r'Grade[:\s]*([A-F][+-]?)',
            r'(First Class|Second Class|Third Class|Honors?)',
            r'(Magna Cum Laude|Summa Cum Laude|Cum Laude)'
        ]
        
        for pattern in gpa_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ''
    
    def _extract_honors(self, description: str) -> str:
        """Extract honors/awards from education description"""
        if not description:
            return ''
        
        # Look for honor patterns
        honor_patterns = [
            r'(Dean\'s List)',
            r'(Honors?.*Program)',
            r'(Scholarship.*)',
            r'(Award.*)',
            r'(Magna Cum Laude|Summa Cum Laude|Cum Laude)',
            r'(First Class.*|Second Class.*|Third Class.*)'
        ]
        
        honors = []
        for pattern in honor_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            honors.extend(matches)
        
        return '; '.join(honors) if honors else ''
    
    def _get_fallback_linkedin_data(self, url: str) -> Dict[str, Any]:
        """Return fallback LinkedIn data when scraping fails"""
        # Try to extract some information from URL patterns
        name_from_url = self._extract_name_from_url(url)
        industry_hint = self._guess_industry_from_url(url)
        
        return {
            'profile_url': url,
            'headline': f'Professional{" at " + industry_hint if industry_hint != "Technology" else ""}',
            'summary': f'Experienced professional with expertise in {industry_hint.lower()} and business. Profile information limited due to privacy settings.',
            'location': 'Location not specified',
            'industry': industry_hint,
            'connections_count': 'N/A',
            'posts_count': 'N/A',
            'articles_count': 'N/A',
            'endorsements': 'N/A',
            'recommendations': 'N/A',
            'activity_keywords': f'{industry_hint.lower()}, professional development, networking'
        }
    
    def _extract_name_from_url(self, url: str) -> str:
        """Extract likely name from LinkedIn URL"""
        try:
            # Extract the profile identifier from URL
            match = re.search(r'linkedin\.com/in/([^/?]+)', url)
            if match:
                profile_id = match.group(1)
                # Convert dashes to spaces and title case
                name_parts = profile_id.split('-')
                # Remove numbers and common suffixes
                clean_parts = [part for part in name_parts if not part.isdigit() and len(part) > 1]
                if clean_parts:
                    return ' '.join(word.capitalize() for word in clean_parts[:2])  # First and last name
        except:
            pass
        return 'Professional'
    
    def _guess_industry_from_url(self, url: str) -> str:
        """Guess industry from URL patterns or common indicators"""
        url_lower = url.lower()
        
        # Common industry indicators in LinkedIn URLs
        if any(indicator in url_lower for indicator in ['engineer', 'tech', 'dev', 'software']):
            return 'Technology'
        elif any(indicator in url_lower for indicator in ['finance', 'banking', 'investment']):
            return 'Finance'
        elif any(indicator in url_lower for indicator in ['health', 'medical', 'doctor']):
            return 'Healthcare'
        elif any(indicator in url_lower for indicator in ['marketing', 'sales', 'growth']):
            return 'Marketing'
        elif any(indicator in url_lower for indicator in ['consultant', 'strategy']):
            return 'Consulting'
        else:
            return 'Technology'  # Default assumption


class ResumeProcessor:
    """Enhanced resume processor with detailed attribute extraction"""
    
    def __init__(self):
        pass
    
    def extract_resume_attributes(self, resume_file_path: str) -> Dict[str, Any]:
        """Extract detailed attributes from resume PDF"""
        try:
            # Extract text from PDF
            extracted_text = self._extract_text_from_pdf(resume_file_path)
            
            # Analyze and extract specific attributes
            attributes = {
                'resume_file_path': resume_file_path,
                'extracted_text': extracted_text,
                'key_achievements': self._extract_key_achievements(extracted_text),
                'technical_keywords': self._extract_technical_keywords(extracted_text),
                'soft_skills': self._extract_soft_skills(extracted_text),
                'certifications': self._extract_certifications(extracted_text),
                'languages': self._extract_languages(extracted_text),
                'publications': self._extract_publications(extracted_text),
                'awards': self._extract_awards(extracted_text),
                'volunteer_work': self._extract_volunteer_work(extracted_text),
                'personal_projects': self._extract_personal_projects(extracted_text)
            }
            
            return attributes
            
        except Exception as e:
            print(f"Error extracting resume attributes: {e}")
            return self._get_default_resume_attributes(resume_file_path)
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def _extract_key_achievements(self, text: str) -> str:
        """Extract key achievements from resume text"""
        achievements = []
        
        # Look for quantified achievements
        metrics_patterns = [
            r'(\d+%[^.]*)',  # Percentages
            r'(\$\d+[^.]*)',  # Dollar amounts
            r'(\d+(?:,\d{3})*(?:\+)?[^.]*(?:users?|customers?|clients?|engineers?|developers?))',  # User counts
            r'(\d+(?:,\d{3})*(?:\+)?[^.]*(?:increase|decrease|improvement|reduction|growth))',  # Improvements
        ]
        
        for pattern in metrics_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievements.extend(matches)
        
        # Look for action-oriented achievements
        action_patterns = [
            r'((?:Built|Developed|Created|Implemented|Led|Designed|Optimized)[^.]+)',
            r'((?:Increased|Decreased|Improved|Reduced|Enhanced)[^.]+)',
            r'((?:Launched|Delivered|Achieved|Won|Earned)[^.]+)'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievements.extend(matches[:3])  # Limit to avoid too much text
        
        return '; '.join(achievements[:10])  # Top 10 achievements
    
    def _extract_technical_keywords(self, text: str) -> str:
        """Extract technical keywords and technologies"""
        # Common technical keywords
        tech_keywords = [
            # Programming languages
            'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Rust', 'R', 'SQL',
            'HTML', 'CSS', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'MATLAB', 'VBA',
            
            # Frameworks and libraries
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Express', 'Spring',
            'TensorFlow', 'PyTorch', 'scikit-learn', 'Pandas', 'NumPy', 'OpenCV',
            
            # Technologies and tools
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitLab', 'GitHub',
            'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch', 'Kafka', 'RabbitMQ',
            'Terraform', 'Ansible', 'Prometheus', 'Grafana', 'Linux', 'Unix',
            
            # Concepts
            'Machine Learning', 'AI', 'Deep Learning', 'NLP', 'Computer Vision', 'Blockchain',
            'Microservices', 'API', 'REST', 'GraphQL', 'DevOps', 'CI/CD', 'Agile', 'Scrum'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in tech_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        return ', '.join(found_keywords)
    
    def _extract_soft_skills(self, text: str) -> str:
        """Extract soft skills from resume text"""
        soft_skills = [
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving', 'Critical Thinking',
            'Project Management', 'Time Management', 'Collaboration', 'Mentoring', 'Training',
            'Presentation', 'Negotiation', 'Strategic Planning', 'Decision Making', 'Adaptability',
            'Innovation', 'Creativity', 'Analytical', 'Detail-oriented', 'Self-motivated'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in soft_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return ', '.join(found_skills)
    
    def _extract_certifications(self, text: str) -> str:
        """Extract certifications and credentials"""
        cert_patterns = [
            r'(AWS[^.]*(?:Certified|Certification))',
            r'(Google[^.]*(?:Certified|Certification))',
            r'(Microsoft[^.]*(?:Certified|Certification))',
            r'(Oracle[^.]*(?:Certified|Certification))',
            r'(PMP|Scrum Master|CISSP|CISA|CISM)',
            r'((?:Certified|Certification)[^.]+)'
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend(matches)
        
        return '; '.join(certifications[:5])
    
    def _extract_languages(self, text: str) -> str:
        """Extract language skills"""
        languages = ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian',
                    'Chinese', 'Mandarin', 'Japanese', 'Korean', 'Arabic', 'Hindi', 'Dutch']
        
        found_languages = []
        text_lower = text.lower()
        
        for lang in languages:
            if lang.lower() in text_lower:
                found_languages.append(lang)
        
        return ', '.join(found_languages)
    
    def _extract_publications(self, text: str) -> str:
        """Extract publications and papers"""
        pub_patterns = [
            r'((?:Published|Publication|Paper|Article|Journal)[^.]+)',
            r'((?:IEEE|ACM|arXiv)[^.]+)',
            r'((?:Conference|Symposium|Workshop)[^.]+(?:presentation|paper))'
        ]
        
        publications = []
        for pattern in pub_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            publications.extend(matches)
        
        return '; '.join(publications[:3])
    
    def _extract_awards(self, text: str) -> str:
        """Extract awards and honors"""
        award_patterns = [
            r'((?:Award|Prize|Honor|Recognition|Achievement)[^.]+)',
            r'((?:Winner|First Place|Best|Top)[^.]+(?:award|prize|honor))',
            r'((?:Dean\'s List|Magna Cum Laude|Summa Cum Laude|Phi Beta Kappa))'
        ]
        
        awards = []
        for pattern in award_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            awards.extend(matches)
        
        return '; '.join(awards[:5])
    
    def _extract_volunteer_work(self, text: str) -> str:
        """Extract volunteer work and community involvement"""
        volunteer_patterns = [
            r'((?:Volunteer|Volunteering)[^.]+)',
            r'((?:Community|Non-profit|Charity)[^.]+)',
            r'((?:Mentor|Mentoring|Teaching|Tutoring)[^.]+)'
        ]
        
        volunteer = []
        for pattern in volunteer_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            volunteer.extend(matches)
        
        return '; '.join(volunteer[:3])
    
    def _extract_personal_projects(self, text: str) -> str:
        """Extract personal projects and side projects"""
        project_patterns = [
            r'((?:Personal Project|Side Project|Open Source)[^.]+)',
            r'((?:GitHub|Portfolio|Pet Social|Flashvault)[^.]+)',
            r'((?:Built|Created|Developed)[^.]*(?:project|application|website|app))'
        ]
        
        projects = []
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            projects.extend(matches)
        
        return '; '.join(projects[:5])
    
    def _get_default_resume_attributes(self, file_path: str) -> Dict[str, Any]:
        """Return default resume attributes structure"""
        return {
            'resume_file_path': file_path,
            'extracted_text': '',
            'key_achievements': '',
            'technical_keywords': '',
            'soft_skills': '',
            'certifications': '',
            'languages': '',
            'publications': '',
            'awards': '',
            'volunteer_work': '',
            'personal_projects': ''
        }


class FileOrganizer:
    """Manages user-specific file organization and storage"""
    
    def __init__(self, base_files_dir: str = "./files"):
        self.base_files_dir = Path(base_files_dir)
        self.base_files_dir.mkdir(exist_ok=True)
    
    def create_user_directory(self, user_id: str) -> Path:
        """Create user-specific directory structure"""
        user_dir = self.base_files_dir / user_id
        user_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (user_dir / "resumes").mkdir(exist_ok=True)
        (user_dir / "conversations").mkdir(exist_ok=True)
        (user_dir / "prompts").mkdir(exist_ok=True)
        
        return user_dir
    
    def get_user_resume_path(self, user_id: str) -> Optional[str]:
        """Find user's resume file in their directory"""
        user_dir = self.base_files_dir / user_id / "resumes"
        
        if not user_dir.exists():
            # Check old location for backward compatibility
            old_resume_path = self.base_files_dir / f"{user_id}_Resume_*.pdf"
            old_files = list(self.base_files_dir.glob(f"*{user_id}*.pdf"))
            if old_files:
                return str(old_files[0])
            return None
        
        # Look for PDF files in user's resume directory
        pdf_files = list(user_dir.glob("*.pdf"))
        if pdf_files:
            return str(pdf_files[0])  # Return first PDF found
        
        return None
    
    def copy_resume_to_user_dir(self, user_id: str, source_resume_path: str) -> str:
        """Copy resume to user's directory and return new path"""
        user_dir = self.create_user_directory(user_id)
        resume_dir = user_dir / "resumes"
        
        source_path = Path(source_resume_path)
        new_resume_path = resume_dir / source_path.name
        
        # Copy file if it doesn't exist
        if not new_resume_path.exists() and source_path.exists():
            import shutil
            shutil.copy2(source_path, new_resume_path)
        
        return str(new_resume_path)
    
    def create_conversation_prompt_prefix(self, user_id: str, conversation_id: str, 
                                        content: str) -> str:
        """Create conversation-specific prompt prefix file"""
        user_dir = self.create_user_directory(user_id)
        prompts_dir = user_dir / "prompts"
        
        prompt_filename = f"prompt_prefix_{conversation_id}.txt"
        prompt_path = prompts_dir / prompt_filename
        
        # Write prompt prefix content
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(prompt_path)


class PromptPrefixGenerator:
    """Generates dynamic prompt prefixes based on user data"""
    
    def __init__(self):
        pass
    
    def generate_comprehensive_prompt_prefix(self, user_profile: Dict[str, Any],
                                           linkedin_data: Optional[Dict[str, Any]],
                                           resume_data: Optional[Dict[str, Any]]) -> str:
        """Generate comprehensive prompt prefix with LinkedIn and resume context"""
        
        # Get user basic info
        user_info = user_profile.get("user", {})
        name = user_info.get("name", "Professional")
        
        # Base prompt prefix
        base_prefix = f"""You are {name}, acting as a digital twin based on your comprehensive professional background and career journey. You have a networking-oriented personality and are genuinely interested in learning about the person you're talking to.

Your role is to engage in meaningful professional conversations, share insights from your experience, and build authentic connections. You should:

1. Draw from your real professional experiences and educational background
2. Show genuine curiosity about others' career paths and interests  
3. Share relevant insights and advice when appropriate
4. Ask thoughtful follow-up questions to understand the other person better
5. Maintain a warm, professional, and approachable tone
6. Focus on building mutually beneficial professional relationships

Your responses should feel natural and authentic, as if you're having a real conversation with a fellow professional at a networking event or coffee meeting."""
        
        # Add LinkedIn context if available
        linkedin_context = ""
        if linkedin_data:
            linkedin_context = f"""

LINKEDIN PROFILE INSIGHTS:
- Professional Headline: {linkedin_data.get('headline', 'N/A')}
- Industry Focus: {linkedin_data.get('industry', 'N/A')}
- Professional Summary: {linkedin_data.get('summary', 'N/A')}
- Key Activity Areas: {linkedin_data.get('activity_keywords', 'N/A')}
- Location: {linkedin_data.get('location', 'N/A')}"""
        
        # Add resume context if available
        resume_context = ""
        if resume_data:
            resume_context = f"""

RESUME HIGHLIGHTS:
- Key Achievements: {resume_data.get('key_achievements', 'N/A')[:500]}...
- Technical Expertise: {resume_data.get('technical_keywords', 'N/A')}
- Core Competencies: {resume_data.get('soft_skills', 'N/A')}
- Certifications: {resume_data.get('certifications', 'N/A')}
- Languages: {resume_data.get('languages', 'N/A')}
- Awards & Recognition: {resume_data.get('awards', 'N/A')}
- Personal Projects: {resume_data.get('personal_projects', 'N/A')}
- Community Involvement: {resume_data.get('volunteer_work', 'N/A')}"""
        
        # Combine all sections
        comprehensive_prefix = base_prefix + linkedin_context + resume_context
        
        return comprehensive_prefix
    
    def create_conversation_summary(self, linkedin_data: Optional[Dict[str, Any]],
                                  resume_data: Optional[Dict[str, Any]]) -> Tuple[str, str]:
        """Create LinkedIn and resume summaries for conversation context"""
        
        linkedin_summary = "No LinkedIn data available"
        if linkedin_data:
            linkedin_summary = f"LinkedIn: {linkedin_data.get('headline', 'N/A')} | {linkedin_data.get('industry', 'N/A')} | {linkedin_data.get('summary', 'N/A')[:200]}..."
        
        resume_summary = "No resume data available"
        if resume_data:
            achievements = resume_data.get('key_achievements', '')[:200]
            skills = resume_data.get('technical_keywords', '')[:100]
            resume_summary = f"Resume: Key achievements: {achievements}... | Technical skills: {skills}..."
        
        return linkedin_summary, resume_summary