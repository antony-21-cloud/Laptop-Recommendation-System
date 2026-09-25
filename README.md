Expert Recommendation System for Course-Specific Hardware Procurement
🎯 Overview
An intelligent web-based platform that helps Kenyan TVET & university students choose the right laptop based on their course, year of study, software needs, and budget — not brand names or salesperson bias.

❗ Problem
Students waste money on underpowered laptops because:

No localized, course-specific hardware advice

Confusing technical specs (SSD, RAM latency, GPU)

Untrustworthy salespeople

Fake online sellers and rapidly changing prices

✨ Key Features
For Students	For Vendors	For Admins
Course-based search	Stock visibility dashboard	Seller verification
Compatibility score	Proof-of-stock upload	Course/software management
Budget filtering	Inventory management	Report handling
New vs refurbished comparison	Listing analytics	Platform analytics
Price alerts		
Verified seller badges		
Expert chat support		
🏗️ Architecture
text
React Frontend → Node.js/Express API → MongoDB + Redis
                        ↓
              Expert System Inference Engine
Inference Engine Logic:

Get software requirements for course

Calculate minimum hardware specs

Query available laptops within budget

Score each laptop for compatibility

Return ranked recommendations

💻 Tech Stack
Layer	Technology
Frontend	React.js, Tailwind CSS
Backend	Node.js, Express.js
Database	MongoDB
Caching	Redis
Auth	JWT, bcrypt
Images	Cloudinary
Hosting	AWS / Heroku
Testing	Jest, Supertest
CI/CD	GitHub Actions
