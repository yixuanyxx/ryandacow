-- PSA Workforce AI - Complete Database Setup Script
-- This script creates the entire database from scratch and populates it with data
-- Run this script in your Supabase SQL editor on an empty database

-- ==============================================
-- STEP 1: CREATE TABLES
-- ==============================================

-- Users table for authentication and basic profile
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255),
    department VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Skills table (simplified)
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Skills (for recommendations context)
CREATE TABLE IF NOT EXISTS user_skills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(50), -- e.g., "Beginner", "Intermediate", "Advanced"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (user_id, skill_id)
);

-- Courses (for recommendations)
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_weeks INTEGER,
    required_skills TEXT[], -- Array of skill names
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Career Pathways (for recommendations)
CREATE TABLE IF NOT EXISTS career_pathways (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    target_role VARCHAR(255),
    required_skills TEXT[], -- Array of skill names
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Chat Sessions
CREATE TABLE IF NOT EXISTS ai_chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Chat Messages
CREATE TABLE IF NOT EXISTS ai_chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES ai_chat_sessions(id) ON DELETE CASCADE,
    sender VARCHAR(50) NOT NULL, -- 'user' or 'ai'
    message TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- STEP 2: INSERT USERS DATA
-- ==============================================

-- Insert users from Employee_Profiles.json
INSERT INTO users (email, password_hash, name, job_title, department) VALUES
('samantha.lee@globalpsa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'Samantha Lee', 'Cloud Solutions Architect', 'Information Technology'),
('aisyah.rahman@globalpsa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'Nur Aisyah Binte Rahman', 'Cybersecurity Analyst', 'Information Technology'),
('rohan.mehta@globalpsa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'Rohan Mehta', 'Finance Manager (FP&A)', 'Finance'),
('grace.lee@globalpsa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'Grace Lee', 'Senior HR Business Partner', 'Human Resource'),
('felicia.goh@globalpsa.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4/LewdBPj4', 'Felicia Goh', 'Treasury Analyst', 'Finance');

-- ==============================================
-- STEP 3: INSERT SKILLS DATA
-- ==============================================

-- Insert skills from Functions & Skills.xlsx (extracted from employee profiles)
INSERT INTO skills (name, category) VALUES
-- Info Tech: Infrastructure skills
('Cloud Architecture', 'Info Tech: Infrastructure'),
('Cloud DevOps & Automation', 'Info Tech: Infrastructure'),
('Securing Cloud Infrastructure', 'Info Tech: Infrastructure'),
('Infrastructure Design, Analysis & Architecture', 'Info Tech: Infrastructure'),
('Network Architecture', 'Info Tech: Infrastructure'),
('Middleware & Web Servers', 'Info Tech: Infrastructure'),
('Enterprise Architecture', 'Info Tech: IT Governance & Strategy'),

-- Info Tech: Cybersecurity skills
('Vulnerability Management', 'Info Tech: Cybersecurity'),
('Network Security Management', 'Info Tech: Cybersecurity'),
('Cybersecurity Threat Intelligence and Detection', 'Info Tech: Cybersecurity'),
('Cybersecurity Forensics', 'Info Tech: Cybersecurity'),
('Cybersecurity Risk Management', 'Info Tech: Cybersecurity'),

-- Finance skills
('Financial Planning and Analysis', 'Finance'),
('Cost Management and Budget', 'Finance'),
('Financial Modeling', 'Finance'),
('Risk Management', 'Finance'),
('Treasury', 'Finance'),
('Terminal Reporting', 'Finance'),
('Carbon Accounting and Management', 'Finance'),
('Claims and Insurance', 'Finance'),

-- Human Resource skills
('Generalist / Business Partner', 'Human Resource'),
('Talent Management', 'Human Resource'),
('Staff Development and Engagement', 'Human Resource'),
('Compensation', 'Human Resource'),
('HR Information Systems / Technology', 'Human Resource'),
('Leadership Development', 'Human Resource'),
('Organisation Development', 'Human Resource');

-- ==============================================
-- STEP 4: INSERT USER SKILLS DATA
-- ==============================================

-- Samantha Lee (samantha.lee@globalpsa.com) - Cloud Solutions Architect
INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cloud Architecture'), 'Advanced'),
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cloud DevOps & Automation'), 'Advanced'),
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Securing Cloud Infrastructure'), 'Advanced'),
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Infrastructure Design, Analysis & Architecture'), 'Advanced'),
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Network Architecture'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Middleware & Web Servers'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Enterprise Architecture'), 'Intermediate');

-- Nur Aisyah Binte Rahman (aisyah.rahman@globalpsa.com) - Cybersecurity Analyst
INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES
((SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Vulnerability Management'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Network Security Management'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cybersecurity Threat Intelligence and Detection'), 'Beginner'),
((SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cybersecurity Forensics'), 'Beginner'),
((SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cybersecurity Risk Management'), 'Beginner');

-- Rohan Mehta (rohan.mehta@globalpsa.com) - Finance Manager (FP&A)
INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Financial Planning and Analysis'), 'Advanced'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cost Management and Budget'), 'Advanced'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Financial Modeling'), 'Advanced'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Risk Management'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Treasury'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Terminal Reporting'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Carbon Accounting and Management'), 'Beginner');

-- Grace Lee (grace.lee@globalpsa.com) - Senior HR Business Partner
INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Generalist / Business Partner'), 'Advanced'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Talent Management'), 'Advanced'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Staff Development and Engagement'), 'Advanced'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Compensation'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'HR Information Systems / Technology'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Leadership Development'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Organisation Development'), 'Intermediate');

-- Felicia Goh (felicia.goh@globalpsa.com) - Treasury Analyst
INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES
((SELECT id FROM users WHERE email = 'felicia.goh@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Treasury'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'felicia.goh@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Risk Management'), 'Intermediate'),
((SELECT id FROM users WHERE email = 'felicia.goh@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Claims and Insurance'), 'Beginner'),
((SELECT id FROM users WHERE email = 'felicia.goh@globalpsa.com'), (SELECT id FROM skills WHERE name = 'Cost Management and Budget'), 'Beginner');

-- ==============================================
-- STEP 5: INSERT SAMPLE COURSES
-- ==============================================

INSERT INTO courses (title, description, duration_weeks, required_skills) VALUES
('AWS Cloud Architecture Certification', 'Comprehensive course on AWS cloud architecture patterns and best practices', 12, ARRAY['Cloud Architecture', 'Infrastructure Design, Analysis & Architecture']),
('Cybersecurity Fundamentals', 'Introduction to cybersecurity concepts and practices', 8, ARRAY['Vulnerability Management', 'Network Security Management']),
('Financial Modeling Masterclass', 'Advanced financial modeling techniques and Excel proficiency', 10, ARRAY['Financial Modeling', 'Financial Planning and Analysis']),
('HR Leadership Development', 'Strategic HR leadership and organizational development', 6, ARRAY['Leadership Development', 'Organisation Development']),
('Treasury Risk Management', 'Advanced treasury operations and risk management', 8, ARRAY['Treasury', 'Risk Management']),
('Cloud Security Best Practices', 'Securing cloud infrastructure and implementing zero-trust architecture', 10, ARRAY['Securing Cloud Infrastructure', 'Cloud Architecture']),
('Advanced Financial Planning', 'Strategic financial planning and analysis for senior roles', 8, ARRAY['Financial Planning and Analysis', 'Cost Management and Budget']),
('Talent Management Excellence', 'Advanced talent acquisition and retention strategies', 6, ARRAY['Talent Management', 'Staff Development and Engagement']);

-- ==============================================
-- STEP 6: INSERT SAMPLE CAREER PATHWAYS
-- ==============================================

INSERT INTO career_pathways (name, description, target_role, required_skills) VALUES
('Cloud Solutions Architect Path', 'Progression path to senior cloud architecture roles', 'Senior Cloud Solutions Architect', ARRAY['Cloud Architecture', 'Enterprise Architecture', 'Cloud DevOps & Automation']),
('Cybersecurity Leadership Path', 'Career progression in cybersecurity leadership', 'Cybersecurity Manager', ARRAY['Cybersecurity Risk Management', 'Cybersecurity Threat Intelligence and Detection', 'Leadership Development']),
('Finance Leadership Path', 'Progression to senior finance leadership roles', 'Finance Director', ARRAY['Financial Planning and Analysis', 'Financial Modeling', 'Leadership Development']),
('HR Business Partner Path', 'Career development in strategic HR business partnering', 'Head of HR', ARRAY['Generalist / Business Partner', 'Talent Management', 'Organisation Development']),
('Treasury Management Path', 'Progression to senior treasury management roles', 'Treasury Manager', ARRAY['Treasury', 'Risk Management', 'Financial Planning and Analysis']),
('IT Infrastructure Leadership', 'Path to IT infrastructure leadership roles', 'IT Infrastructure Manager', ARRAY['Infrastructure Design, Analysis & Architecture', 'Network Architecture', 'Leadership Development']),
('Financial Risk Management', 'Specialized path in financial risk management', 'Risk Management Director', ARRAY['Risk Management', 'Financial Planning and Analysis', 'Treasury']);

-- ==============================================
-- STEP 7: INSERT SAMPLE AI CHAT SESSIONS
-- ==============================================

-- Create sample chat sessions for each user
INSERT INTO ai_chat_sessions (user_id, started_at, last_activity_at) VALUES
((SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com'), NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 hour'),
((SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com'), NOW() - INTERVAL '1 day', NOW() - INTERVAL '30 minutes'),
((SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com'), NOW() - INTERVAL '3 days', NOW() - INTERVAL '2 hours'),
((SELECT id FROM users WHERE email = 'grace.lee@globalpsa.com'), NOW() - INTERVAL '1 day', NOW() - INTERVAL '45 minutes'),
((SELECT id FROM users WHERE email = 'felicia.goh@globalpsa.com'), NOW() - INTERVAL '4 days', NOW() - INTERVAL '1 hour');

-- ==============================================
-- STEP 8: INSERT SAMPLE AI CHAT MESSAGES
-- ==============================================

-- Sample chat messages for Samantha Lee
INSERT INTO ai_chat_messages (session_id, sender, message, timestamp) VALUES
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com') LIMIT 1), 'user', 'Hi! I''m looking to advance my cloud architecture career. What skills should I focus on?', NOW() - INTERVAL '2 days'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com') LIMIT 1), 'ai', 'Based on your current skills in Cloud Architecture and Cloud DevOps, I recommend focusing on Enterprise Architecture and advanced security practices. Consider the AWS Cloud Architecture Certification course.', NOW() - INTERVAL '2 days' + INTERVAL '1 minute'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com') LIMIT 1), 'user', 'What about career progression opportunities?', NOW() - INTERVAL '1 hour'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'samantha.lee@globalpsa.com') LIMIT 1), 'ai', 'You''re well-positioned for the Cloud Solutions Architect Path. With your advanced skills, you could progress to Senior Cloud Solutions Architect or IT Infrastructure Manager roles.', NOW() - INTERVAL '1 hour' + INTERVAL '30 seconds');

-- Sample chat messages for Aisyah Rahman
INSERT INTO ai_chat_messages (session_id, sender, message, timestamp) VALUES
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com') LIMIT 1), 'user', 'I want to improve my cybersecurity skills. Where should I start?', NOW() - INTERVAL '1 day'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com') LIMIT 1), 'ai', 'Great! I see you have intermediate skills in Vulnerability Management. I recommend the Cybersecurity Fundamentals course to strengthen your Threat Intelligence and Forensics skills.', NOW() - INTERVAL '1 day' + INTERVAL '1 minute'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com') LIMIT 1), 'user', 'What career opportunities are available in cybersecurity?', NOW() - INTERVAL '30 minutes'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'aisyah.rahman@globalpsa.com') LIMIT 1), 'ai', 'The Cybersecurity Leadership Path offers excellent opportunities. You could progress to Cybersecurity Manager roles by developing your Risk Management and Leadership skills.', NOW() - INTERVAL '30 minutes' + INTERVAL '30 seconds');

-- Sample chat messages for Rohan Mehta
INSERT INTO ai_chat_messages (session_id, sender, message, timestamp) VALUES
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com') LIMIT 1), 'user', 'I''m interested in advancing to a Finance Director role. What should I focus on?', NOW() - INTERVAL '3 days'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com') LIMIT 1), 'ai', 'With your advanced skills in Financial Planning and Analysis, you''re on the right track! Focus on Leadership Development and consider the Advanced Financial Planning course to strengthen your strategic capabilities.', NOW() - INTERVAL '3 days' + INTERVAL '1 minute'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com') LIMIT 1), 'user', 'What about risk management skills?', NOW() - INTERVAL '2 hours'),
((SELECT id FROM ai_chat_sessions WHERE user_id = (SELECT id FROM users WHERE email = 'rohan.mehta@globalpsa.com') LIMIT 1), 'ai', 'Excellent question! The Financial Risk Management pathway would be perfect for you. Consider developing your Risk Management skills further and exploring Treasury operations.', NOW() - INTERVAL '2 hours' + INTERVAL '30 seconds');

-- ==============================================
-- STEP 9: CREATE INDEXES FOR PERFORMANCE
-- ==============================================

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX IF NOT EXISTS idx_user_skills_skill_id ON user_skills(skill_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_sessions_user_id ON ai_chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_messages_session_id ON ai_chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);

-- ==============================================
-- STEP 10: VERIFICATION QUERIES
-- ==============================================

-- Verify the data was inserted correctly
SELECT 'Users Count' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Skills Count', COUNT(*) FROM skills
UNION ALL
SELECT 'User Skills Count', COUNT(*) FROM user_skills
UNION ALL
SELECT 'Courses Count', COUNT(*) FROM courses
UNION ALL
SELECT 'Career Pathways Count', COUNT(*) FROM career_pathways
UNION ALL
SELECT 'AI Chat Sessions Count', COUNT(*) FROM ai_chat_sessions
UNION ALL
SELECT 'AI Chat Messages Count', COUNT(*) FROM ai_chat_messages;

-- Show sample user with their skills
SELECT 
    u.name,
    u.job_title,
    u.department,
    s.name as skill_name,
    s.category as skill_category,
    us.proficiency_level
FROM users u
JOIN user_skills us ON u.id = us.user_id
JOIN skills s ON us.skill_id = s.id
WHERE u.email = 'samantha.lee@globalpsa.com'
ORDER BY us.proficiency_level DESC, s.name;

-- Show available courses
SELECT title, description, duration_weeks, required_skills
FROM courses
ORDER BY title;

-- Show career pathways
SELECT name, description, target_role, required_skills
FROM career_pathways
ORDER BY name;

-- ==============================================
-- COMPLETION MESSAGE
-- ==============================================

-- This script has successfully:
-- 1. Created all required tables
-- 2. Inserted 5 employee profiles
-- 3. Inserted 25+ skills across IT, Finance, and HR
-- 4. Linked users to their skills with proficiency levels
-- 5. Added sample courses and career pathways
-- 6. Created sample AI chat sessions and messages
-- 7. Added performance indexes
-- 8. Verified data integrity

-- Your database is now ready for the PSA Workforce AI MVP!
-- Demo login credentials: All users use password 'demo123'
