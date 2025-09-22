# api/main_api.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, security
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)