-- PSA Workforce Compass Database Schema
-- Based on Employee Profiles data structure
-- Comprehensive schema for microservices architecture

-- ==============================================
-- CORE USER MANAGEMENT TABLES
-- ==============================================

-- Users/Authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Personal Information
CREATE TABLE IF NOT EXISTS user_personal_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    office_location VARCHAR(100),
    bio TEXT,
    profile_photo_url VARCHAR(500),
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Languages
CREATE TABLE IF NOT EXISTS user_languages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    language VARCHAR(50) NOT NULL,
    proficiency VARCHAR(50) NOT NULL, -- Fluent, Professional, Intermediate, Beginner
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- EMPLOYMENT INFORMATION TABLES
-- ==============================================

-- Employment Information
CREATE TABLE IF NOT EXISTS employment_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    job_title VARCHAR(200) NOT NULL,
    department VARCHAR(100) NOT NULL,
    unit VARCHAR(200),
    line_manager VARCHAR(200),
    in_role_since DATE,
    hire_date DATE NOT NULL,
    last_updated DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Position History
CREATE TABLE IF NOT EXISTS position_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_title VARCHAR(200) NOT NULL,
    organization VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    focus_areas TEXT[],
    key_skills_used TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- SKILLS AND COMPETENCIES TABLES
-- ==============================================

-- Function Areas (from the data: Info Tech: Infrastructure, Finance, etc.)
CREATE TABLE IF NOT EXISTS function_areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Specializations (Cloud Computing: Cloud Architecture, etc.)
CREATE TABLE IF NOT EXISTS specializations (
    id SERIAL PRIMARY KEY,
    function_area_id INTEGER REFERENCES function_areas(id) ON DELETE CASCADE,
    name VARCHAR(300) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Skills
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    specialization_id INTEGER REFERENCES specializations(id) ON DELETE CASCADE,
    name VARCHAR(300) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Skills
CREATE TABLE IF NOT EXISTS user_skills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level INTEGER CHECK (proficiency_level BETWEEN 1 AND 5),
    years_experience DECIMAL(3,1),
    last_used DATE,
    is_certified BOOLEAN DEFAULT false,
    certification_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

-- Competencies
CREATE TABLE IF NOT EXISTS competencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100), -- Soft Skills, Technical Skills, etc.
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Competencies
CREATE TABLE IF NOT EXISTS user_competencies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    competency_id INTEGER REFERENCES competencies(id) ON DELETE CASCADE,
    level VARCHAR(50) NOT NULL, -- Advanced, Intermediate, Beginner
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, competency_id)
);

-- ==============================================
-- EXPERIENCE AND PROJECTS TABLES
-- ==============================================

-- Experience Types
CREATE TABLE IF NOT EXISTS experience_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL, -- Program, Rotation, Exercise, Regional Portfolio, Transformation, etc.
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Experiences
CREATE TABLE IF NOT EXISTS user_experiences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    experience_type_id INTEGER REFERENCES experience_types(id) ON DELETE CASCADE,
    organization VARCHAR(200) NOT NULL,
    program VARCHAR(200),
    start_date DATE NOT NULL,
    end_date DATE,
    focus TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    project_name VARCHAR(300) NOT NULL,
    role VARCHAR(200),
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    outcomes TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- EDUCATION TABLES
-- ==============================================

-- Education
CREATE TABLE IF NOT EXISTS education (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    degree VARCHAR(300) NOT NULL,
    institution VARCHAR(300) NOT NULL,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- CAREER DEVELOPMENT TABLES
-- ==============================================

-- Career Pathways
CREATE TABLE IF NOT EXISTS career_pathways (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    department VARCHAR(100),
    level VARCHAR(50), -- Junior, Mid, Senior, Lead, Manager, Director
    min_years_experience INTEGER,
    max_years_experience INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Career Pathway Requirements
CREATE TABLE IF NOT EXISTS pathway_requirements (
    id SERIAL PRIMARY KEY,
    pathway_id INTEGER REFERENCES career_pathways(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    required_proficiency INTEGER CHECK (required_proficiency BETWEEN 1 AND 5),
    is_mandatory BOOLEAN DEFAULT true,
    weight DECIMAL(3,2) DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Career Goals
CREATE TABLE IF NOT EXISTS user_career_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    target_pathway_id INTEGER REFERENCES career_pathways(id),
    target_position VARCHAR(200),
    target_date DATE,
    priority INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- TRAINING AND LEARNING TABLES
-- ==============================================

-- Training/Courses
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    provider VARCHAR(200),
    duration_hours INTEGER,
    difficulty_level VARCHAR(50),
    category VARCHAR(100),
    skills_covered INTEGER[],
    prerequisites INTEGER[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Training Progress
CREATE TABLE IF NOT EXISTS user_training (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    completion_date DATE,
    progress_percentage DECIMAL(5,2) DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'enrolled',
    grade VARCHAR(10),
    certificate_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, course_id)
);

-- ==============================================
-- MENTORSHIP TABLES
-- ==============================================

-- Mentorship Requests
CREATE TABLE IF NOT EXISTS mentorship_requests (
    id SERIAL PRIMARY KEY,
    mentee_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    mentor_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message TEXT,
    skills_focus INTEGER[],
    status VARCHAR(50) DEFAULT 'pending',
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    responded_at TIMESTAMP WITH TIME ZONE,
    start_date DATE,
    end_date DATE,
    notes TEXT
);

-- ==============================================
-- AI AND ANALYTICS TABLES
-- ==============================================

-- AI Chat Sessions
CREATE TABLE IF NOT EXISTS ai_chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_name VARCHAR(200),
    context_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Chat Messages
CREATE TABLE IF NOT EXISTS ai_chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES ai_chat_sessions(id) ON DELETE CASCADE,
    sender VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text',
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Analytics
CREATE TABLE IF NOT EXISTS user_analytics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metric_date DATE DEFAULT CURRENT_DATE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    is_read BOOLEAN DEFAULT false,
    action_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- INDEXES FOR PERFORMANCE
-- ==============================================

-- User indexes
CREATE INDEX IF NOT EXISTS idx_users_employee_id ON users(employee_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_department ON employment_info(department);

-- Skills indexes
CREATE INDEX IF NOT EXISTS idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX IF NOT EXISTS idx_user_skills_skill_id ON user_skills(skill_id);
CREATE INDEX IF NOT EXISTS idx_skills_specialization ON skills(specialization_id);

-- Career indexes
CREATE INDEX IF NOT EXISTS idx_user_goals_user_id ON user_career_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_pathway_requirements ON pathway_requirements(pathway_id);

-- Training indexes
CREATE INDEX IF NOT EXISTS idx_user_training_user_id ON user_training(user_id);
CREATE INDEX IF NOT EXISTS idx_user_training_course_id ON user_training(course_id);

-- Mentorship indexes
CREATE INDEX IF NOT EXISTS idx_mentorship_mentee ON mentorship_requests(mentee_id);
CREATE INDEX IF NOT EXISTS idx_mentorship_mentor ON mentorship_requests(mentor_id);

-- AI indexes
CREATE INDEX IF NOT EXISTS idx_ai_chat_user_id ON ai_chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_messages_session ON ai_chat_messages(session_id);

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(user_id, is_read);

-- ==============================================
-- FUNCTIONS AND TRIGGERS
-- ==============================================

-- Function for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_personal_info_updated_at BEFORE UPDATE ON user_personal_info FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_employment_info_updated_at BEFORE UPDATE ON employment_info FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_skills_updated_at BEFORE UPDATE ON user_skills FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_career_goals_updated_at BEFORE UPDATE ON user_career_goals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_training_updated_at BEFORE UPDATE ON user_training FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ai_chat_sessions_updated_at BEFORE UPDATE ON ai_chat_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================
-- SAMPLE DATA INSERTION
-- ==============================================

-- Insert Function Areas
INSERT INTO function_areas (name, description) VALUES
('Info Tech: Infrastructure', 'Information Technology Infrastructure'),
('Info Tech: Cybersecurity', 'Information Technology Cybersecurity'),
('Finance', 'Financial Services and Management'),
('Human Resources', 'Human Resources Management'),
('Operations', 'Port Operations and Management')
ON CONFLICT (name) DO NOTHING;

-- Insert Specializations
INSERT INTO specializations (function_area_id, name) VALUES
(1, 'Cloud Computing: Cloud Architecture'),
(1, 'Cloud Computing: Cloud DevOps & Automation'),
(1, 'Cloud Computing: Securing Cloud Infrastructure'),
(1, 'Infrastructure Architecture: Infrastructure Design, Analysis & Architecture'),
(1, 'Infrastructure Architecture: Network Architecture'),
(1, 'Systems & Middleware Management: Middleware & Web Servers'),
(1, 'IT Governance & Strategy: Enterprise Architecture'),
(2, 'Cybersecurity Operation: Vulnerability Management'),
(2, 'Cybersecurity Operation: Network Security Management'),
(2, 'Cybersecurity Incident Handling: Cybersecurity Threat Intelligence and Detection'),
(2, 'Cybersecurity Incident Handling: Cybersecurity Forensics'),
(2, 'Cybersecurity Governance: Cybersecurity Risk Management'),
(3, 'Financial Planning and Analysis'),
(3, 'Cost Management and Budget'),
(3, 'Financial Modeling'),
(3, 'Risk Management'),
(3, 'Treasury'),
(3, 'Terminal Reporting'),
(3, 'Green Finance: Carbon Accounting and Management')
ON CONFLICT DO NOTHING;

-- Insert Skills
INSERT INTO skills (specialization_id, name) VALUES
(1, 'Cloud Architecture'),
(2, 'Cloud DevOps & Automation'),
(3, 'Securing Cloud Infrastructure'),
(4, 'Infrastructure Design, Analysis & Architecture'),
(5, 'Network Architecture'),
(6, 'Middleware & Web Servers'),
(7, 'Enterprise Architecture'),
(8, 'Vulnerability Management'),
(9, 'Network Security Management'),
(10, 'Cybersecurity Threat Intelligence and Detection'),
(11, 'Cybersecurity Forensics'),
(12, 'Cybersecurity Risk Management'),
(13, 'Financial Planning and Analysis'),
(14, 'Cost Management and Budget'),
(15, 'Financial Modeling'),
(16, 'Risk Management'),
(17, 'Treasury'),
(18, 'Terminal Reporting'),
(19, 'Carbon Accounting and Management')
ON CONFLICT DO NOTHING;

-- Insert Competencies
INSERT INTO competencies (name, category) VALUES
('Stakeholder & Partnership Management', 'Soft Skills'),
('Change & Transformation Management', 'Soft Skills'),
('Technology Management & Innovation', 'Technical Skills'),
('IT Audit', 'Technical Skills'),
('Quality Standards', 'Technical Skills'),
('Incident Response Playbook Development', 'Technical Skills'),
('Process Improvement & Optimisation and Problem Management', 'Soft Skills'),
('IT Strategy & Planning', 'Technical Skills')
ON CONFLICT (name) DO NOTHING;

-- Insert Experience Types
INSERT INTO experience_types (name) VALUES
('Program'),
('Rotation'),
('Exercise'),
('Regional Portfolio'),
('Transformation'),
('Treasury Operations'),
('Risk Reporting')
ON CONFLICT (name) DO NOTHING;

-- Insert Career Pathways
INSERT INTO career_pathways (name, description, department, level, min_years_experience, max_years_experience) VALUES
('Cloud Solutions Architect', 'Design and implement cloud infrastructure solutions', 'Information Technology', 'Senior', 5, 10),
('Cybersecurity Analyst', 'Monitor and analyze security threats and vulnerabilities', 'Information Technology', 'Mid', 2, 5),
('Finance Manager (FP&A)', 'Lead financial planning and analysis activities', 'Finance', 'Senior', 5, 10),
('HR Business Partner', 'Strategic HR support for business units', 'Human Resources', 'Senior', 5, 10),
('Treasury Analyst', 'Manage treasury operations and risk', 'Finance', 'Mid', 2, 5)
ON CONFLICT DO NOTHING;

-- Insert Sample Courses
INSERT INTO courses (title, description, provider, duration_hours, difficulty_level, category) VALUES
('AWS Cloud Architecture', 'Advanced cloud architecture design patterns', 'PSA Academy', 40, 'Advanced', 'Cloud Computing'),
('Cybersecurity Fundamentals', 'Core cybersecurity concepts and practices', 'PSA Academy', 24, 'Beginner', 'Cybersecurity'),
('Financial Modeling', 'Advanced financial modeling techniques', 'PSA Academy', 32, 'Intermediate', 'Finance'),
('Leadership Essentials', 'Core leadership skills for managers', 'PSA Academy', 16, 'Intermediate', 'Soft Skills')
ON CONFLICT DO NOTHING;
