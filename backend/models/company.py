"""
Hermes Business OS - Company Models
Core entities: Company, Department, Client, Project, Document, User
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Company(Base):
    """Company/tenant model."""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(100), default="general")
    size = Column(String(50), default="small")
    config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    departments = relationship("Department", back_populates="company")
    clients = relationship("Client", back_populates="company")
    projects = relationship("Project", back_populates="company")
    users = relationship("User", back_populates="company")


class Department(Base):
    """Department within a company."""
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, default=True)
    config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="departments")


class Client(Base):
    """CRM client/customer."""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    source = Column(String(100))  # referral, social, organic, etc.
    status = Column(String(50), default="lead")  # lead, prospect, active, inactive
    notes = Column(Text)
    metadata_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="clients")
    projects = relationship("Project", back_populates="client")


class Project(Base):
    """Operational project."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="planning")  # planning, active, paused, completed, cancelled
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float, default=0.0)
    metadata_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="projects")
    client = relationship("Client", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    """Task within a project."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="todo")  # todo, in_progress, review, done
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    metadata_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")


class Document(Base):
    """Generated document."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(255), nullable=False)
    doc_type = Column(String(100))  # quote, contract, report, etc.
    template = Column(String(100))
    content = Column(Text)
    file_url = Column(String(500))
    google_doc_id = Column(String(255))
    metadata_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    """Company user/employee."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    role = Column(String(100), default="member")  # admin, manager, member
    department = Column(String(100))
    telegram_id = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="users")
